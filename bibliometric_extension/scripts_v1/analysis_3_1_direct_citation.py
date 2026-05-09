"""
3.1 Direct citation analysis.

For each canonical creativity paper, count how many primary-corpus papers
reference it. Aggregate to figure-group level. Save citing-paper lists
for inspection of any non-zero figure-paper pairs.
"""

import json
import sys
from pathlib import Path
from collections import defaultdict

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
PROC.mkdir(exist_ok=True)


def main():
    canon = json.loads((RAW / "canonical_papers.json").read_text())
    df = pd.read_parquet(RAW / "primary_corpus.parquet")
    print(f"Corpus: {len(df):,} papers ({(df['n_references']>0).sum():,} with references)")

    # Build canonical-paper -> (figure_row_id, figure_group, individual_name) map
    canon_id_to_meta: dict[str, dict] = {}
    figure_to_canon: dict[str, list[str]] = defaultdict(list)
    figure_meta: dict[str, dict] = {}
    for row_id, rec in canon.items():
        fg = rec["figure_group"]
        figure_meta[row_id] = rec
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

    # Iterate corpus, build per-canonical citation counts and citing-paper lists
    counts = defaultdict(int)             # canonical_id -> count
    citing_lists = defaultdict(list)      # canonical_id -> list of citing paper records (slim)
    figure_paper_counts = defaultdict(int)  # figure_row_id -> count of papers citing >=1 of figure's works
    figure_pair_counts_corpus = defaultdict(set)  # figure_row_id -> set of corpus paper IDs

    canon_ids = set(canon_id_to_meta.keys())

    for _, row in df.iterrows():
        refs = row["referenced_works"]
        if refs is None or len(refs) == 0:
            continue
        # iterate refs and check canonical
        cited_canons = []
        for r in refs:
            if r in canon_ids:
                cited_canons.append(r)
        if not cited_canons:
            continue
        # Record
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

    for fid, pset in figure_pair_counts_corpus.items():
        figure_paper_counts[fid] = len(pset)

    # Per-canonical-paper citation table
    rows_canon = []
    for cid, meta in canon_id_to_meta.items():
        rows_canon.append({
            "canonical_id": cid,
            "figure_row_id": meta["figure_row_id"],
            "figure_group": meta["figure_group"],
            "individual_name": meta["individual_name"],
            "title": meta["title"],
            "year": meta["year"],
            "global_cited_by_count": meta["cited_by_count_global"],
            "corpus_citers": counts.get(cid, 0),
        })
    canon_df = pd.DataFrame(rows_canon).sort_values(
        ["figure_row_id", "corpus_citers", "global_cited_by_count"],
        ascending=[True, False, False],
    )
    canon_df.to_csv(PROC / "direct_citation_per_canonical.csv", index=False)
    print(f"\nWrote: processed/direct_citation_per_canonical.csv ({len(canon_df)} rows)")

    # Per-figure-row aggregate
    rows_fig = []
    for fid, rec in canon.items():
        fg = rec["figure_group"]
        n_works = len(rec["canonical_works"])
        works_cited = sum(1 for w in rec["canonical_works"] if counts.get(w["id"], 0) > 0)
        total_citing_pairs = sum(counts.get(w["id"], 0) for w in rec["canonical_works"])
        unique_corpus_papers = figure_paper_counts.get(fid, 0)
        rows_fig.append({
            "figure_row_id": fid,
            "figure_group": fg,
            "individual_name": rec["individual_name"],
            "group": rec["group"],
            "n_canonical_works": n_works,
            "n_works_with_any_corpus_citation": works_cited,
            "total_corpus_figure_paper_pairs": total_citing_pairs,
            "unique_corpus_papers_citing_figure": unique_corpus_papers,
        })
    fig_df = pd.DataFrame(rows_fig).sort_values("unique_corpus_papers_citing_figure", ascending=False)
    fig_df.to_csv(PROC / "direct_citation_per_figure_row.csv", index=False)
    print(f"Wrote: processed/direct_citation_per_figure_row.csv ({len(fig_df)} rows)")

    # Per-figure-group aggregate (the 30 named figures)
    fg_agg = fig_df.groupby("figure_group").agg(
        individual_names=("individual_name", lambda s: " | ".join(sorted(set(s)))),
        group=("group", "first"),
        n_canonical_works=("n_canonical_works", "sum"),
        n_works_with_any_corpus_citation=("n_works_with_any_corpus_citation", "sum"),
        total_corpus_figure_paper_pairs=("total_corpus_figure_paper_pairs", "sum"),
        unique_corpus_papers_citing_figure=("unique_corpus_papers_citing_figure", "max"),
        # NB: max not sum to avoid double-count for joint figures (Fauconnier-Turner etc.).
        # Joint figures may have any individual cited; we approximate with max.
    ).reset_index().sort_values("total_corpus_figure_paper_pairs", ascending=False)
    fg_agg.to_csv(PROC / "direct_citation_per_figure_group.csv", index=False)
    print(f"Wrote: processed/direct_citation_per_figure_group.csv ({len(fg_agg)} rows)")

    # Citing-paper lists (per canonical work, sorted by citation count)
    citing_dump = {}
    for cid, lst in citing_lists.items():
        meta = canon_id_to_meta[cid]
        citing_dump[cid] = {
            "figure_group": meta["figure_group"],
            "figure_row_id": meta["figure_row_id"],
            "individual_name": meta["individual_name"],
            "canonical_title": meta["title"],
            "canonical_year": meta["year"],
            "n_citing_corpus_papers": len(lst),
            "citing_papers": lst,
        }
    (PROC / "direct_citation_citing_papers.json").write_text(
        json.dumps(citing_dump, indent=2, ensure_ascii=False)
    )
    print(f"Wrote: processed/direct_citation_citing_papers.json")

    # Headline summary
    total_figure_paper_pairs = sum(len(rec["canonical_works"]) for rec in canon.values())
    n_figure_paper_pairs_with_any_corpus_citation = sum(
        1 for cid in canon_id_to_meta if counts.get(cid, 0) > 0
    )
    n_corpus_papers_citing_any_canonical = len(set(
        p["corpus_paper_id"]
        for lst in citing_lists.values()
        for p in lst
    ))
    print(f"\n=== Headline ===")
    print(f"Corpus size: {len(df):,} papers")
    print(f"Corpus papers with references: {(df['n_references']>0).sum():,}")
    print(f"Total canonical (figure × work) pairs checked: {total_figure_paper_pairs}")
    print(f"Canonical works cited by ≥1 corpus paper: {n_figure_paper_pairs_with_any_corpus_citation}")
    print(f"Unique corpus papers citing ≥1 canonical work: {n_corpus_papers_citing_any_canonical}")
    print(f"\nTop figures by corpus-figure-pair count:")
    print(fg_agg.head(15)[["figure_group","group","total_corpus_figure_paper_pairs","unique_corpus_papers_citing_figure"]].to_string(index=False))


if __name__ == "__main__":
    main()
