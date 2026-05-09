"""
3.1 v2 Direct citation analysis on the v2 broader corpus.

Reuses the v1 canonical_papers.json (156 works × 30 figures).
Adds an explicit v1-vs-v2 comparison table per spec Section 4.1.
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
V1_PROC = ROOT.parent / "bibliometrics" / "processed"


def main():
    canon = json.loads((V1_RAW / "canonical_papers.json").read_text())
    df = pd.read_parquet(RAW / "primary_corpus_v3.parquet")
    print(f"v2 Corpus: {len(df):,} papers ({(df['n_references']>0).sum():,} with references)")

    canon_id_to_meta: dict[str, dict] = {}
    figure_to_canon: dict[str, list[str]] = defaultdict(list)
    for row_id, rec in canon.items():
        fg = rec["figure_group"]
        for w in rec["canonical_works"]:
            wid = w["id"]
            if not wid:
                continue
            canon_id_to_meta[wid] = {
                "figure_row_id": row_id,
                "figure_group": fg,
                "individual_name": rec["individual_name"],
                "title": w["title"],
                "year": w["publication_year"],
                "cited_by_count_global": w["cited_by_count"],
            }
            figure_to_canon[row_id].append(wid)

    print(f"Canonical works: {len(canon_id_to_meta)} from {len(figure_to_canon)} figure rows")

    counts = defaultdict(int)
    citing_lists = defaultdict(list)
    figure_pair_counts_corpus = defaultdict(set)

    canon_ids = set(canon_id_to_meta.keys())
    for _, row in df.iterrows():
        refs = row["referenced_works"]
        if refs is None or len(refs) == 0:
            continue
        cited_canons = [r for r in refs if r in canon_ids]
        if not cited_canons:
            continue
        slim_paper = {
            "corpus_paper_id": row["id"],
            "doi": row["doi"],
            "title": row["title"],
            "year": int(row["publication_year"]) if row["publication_year"] is not None else None,
            "venue": row["venue"],
            "n_corpus_refs": int(row["n_references"]),
            "cited_canonical_ids": cited_canons,
        }
        for cid in cited_canons:
            counts[cid] += 1
            citing_lists[cid].append(slim_paper)
            fid = canon_id_to_meta[cid]["figure_row_id"]
            figure_pair_counts_corpus[fid].add(row["id"])

    rows_canon = [{
        "canonical_id": cid,
        "figure_row_id": meta["figure_row_id"],
        "figure_group": meta["figure_group"],
        "individual_name": meta["individual_name"],
        "title": meta["title"],
        "year": meta["year"],
        "global_cited_by_count": meta["cited_by_count_global"],
        "v3_corpus_citers": counts.get(cid, 0),
    } for cid, meta in canon_id_to_meta.items()]
    canon_df = pd.DataFrame(rows_canon).sort_values(
        ["figure_row_id", "v3_corpus_citers", "global_cited_by_count"],
        ascending=[True, False, False],
    )
    canon_df.to_csv(PROC / "direct_citation_v3_per_canonical.csv", index=False)

    rows_fig = [{
        "figure_row_id": fid,
        "figure_group": rec["figure_group"],
        "individual_name": rec["individual_name"],
        "group": rec["group"],
        "n_canonical_works": len(rec["canonical_works"]),
        "n_works_with_any_v3_citation": sum(1 for w in rec["canonical_works"] if counts.get(w["id"], 0) > 0),
        "total_v3_corpus_figure_paper_pairs": sum(counts.get(w["id"], 0) for w in rec["canonical_works"]),
        "unique_v3_corpus_papers_citing_figure": len(figure_pair_counts_corpus.get(fid, set())),
    } for fid, rec in canon.items()]
    fig_df = pd.DataFrame(rows_fig).sort_values("unique_v3_corpus_papers_citing_figure", ascending=False)
    fig_df.to_csv(PROC / "direct_citation_v3_per_figure_row.csv", index=False)

    fg_agg = fig_df.groupby("figure_group").agg(
        individual_names=("individual_name", lambda s: " | ".join(sorted(set(s)))),
        group=("group", "first"),
        n_canonical_works=("n_canonical_works", "sum"),
        n_works_with_any_v3_citation=("n_works_with_any_v3_citation", "sum"),
        total_v3_corpus_figure_paper_pairs=("total_v3_corpus_figure_paper_pairs", "sum"),
        unique_v3_corpus_papers_citing_figure=("unique_v3_corpus_papers_citing_figure", "max"),
    ).reset_index().sort_values("total_v3_corpus_figure_paper_pairs", ascending=False)
    fg_agg.to_csv(PROC / "direct_citation_v3_per_figure_group.csv", index=False)

    citing_dump = {}
    for cid, lst in citing_lists.items():
        meta = canon_id_to_meta[cid]
        citing_dump[cid] = {
            "figure_group": meta["figure_group"],
            "figure_row_id": meta["figure_row_id"],
            "individual_name": meta["individual_name"],
            "canonical_title": meta["title"],
            "canonical_year": meta["year"],
            "n_citing_v3_corpus_papers": len(lst),
            "citing_papers": lst,
        }
    (PROC / "direct_citation_v3_citing_papers.json").write_text(
        json.dumps(citing_dump, indent=2, ensure_ascii=False)
    )

    # v1 vs v2 comparison
    v1_canon = pd.read_csv(V1_PROC / "direct_citation_per_canonical.csv")
    v1_fg = pd.read_csv(V1_PROC / "direct_citation_per_figure_group.csv")

    v1_v2_canon = pd.merge(
        v1_canon[["canonical_id","figure_group","individual_name","title","year","global_cited_by_count","corpus_citers"]].rename(columns={"corpus_citers":"v1_corpus_citers"}),
        canon_df[["canonical_id","v3_corpus_citers"]],
        on="canonical_id",
        how="outer",
    )
    v1_v2_canon["delta_v2_minus_v1"] = v1_v2_canon["v3_corpus_citers"].fillna(0) - v1_v2_canon["v1_corpus_citers"].fillna(0)
    v1_v2_canon = v1_v2_canon.sort_values("delta_v2_minus_v1", ascending=False)
    v1_v2_canon.to_csv(PROC / "v2_vs_v3_per_canonical.csv", index=False)

    v1_v2_fg = pd.merge(
        v1_fg.rename(columns={
            "total_corpus_figure_paper_pairs":"v1_total_pairs",
            "unique_corpus_papers_citing_figure":"v1_unique_papers",
            "n_works_with_any_corpus_citation":"v1_n_works_cited",
        })[["figure_group","group","v1_total_pairs","v1_unique_papers","v1_n_works_cited"]],
        fg_agg.rename(columns={
            "total_v3_corpus_figure_paper_pairs":"v2_total_pairs",
            "unique_v3_corpus_papers_citing_figure":"v2_unique_papers",
            "n_works_with_any_v3_citation":"v2_n_works_cited",
        })[["figure_group","v2_total_pairs","v2_unique_papers","v2_n_works_cited"]],
        on="figure_group",
        how="outer",
    )
    v1_v2_fg["delta_pairs"] = v1_v2_fg["v2_total_pairs"].fillna(0) - v1_v2_fg["v1_total_pairs"].fillna(0)
    v1_v2_fg["delta_unique_papers"] = v1_v2_fg["v2_unique_papers"].fillna(0) - v1_v2_fg["v1_unique_papers"].fillna(0)
    v1_v2_fg = v1_v2_fg.sort_values("delta_unique_papers", ascending=False)
    v1_v2_fg.to_csv(PROC / "v2_vs_v3_per_figure_group.csv", index=False)

    # Headline
    n_corpus = len(df)
    n_canonicals_cited = int((canon_df["v3_corpus_citers"] > 0).sum())
    n_corpus_papers_citing = len(set(p["corpus_paper_id"] for lst in citing_lists.values() for p in lst))
    print(f"\n=== v2 Headline ===")
    print(f"v3 corpus: {n_corpus:,} papers")
    print(f"Canonical works cited by ≥1 v3 corpus paper: {n_canonicals_cited}")
    print(f"Unique v3 corpus papers citing ≥1 canonical: {n_corpus_papers_citing} ({100*n_corpus_papers_citing/n_corpus:.3f}%)")

    print(f"\nTop 10 figure groups by total v3-corpus pairs:")
    print(fg_agg.head(10)[["figure_group","total_v3_corpus_figure_paper_pairs","unique_v3_corpus_papers_citing_figure"]].to_string(index=False))

    print(f"\n=== v1 vs v2 delta (per figure group, top deltas) ===")
    print(v1_v2_fg.sort_values("delta_unique_papers", ascending=False).head(15)[
        ["figure_group","v1_unique_papers","v2_unique_papers","delta_unique_papers"]
    ].to_string(index=False))


if __name__ == "__main__":
    main()
