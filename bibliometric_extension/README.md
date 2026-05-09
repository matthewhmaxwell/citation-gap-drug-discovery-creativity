# Bibliometric extension — execution specs and reproducibility scripts

This directory holds the specifications and reproducibility scripts for the bibliometric corpus build at three iterations (v1, v2, v3).

## Contents

```
bibliometric_extension/
├── README.md                        # this file
├── extension_spec.md                # v1 specification (strict drug-discovery corpus)
├── extension_spec_v2.md             # v2 specification (broader chemistry-AI methodology)
├── run_v1.sh                        # v1 end-to-end runner
├── run_v2.sh                        # v2 end-to-end runner
├── scripts_v1/                      # v1 Python pipeline (15 scripts)
├── scripts_v2/                      # v2 Python pipeline (13 scripts)
└── scripts_v3/                      # v3 Python pipeline (11 scripts)
```

## Where the raw data lives

The raw OpenAlex parquet files (~32–49 MB each), saved BERTopic models, run logs, and processed CSVs are **NOT** committed to this repository. They are attached to the v1.0 release as `.tar.gz` downloads:

| Tarball | Size | Contents |
|---|---|---|
| `bibliometrics_v1.tar.gz` | ~32 MB | v1 strict drug-discovery corpus (30,935 papers) + scripts + run logs + BERTopic model |
| `bibliometrics_v2.tar.gz` | ~32 MB | v2 broader chemistry-AI methodology corpus (33,469 papers) + scripts + run logs + BERTopic model |
| `bibliometrics_v3.tar.gz` | ~49 MB | v3 final corpus (53,792 papers) + scripts + run logs + BERTopic model + cross-OpenAlex co-citation results |

Download from the [v1.0-biorxiv-preprint release page](../../releases/tag/v1.0-biorxiv-preprint).

## To reproduce

1. Download a tarball (e.g. `bibliometrics_v3.tar.gz`)
2. Extract to a working directory: `tar xzf bibliometrics_v3.tar.gz`
3. The extracted `bibliometrics_v3/` contains a `.venv/` symlink (broken — needs recreation), `raw/`, `processed/`, `outputs/`, `scripts/`, and `run_full_analysis_v2.sh`.
4. Recreate the venv:
   ```
   python3 -m venv .venv
   .venv/bin/pip install pyalex pandas numpy pyarrow tqdm bertopic sentence-transformers scikit-learn umap-learn hdbscan tabulate requests
   ```
5. Re-run analyses (see each `bibliometric_findings*.md` for analysis-specific commands)

## OpenAlex budget caveat

The cross-OpenAlex co-citation analysis (3.2) requires ~3,432 (v2) or ~4,212 (v3) chained-cites pair queries. OpenAlex's polite pool enforces a $1/day budget cap per IP (~10,000 chained-cites queries per day). v2's 3.2 hit this cap mid-run; v3's 3.2 was completed from a different IP with a fresh daily budget.

If reproducing 3.2 cross-OpenAlex, plan for either a paid OpenAlex API key, multiple IPs, or splitting the analysis across multiple days.

## Within-corpus 3.2 substitute

For analysis 3.2 without cross-OpenAlex API budget, the within-corpus co-citation derivation (`analysis_3_2_v[2,3]_within_corpus.py`) computes co-citation counts from the corpus's own reference lists — no further API calls. This is a strict subset of cross-OpenAlex co-citation but captures the methodology-layer signal sufficient for outcome classification.

## v1 → v2 → v3 progression

The three corpora represent escalating responses to scope-narrowness concerns. Each iteration adds keyword groups to the OpenAlex filter:

- **v1**: `(drug-discovery term) AND (AI term)` — strict
- **v2**: v1 OR `chemistry-AI methodology terms` (molecular ML, autonomous chemistry, retrosynthesis, etc.)
- **v3**: v2 OR `protein-AI / materials informatics / computational-chemistry-ML / QSAR-cheminformatics`

The proportional citation rate (papers in corpus citing canonical creativity figures) is stable at 0.041–0.045% across all three iterations despite the v1→v3 corpus growth of 74%. The architectural-impoverishment inference for the methodology layer is robust to the corpus boundary choice.

See `bibliometric_findings_v3.md` (in the repo root) for the final calibrated headline; `bibliometric_findings.md` and `bibliometric_findings_v2.md` are preserved for record but superseded.
