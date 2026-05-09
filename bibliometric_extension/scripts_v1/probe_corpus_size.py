"""
Estimate the primary drug-discovery AI corpus size before pulling everything.

OpenAlex's `default.search` does fuzzy search with stemming. To match the
spec's two-token-plus-AI requirement reasonably we use multiple specialized
filters and union-count via OR queries on title_and_abstract.search.
"""

import json
import sys
import time
from pathlib import Path

import pyalex
from pyalex import Works

pyalex.config.email = "bibliometric_extension@example.org"
pyalex.config.max_retries = 3

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)

DRUG_TERMS = [
    "drug discovery",
    "drug design",
    "drug repurposing",
    "molecular generation",
    "de novo design",
    "virtual screening",
    "ADMET prediction",
    "lead optimization",
    "binding affinity prediction",
    "compound generation",
]

AI_TERMS = [
    "deep learning",
    "machine learning",
    "artificial intelligence",
    "neural network",
    "transformer",
    "graph neural network",
    "diffusion model",
    "generative model",
    "foundation model",
    "large language model",
    "agent",
    "agentic",
]


def or_phrase(terms):
    # OpenAlex search supports parens and OR
    return "(" + " OR ".join(f'"{t}"' for t in terms) + ")"


def main():
    drug_or = or_phrase(DRUG_TERMS)
    ai_or = or_phrase(AI_TERMS)

    print(f"Drug-OR phrase: {drug_or[:120]}…")
    print(f"AI-OR phrase: {ai_or[:120]}…")

    # Each query: title-and-abstract search includes ANY drug term AND ANY AI term, 2017-2026
    print("\nProbing corpus size with strict filter (any drug term AND any AI term)…")
    res = (
        Works()
        .search_filter(title_and_abstract=drug_or + " AND " + ai_or)
        .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
        .filter(language="en")
    )
    page1 = res.get(per_page=1)
    meta = res.count()
    print(f"  count: {meta}")

    # Tighter: drug term in title, AI term anywhere
    print("\nProbing tighter (drug term in TITLE, AI term in title-or-abstract)…")
    res2 = (
        Works()
        .search_filter(title=drug_or)
        .search_filter(title_and_abstract=ai_or)
        .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
        .filter(language="en")
    )
    print(f"  count: {res2.count()}")

    # Even tighter: each in title
    print("\nProbing tightest (both in title)…")
    res3 = (
        Works()
        .search_filter(title=drug_or + " AND " + ai_or)
        .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
        .filter(language="en")
    )
    print(f"  count: {res3.count()}")

    # Save the probe
    (RAW / "corpus_probe.json").write_text(json.dumps({
        "drug_or_terms": DRUG_TERMS,
        "ai_or_terms": AI_TERMS,
        "drug_AND_ai_in_title_and_abstract": meta,
        "drug_in_title_AND_ai_anywhere": res2.count(),
        "both_in_title": res3.count(),
    }, indent=2))


if __name__ == "__main__":
    main()
