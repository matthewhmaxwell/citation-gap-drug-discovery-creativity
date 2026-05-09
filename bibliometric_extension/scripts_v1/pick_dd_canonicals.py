"""
Pick a small set of drug-discovery AI canonical papers — used for co-citation
analysis (3.2). Strategy: top-cited papers from the primary corpus, filtered
to ones that are clearly DD-AI methodology / review (not editorials, not
non-AI papers swept in by broad keywords).
"""

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"

df = pd.read_parquet(RAW / "primary_corpus.parquet")
print(f"Corpus: {len(df):,}")

# Filter: at least 200 citations, paper or review type, has abstract
ddc = df[
    (df["cited_by_count"] >= 200)
    & (df["type"].isin(["article", "review"]))
    & (df["abstract"].notna())
].sort_values("cited_by_count", ascending=False)

print(f"After filter: {len(ddc):,}")
print("\nTop 30 by citation count:")
for _, r in ddc.head(30).iterrows():
    title = (r["title"] or "")[:90]
    print(f"  {r['cited_by_count']:>5}  {r['publication_year']}  {title}")

# Hand-pick canonical DD-AI papers from the top-cited set.
# We'll record (openalex_id, label, reason) so the choice is auditable.
HAND_PICKS = [
    ("AlphaFold protein structure", lambda r: "alphafold" in (r["title"] or "").lower() and "highly accurate" in (r["title"] or "").lower()),
    ("MoleculeNet benchmark", lambda r: "moleculenet" in (r["title"] or "").lower()),
    ("Junction Tree VAE", lambda r: "junction tree" in (r["title"] or "").lower()),
    ("REINVENT", lambda r: "reinvent" in (r["title"] or "").lower()),
    ("MolGAN", lambda r: "molgan" in (r["title"] or "").lower()),
    ("DiffDock", lambda r: "diffdock" in (r["title"] or "").lower()),
    ("ChemCrow", lambda r: "chemcrow" in (r["title"] or "").lower()),
    ("Coscientist", lambda r: "coscientist" in (r["title"] or "").lower() or ("autonomous chemical research" in (r["title"] or "").lower())),
    ("Stokes antibiotic deep learning", lambda r: "deep learning approach to antibiotic" in (r["title"] or "").lower()),
    ("Zhavoronkov DDR1", lambda r: "ddr1" in (r["title"] or "").lower() and "kinase" in (r["title"] or "").lower()),
    ("RFdiffusion", lambda r: "rfdiffusion" in (r["title"] or "").lower() or ("de novo design of protein structure" in (r["title"] or "").lower())),
    ("ProteinMPNN", lambda r: "proteinmpnn" in (r["title"] or "").lower() or "robust deep learning" in (r["title"] or "").lower() and "protein sequence" in (r["title"] or "").lower()),
    ("Vamathevan ML in drug discovery", lambda r: "applications of machine learning" in (r["title"] or "").lower() and "drug discovery" in (r["title"] or "").lower()),
    ("Chen et al. ML drug discovery", lambda r: "machine learning in drug discovery" in (r["title"] or "").lower()),
    ("Schneider 2018 automating", lambda r: "automating drug discovery" in (r["title"] or "").lower()),
]

picks = []
for label, pred in HAND_PICKS:
    matches = ddc[ddc.apply(pred, axis=1)]
    if len(matches) == 0:
        print(f"  [no match] {label}")
        continue
    top = matches.iloc[0]
    picks.append({
        "openalex_id": top["id"],
        "doi": top["doi"],
        "title": top["title"],
        "year": int(top["publication_year"]),
        "venue": top["venue"],
        "cited_by_count": int(top["cited_by_count"]),
        "label": label,
    })

# Add the very top-cited papers to make sure we capture them even without explicit labels
seen_ids = {p["openalex_id"] for p in picks}
for _, r in ddc.head(20).iterrows():
    if r["id"] not in seen_ids and r["type"] != "editorial":
        picks.append({
            "openalex_id": r["id"],
            "doi": r["doi"],
            "title": r["title"],
            "year": int(r["publication_year"]),
            "venue": r["venue"],
            "cited_by_count": int(r["cited_by_count"]),
            "label": "top-cited-corpus",
        })
        seen_ids.add(r["id"])

print(f"\nFinal DD-canonical set: {len(picks)}")
for p in picks:
    print(f"  {p['cited_by_count']:>5}  {p['year']}  {p['label']:30}  {(p['title'] or '')[:60]}")

(RAW / "dd_canonical_papers.json").write_text(json.dumps(picks, indent=2, ensure_ascii=False))
print(f"\nWrote raw/dd_canonical_papers.json")
