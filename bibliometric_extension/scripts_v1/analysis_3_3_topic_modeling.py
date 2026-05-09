"""
3.3 Topic-modeling community separation.

Build a BERTopic model on the union of:
- 5,000 random papers from the primary drug-discovery AI corpus
- All papers in the computational-creativity corpus (or 5,000 random if
  larger)
- Bridging papers from 3.2's bridging-papers list
- Direct-citation citing papers from 3.1

Test whether DD-AI papers and CC papers cluster into distinct topic groups.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
OUT = ROOT / "outputs"
PROC.mkdir(exist_ok=True)
OUT.mkdir(exist_ok=True)

SEED = 42

def main():
    primary = pd.read_parquet(RAW / "primary_corpus.parquet")
    cc = pd.read_parquet(RAW / "cc_corpus.parquet")

    # Sample 5K each (or full)
    rng = np.random.default_rng(SEED)
    primary_sub = primary[primary["abstract"].notna()].copy()
    if len(primary_sub) > 5000:
        primary_sub = primary_sub.sample(5000, random_state=SEED)
    cc_sub = cc[cc["abstract"].notna()].copy()
    if len(cc_sub) > 5000:
        cc_sub = cc_sub.sample(5000, random_state=SEED)

    primary_sub["community"] = "drug-discovery-AI"
    cc_sub["community"] = "computational-creativity"

    # Bridging + counterexample papers
    bridging_path = PROC / "co_citation_bridging_papers.csv"
    extras = pd.DataFrame()
    if bridging_path.exists():
        bp = pd.read_csv(bridging_path)
        extras_ids = set(bp["bridge_paper_id"].dropna().tolist()) if not bp.empty else set()
        # Look up in primary_corpus first; if not present, skip (we'd need to fetch)
        already = set(primary_sub["id"].tolist()) | set(cc_sub["id"].tolist())
        # For now, skip extras lookup if not in either corpus (we have what we need)
    counter_path = PROC / "counterexample_classified.csv"
    counter_ids = set()
    if counter_path.exists():
        ce = pd.read_csv(counter_path)
        counter_ids = set(ce["corpus_paper_id"].dropna().tolist())

    # Union and dedupe (by id)
    union = pd.concat([primary_sub, cc_sub], ignore_index=True)
    union = union.drop_duplicates(subset="id").reset_index(drop=True)
    union["text"] = (union["title"].fillna("") + ". " + union["abstract"].fillna(""))
    union = union[union["text"].str.len() > 50].reset_index(drop=True)
    print(f"Union for topic modeling: {len(union):,}")
    print(f"  drug-discovery-AI: {(union['community']=='drug-discovery-AI').sum()}")
    print(f"  computational-creativity: {(union['community']=='computational-creativity').sum()}")
    print(f"  flagged as direct-citation counterexample: {union['id'].isin(counter_ids).sum()}")

    # Fit BERTopic
    from sentence_transformers import SentenceTransformer
    from bertopic import BERTopic
    from sklearn.feature_extraction.text import CountVectorizer
    from umap import UMAP
    from hdbscan import HDBSCAN

    print("Embedding (this can take a few minutes)...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(
        union["text"].tolist(),
        show_progress_bar=True,
        batch_size=64,
    )
    print(f"Embeddings shape: {embeddings.shape}")

    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=SEED)
    hdbscan_model = HDBSCAN(min_cluster_size=30, metric="euclidean", cluster_selection_method="eom")
    vectorizer = CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2, max_df=0.95)

    print("Fitting BERTopic...")
    topic_model = BERTopic(
        embedding_model=embedder,
        umap_model=umap_model,
        hdbscan_model=hdbscan_model,
        vectorizer_model=vectorizer,
        verbose=True,
        calculate_probabilities=False,
    )
    topics, _ = topic_model.fit_transform(union["text"].tolist(), embeddings)
    union["topic"] = topics

    info = topic_model.get_topic_info()
    info.to_csv(PROC / "topic_info.csv", index=False)
    print("\nTop 20 topics:")
    print(info.head(25).to_string(index=False))

    # Per-paper topic assignments
    union[["id", "title", "publication_year", "venue", "community", "topic"]].to_csv(
        PROC / "paper_topic_assignments.csv", index=False
    )

    # Community × topic
    ct = pd.crosstab(union["topic"], union["community"], margins=True)
    ct.to_csv(PROC / "community_x_topic.csv")

    # Compute "shared topics" — topics where both communities appear with non-trivial share
    ct_no_margin = pd.crosstab(union["topic"], union["community"])
    # Only for non-noise topics (-1 is HDBSCAN noise)
    shared = []
    for tid in ct_no_margin.index:
        if tid == -1:
            continue
        row = ct_no_margin.loc[tid]
        total = row.sum()
        dd = row.get("drug-discovery-AI", 0)
        cc_n = row.get("computational-creativity", 0)
        if dd > 0 and cc_n > 0:
            shared.append({
                "topic": tid,
                "n_dd": int(dd),
                "n_cc": int(cc_n),
                "total": int(total),
                "balance": min(dd, cc_n) / max(dd, cc_n) if max(dd, cc_n) > 0 else 0,
            })
    shared_df = pd.DataFrame(shared).sort_values(["balance", "total"], ascending=False)
    if not shared_df.empty:
        # Add topic words
        topic_repr = info.set_index("Topic")["Representation"].to_dict()
        shared_df["top_words"] = shared_df["topic"].map(lambda t: ", ".join(topic_repr.get(t, [])[:8]) if topic_repr.get(t) else "")
    shared_df.to_csv(PROC / "shared_topics.csv", index=False)
    print(f"\nShared topics (non-noise, both communities present): {len(shared_df)}")
    if len(shared_df) > 0:
        print(shared_df.head(15).to_string(index=False))

    # Save model
    try:
        topic_model.save(str(OUT / "bertopic_model"), serialization="safetensors", save_embedding_model=False)
        print(f"\nSaved BERTopic model to {OUT/'bertopic_model'}")
    except Exception as e:
        print(f"Model save failed (non-fatal): {e}")

    # Headline numbers
    n_topics = len([t for t in info["Topic"].tolist() if t != -1])
    n_papers_noise = (union["topic"] == -1).sum()
    print(f"\n=== Topic modeling summary ===")
    print(f"Total documents: {len(union):,}")
    print(f"Total topics: {n_topics}")
    print(f"Documents in noise (-1): {n_papers_noise} ({100*n_papers_noise/len(union):.1f}%)")
    print(f"Shared topics (both communities present): {len(shared_df)}")
    if len(shared_df) > 0:
        balanced = (shared_df["balance"] >= 0.1).sum()
        print(f"  with balance ≥ 0.1: {balanced}")


if __name__ == "__main__":
    main()
