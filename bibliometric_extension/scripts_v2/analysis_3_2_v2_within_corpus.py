"""
3.2 v2 — within-corpus co-citation derivation.

The intended approach was to query OpenAlex for papers anywhere that
co-cite each (creativity_canonical, dd/methodology_canonical) pair —
identical to v1's 3.2 method. Mid-run we hit OpenAlex's $1/day polite-pool
budget cap; the chained-cites query is no longer reachable today.

This substitute uses already-retrieved data: for each pair, count the
*v2-corpus* papers whose `referenced_works` includes BOTH the creativity
canonical and the DD/methodology canonical. This is a strict subset of
the intended "anywhere in OpenAlex" co-citation — it's the corpus-internal
co-citation only — but it's directly measurable from the parquet we have.

Output is labelled clearly to avoid being mistaken for the
cross-OpenAlex measurement.
"""

import json
from pathlib import Path
from collections import defaultdict

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
PROC.mkdir(exist_ok=True)
V1_RAW = ROOT.parent / "bibliometrics" / "raw"


def main():
    canon = json.loads((V1_RAW / "canonical_papers.json").read_text())
    canonical_set = json.loads((RAW / "dd_and_methodology_canonical_papers.json").read_text())
    dd = canonical_set["final_22_set"]
    df = pd.read_parquet(RAW / "primary_corpus_v2.parquet")

    # Build creativity-canonical id set
    creat_meta = {}
    for row_id, rec in canon.items():
        for w in rec["canonical_works"]:
            if w["id"]:
                creat_meta[w["id"]] = {
                    "figure_group": rec["figure_group"],
                    "individual_name": rec["individual_name"],
                    "title": w["title"],
                    "year": w["publication_year"],
                    "global_cites": w["cited_by_count"],
                }
    dd_set = {d["openalex_id"]: d for d in dd}
    print(f"Creativity canonicals: {len(creat_meta)}; DD/methodology canonicals: {len(dd_set)}")

    # For each corpus paper with refs, check intersection
    pair_counts = defaultdict(int)        # (creat_id, dd_id) -> count
    pair_papers = defaultdict(list)       # (creat_id, dd_id) -> [(corpus_pid, title, year)]

    for _, row in df.iterrows():
        refs = row["referenced_works"]
        if refs is None or len(refs) == 0:
            continue
        refs_set = set(refs)
        cited_creat = refs_set & creat_meta.keys()
        cited_dd = refs_set & dd_set.keys()
        if not cited_creat or not cited_dd:
            continue
        for c in cited_creat:
            for d in cited_dd:
                pair_counts[(c, d)] += 1
                pair_papers[(c, d)].append({
                    "corpus_pid": row["id"],
                    "title": row["title"],
                    "year": int(row["publication_year"]) if row["publication_year"] is not None else None,
                    "venue": row["venue"],
                    "doi": row["doi"],
                })

    # Build pair table
    rows = []
    for (cid, did), count in pair_counts.items():
        cm = creat_meta[cid]
        dm = dd_set[did]
        rows.append({
            "creativity_canonical_id": cid,
            "figure_group": cm["figure_group"],
            "individual_name": cm["individual_name"],
            "creativity_title": cm["title"],
            "dd_canonical_id": did,
            "dd_label": dm["label"],
            "dd_subdomain": dm.get("subdomain"),
            "dd_in_v1_corpus": dm.get("in_v1_corpus"),
            "dd_in_v2_corpus": dm.get("in_v2_corpus"),
            "within_v2_corpus_co_citers": count,
        })
    df_pairs = pd.DataFrame(rows).sort_values("within_v2_corpus_co_citers", ascending=False)
    df_pairs.to_csv(PROC / "co_citation_v2_within_corpus_pairs.csv", index=False)

    # Aggregate by figure group
    fg = df_pairs.groupby("figure_group")["within_v2_corpus_co_citers"].sum().sort_values(ascending=False)
    fg.to_csv(PROC / "co_citation_v2_within_corpus_by_figure_group.csv")
    print("\nWithin-v2-corpus co-citations (sum across all 22 DD canonicals):")
    print(fg.to_string())

    # Per-figure-group counts
    fg_count = df_pairs.groupby("figure_group").size().sort_values(ascending=False)
    print("\nNumber of distinct (creativity, DD) pairs with within-v2-corpus co-citation > 0, by figure group:")
    print(fg_count.to_string())

    # All bridging papers (within-v2-corpus only)
    bridging_rows = []
    for (cid, did), papers in pair_papers.items():
        cm = creat_meta[cid]
        dm = dd_set[did]
        for p in papers:
            bridging_rows.append({
                "bridge_paper_id": p["corpus_pid"],
                "bridge_paper_title": p["title"],
                "bridge_paper_year": p["year"],
                "bridge_paper_venue": p["venue"],
                "bridge_paper_doi": p["doi"],
                "creativity_canonical_id": cid,
                "figure_group": cm["figure_group"],
                "creativity_title": cm["title"],
                "dd_canonical_id": did,
                "dd_label": dm["label"],
                "dd_in_v1_corpus": dm.get("in_v1_corpus"),
                "dd_in_v2_corpus": dm.get("in_v2_corpus"),
            })
    if bridging_rows:
        bp = pd.DataFrame(bridging_rows).sort_values(["figure_group","dd_label"])
        bp.to_csv(PROC / "co_citation_v2_within_corpus_bridging_papers.csv", index=False)
        print(f"\nBridging papers within v2 corpus: {len(bp)} (papers that reference ≥1 creativity canonical AND ≥1 DD/methodology canonical)")
        print(f"Unique bridging papers: {bp['bridge_paper_id'].nunique()}")
        print()
        for _, r in bp.head(30).iterrows():
            print(f"  {r['bridge_paper_year']}  {r['figure_group']:20} ↔ {r['dd_label'][:50]:50}  {(r['bridge_paper_title'] or '')[:60]}")
    else:
        print("\nNo within-v2-corpus bridging papers found.")


if __name__ == "__main__":
    main()
