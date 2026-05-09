"""
3.5 Counterexample search at scale.

Builds on 3.1 (which already finds papers in the primary corpus citing
≥1 canonical work). Here we (a) re-fetch each citing paper's full
metadata (abstract + venue + concepts) so we can classify, and (b) run
a fuzzy text-search pass over the corpus abstracts for figure-name
strings (catches in-text mentions that may not have made it into
referenced_works due to OpenAlex coverage gaps).
"""

import json
import re
import time
from pathlib import Path

import pandas as pd
import pyalex
from pyalex import Works
from tqdm import tqdm

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 5

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
PROC = ROOT / "processed"
PROC.mkdir(exist_ok=True)


def short_id(url: str) -> str:
    return url.rsplit("/", 1)[-1]


def reconstruct_abstract(inv_idx):
    if not inv_idx:
        return None
    positions = []
    for word, ps in inv_idx.items():
        for p in ps:
            positions.append((p, word))
    positions.sort()
    return " ".join(w for _, w in positions)


# Surname-only patterns (used for fuzzy abstract scan).
# Use word boundaries to avoid false positives. Some surnames are too generic
# to scan reliably (Smith, Ward, Newell — last is OK but the others are noisy).
SURNAME_PATTERNS = [
    ("Wiggins", r"\bWiggins\b"),
    ("Boden", r"\bBoden\b"),
    ("Hofstadter", r"\bHofstadter\b"),
    ("Lakatos", r"\bLakatos\b"),
    ("Wallas", r"\bWallas\b"),
    ("Csikszentmihalyi", r"\bCsikszentmih"),  # forgive umlaut variations
    ("Gentner", r"\bGentner\b"),
    ("Fauconnier", r"\bFauconnier\b"),
    ("Finke", r"\bFinke\b"),
    ("Koestler", r"\bKoestler\b"),
    ("Levin (Tufts)", r"\bLevin\b"),  # noisy — needs context filter
    ("Simon (Herbert)", r"\bH(\.?)\s*A(\.?)\s*Simon\b|Herbert\s+Simon"),
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

# Generic "creativity-research framework" terms: structure-mapping, bisociation, etc.
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


def main():
    print("Loading primary corpus & 3.1 outputs...")
    df = pd.read_parquet(RAW / "primary_corpus.parquet")
    citing = json.loads((PROC / "direct_citation_citing_papers.json").read_text())
    canon = json.loads((RAW / "canonical_papers.json").read_text())

    # Step 1: Re-classify the 3.1 papers (load richer metadata)
    classified = []
    seen_paper_ids = set()
    for cid, rec in citing.items():
        for cit in rec["citing_papers"]:
            pid = cit["corpus_paper_id"]
            if pid in seen_paper_ids:
                continue
            seen_paper_ids.add(pid)
            row = df[df["id"] == pid]
            if len(row) == 0:
                continue
            r = row.iloc[0]
            # Aggregate which canonical IDs this paper cited
            cited_canons_for_paper = []
            for c2 in citing.values():
                for ccp in c2["citing_papers"]:
                    if ccp["corpus_paper_id"] == pid:
                        cited_canons_for_paper.append({
                            "canonical_id": list(citing.keys())[list(citing.values()).index(c2)],
                            "figure_group": c2["figure_group"],
                            "title": c2["canonical_title"],
                        })
                        break
            classified.append({
                "corpus_paper_id": pid,
                "doi": r["doi"],
                "title": r["title"],
                "year": int(r["publication_year"]) if r["publication_year"] is not None else None,
                "venue": r["venue"],
                "type": r["type"],
                "abstract": r["abstract"],
                "n_corpus_refs": int(r["n_references"]),
                "concepts": r["concepts"],
                "cited_canonicals": cited_canons_for_paper,
            })

    # Build dedup'd cited-canonicals view
    pid_to_canons = {}
    for cid, rec in citing.items():
        for cit in rec["citing_papers"]:
            pid = cit["corpus_paper_id"]
            pid_to_canons.setdefault(pid, []).append({
                "canonical_id": cid,
                "figure_group": rec["figure_group"],
                "individual_name": rec["individual_name"],
                "canonical_title": rec["canonical_title"],
                "canonical_year": rec["canonical_year"],
            })
    for c in classified:
        c["cited_canonicals"] = pid_to_canons.get(c["corpus_paper_id"], [])

    # Heuristic classification
    DD_KEYWORDS = ["drug discovery", "drug design", "drug repurposing", "molecular generation",
                   "de novo design", "virtual screening", "ADMET", "lead optimization",
                   "binding affinity", "compound generation", "ligand", "molecular design",
                   "small molecule", "qsar", "molecular property", "smiles"]
    SURVEY_KEYWORDS = ["survey", "review", "overview", "perspective", "viewpoint",
                       "editorial", "introduction", "comment"]
    EPISTEM_KEYWORDS = ["epistemological", "epistemology", "philosophy of", "post-truth",
                       "ethics", "creativity", "creative"]

    def classify(c):
        t = str(c["title"] or "").lower() if not pd.isna(c.get("title")) else ""
        a = str(c["abstract"] or "").lower() if not pd.isna(c.get("abstract")) else ""
        text = t + " | " + a
        is_dd = any(kw in text for kw in DD_KEYWORDS)
        is_survey = any(kw in t for kw in SURVEY_KEYWORDS)
        is_epistem = any(kw in text for kw in EPISTEM_KEYWORDS)
        # depth: substantive if any creativity/AI epistem keyword OR if the paper title contains the figure name
        figure_in_title = any(
            (canc.get("individual_name") or "").split()[-1].lower() in t
            for canc in c["cited_canonicals"]
        )
        if is_dd:
            primary = "drug-discovery-AI primary"
        elif is_survey:
            primary = "survey/position adjacent"
        else:
            primary = "tangential corpus member"
        depth = "substantive" if (is_epistem or figure_in_title) else "passing"
        return primary, depth

    for c in classified:
        c["paper_class"], c["engagement_depth"] = classify(c)

    out_df = pd.DataFrame([
        {
            "corpus_paper_id": c["corpus_paper_id"],
            "doi": c["doi"],
            "title": c["title"],
            "year": c["year"],
            "venue": c["venue"],
            "type": c["type"],
            "n_canonicals_cited": len(c["cited_canonicals"]),
            "figure_groups": " | ".join(sorted(set(x["figure_group"] for x in c["cited_canonicals"]))),
            "canonical_titles": " | ".join(x["canonical_title"] for x in c["cited_canonicals"]),
            "paper_class": c["paper_class"],
            "engagement_depth": c["engagement_depth"],
        } for c in classified
    ])
    out_df.to_csv(PROC / "counterexample_classified.csv", index=False)
    # Convert any numpy arrays in classified records to plain types
    def _normalize(x):
        try:
            import numpy as _np
            if isinstance(x, _np.ndarray):
                return [_normalize(v) for v in x.tolist()]
        except Exception:
            pass
        if isinstance(x, dict):
            return {k: _normalize(v) for k, v in x.items()}
        if isinstance(x, list):
            return [_normalize(v) for v in x]
        if pd.isna(x) if not isinstance(x, (list, dict, set)) else False:
            return None
        return x
    classified_clean = [_normalize(c) for c in classified]
    (PROC / "counterexample_full.json").write_text(json.dumps(classified_clean, indent=2, ensure_ascii=False, default=str))
    print(f"\nWrote processed/counterexample_classified.csv ({len(out_df)} rows)")
    print(f"Wrote processed/counterexample_full.json")
    print("\nClassification breakdown:")
    print(out_df.groupby(["paper_class","engagement_depth"]).size().to_string())

    # Step 2: Fuzzy abstract scan for figure surnames + concept terms
    print("\nFuzzy abstract scan over primary corpus...")
    surname_re = [(label, re.compile(p, re.I)) for label, p in SURNAME_PATTERNS]
    concept_re = [(label, re.compile(p, re.I)) for label, p in CONCEPT_PATTERNS]

    surname_hits: dict[str, list] = {label: [] for label, _ in surname_re}
    concept_hits: dict[str, list] = {label: [] for label, _ in concept_re}

    for _, r in df.iterrows():
        title = str(r["title"]) if not pd.isna(r["title"]) else ""
        abstract = str(r["abstract"]) if not pd.isna(r["abstract"]) else ""
        text = title + " " + abstract
        if not text.strip():
            continue
        for label, pat in surname_re:
            m = pat.search(text)
            if m:
                # context window
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                ctx = text[start:end]
                surname_hits[label].append({
                    "corpus_paper_id": r["id"],
                    "title": r["title"],
                    "year": int(r["publication_year"]) if r["publication_year"] is not None else None,
                    "venue": r["venue"],
                    "match": m.group(0),
                    "context": ctx,
                })
        for label, pat in concept_re:
            m = pat.search(text)
            if m:
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                ctx = text[start:end]
                concept_hits[label].append({
                    "corpus_paper_id": r["id"],
                    "title": r["title"],
                    "year": int(r["publication_year"]) if r["publication_year"] is not None else None,
                    "venue": r["venue"],
                    "match": m.group(0),
                    "context": ctx,
                })

    # Filter Levin / Newell hits down to those whose context suggests the right person
    def filter_levin(hits):
        # Keep only those whose context mentions xenobots, bioelectric, regen, morphogenesis,
        # planar, multi-scale, or Tufts
        keep = []
        for h in hits:
            ctx = (h["context"] or "").lower()
            if any(k in ctx for k in ["xenobot", "bioelectric", "regen", "morphogen", "planar",
                                       "multi-scale", "tufts", "tame", "agency", "anatomi"]):
                keep.append(h)
        return keep

    if "Levin (Tufts)" in surname_hits:
        before = len(surname_hits["Levin (Tufts)"])
        surname_hits["Levin (Tufts)"] = filter_levin(surname_hits["Levin (Tufts)"])
        print(f"  Levin filter: {before} -> {len(surname_hits['Levin (Tufts)'])} (kept those with bioelectric/xenobot/morphogenesis context)")

    # Filter Smith hits — too generic without context
    # Skip Smith entirely from output
    surname_hits_summary = {k: len(v) for k, v in surname_hits.items()}
    concept_hits_summary = {k: len(v) for k, v in concept_hits.items()}
    print("\nSurname hits in corpus abstracts:")
    for k, v in sorted(surname_hits_summary.items(), key=lambda x: -x[1]):
        print(f"  {v:>4}  {k}")
    print("\nConcept hits in corpus abstracts:")
    for k, v in sorted(concept_hits_summary.items(), key=lambda x: -x[1]):
        print(f"  {v:>4}  {k}")

    (PROC / "fuzzy_surname_hits.json").write_text(json.dumps(surname_hits, indent=2, ensure_ascii=False))
    (PROC / "fuzzy_concept_hits.json").write_text(json.dumps(concept_hits, indent=2, ensure_ascii=False))
    print("\nWrote processed/fuzzy_surname_hits.json")
    print("Wrote processed/fuzzy_concept_hits.json")

    summary_rows = []
    for k, v in concept_hits_summary.items():
        summary_rows.append({"kind": "concept", "label": k, "n_papers": v})
    for k, v in surname_hits_summary.items():
        summary_rows.append({"kind": "surname", "label": k, "n_papers": v})
    pd.DataFrame(summary_rows).to_csv(PROC / "fuzzy_scan_summary.csv", index=False)


if __name__ == "__main__":
    main()
