# Release Notes — v1.0

**Title:** Expanding the Method Space of Drug-Discovery AI: Directions from Creativity Research

**Author:** Matthew H. Maxwell

**Affiliation:** American Institute for Medical Research (AIMR)

**Date:** 2026-05-09

**License:** CC BY 4.0

---

## About this release

This release accompanies the preprint submission of *Expanding the Method Space of Drug-Discovery AI: Directions from Creativity Research* (Maxwell, 2026). The paper documents a citation gap between drug-discovery AI literature and creativity research, infers an architectural gap from that citation gap, and derives six research-derived architectural directions for future drug-discovery AI systems.

## What this release contains

The empirical core of the project at the moment of preprint submission:

**Primary deliverable:**
- `paper.md` — main paper (~22,500 words across 13 sections plus references), with four inline figures

**Standalone figures** (`figures/` directory):
- `figure_1_bibliometric_stability.svg` — citation rate stability across v1/v2/v3 corpus iterations
- `figure_2_figure_engagement.svg` — engagement with 30 canonical creativity-research figures (three-tier visualization)
- `figure_3_matrix_heatmap.svg` — 31 × 14 cell-status heatmap for the Creativity × Medical Discovery Matrix
- `figure_4_substrate_sharing.svg` — substrate-sharing relationships among the six derived hypotheses

**Bibliometric analysis artifacts:**
- `citation_network_analysis.md` — n=100 systematic citation survey methodology and findings, plus Section 8 reporting the bibliometric extension at scale
- `bibliometric_findings.md` (v1, strict drug-discovery), `bibliometric_findings_v2.md` (broader chemistry-AI methodology), `bibliometric_findings_v3.md` (final calibrated headline at 53,792-paper scale)
- `bibliometric_extension/` — execution specifications for the bibliometric corpus build

**Methodological accounting:**
- `philosophical_accounting.md` — substantive-vs-decorative philosophical apparatus accounting
- `novel_prediction_operationalization.md` — operationalization of Lakatosian "novel prediction" for P1's Programme-Progressivity Tracker, with six worked examples (imatinib, trastuzumab, CFTR modulators, amyloid-cascade, anti-VEGF, tau-targeting)
- `preregistered_matrix_predictions.md` — held-out validation on 8 drug-discovery AI systems not used in matrix construction

**Honest accounting of what's pending:**
- `MISSING_ARTIFACTS.md` — explicit accounting of supplementary materials referenced in the paper but not yet committed to this repository, with v1.1 commitment

**Release attachments (downloaded separately):**
- `bibliometrics_v1.tar.gz` (~33.5 MB) — v1 corpus raw data, scripts, run logs
- `bibliometrics_v2.tar.gz` (~33.4 MB) — v2 corpus raw data, scripts, run logs
- `bibliometrics_v3.tar.gz` (~51.1 MB) — v3 final corpus raw data, scripts, BERTopic model, run logs

## What this release does NOT yet contain (planned for v1.1)

Several supplementary artifacts referenced in the paper are not in v1.0 — see `MISSING_ARTIFACTS.md` for the full accounting. In summary: hypothesis specifications and implementation files (`proposals.md`, `p1_implementation.md` through `p6_implementation.md`), matrix population artifacts (`matrix_populated.md`, `matrix_drilldown.md`, `matrix_data.json`, `matrix_heatmap.html`), and review documents (`multidisciplinary_review.md`, `adversarial.md`, `experiments.md`) are pending audit. No fixed timeline; see `MISSING_ARTIFACTS.md` for the rationale.

The decision to release v1.0 with the empirical core rather than the full supplementary set was deliberate: honesty about what backs the paper is more important than completeness of supplementary materials.

## Headline empirical findings

- **Citation rate.** 22 of 53,792 corpus papers (0.041%) cite at least one of thirty canonical creativity-research figures; three substantive engagements appear, all at the biology-AI-philosophy frontier rather than in core methodology.
- **Stability.** Proportional citation rate is stable at 0.041–0.045% across v1, v2, v3 corpus iterations despite v3 being 74% larger than v1, ruling out the corpus-boundary objection from hostile review.
- **Parallel vocabulary.** Kuhn's "paradigm shift" appears in 411 corpus abstracts with zero Kuhn citations among them.
- **Architectural pattern.** Matrix analysis surfaces hybrid neurosymbolic architecture as Type 1 EMPTY across all 31 creativity sub-clusters under strict reading; held-out validation reproduces the pattern with one borderline KG-RAG exception (RUGGED) forcing threshold examination.

## What changed for v1.0 public release

The paper has been:

1. **Reframed for opportunity-forward presentation.** Title and opening emphasize the architectural directions the analysis points toward rather than leading with the citation-gap methodology. The citation gap and matrix analysis are framed as evidence supporting the inference that drug-discovery AI has committed to a narrower method space than it otherwise would, with six research-derived architectural directions translating the empty cells into specifiable AI systems.

2. **Calibrated against external citation verification** — language calibrated from "absolute absence" to "absence of sustained engagement with canonical creativity-process frameworks" after verifying that Krenn 2022 *Nature Reviews Physics* does cite Boden's *Mind as Machine* (2008) in cognitive-science / AI-history context. Several other citation corrections applied (Schwaller misattribution retracted; FunSearch and AlphaEvolve disambiguated; Coscientist abstract language corrected; Pineau et al. corrected to 2021).

3. **Substantial AI use disclosure** — Section 1.6 documents in detail how large language models (primarily Claude / Claude Code, Anthropic) contributed to the work, with explicit accountability statement and limitations acknowledgment.

4. **AIMR-only public positioning** — earlier private drafts referenced operational engagements that have been removed for the public version. The author signs as Matthew H. Maxwell, AIMR.

## Pre-registered limitations

The work's claim hierarchy (Established / Plausible / Speculative — see Section 1.1) is preserved with calibrated evidential strength at each level. The paper does not demonstrate that the derived architectural directions outperform existing dominant patterns in drug discovery; performance comparison requires implementation and validation work specified but not executed.

The matrix is the work of a single author throughout; cell classifications would likely shift at margins under further review.

## License

CC BY 4.0 (Creative Commons Attribution 4.0 International). Cite the preprint when referencing this work.

## Cite as

```
Maxwell, M.H. (2026). Expanding the Method Space of Drug-Discovery AI:
Directions from Creativity Research. SSRN preprint.
American Institute for Medical Research (AIMR).
```

## Acknowledgments

Section 1.6 of the paper details the substantial role of LLM assistance (primarily Claude / Claude Code, Anthropic) in producing this work, including the bibliometric extension at 53,792-paper scale that would not have been feasible without automated execution. The author takes full responsibility for all contents of the paper.
