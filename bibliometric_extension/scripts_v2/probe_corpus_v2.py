"""
v2 corpus probe: estimate size before full retrieval.

v2 corpus filter (per spec Section 2):
- Date 2017-01-01 to 2026-05-09, English
- Title or abstract contains:
    (any drug-discovery term OR any chemistry-AI methodology term)
    AND any AI term
"""

import json
from pathlib import Path

import pyalex
from pyalex import Works

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 3

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)

# v1 drug-discovery terms (retained verbatim from v1 spec)
DRUG_TERMS = [
    "drug discovery", "drug design", "drug repurposing",
    "molecular generation", "de novo design", "virtual screening",
    "ADMET prediction", "lead optimization", "binding affinity prediction",
    "compound generation",
]

# v2 chemistry-AI methodology terms (per spec Section 2)
CHEM_METHODOLOGY_TERMS = [
    "molecular machine learning",
    "autonomous chemistry",
    "autonomous chemical discovery",
    "autonomous synthesis",
    "retrosynthesis",
    "synthetic chemistry AI",
    "generative chemistry",
    "molecular property prediction",
    "chemoinformatics",
    "cheminformatics",
    "molecular representation learning",
    "chemical foundation model",
    "molecular foundation model",
    "reaction prediction",
    "self-driving laboratory",
    "self-driving lab",
    "autonomous laboratory",
]

# v1 AI terms (retained)
AI_TERMS = [
    "deep learning", "machine learning", "artificial intelligence",
    "neural network", "transformer", "graph neural network",
    "diffusion model", "generative model", "foundation model",
    "large language model", "LLM", "agent", "agentic",
]


def or_phrase(terms):
    return "(" + " OR ".join(f'"{t}"' for t in terms) + ")"


def main():
    drug_or = or_phrase(DRUG_TERMS)
    chem_or = or_phrase(CHEM_METHODOLOGY_TERMS)
    drug_plus_chem_or = "(" + " OR ".join(f'"{t}"' for t in DRUG_TERMS + CHEM_METHODOLOGY_TERMS) + ")"
    ai_or = or_phrase(AI_TERMS)

    # v1-strict probe (for comparison)
    v1_strict = (
        Works()
        .search_filter(title_and_abstract=drug_or + " AND " + ai_or)
        .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
        .filter(language="en")
    ).count()
    print(f"v1 strict (drug AND AI): {v1_strict:,}")

    # v2-broad probe
    v2_broad = (
        Works()
        .search_filter(title_and_abstract=drug_plus_chem_or + " AND " + ai_or)
        .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
        .filter(language="en")
    ).count()
    print(f"v2 broad ((drug OR chem-methodology) AND AI): {v2_broad:,}")

    # Chem-methodology only (papers added by v2 expansion)
    chem_only = (
        Works()
        .search_filter(title_and_abstract=chem_or + " AND " + ai_or)
        .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
        .filter(language="en")
    ).count()
    print(f"chem-methodology only AND AI: {chem_only:,}")

    addition_estimate = v2_broad - v1_strict
    print(f"v2 expansion adds approximately: {addition_estimate:,} papers")

    (RAW / "corpus_probe_v2.json").write_text(json.dumps({
        "drug_terms": DRUG_TERMS,
        "chem_methodology_terms": CHEM_METHODOLOGY_TERMS,
        "ai_terms": AI_TERMS,
        "v1_strict_count": v1_strict,
        "v2_broad_count": v2_broad,
        "chem_only_count": chem_only,
        "v2_expansion_estimate": addition_estimate,
    }, indent=2))


if __name__ == "__main__":
    main()
