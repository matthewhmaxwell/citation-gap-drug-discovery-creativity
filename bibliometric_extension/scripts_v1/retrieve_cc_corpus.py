"""
Retrieve the tertiary computational-creativity corpus (used in 3.3).

Spec: 1995-2026 window, terms 'computational creativity', 'creative AI',
'creative computing', 'AI creativity', 'machine creativity', plus venue
filters for ICCC.
"""

import json
import time
from pathlib import Path

import pyalex
from pyalex import Works, Sources
import pandas as pd
from tqdm import tqdm

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 5

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)

CC_TERMS = [
    "computational creativity",
    "creative AI",
    "creative computing",
    "AI creativity",
    "machine creativity",
    "computational creativity systems",
    "creative artificial intelligence",
    "artificial creativity",
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
        "authors": [
            (a.get("author") or {}).get("display_name")
            for a in (w.get("authorships") or [])
        ][:10],
        "n_authors": len(w.get("authorships") or []),
        "referenced_works": w.get("referenced_works") or [],
        "n_references": len(w.get("referenced_works") or []),
        "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
        "concepts": [
            {"id": c.get("id"), "display_name": c.get("display_name"), "score": c.get("score")}
            for c in (w.get("concepts") or [])
        ][:8],
    }


def main():
    cc_or = or_phrase(CC_TERMS)
    print(f"CC OR query: {cc_or[:120]}…")

    q = (
        Works()
        .search_filter(title_and_abstract=cc_or)
        .filter(from_publication_date="1995-01-01", to_publication_date="2026-05-09")
        .select(SELECT_FIELDS)
    )
    n = q.count()
    print(f"Computational creativity term match: {n:,}")

    rows = []
    pbar = tqdm(total=n, unit="paper")
    for page in q.paginate(per_page=200, n_max=None):
        for w in page:
            rows.append(slim(w))
            pbar.update(1)
        time.sleep(0.05)
    pbar.close()

    # Also retrieve papers from ICCC venue if its source ID is findable
    try:
        s = Sources().search("International Conference on Computational Creativity").get(per_page=5)
        iccc_ids = [src["id"] for src in s if "computational creativity" in (src.get("display_name") or "").lower()]
        print(f"ICCC source IDs found: {iccc_ids}")
        for sid in iccc_ids:
            ic_q = Works().filter(primary_location={"source": {"id": sid.rsplit('/', 1)[-1]}}).select(SELECT_FIELDS)
            ic_count = ic_q.count()
            print(f"  ICCC source {sid}: {ic_count} works")
            existing = {r["id"] for r in rows}
            added = 0
            for page in ic_q.paginate(per_page=200, n_max=None):
                for w in page:
                    if w.get("id") not in existing:
                        rows.append(slim(w))
                        existing.add(w.get("id"))
                        added += 1
            print(f"  added {added} ICCC works not in term-match set")
    except Exception as e:
        print(f"ICCC venue lookup failed: {e}")

    print(f"\nFinal CC corpus: {len(rows):,} papers")
    df = pd.DataFrame(rows)
    out_pq = RAW / "cc_corpus.parquet"
    df.to_parquet(out_pq, compression="zstd")
    print(f"Saved: {out_pq} ({out_pq.stat().st_size/1e6:.1f} MB)")
    print(f"With abstract: {df['abstract'].notna().sum():,}")
    print(f"With references: {(df['n_references']>0).sum():,}")

    (RAW / "cc_corpus_meta.json").write_text(json.dumps({
        "cc_or_terms": CC_TERMS,
        "filter": cc_or,
        "from_date": "1995-01-01",
        "to_date": "2026-05-09",
        "n_works": len(rows),
    }, indent=2))


if __name__ == "__main__":
    main()
