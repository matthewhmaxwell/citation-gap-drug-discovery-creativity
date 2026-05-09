"""
Check whether Coley 2019 and Schwaller 2020 papers are in the v2 corpus
filter — and if not, why. Also measures sensitivity of corpus size to
filter relaxations.
"""

import json
from pathlib import Path

import pyalex
from pyalex import Works
import requests

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 3

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"

DRUG_TERMS = [
    "drug discovery", "drug design", "drug repurposing",
    "molecular generation", "de novo design", "virtual screening",
    "ADMET prediction", "lead optimization", "binding affinity prediction",
    "compound generation",
]
CHEM_METHODOLOGY_TERMS = [
    "molecular machine learning", "autonomous chemistry",
    "autonomous chemical discovery", "autonomous synthesis",
    "retrosynthesis", "synthetic chemistry AI", "generative chemistry",
    "molecular property prediction", "chemoinformatics", "cheminformatics",
    "molecular representation learning", "chemical foundation model",
    "molecular foundation model", "reaction prediction",
    "self-driving laboratory", "self-driving lab", "autonomous laboratory",
]
AI_TERMS = [
    "deep learning", "machine learning", "artificial intelligence",
    "neural network", "transformer", "graph neural network",
    "diffusion model", "generative model", "foundation model",
    "large language model", "LLM", "agent", "agentic",
]


def search_doi(doi: str):
    """Look up a paper by DOI directly."""
    r = requests.get(f"https://api.openalex.org/works/doi:{doi}",
                     params={"mailto": "bibliometric_extension@example.org"},
                     timeout=30)
    if r.status_code == 200:
        return r.json()
    return None


def matches_filter(work, drug_terms, chem_terms, ai_terms):
    """Manually check whether work would match v2 filter."""
    title = (work.get("title") or "").lower()
    inv = work.get("abstract_inverted_index") or {}
    abstract_words = " ".join(inv.keys()).lower() if inv else ""
    text = title + " " + abstract_words
    drug_or_chem_hit = any(t.lower() in text for t in drug_terms + chem_terms)
    ai_hit = any(t.lower() in text for t in ai_terms)
    return drug_or_chem_hit, ai_hit, text


def main():
    # Coley 2019: "Autonomous Discovery in the Chemical Sciences Part II: Outlook"
    # Angewandte Chemie. DOI: 10.1002/anie.201909987
    # Schwaller 2020: "Molecular Machine Learning: The Future of Synthetic Chemistry?"
    # Angewandte Chemie. Note title actually is "...Discovery in the Chemical Sciences Part I: Progress"
    # Let me also check by title search.

    candidates = [
        ("Coley 2019 Part II", "10.1002/anie.201909987"),  # tentative
        ("Coley 2019 Part I",  "10.1002/anie.201909989"),  # tentative
    ]

    found_coley = None
    found_schwaller = None

    # Search by title for Coley
    print("Searching for Coley 2019 'Autonomous Discovery'...")
    res = Works().search("Autonomous Discovery in the Chemical Sciences").get(per_page=10)
    for w in res:
        title = (w.get("title") or "")
        year = w.get("publication_year")
        if "Autonomous Discovery in the Chemical Sciences" in title and year and year <= 2020:
            print(f"  Found: [{year}] {title}")
            print(f"    OpenAlex ID: {w['id']}")
            print(f"    DOI: {w.get('doi')}")
            d, a, _ = matches_filter(w, DRUG_TERMS, CHEM_METHODOLOGY_TERMS, AI_TERMS)
            print(f"    drug-or-chem term in title/abstract: {d}; AI term: {a}; would-match-v2: {d and a}")
            found_coley = w if "Outlook" in title or "Part II" in title else found_coley

    # Search by title for Schwaller 2020 Molecular ML
    print("\nSearching for Schwaller 2020 'Molecular Machine Learning'...")
    res = Works().search("Molecular Machine Learning Future Synthetic Chemistry").get(per_page=10)
    for w in res:
        title = (w.get("title") or "")
        year = w.get("publication_year")
        if "Molecular Machine Learning" in title and year and year <= 2021:
            print(f"  Found: [{year}] {title}")
            print(f"    OpenAlex ID: {w['id']}")
            print(f"    DOI: {w.get('doi')}")
            d, a, t = matches_filter(w, DRUG_TERMS, CHEM_METHODOLOGY_TERMS, AI_TERMS)
            print(f"    drug-or-chem term in title/abstract: {d}; AI term: {a}; would-match-v2: {d and a}")
            # show which terms matched
            chem_matches = [tt for tt in CHEM_METHODOLOGY_TERMS if tt.lower() in t]
            drug_matches = [tt for tt in DRUG_TERMS if tt.lower() in t]
            ai_matches = [tt for tt in AI_TERMS if tt.lower() in t]
            print(f"    chem-methodology terms matched: {chem_matches}")
            print(f"    drug terms matched: {drug_matches}")
            print(f"    AI terms matched: {ai_matches}")
            found_schwaller = w

    # Also search for ChemCrow, Coscientist, Burger 2020, RDChiral
    print("\nSearching for ChemCrow...")
    for w in Works().search("ChemCrow chemistry tools").get(per_page=5):
        title = (w.get("title") or "")
        if "chemistry" in title.lower() and "tools" in title.lower():
            year = w.get("publication_year")
            print(f"  [{year}] {title}")
            print(f"    OpenAlex ID: {w['id']}, DOI: {w.get('doi')}")
            break

    print("\nSearching for Coscientist (Boiko 2023)...")
    for w in Works().search("Autonomous chemical research large language models").get(per_page=5):
        title = (w.get("title") or "")
        year = w.get("publication_year")
        if "Autonomous chemical research" in title:
            print(f"  [{year}] {title}")
            print(f"    OpenAlex ID: {w['id']}, DOI: {w.get('doi')}")
            break

    print("\nSearching for Burger 2020 mobile robotic chemist...")
    for w in Works().search("mobile robotic chemist").get(per_page=5):
        title = (w.get("title") or "")
        year = w.get("publication_year")
        if "mobile robotic chemist" in title.lower():
            print(f"  [{year}] {title}")
            print(f"    OpenAlex ID: {w['id']}, DOI: {w.get('doi')}")
            break

    print("\nSearching for Molecular Transformer (Schwaller)...")
    for w in Works().search("Molecular Transformer Schwaller").get(per_page=5):
        title = (w.get("title") or "")
        year = w.get("publication_year")
        if "Molecular Transformer" in title:
            print(f"  [{year}] {title}")
            print(f"    OpenAlex ID: {w['id']}, DOI: {w.get('doi')}")
            break


if __name__ == "__main__":
    main()
