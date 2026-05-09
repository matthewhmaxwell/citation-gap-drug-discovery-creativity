"""
v3 canonical set: extends v2's 22-set with 5 papers from the v3 expansion sub-domains
(protein-AI, materials informatics, comp-chem ML, QSAR).

Selection rule: top-cited papers in v3 corpus that are NOT in v2 corpus AND
match one of the 4 expansion subdomains by keyword.
"""

import json, re
from pathlib import Path
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
V2_RAW = ROOT.parent / "bibliometrics_v2" / "raw"


def get_meta(openalex_id):
    short = openalex_id.rsplit("/", 1)[-1]
    r = requests.get(f"https://api.openalex.org/works/{short}", params={"mailto":"biblio_v3@example.org"}, timeout=20)
    if r.status_code == 200:
        return r.json()
    return None


def main():
    v2 = pd.read_parquet(ROOT.parent / "bibliometrics_v2" / "raw" / "primary_corpus_v2.parquet")
    v3 = pd.read_parquet(RAW / "primary_corpus_v3.parquet")
    v2_ids = set(v2["id"].tolist())
    v3_only = v3[~v3["id"].isin(v2_ids)].copy()
    print(f"v2 corpus: {len(v2):,}  v3 corpus: {len(v3):,}  v3-only delta: {len(v3_only):,}")

    print("\nTop 30 v3-only by citations:")
    for _, r in v3_only.sort_values("cited_by_count", ascending=False).head(30).iterrows():
        print(f"  {r['cited_by_count']:>6} {r['publication_year']} {(r['title'] or '')[:90]}")

    # Now pick top 5 across the four sub-domains
    # Keyword matching for sub-domain assignment
    SUBDOMAIN_PATTERNS = {
        "protein-AI": [r"protein structure prediction", r"\bprotein design\b", r"protein language model", r"antibody design", r"\bde novo\b.*protein", r"alphafold"],
        "materials":  [r"materials informatics", r"materials discovery", r"crystal structure prediction", r"materials machine learning", r"inverse materials"],
        "comp-chem-ML": [r"DFT machine learning", r"molecular dynamics machine learning", r"interatomic potential", r"neural network potential", r"machine learning potential", r"force field"],
        "QSAR":       [r"\bQSAR\b", r"quantitative structure activity", r"molecular descriptor", r"structure activity relationship", r"\bQSPR\b"],
    }
    def assign_subdomain(title, abstract):
        t = "" if title is None or (isinstance(title, float) and pd.isna(title)) else str(title)
        a = "" if abstract is None or (isinstance(abstract, float) and pd.isna(abstract)) else str(abstract)
        text = (t + " " + a).lower()
        hits = []
        for sd, pats in SUBDOMAIN_PATTERNS.items():
            for p in pats:
                if re.search(p, text, re.I):
                    hits.append(sd)
                    break
        return hits[0] if hits else None

    v3_only["subdomain"] = v3_only.apply(lambda r: assign_subdomain(r["title"], r["abstract"]), axis=1)
    print("\nv3-only subdomain distribution:")
    print(v3_only["subdomain"].value_counts(dropna=False).to_string())

    # Pick top-cited per subdomain
    v3_canonicals = []
    for sd in ["protein-AI", "materials", "comp-chem-ML", "QSAR"]:
        sub = v3_only[v3_only["subdomain"] == sd].sort_values("cited_by_count", ascending=False)
        if len(sub) > 0:
            top = sub.iloc[0]
            v3_canonicals.append({
                "openalex_id": top["id"],
                "doi": top["doi"],
                "title": top["title"],
                "year": int(top["publication_year"]) if top["publication_year"] is not None else None,
                "venue": top["venue"],
                "cited_by_count": int(top["cited_by_count"]),
                "label": f"v3-{sd}-canonical",
                "subdomain": sd,
                "in_v2_corpus": False,
                "in_v3_corpus": True,
                "selection_rationale": f"top-cited v3-only paper in {sd} subdomain",
            })

    # Plus the 1 highest-cited v3-only paper overall
    seen = {p["openalex_id"] for p in v3_canonicals}
    for _, r in v3_only.sort_values("cited_by_count", ascending=False).iterrows():
        if r["id"] not in seen:
            v3_canonicals.append({
                "openalex_id": r["id"],
                "doi": r["doi"],
                "title": r["title"],
                "year": int(r["publication_year"]) if r["publication_year"] is not None else None,
                "venue": r["venue"],
                "cited_by_count": int(r["cited_by_count"]),
                "label": f"v3-top-cited",
                "subdomain": r["subdomain"] or "uncategorized",
                "in_v2_corpus": False,
                "in_v3_corpus": True,
                "selection_rationale": "highest-cited v3-only paper",
            })
            break

    print(f"\nv3 expansion canonicals (5 selected):")
    for p in v3_canonicals:
        print(f"  [{p['subdomain']:15}] {p['cited_by_count']:>6} {p['year']} {(p['title'] or '')[:80]}")

    # Load v2's 22-set
    v2_set = json.loads((V2_RAW / "dd_and_methodology_canonical_papers.json").read_text())
    final = v2_set["final_22_set"] + v3_canonicals
    print(f"\nFinal v3 set: {len(final)} (22 v2 + {len(v3_canonicals)} v3 expansion)")

    out = {
        "v2_22_set_inherited": v2_set["final_22_set"],
        "v3_expansion_canonicals": v3_canonicals,
        "final_27_set": final,
    }
    (RAW / "v3_canonical_papers.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"Wrote raw/v3_canonical_papers.json")


if __name__ == "__main__":
    main()
