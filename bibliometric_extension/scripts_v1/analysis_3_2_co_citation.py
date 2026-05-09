"""
3.2 Co-citation analysis.

For each (creativity_canonical, dd_canonical) pair, count papers in
OpenAlex (any corpus) that cite both. Uses chained `cites` filter on
OpenAlex which gives an exact count without paginating citers.

Output: full pair-matrix CSV + a list of bridging papers (papers that
co-cite at least one creativity canonical with at least one DD canonical).
"""

import json
import time
from pathlib import Path
from itertools import product

import pyalex
from pyalex import Works
import pandas as pd
from tqdm import tqdm

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 5
pyalex.config.retry_backoff_factor = 1.0

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
PROC.mkdir(exist_ok=True)


def short_id(url: str) -> str:
    return url.rsplit("/", 1)[-1]


def main():
    canon = json.loads((RAW / "canonical_papers.json").read_text())
    dd = json.loads((RAW / "dd_canonical_papers.json").read_text())

    # Flatten creativity canonicals
    creat = []
    for row_id, rec in canon.items():
        for w in rec["canonical_works"]:
            creat.append({
                "id": w["id"],
                "short_id": short_id(w["id"]) if w.get("id") else None,
                "figure_row_id": row_id,
                "figure_group": rec["figure_group"],
                "individual_name": rec["individual_name"],
                "title": w["title"],
                "year": w["publication_year"],
                "global_cited_by_count": w["cited_by_count"],
            })
    # dedupe
    seen = set()
    creat_unique = []
    for c in creat:
        if not c["id"] or c["id"] in seen:
            continue
        seen.add(c["id"])
        creat_unique.append(c)
    print(f"Creativity canonicals (unique): {len(creat_unique)}")
    print(f"DD canonicals: {len(dd)}")
    n_pairs = len(creat_unique) * len(dd)
    print(f"Pairs to test: {n_pairs}")

    # Save figure-level cite counts (needed below for "bridging papers")
    rows = []
    pbar = tqdm(total=n_pairs, unit="pair")
    bridging_query_results = {}  # (creat_id, dd_id) -> first 25 papers
    for c in creat_unique:
        # Skip canonicals with very low global citation count (no point)
        if c["global_cited_by_count"] < 5:
            for d in dd:
                rows.append({
                    "creativity_canonical_id": c["id"],
                    "creativity_short_id": c["short_id"],
                    "figure_group": c["figure_group"],
                    "individual_name": c["individual_name"],
                    "creativity_title": c["title"],
                    "creativity_year": c["year"],
                    "creativity_global_cites": c["global_cited_by_count"],
                    "dd_canonical_id": d["openalex_id"],
                    "dd_label": d["label"],
                    "dd_title": d["title"],
                    "dd_year": d["year"],
                    "co_citation_count": 0,
                    "skipped_low_cites": True,
                })
                pbar.update(1)
            continue
        for d in dd:
            try:
                cnt = (
                    Works()
                    .filter(cites=c["short_id"])
                    .filter(cites=short_id(d["openalex_id"]))
                    .count()
                )
            except Exception as e:
                cnt = -1
                print(f"\n[err] {c['short_id']} x {short_id(d['openalex_id'])}: {e}")
            rows.append({
                "creativity_canonical_id": c["id"],
                "creativity_short_id": c["short_id"],
                "figure_group": c["figure_group"],
                "individual_name": c["individual_name"],
                "creativity_title": c["title"],
                "creativity_year": c["year"],
                "creativity_global_cites": c["global_cited_by_count"],
                "dd_canonical_id": d["openalex_id"],
                "dd_label": d["label"],
                "dd_title": d["title"],
                "dd_year": d["year"],
                "co_citation_count": cnt,
                "skipped_low_cites": False,
            })
            pbar.update(1)
            time.sleep(0.05)
    pbar.close()

    df = pd.DataFrame(rows)
    df.to_csv(PROC / "co_citation_pairs.csv", index=False)
    print(f"\nWrote: processed/co_citation_pairs.csv ({len(df)} rows)")

    # Aggregate to figure-group × dd-canonical
    agg_fg = (
        df[~df["skipped_low_cites"]]
        .groupby(["figure_group", "dd_label", "dd_title", "dd_year"], as_index=False)
        .agg(
            total_co_cites=("co_citation_count", lambda s: int(s[s >= 0].sum())),
            n_pairs_with_any_co_cite=("co_citation_count", lambda s: int((s > 0).sum())),
        )
    )
    agg_fg.to_csv(PROC / "co_citation_by_figure_group_x_dd.csv", index=False)
    print(f"Wrote: processed/co_citation_by_figure_group_x_dd.csv ({len(agg_fg)} rows)")

    # Aggregate to figure-group level (sum across DD canonicals)
    fg = (
        df[~df["skipped_low_cites"]]
        .groupby(["figure_group"], as_index=False)
        .agg(
            total_co_cites=("co_citation_count", lambda s: int(s[s >= 0].sum())),
            n_dd_papers_with_any_co_cite=(
                "co_citation_count",
                lambda s: int((s > 0).sum()),
            ),
        )
        .sort_values("total_co_cites", ascending=False)
    )
    fg.to_csv(PROC / "co_citation_by_figure_group.csv", index=False)
    print(f"Wrote: processed/co_citation_by_figure_group.csv ({len(fg)} rows)")

    # Pairs with at least one co-citation: collect actual bridging papers
    nonzero_pairs = df[df["co_citation_count"] > 0]
    print(f"\nPairs with co-cite > 0: {len(nonzero_pairs)}")
    bridging_papers = []
    for _, r in tqdm(nonzero_pairs.iterrows(), total=len(nonzero_pairs), desc="fetching bridge papers"):
        try:
            res = (
                Works()
                .filter(cites=r["creativity_short_id"])
                .filter(cites=short_id(r["dd_canonical_id"]))
                .select(["id","doi","title","publication_year","type","cited_by_count","primary_location"])
                .get(per_page=25)
            )
        except Exception as e:
            print(f"  [err] {e}")
            continue
        for w in res:
            primary_loc = w.get("primary_location") or {}
            src = (primary_loc.get("source") or {}) if isinstance(primary_loc, dict) else {}
            bridging_papers.append({
                "bridge_paper_id": w.get("id"),
                "bridge_paper_doi": w.get("doi"),
                "bridge_paper_title": w.get("title"),
                "bridge_paper_year": w.get("publication_year"),
                "bridge_paper_venue": src.get("display_name"),
                "bridge_paper_type": w.get("type"),
                "bridge_paper_cites_count": w.get("cited_by_count"),
                "creativity_canonical_id": r["creativity_canonical_id"],
                "figure_group": r["figure_group"],
                "creativity_title": r["creativity_title"],
                "dd_canonical_id": r["dd_canonical_id"],
                "dd_label": r["dd_label"],
                "dd_title": r["dd_title"],
            })
        time.sleep(0.1)
    bp_df = pd.DataFrame(bridging_papers)
    bp_df.to_csv(PROC / "co_citation_bridging_papers.csv", index=False)
    print(f"Wrote: processed/co_citation_bridging_papers.csv ({len(bp_df)} rows)")

    # Top-of-screen summary
    print("\n=== Co-citation summary ===")
    print(f"Total creativity-canonical × DD-canonical pairs tested: {(~df['skipped_low_cites']).sum()}")
    print(f"Pairs with ≥1 co-citation: {(df['co_citation_count']>0).sum()}")
    print(f"Sum of co-cite counts: {df.loc[df['co_citation_count']>=0,'co_citation_count'].sum()}")
    print("\nFigure groups by total co-citations:")
    print(fg.head(15).to_string(index=False))


if __name__ == "__main__":
    main()
