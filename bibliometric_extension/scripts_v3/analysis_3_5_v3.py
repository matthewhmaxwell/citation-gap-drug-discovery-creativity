"""
3.5 v2 — counterexample classification + fuzzy concept scan.

Reuses v1 fuzzy patterns; runs them against the v3 corpus.
Adds a 'chemistry-AI methodology primary' classification as required by spec.
"""

import json
import re
from pathlib import Path
from collections import defaultdict

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
PROC.mkdir(exist_ok=True)
V1_RAW = ROOT.parent / "bibliometrics" / "raw"
V1_PROC = ROOT.parent / "bibliometrics" / "processed"


SURNAME_PATTERNS = [
    ("Wiggins", r"\bWiggins\b"),
    ("Boden", r"\bBoden\b"),
    ("Hofstadter", r"\bHofstadter\b"),
    ("Lakatos", r"\bLakatos\b"),
    ("Wallas", r"\bWallas\b"),
    ("Csikszentmihalyi", r"\bCsikszentmih"),
    ("Gentner", r"\bGentner\b"),
    ("Fauconnier", r"\bFauconnier\b"),
    ("Finke", r"\bFinke\b"),
    ("Koestler", r"\bKoestler\b"),
    ("Levin (Tufts)", r"\bLevin\b"),
    ("Simon (Herbert)", r"H(\.?)\s*A(\.?)\s*Simon\b|Herbert\s+Simon"),
    ("Newell (Allen)", r"Allen\s+Newell|\bNewell\b"),
    ("Amabile", r"\bAmabile\b"),
    ("Sternberg", r"\bSternberg\b"),
    ("Campbell (Donald T.)", r"D(\.?)\s*T(\.?)\s*Campbell|Donald\s+(T\.?\s+)?Campbell"),
    ("Simonton", r"\bSimonton\b"),
    ("Schon", r"\bSch(o|ö)n\b"),
    ("Alexander (Christopher)", r"Christopher\s+Alexander"),
    ("Altshuller", r"\bAltshuller\b|\bAltshul[lt]?er\b"),
    ("Stokes (Donald)", r"Donald\s+(E\.?\s+)?Stokes|Stokes,\s*D"),
    ("Hutchins", r"\bHutchins\b"),
    ("Clark (Andy)", r"Andy\s+Clark"),
    ("Chalmers (David)", r"David\s+Chalmers|D(\.?)\s*J(\.?)\s*Chalmers"),
    ("Latour", r"\bLatour\b"),
    ("Knorr-Cetina", r"Knorr[\s-]?Cetina"),
    ("Kuhn (Thomas)", r"Thomas\s+(S\.?\s+)?Kuhn|\bT(\.?)\s*S(\.?)\s*Kuhn\b"),
    ("Feyerabend", r"\bFeyerabend\b"),
    ("Kauffman", r"\bKauffman\b"),
    ("Kaufman (James C.)", r"James\s+C\.?\s+Kaufman|J(\.?)\s*C(\.?)\s*Kaufman"),
    ("Runco", r"\bRunco\b"),
]

CONCEPT_PATTERNS = [
    ("structure-mapping", r"structure[\s-]?mapping"),
    ("conceptual blending", r"conceptual blending|conceptual integration"),
    ("bisociation", r"bisociation"),
    ("R/T/E formalism", r"\bR/T/E\b"),
    ("preinventive structures", r"pre[\s-]?inventive structures?"),
    ("incubation phase", r"\bincubation\b.{0,50}\b(phase|stage|period)\b|preparation.{0,30}illumination"),
    ("flow state (Csikszentmihalyi)", r"\bflow state\b|flow theory"),
    ("paradigm shift (Kuhn)", r"paradigm[\s-]?shift|paradigm[\s-]?change"),
    ("research programme (Lakatos)", r"research programme|research program of(ten)?\s+lakatos"),
    ("blind variation", r"blind variation"),
    ("adjacent possible (Kauffman)", r"adjacent[\s-]?possible"),
    ("bounded rationality (Simon)", r"bounded rationality"),
    ("problem space (Newell-Simon)", r"problem[\s-]?space\s+search"),
    ("componential theory (Amabile)", r"componential theory"),
    ("Pasteur's quadrant (Stokes)", r"pasteur'?s\s+quadrant"),
    ("TRIZ", r"\bTRIZ\b"),
    ("pattern language (Alexander)", r"pattern language"),
    ("reflective practitioner (Schön)", r"reflective practitioner"),
    ("extended mind", r"extended mind"),
    ("distributed cognition (Hutchins)", r"distributed cognition"),
    ("epistemic culture (Knorr-Cetina)", r"epistemic culture"),
    ("actor-network (Latour)", r"actor[\s-]?network"),
    ("4P / 4Ps (Rhodes)", r"\b4P[s]?\b|four\s*P[s]?\b"),
    ("xenobot", r"xenobot"),
    ("TAME (Levin)", r"\bTAME\b|technological approach to mind"),
]

DD_KEYWORDS = ["drug discovery", "drug design", "drug repurposing", "molecular generation",
               "de novo design", "virtual screening", "ADMET", "lead optimization",
               "binding affinity", "compound generation", "ligand", "molecular design",
               "small molecule", "qsar", "molecular property", "smiles"]
CHEM_AI_KEYWORDS = ["molecular machine learning", "autonomous chemistry", "autonomous chemical",
                    "autonomous synthesis", "retrosynthesis", "synthetic chemistry", "generative chemistry",
                    "chemoinformatics", "cheminformatics", "molecular representation", "chemical foundation",
                    "molecular foundation", "reaction prediction", "self-driving lab", "autonomous laboratory"]
SURVEY_KEYWORDS = ["survey", "review", "overview", "perspective", "viewpoint",
                   "editorial", "introduction", "comment"]
EPISTEM_KEYWORDS = ["epistemological", "epistemology", "philosophy of", "post-truth",
                    "ethics", "creativity", "creative"]


def main():
    df = pd.read_parquet(RAW / "primary_corpus_v3.parquet")
    citing = json.loads((PROC / "direct_citation_v3_citing_papers.json").read_text())

    # Build pid -> [canonicals cited] map
    pid_to_canons = defaultdict(list)
    for cid, rec in citing.items():
        for cit in rec["citing_papers"]:
            pid_to_canons[cit["corpus_paper_id"]].append({
                "canonical_id": cid,
                "figure_group": rec["figure_group"],
                "individual_name": rec["individual_name"],
                "canonical_title": rec["canonical_title"],
                "canonical_year": rec["canonical_year"],
            })

    classified = []
    for pid, canons in pid_to_canons.items():
        row = df[df["id"] == pid]
        if len(row) == 0:
            continue
        r = row.iloc[0]
        title = str(r["title"] or "")
        abstract = str(r["abstract"] or "") if pd.notna(r["abstract"]) else ""
        text = (title + " " + abstract).lower()

        is_dd = any(kw in text for kw in DD_KEYWORDS)
        is_chem_ai = any(kw in text for kw in CHEM_AI_KEYWORDS)
        is_survey = any(kw in title.lower() for kw in SURVEY_KEYWORDS)
        is_epistem = any(kw in text for kw in EPISTEM_KEYWORDS)
        figure_in_title = any(
            (c.get("individual_name") or "").split()[-1].lower() in title.lower()
            for c in canons
        )

        if is_dd:
            paper_class = "drug-discovery-AI primary"
        elif is_chem_ai:
            paper_class = "chemistry-AI methodology primary"
        elif is_survey:
            paper_class = "survey/position adjacent"
        else:
            paper_class = "tangential corpus member"
        depth = "substantive" if (is_epistem or figure_in_title) else "passing"

        classified.append({
            "corpus_paper_id": pid,
            "doi": r["doi"],
            "title": r["title"],
            "year": int(r["publication_year"]) if r["publication_year"] is not None else None,
            "venue": r["venue"],
            "type": r["type"],
            "n_canonicals_cited": len(canons),
            "figure_groups": " | ".join(sorted(set(c["figure_group"] for c in canons))),
            "canonical_titles": " | ".join(c["canonical_title"] for c in canons),
            "paper_class": paper_class,
            "engagement_depth": depth,
        })

    out_df = pd.DataFrame(classified).sort_values("year")
    out_df.to_csv(PROC / "counterexample_v3_classified.csv", index=False)
    print(f"v2 counterexamples: {len(out_df)}")
    print("\nClassification breakdown:")
    print(out_df.groupby(["paper_class","engagement_depth"]).size().to_string())
    print()

    # Compare to v1
    v1_class = pd.read_csv(V1_PROC / "counterexample_classified.csv")
    print("v1 classification (for comparison):")
    print(v1_class.groupby(["paper_class","engagement_depth"]).size().to_string())

    # Print all v2 papers
    print(f"\nAll {len(out_df)} v2 counterexample papers:")
    for _, r in out_df.iterrows():
        new_in_v2 = r["corpus_paper_id"] not in set(v1_class["corpus_paper_id"].dropna())
        marker = "[NEW in v2]" if new_in_v2 else "          "
        print(f"  {marker} {r['year']} | {r['paper_class']:30} | {r['engagement_depth']:11} | "
              f"{r['figure_groups']:25} | {(r['title'] or '')[:75]}")

    # Fuzzy scan
    print("\nFuzzy concept scan over v3 corpus (~33K papers)...")
    surname_re = [(label, re.compile(p, re.I)) for label, p in SURNAME_PATTERNS]
    concept_re = [(label, re.compile(p, re.I)) for label, p in CONCEPT_PATTERNS]
    surname_hits = {label: [] for label, _ in surname_re}
    concept_hits = {label: [] for label, _ in concept_re}

    for _, r in df.iterrows():
        title = str(r["title"]) if pd.notna(r["title"]) else ""
        abstract = str(r["abstract"]) if pd.notna(r["abstract"]) else ""
        text = title + " " + abstract
        if not text.strip():
            continue
        for label, pat in surname_re:
            m = pat.search(text)
            if m:
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                surname_hits[label].append({"id": r["id"], "year": int(r["publication_year"]) if r["publication_year"] is not None else None, "match": m.group(0), "context": text[start:end]})
        for label, pat in concept_re:
            m = pat.search(text)
            if m:
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                concept_hits[label].append({"id": r["id"], "year": int(r["publication_year"]) if r["publication_year"] is not None else None, "match": m.group(0), "context": text[start:end]})

    # Filter Levin context for bioelectric/xenobot (same as v1)
    def filter_levin(hits):
        keep = []
        for h in hits:
            ctx = (h["context"] or "").lower()
            if any(k in ctx for k in ["xenobot", "bioelectric", "regen", "morphogen", "planar",
                                       "multi-scale", "tufts", "tame", "agency", "anatomi"]):
                keep.append(h)
        return keep

    surname_hits["Levin (Tufts)"] = filter_levin(surname_hits["Levin (Tufts)"])

    # Compare to v1 hits
    v1_fuzzy = pd.read_csv(V1_PROC / "fuzzy_scan_summary.csv")
    v1_concept = v1_fuzzy[v1_fuzzy["kind"] == "concept"].set_index("label")["n_papers"].to_dict()
    v1_surname = v1_fuzzy[v1_fuzzy["kind"] == "surname"].set_index("label")["n_papers"].to_dict()

    print("\nConcept hits (v1 → v2, sorted by v2 count desc):")
    for label, hits in sorted(concept_hits.items(), key=lambda kv: -len(kv[1])):
        v1_n = v1_concept.get(label, 0)
        v2_n = len(hits)
        delta = v2_n - v1_n
        print(f"  {label:35} v1={v1_n:>4}  v2={v2_n:>4}  delta={delta:+}")

    print("\nSurname hits (v1 → v2, sorted by v2 count desc):")
    for label, hits in sorted(surname_hits.items(), key=lambda kv: -len(kv[1])):
        v1_n = v1_surname.get(label, 0)
        v2_n = len(hits)
        delta = v2_n - v1_n
        print(f"  {label:35} v1={v1_n:>4}  v2={v2_n:>4}  delta={delta:+}")

    summary_rows = []
    for label, hits in concept_hits.items():
        summary_rows.append({"kind": "concept", "label": label, "n_papers_v2": len(hits), "n_papers_v1": v1_concept.get(label, 0), "delta": len(hits) - v1_concept.get(label, 0)})
    for label, hits in surname_hits.items():
        summary_rows.append({"kind": "surname", "label": label, "n_papers_v2": len(hits), "n_papers_v1": v1_surname.get(label, 0), "delta": len(hits) - v1_surname.get(label, 0)})
    pd.DataFrame(summary_rows).to_csv(PROC / "fuzzy_scan_v3_with_v1_compare.csv", index=False)
    (PROC / "fuzzy_concept_hits_v3.json").write_text(json.dumps(concept_hits, indent=2, ensure_ascii=False))
    (PROC / "fuzzy_surname_hits_v3.json").write_text(json.dumps(surname_hits, indent=2, ensure_ascii=False))
    print("\nWrote fuzzy_*_v2*.{json,csv}")


if __name__ == "__main__":
    main()
