"""
Pull the v2 broader chemistry-AI methodology corpus.

Filter:  ((any drug term) OR (any chem-methodology term)) AND (any AI term)
         in title or abstract; English; 2017-01-01 to 2026-05-09.
"""

import json
import time
from pathlib import Path

import pyalex
from pyalex import Works
import pandas as pd
from tqdm import tqdm

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 5
pyalex.config.retry_backoff_factor = 1.0

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)

DRUG_TERMS = [
    "drug discovery", "drug design", "drug repurposing",
    "molecular generation", "de novo design", "virtual screening",
    "ADMET prediction", "lead optimization", "binding affinity prediction",
    "compound generation",
]
CHEM_METHODOLOGY_TERMS = [
    "molecular machine learning", "autonomous chemistry",
    "autonomous chemical discovery", "autonomous synthesis",
    "retrosynthesis", "synthetic chemistry AI", "generative chemistry",
    "molecular property prediction", "chemoinformatics", "cheminformatics",
    "molecular representation learning", "chemical foundation model",
    "molecular foundation model", "reaction prediction",
    "self-driving laboratory", "self-driving lab", "autonomous laboratory",
]
AI_TERMS = [
    "deep learning", "machine learning", "artificial intelligence",
    "neural network", "transformer", "graph neural network",
    "diffusion model", "generative model", "foundation model",
    "large language model", "LLM", "agent", "agentic",
]


def or_phrase(terms):
    return "(" + " OR ".join(f'"{t}"' for t in terms) + ")"


SELECT_FIELDS = [
    "id", "doi", "title", "publication_year", "publication_date",
    "type", "language", "cited_by_count",
    "authorships", "primary_location",
    "referenced_works", "concepts", "topics",
    "abstract_inverted_index",
]


def reconstruct_abstract(inv_idx):
    if not inv_idx:
        return None
    positions = []
    for word, ps in inv_idx.items():
        for p in ps:
            positions.append((p, word))
    positions.sort()
    return " ".join(w for _, w in positions)


def slim(w):
    primary_loc = w.get("primary_location") or {}
    src = (primary_loc.get("source") or {}) if isinstance(primary_loc, dict) else {}
    return {
        "id": w.get("id"),
        "doi": w.get("doi"),
        "title": w.get("title"),
        "publication_year": w.get("publication_year"),
        "publication_date": w.get("publication_date"),
        "type": w.get("type"),
        "language": w.get("language"),
        "cited_by_count": w.get("cited_by_count") or 0,
        "venue": src.get("display_name"),
        "venue_id": src.get("id"),
        "venue_type": src.get("type"),
        "authors": [(a.get("author") or {}).get("display_name") for a in (w.get("authorships") or [])][:10],
        "author_ids": [(a.get("author") or {}).get("id") for a in (w.get("authorships") or [])][:10],
        "n_authors": len(w.get("authorships") or []),
        "referenced_works": w.get("referenced_works") or [],
        "n_references": len(w.get("referenced_works") or []),
        "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
        "concepts": [
            {"id": c.get("id"), "display_name": c.get("display_name"), "score": c.get("score")}
            for c in (w.get("concepts") or [])
        ][:8],
        "topic_id": ((w.get("topics") or [{}])[0] or {}).get("id"),
        "topic_name": ((w.get("topics") or [{}])[0] or {}).get("display_name"),
    }


def main():
    drug_or_chem_or = "(" + " OR ".join(f'"{t}"' for t in DRUG_TERMS + CHEM_METHODOLOGY_TERMS) + ")"
    ai_or = or_phrase(AI_TERMS)
    query = drug_or_chem_or + " AND " + ai_or
    print(f"Filter: {query[:120]}…")

    q = (
        Works()
        .search_filter(title_and_abstract=query)
        .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
        .filter(language="en")
        .select(SELECT_FIELDS)
    )
    total = q.count()
    print(f"Expected: {total:,} works")

    rows = []
    pbar = tqdm(total=total, unit="paper")
    for page in q.paginate(per_page=200, n_max=None):
        for w in page:
            rows.append(slim(w))
            pbar.update(1)
        time.sleep(0.05)
    pbar.close()
    print(f"\nRetrieved {len(rows):,} papers")

    df = pd.DataFrame(rows)
    print(f"Memory: {df.memory_usage(deep=True).sum()/1e6:.1f} MB")
    out_pq = RAW / "primary_corpus_v2.parquet"
    df.to_parquet(out_pq, compression="zstd")
    print(f"Saved: {out_pq} ({out_pq.stat().st_size/1e6:.1f} MB)")

    print(f"\nYear distribution (most recent 12):")
    print(df["publication_year"].value_counts().sort_index(ascending=False).head(12).to_string())
    print(f"\nWith abstract: {df['abstract'].notna().sum():,}")
    print(f"With references: {(df['n_references']>0).sum():,}")
    print(f"Total reference edges: {df['n_references'].sum():,}")
    print(f"Mean cited_by_count: {df['cited_by_count'].mean():.1f}")

    (RAW / "primary_corpus_v2_meta.json").write_text(json.dumps({
        "drug_terms": DRUG_TERMS,
        "chem_methodology_terms": CHEM_METHODOLOGY_TERMS,
        "ai_terms": AI_TERMS,
        "filter": query,
        "from_date": "2017-01-01",
        "to_date": "2026-05-09",
        "language": "en",
        "n_works": len(rows),
        "n_works_expected_by_count": total,
    }, indent=2))


if __name__ == "__main__":
    main()
