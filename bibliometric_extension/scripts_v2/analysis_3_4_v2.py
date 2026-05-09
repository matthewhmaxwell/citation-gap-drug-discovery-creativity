"""
3.4 v2 forward citation share — uses v1's group_by approach,
swapping primary corpus for v2.

Reuses the v1 forward citation OpenAlex counts (publication_year totals
are stable enough; no need to re-query them). The only thing that
changes is the primary-corpus overlap intersection (since v2 corpus
membership differs from v1).
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
PROC.mkdir(exist_ok=True)
V1_PROC = ROOT.parent / "bibliometrics" / "processed"


def main():
    # v1 forward summary already has openalex_total_citers_via_groupby for each canonical
    v1_forward = pd.read_csv(V1_PROC / "forward_citation_summary.csv")
    v2_corpus = pd.read_parquet(RAW / "primary_corpus_v2.parquet")
    v2_ids = set(v2_corpus["id"].tolist())

    # We need to know which citers are in v2 corpus.
    # The v1 script intersects on primary corpus IDs but didn't store the citer list.
    # However, we can re-derive overlap from the direct-citation analysis:
    #   for each canonical id, the v2-corpus papers citing it ARE the citers in v2 ∩ that work's citers.
    direct_v2 = pd.read_csv(PROC / "direct_citation_v2_per_canonical.csv")
    direct_v2_lookup = direct_v2.set_index("canonical_id")["v2_corpus_citers"].to_dict()

    rows = []
    for _, r in v1_forward.iterrows():
        cid = r["canonical_id"]
        v1_total = r.get("openalex_total_citers_via_groupby") or 0
        v1_primary = r.get("citers_in_primary_corpus") or 0
        v2_primary = direct_v2_lookup.get(cid, 0)
        rows.append({
            "canonical_id": cid,
            "figure_group": r["figure_group"],
            "individual_name": r["individual_name"],
            "canonical_title": r["canonical_title"],
            "canonical_year": r["canonical_year"],
            "openalex_total_citers": v1_total,
            "v1_corpus_citers": v1_primary,
            "v2_corpus_citers": v2_primary,
            "v1_share": v1_primary / v1_total if v1_total else 0.0,
            "v2_share": v2_primary / v1_total if v1_total else 0.0,
            "delta_share": (v2_primary - v1_primary) / v1_total if v1_total else 0.0,
        })

    fdf = pd.DataFrame(rows)
    fdf.to_csv(PROC / "forward_citation_v2_with_v1_compare.csv", index=False)

    print(f"Targets: {len(fdf)}")
    print(f"Mean v1 primary-share: {fdf['v1_share'].mean()*100:.4f}%")
    print(f"Mean v2 primary-share: {fdf['v2_share'].mean()*100:.4f}%")
    print(f"Mean delta share: {fdf['delta_share'].mean()*100:.4f}%")

    print("\nTop 10 by v2-corpus citers:")
    print(fdf.sort_values("v2_corpus_citers", ascending=False).head(10)[
        ["figure_group","individual_name","canonical_title","canonical_year",
         "openalex_total_citers","v1_corpus_citers","v2_corpus_citers"]
    ].to_string(index=False))

    print("\nWorks where v2 share > v1 share (i.e., v2 expansion adds citers):")
    delta_pos = fdf[fdf["v2_corpus_citers"] > fdf["v1_corpus_citers"]]
    print(f"  {len(delta_pos)} works")
    print(delta_pos.sort_values("delta_share", ascending=False)[
        ["figure_group","individual_name","canonical_title","openalex_total_citers",
         "v1_corpus_citers","v2_corpus_citers"]
    ].to_string(index=False))


if __name__ == "__main__":
    main()
