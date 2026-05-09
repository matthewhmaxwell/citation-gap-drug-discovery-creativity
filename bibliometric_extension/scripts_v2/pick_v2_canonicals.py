"""
Build the 22-paper drug-discovery + chemistry-AI methodology canonical set.

Section 3 of the v2 spec specifies the 12 v1 drug-discovery canonicals
explicitly (by OpenAlex ID). For the v2 additions, the spec provides
candidate names (Coley 2019, Schwaller 2020, ChemCrow, Coscientist, etc.)
and asks the executor to confirm and select 10.

Selection rule (per spec): "top-cited in v2 corpus but not v1 corpus
(i.e., papers that entered the corpus due to v2 expansion); span the
methodology subdomains".

Algorithm:
1. Identify the v2-only delta (papers in v2 corpus but not v1 corpus).
2. Confirm the spec's named candidates (Coley, Schwaller, etc.) are in the
   v2-only delta.
3. From the delta, pick 10 representing the methodology subdomains.
4. Combine with the 12 v1 canonicals (specified by ID).
"""

import json
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
V1_RAW = ROOT.parent / "bibliometrics" / "raw"

# v1 canonical drug-discovery AI papers (from v2 spec Section 3, explicit list)
V1_DD_CANONICALS = [
    {"id": "https://openalex.org/W3094686696", "label": "REINVENT 2.0"},
    {"id": "https://openalex.org/W2971801381", "label": "Molecular Docking: Shifting Paradigms"},
    {"id": "https://openalex.org/W2790808809", "label": "The rise of deep learning in drug discovery"},
    {"id": "https://openalex.org/W2578240541", "label": "Generating Focused Molecule Libraries (RNN)"},
    {"id": "https://openalex.org/W2785947426", "label": "DeepDTA"},
    {"id": "https://openalex.org/W2610148085", "label": "Molecular de novo design through deep RL (Olivecrona 2017)"},
    {"id": "https://openalex.org/W2773987374", "label": "Deep RL for de novo drug design (Popova 2018)"},
    {"id": "https://openalex.org/W4367049415", "label": "Computational approaches streamlining drug discovery"},
    {"id": "https://openalex.org/W3096561213", "label": "GraphDTA"},
    {"id": "https://openalex.org/W2959938226", "label": "Concepts of AI for CADD"},
    {"id": "https://openalex.org/W2784213390", "label": "KDEEP"},
    {"id": "https://openalex.org/W2801991413", "label": "Machine learning in chemoinformatics and drug discovery"},
]

# v2 chemistry-AI methodology candidates (from spec Section 3)
# Each entry has a search query — we'll resolve to OpenAlex ID
V2_METHOD_CANDIDATES = [
    # OpenAlex ID (if known) -> label.
    # We'll resolve any unknown IDs by title search below.
    {"id": "https://openalex.org/W2975022113", "label": "Coley 2019 Autonomous Discovery Part I (Progress)", "subdomain": "autonomous chemistry"},
    {"id": "https://openalex.org/W2975047661", "label": "Coley 2019 Autonomous Discovery Part II (Outlook)", "subdomain": "autonomous chemistry"},
    {"id": "https://openalex.org/W3084673918", "label": "Schwaller 2020 Molecular ML Future Synthetic Chem", "subdomain": "molecular ML"},
    {"id": "https://openalex.org/W4365597205", "label": "ChemCrow", "subdomain": "agentic chemistry"},
    {"id": "https://openalex.org/W4389991792", "label": "Coscientist (Boiko 2023)", "subdomain": "agentic chemistry / SDL"},
    {"id": "https://openalex.org/W3042021489", "label": "Burger 2020 Mobile robotic chemist", "subdomain": "self-driving lab"},
    # Need to look up: Schwaller Molecular Transformer; Coley RDChiral; AlphaFold; RFdiffusion
]


def resolve_by_title(title_query: str, year_max: int | None = None) -> dict | None:
    r = requests.get(
        "https://api.openalex.org/works",
        params={"search": title_query, "per_page": 5, "mailto": "bibliometric_extension@example.org"},
        timeout=30,
    )
    r.raise_for_status()
    for w in r.json().get("results", []):
        title = (w.get("title") or "")
        if title_query.lower().split()[0] in title.lower():
            if year_max is None or (w.get("publication_year") and w["publication_year"] <= year_max):
                return w
    return None


def get_meta(openalex_id: str) -> dict | None:
    short = openalex_id.rsplit("/", 1)[-1]
    r = requests.get(
        f"https://api.openalex.org/works/{short}",
        params={"mailto": "bibliometric_extension@example.org"},
        timeout=30,
    )
    if r.status_code == 200:
        return r.json()
    return None


def main():
    v2_df = pd.read_parquet(RAW / "primary_corpus_v2.parquet")
    v1_df = pd.read_parquet(V1_RAW / "primary_corpus.parquet")
    v1_ids = set(v1_df["id"].tolist())
    v2_ids = set(v2_df["id"].tolist())
    v2_only = v2_ids - v1_ids
    v1_only = v1_ids - v2_ids
    overlap = v1_ids & v2_ids
    print(f"v1 corpus: {len(v1_ids):,} papers")
    print(f"v2 corpus: {len(v2_ids):,} papers")
    print(f"v2 ∩ v1: {len(overlap):,}")
    print(f"v2 \\ v1 (newly added by v2 expansion): {len(v2_only):,}")
    print(f"v1 \\ v2 (in v1, not in v2 — likely OpenAlex churn): {len(v1_only):,}")

    # Resolve all v2 method candidates
    print("\nResolving v2 method canonical candidates...")
    resolved = []
    for cand in V2_METHOD_CANDIDATES:
        meta = get_meta(cand["id"])
        if not meta:
            print(f"  [warn] could not fetch {cand['id']}")
            continue
        wid = meta["id"]
        in_v2 = wid in v2_ids
        in_v1 = wid in v1_ids
        cited = meta.get("cited_by_count", 0)
        title = meta.get("title")
        year = meta.get("publication_year")
        venue = ((meta.get("primary_location") or {}).get("source") or {}).get("display_name")
        print(f"  {cand['label']:55} | year={year} | in_v1={in_v1} | in_v2={in_v2} | cites={cited} | {venue}")
        resolved.append({
            **cand,
            "openalex_id": wid,
            "doi": meta.get("doi"),
            "year": year,
            "venue": venue,
            "cited_by_count": cited,
            "in_v1_corpus": in_v1,
            "in_v2_corpus": in_v2,
            "title": title,
        })

    # Look up additional named candidates from spec
    print("\nLooking up additional named candidates...")
    additional_searches = [
        ("Molecular Transformer chemistry reaction", "Molecular Transformer (Schwaller)"),
        ("AlphaFold highly accurate protein structure prediction", "AlphaFold (Jumper 2021)"),
        ("De novo design protein RFdiffusion Watson", "RFdiffusion (Watson 2023)"),
    ]
    for query, label in additional_searches:
        w = resolve_by_title(query)
        if not w:
            print(f"  [not found] {label}")
            continue
        wid = w["id"]
        in_v2 = wid in v2_ids
        in_v1 = wid in v1_ids
        cited = w.get("cited_by_count", 0)
        venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name")
        print(f"  {label:55} | year={w.get('publication_year')} | in_v1={in_v1} | in_v2={in_v2} | cites={cited} | {venue}")
        if not in_v2:
            continue  # skip if not in our corpus
        resolved.append({
            "openalex_id": wid,
            "doi": w.get("doi"),
            "label": label,
            "subdomain": "additional",
            "year": w.get("publication_year"),
            "venue": venue,
            "cited_by_count": cited,
            "in_v1_corpus": in_v1,
            "in_v2_corpus": in_v2,
            "title": w.get("title"),
        })

    # Top-cited v2-only papers (papers entered by v2 expansion)
    v2_only_df = v2_df[v2_df["id"].isin(v2_only)].sort_values("cited_by_count", ascending=False)
    print(f"\nTop 30 v2-only papers (entered corpus due to expansion):")
    for _, r in v2_only_df.head(30).iterrows():
        title = (r["title"] or "")[:80]
        print(f"  {r['cited_by_count']:>5}  {r['publication_year']}  {title}  | {r['venue']}")

    # Final selection: target 10 v2 method canonicals
    # Priorities:
    #   - all the named candidates from spec that are in v2 (some may be in v1 too — still keep)
    #   - top-cited v2-only papers covering different methodology subdomains
    # We'll write the 10 explicitly here.

    selected_v2_methods = []
    # Include all named candidates that exist (regardless of whether in_v1 — they are methodologically canonical)
    for r in resolved:
        if r.get("title"):
            selected_v2_methods.append({
                "openalex_id": r["openalex_id"],
                "doi": r.get("doi"),
                "title": r["title"],
                "year": r["year"],
                "venue": r["venue"],
                "cited_by_count": r["cited_by_count"],
                "label": r["label"],
                "subdomain": r["subdomain"],
                "selection_rationale": "named in v2 spec Section 3 candidate list",
                "in_v1_corpus": r["in_v1_corpus"],
                "in_v2_corpus": r["in_v2_corpus"],
            })

    # If we have <10 named, add top-cited v2-only papers
    seen_ids = {s["openalex_id"] for s in selected_v2_methods}
    target = 10
    pad = []
    for _, r in v2_only_df.iterrows():
        if r["id"] in seen_ids:
            continue
        pad.append({
            "openalex_id": r["id"],
            "doi": r["doi"],
            "title": r["title"],
            "year": int(r["publication_year"]) if r["publication_year"] is not None else None,
            "venue": r["venue"],
            "cited_by_count": int(r["cited_by_count"]),
            "label": "top-cited-v2-only",
            "subdomain": "v2 expansion",
            "selection_rationale": "top-cited paper that entered corpus due to v2 expansion",
            "in_v1_corpus": False,
            "in_v2_corpus": True,
        })
        seen_ids.add(r["id"])
        if len(selected_v2_methods) + len(pad) >= 25:
            break

    selected_v2_methods.extend(pad)
    print(f"\nFinal v2 method canonical candidates: {len(selected_v2_methods)}")

    # v1 canonical papers — confirm metadata
    print("\nConfirming v1 canonical metadata...")
    v1_resolved = []
    for c in V1_DD_CANONICALS:
        meta = get_meta(c["id"])
        if meta:
            v1_resolved.append({
                "openalex_id": c["id"],
                "doi": meta.get("doi"),
                "title": meta.get("title"),
                "year": meta.get("publication_year"),
                "venue": ((meta.get("primary_location") or {}).get("source") or {}).get("display_name"),
                "cited_by_count": meta.get("cited_by_count", 0),
                "label": c["label"],
                "subdomain": "v1 drug-discovery AI canonical (specified)",
                "selection_rationale": "fixed by v2 spec Section 3",
                "in_v1_corpus": c["id"] in v1_ids,
                "in_v2_corpus": c["id"] in v2_ids,
            })
            print(f"  {c['label']:55} | cites={meta.get('cited_by_count',0)} | year={meta.get('publication_year')}")

    # Write output: full 22-set
    final_22 = v1_resolved + selected_v2_methods[:10]
    print(f"\nFinal canonical set: {len(v1_resolved)} v1 + {min(10, len(selected_v2_methods))} v2 = {len(final_22)}")

    out = {
        "v1_dd_canonicals": v1_resolved,
        "v2_method_canonical_candidates_resolved": selected_v2_methods,
        "v2_method_canonicals_selected_top_10": selected_v2_methods[:10],
        "final_22_set": final_22,
    }
    (RAW / "dd_and_methodology_canonical_papers.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nWrote raw/dd_and_methodology_canonical_papers.json")


if __name__ == "__main__":
    main()
