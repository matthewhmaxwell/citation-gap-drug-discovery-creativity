"""
3.3 v2 topic modeling using v2 primary corpus + v1 cc corpus.
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
V1_RAW = ROOT.parent / "bibliometrics" / "raw"
V1_PROC = ROOT.parent / "bibliometrics" / "processed"

SEED = 42


def main():
    primary = pd.read_parquet(RAW / "primary_corpus_v2.parquet")
    cc = pd.read_parquet(V1_RAW / "cc_corpus.parquet")

    rng = np.random.default_rng(SEED)
    primary_sub = primary[primary["abstract"].notna()].copy()
    if len(primary_sub) > 5000:
        primary_sub = primary_sub.sample(5000, random_state=SEED)
    cc_sub = cc[cc["abstract"].notna()].copy()
    if len(cc_sub) > 5000:
        cc_sub = cc_sub.sample(5000, random_state=SEED)

    primary_sub["community"] = "drug-discovery-AI-v2"
    cc_sub["community"] = "computational-creativity"

    union = pd.concat([primary_sub, cc_sub], ignore_index=True).drop_duplicates(subset="id").reset_index(drop=True)
    union["text"] = (union["title"].fillna("") + ". " + union["abstract"].fillna(""))
    union = union[union["text"].str.len() > 50].reset_index(drop=True)
    print(f"Union for v2 topic modeling: {len(union):,}")
    print(f"  drug-discovery-AI-v2: {(union['community']=='drug-discovery-AI-v2').sum()}")
    print(f"  computational-creativity: {(union['community']=='computational-creativity').sum()}")

    from sentence_transformers import SentenceTransformer
    from bertopic import BERTopic
    from sklearn.feature_extraction.text import CountVectorizer
    from umap import UMAP
    from hdbscan import HDBSCAN

    print("Embedding...")
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedder.encode(union["text"].tolist(), show_progress_bar=True, batch_size=64)

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
    info.to_csv(PROC / "topic_info_v2.csv", index=False)
    union[["id","title","publication_year","venue","community","topic"]].to_csv(
        PROC / "paper_topic_assignments_v2.csv", index=False
    )

    ct = pd.crosstab(union["topic"], union["community"])
    shared = []
    for tid in ct.index:
        if tid == -1:
            continue
        row = ct.loc[tid]
        dd = int(row.get("drug-discovery-AI-v2", 0))
        cc_n = int(row.get("computational-creativity", 0))
        if dd > 0 and cc_n > 0:
            shared.append({
                "topic": tid,
                "n_dd": dd, "n_cc": cc_n, "total": dd + cc_n,
                "balance": min(dd, cc_n) / max(dd, cc_n) if max(dd, cc_n) > 0 else 0,
            })
    shared_df = pd.DataFrame(shared).sort_values(["balance","total"], ascending=False)
    if len(shared_df) > 0:
        topic_repr = info.set_index("Topic")["Representation"].to_dict()
        shared_df["top_words"] = shared_df["topic"].map(lambda t: ", ".join(topic_repr.get(t, [])[:8]) if topic_repr.get(t) else "")
    shared_df.to_csv(PROC / "shared_topics_v2.csv", index=False)

    n_topics = (info["Topic"] != -1).sum()
    n_noise = (union["topic"] == -1).sum()
    print(f"\nv2 topics: {n_topics}; noise: {n_noise} ({100*n_noise/len(union):.1f}%)")
    print(f"Shared topics (both communities): {len(shared_df)}")
    if len(shared_df) > 0:
        print(f"Max balance: {shared_df['balance'].max():.3f}")
        print(f"Topics with balance ≥ 0.1: {(shared_df['balance'] >= 0.1).sum()}")

    # v1 vs v2 comparison
    v1_shared = pd.read_csv(V1_PROC / "shared_topics.csv")
    print(f"\n--- comparison ---")
    print(f"v1 topics: 26 (from v1 log); shared: {len(v1_shared)}; max balance: {v1_shared['balance'].max() if len(v1_shared)>0 else 0:.3f}")
    print(f"v2 topics: {n_topics}; shared: {len(shared_df)}; max balance: {shared_df['balance'].max() if len(shared_df)>0 else 0:.3f}")

    try:
        topic_model.save(str(OUT / "bertopic_model_v2"), serialization="safetensors", save_embedding_model=False)
    except Exception as e:
        print(f"Model save: {e}")


if __name__ == "__main__":
    main()
