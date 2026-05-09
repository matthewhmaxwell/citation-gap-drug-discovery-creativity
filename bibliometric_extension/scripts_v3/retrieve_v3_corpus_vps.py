"""
v3 corpus retrieval — runs on VPS with fresh OpenAlex budget.

Adds four sub-domain term groups to v2's filter:
- Protein structure / design AI
- Materials informatics
- Computational chemistry + ML
- QSAR / classical cheminformatics

Run: scp this to VPS, run there, scp parquet back.
"""

import json, time, sys
from pathlib import Path

import pyalex
from pyalex import Works
import pandas as pd
from tqdm import tqdm

pyalex.config.email = "biblio_v3@example.org"
pyalex.config.max_retries = 5
pyalex.config.retry_backoff_factor = 1.0

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
RAW.mkdir(exist_ok=True)

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
# v3 expansions
PROTEIN_AI_TERMS = [
    "protein structure prediction", "protein design",
    "protein language model", "antibody design",
    "structure-based protein design", "de novo protein",
]
MATERIALS_INFORMATICS_TERMS = [
    "materials informatics", "materials discovery",
    "crystal structure prediction", "materials machine learning",
    "inverse materials design", "high-throughput materials",
]
COMP_CHEMISTRY_ML_TERMS = [
    "DFT machine learning", "molecular dynamics machine learning",
    "quantum chemistry deep learning", "force field machine learning",
    "interatomic potential", "neural network potential",
    "machine learning potential", "ab initio machine learning",
]
QSAR_CLASSICAL_TERMS = [
    "QSAR", "quantitative structure activity",
    "molecular descriptor", "structure activity relationship",
    "QSPR", "quantitative structure property",
]
ALL_DOMAIN_TERMS = (
    DRUG_TERMS + CHEM_METHODOLOGY_TERMS
    + PROTEIN_AI_TERMS + MATERIALS_INFORMATICS_TERMS
    + COMP_CHEMISTRY_ML_TERMS + QSAR_CLASSICAL_TERMS
)
AI_TERMS = [
    "deep learning", "machine learning", "artificial intelligence",
    "neural network", "transformer", "graph neural network",
    "diffusion model", "generative model", "foundation model",
    "large language model", "LLM", "agent", "agentic",
]


def or_phrase(terms):
    return "(" + " OR ".join(f'"{t}"' for t in terms) + ")"


SELECT_FIELDS = [
    "id", "doi", "title", "publication_year", "publication_date",
    "type", "language", "cited_by_count",
    "authorships", "primary_location",
    "referenced_works", "concepts", "topics",
    "abstract_inverted_index",
]


def reconstruct_abstract(inv_idx):
    if not inv_idx:
        return None
    pos = []
    for word, ps in inv_idx.items():
        for p in ps:
            pos.append((p, word))
    pos.sort()
    return " ".join(w for _, w in pos)


def slim(w):
    primary_loc = w.get("primary_location") or {}
    src = (primary_loc.get("source") or {}) if isinstance(primary_loc, dict) else {}
    return {
        "id": w.get("id"),
        "doi": w.get("doi"),
        "title": w.get("title"),
        "publication_year": w.get("publication_year"),
        "publication_date": w.get("publication_date"),
        "type": w.get("type"),
        "language": w.get("language"),
        "cited_by_count": w.get("cited_by_count") or 0,
        "venue": src.get("display_name"),
        "venue_id": src.get("id"),
        "venue_type": src.get("type"),
        "authors": [(a.get("author") or {}).get("display_name") for a in (w.get("authorships") or [])][:10],
        "author_ids": [(a.get("author") or {}).get("id") for a in (w.get("authorships") or [])][:10],
        "n_authors": len(w.get("authorships") or []),
        "referenced_works": w.get("referenced_works") or [],
        "n_references": len(w.get("referenced_works") or []),
        "abstract": reconstruct_abstract(w.get("abstract_inverted_index")),
        "concepts": [
            {"id": c.get("id"), "display_name": c.get("display_name"), "score": c.get("score")}
            for c in (w.get("concepts") or [])
        ][:8],
        "topic_id": ((w.get("topics") or [{}])[0] or {}).get("id"),
        "topic_name": ((w.get("topics") or [{}])[0] or {}).get("display_name"),
    }


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "probe"
    domain_or = or_phrase(ALL_DOMAIN_TERMS)
    ai_or = or_phrase(AI_TERMS)
    query = domain_or + " AND " + ai_or

    print(f"Domain terms: {len(ALL_DOMAIN_TERMS)} (drug={len(DRUG_TERMS)} chem={len(CHEM_METHODOLOGY_TERMS)} "
          f"protein={len(PROTEIN_AI_TERMS)} materials={len(MATERIALS_INFORMATICS_TERMS)} "
          f"compchem={len(COMP_CHEMISTRY_ML_TERMS)} qsar={len(QSAR_CLASSICAL_TERMS)})")
    print(f"AI terms: {len(AI_TERMS)}")

    # Probe each subgroup separately too
    if cmd == "probe":
        for name, terms in [
            ("DRUG (v1)", DRUG_TERMS),
            ("CHEM_METHOD (v2)", CHEM_METHODOLOGY_TERMS),
            ("PROTEIN_AI (v3)", PROTEIN_AI_TERMS),
            ("MATERIALS (v3)", MATERIALS_INFORMATICS_TERMS),
            ("COMP_CHEM_ML (v3)", COMP_CHEMISTRY_ML_TERMS),
            ("QSAR (v3)", QSAR_CLASSICAL_TERMS),
        ]:
            sub_q = or_phrase(terms) + " AND " + ai_or
            n = (
                Works()
                .search_filter(title_and_abstract=sub_q)
                .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
                .filter(language="en")
                .count()
            )
            print(f"  {name:25} alone × AI: {n:,}")
            time.sleep(0.1)
        n_v3 = (
            Works()
            .search_filter(title_and_abstract=query)
            .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
            .filter(language="en")
            .count()
        )
        print(f"\nv3 union (all 6 groups OR-ed) AND AI: {n_v3:,}")
        return

    if cmd == "retrieve":
        q = (
            Works()
            .search_filter(title_and_abstract=query)
            .filter(from_publication_date="2017-01-01", to_publication_date="2026-05-09")
            .filter(language="en")
            .select(SELECT_FIELDS)
        )
        total = q.count()
        print(f"Expected: {total:,}")
        rows = []
        pbar = tqdm(total=total, unit="paper")
        for page in q.paginate(per_page=200, n_max=None):
            for w in page:
                rows.append(slim(w))
                pbar.update(1)
            time.sleep(0.05)
        pbar.close()

        df = pd.DataFrame(rows)
        out_pq = RAW / "primary_corpus_v3.parquet"
        df.to_parquet(out_pq, compression="zstd")
        print(f"Saved: {out_pq} ({out_pq.stat().st_size/1e6:.1f} MB)")
        print(f"Year distribution:")
        print(df["publication_year"].value_counts().sort_index(ascending=False).head(12).to_string())
        print(f"With abstract: {df['abstract'].notna().sum():,}; with refs: {(df['n_references']>0).sum():,}")

        (RAW / "primary_corpus_v3_meta.json").write_text(json.dumps({
            "drug_terms": DRUG_TERMS,
            "chem_methodology_terms": CHEM_METHODOLOGY_TERMS,
            "protein_ai_terms": PROTEIN_AI_TERMS,
            "materials_informatics_terms": MATERIALS_INFORMATICS_TERMS,
            "comp_chemistry_ml_terms": COMP_CHEMISTRY_ML_TERMS,
            "qsar_classical_terms": QSAR_CLASSICAL_TERMS,
            "ai_terms": AI_TERMS,
            "filter": query,
            "from_date": "2017-01-01",
            "to_date": "2026-05-09",
            "language": "en",
            "n_works": len(rows),
            "n_works_expected_by_count": total,
        }, indent=2))


if __name__ == "__main__":
    main()
