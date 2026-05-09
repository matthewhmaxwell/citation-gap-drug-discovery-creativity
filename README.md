# Citation Gap: Drug-Discovery AI and Creativity Research

Companion repository to the bioRxiv preprint *The Citation Gap Between Drug-Discovery AI and Creativity Research: A 53,792-Paper Bibliometric Analysis with Architectural Hypotheses* (Maxwell, 2026).

## What this is

This repo accompanies a paper that documents the citation gap between drug-discovery AI and creativity research at two empirical scales (n=100 structured systematic survey + 53,792-paper formal bibliometric extension), characterizes the gap with a 31-row × 14-column structured matrix populating creativity-framework × AI-method cell statuses, and derives six architectural hypotheses (P1–P6) for testing.

The repo's empirical core (paper, four figures, bibliometric findings, philosophical accounting, held-out validation, novel-prediction operationalization) is committed here. Several supplementary materials referenced in the paper are pending v1.1 — see [`MISSING_ARTIFACTS.md`](MISSING_ARTIFACTS.md) for the honest accounting.

## Headline empirical findings

| Metric | Result |
|---|---|
| Corpus size (v3, broadest) | **53,792 papers** (drug-discovery AI + chem-AI methodology + protein-AI + materials informatics + comp-chem-ML + QSAR/cheminformatics) |
| Direct-citation rate | **22 papers (0.041%)** cite ≥1 of 30 canonical creativity-research figures |
| Substantive engagements | **3** — all at the biology-AI-philosophy frontier, none in core methodology |
| Citation-rate stability across corpora | **0.041–0.045%** across v1 (30,935 papers) → v2 (33,469) → v3 (53,792); 74% corpus growth, rate unchanged — empirically rules out corpus-boundary objection |
| Kuhn parallel-vocabulary | **"paradigm shift" in 411 corpus abstracts with zero Kuhn citations among them** — cleanest single quantification of reinvention without attribution |
| Topic-modeling community separation | Max community balance 0.018 in v3 (lower = stronger separation; v1 was 0.080) |

## Figures

The paper embeds four SVG figures inline. Standalone copies are also available in [`figures/`](figures/):

- **Figure 1**: [Citation rate stability across corpus boundary expansions](figures/figure_1_bibliometric_stability.svg)
- **Figure 2**: [Engagement with 30 canonical creativity-research figures](figures/figure_2_figure_engagement.svg)
- **Figure 3**: [Matrix heatmap of cell statuses (31 × 14)](figures/figure_3_matrix_heatmap.svg)
- **Figure 4**: [Substrate-sharing among the six derived hypotheses](figures/figure_4_substrate_sharing.svg)

Figure 1 and Figure 2 are derived directly from the bibliometric findings reported in [`bibliometric_findings_v3.md`](bibliometric_findings_v3.md) and [`citation_network_analysis.md`](citation_network_analysis.md). The numbers shown are the headline results from those analyses.

Figure 3 is generated from the populated matrix; cell-status counts in the figure match the paper's reported counts: 14 IMPLEMENTED, 62 PARTIAL, 80 INCIDENTAL, 188 Type 1 EMPTY, 90 Type 4 EMPTY (total 434).

Figure 4 is a designed architectural diagram, not a data visualization; substrate-sharing relationships are documented in the paper's Sections 5–10 and (when v1.1 lands) in `proposals.md` and the per-hypothesis implementation specifications.

## Repository contents

```
.
├── README.md                                # this file
├── LICENSE                                  # CC BY 4.0
├── MISSING_ARTIFACTS.md                     # what's pending in v1.1
├── paper.md                                 # main paper (~22,500 words, 13 sections)
├── figures/                                 # four standalone SVG figures
├── citation_network_analysis.md             # n=100 survey + bibliometric extension
├── bibliometric_findings.md                 # v1 corpus findings (30,935 papers)
├── bibliometric_findings_v2.md              # v2 corpus findings (33,469 papers, superseded by v3)
├── bibliometric_findings_v3.md              # v3 final calibrated findings (53,792 papers)
├── bibliometric_extension/                  # execution specs + reproducibility scripts
├── philosophical_accounting.md              # substantive-vs-decorative apparatus accounting
├── novel_prediction_operationalization.md   # PPT operationalization with 6 worked examples
└── preregistered_matrix_predictions.md      # held-out validation on 8 systems
```

## Release attachments

Large derived data bundles (raw OpenAlex parquet files, BERTopic models, run logs) are attached to the v1.0 release as `.tar.gz` downloads rather than committed to the repo:

- `bibliometrics_v1.tar.gz` (~32 MB) — v1 strict drug-discovery corpus + scripts
- `bibliometrics_v2.tar.gz` (~32 MB) — v2 broader chemistry-AI methodology corpus
- `bibliometrics_v3.tar.gz` (~49 MB) — v3 final 53,792-paper corpus + BERTopic model

To reproduce the bibliometric analyses:
1. Download the appropriate tarball from the release page
2. Extract: `tar xzf bibliometrics_v3.tar.gz`
3. Reproducibility scripts and `run_full_analysis*.sh` are inside

## License

CC BY 4.0 (Creative Commons Attribution 4.0 International). All figures, paper text, and supplementary materials are released under this license.

## Cite as

```
Maxwell, M.H. (2026). The Citation Gap Between Drug-Discovery AI and Creativity Research:
A 53,792-Paper Bibliometric Analysis with Architectural Hypotheses. bioRxiv DOI: [INSERT DOI].
American Institute for Medical Research (AIMR).
```

## Acknowledgments

Section 1.4 of `paper.md` and the Acknowledgments document the substantial role of LLM assistance (primarily Claude / Claude Code, Anthropic) in producing this work, including the bibliometric extension at 53,792-paper scale that would not have been feasible without automated execution. The author takes full responsibility for all contents of the paper.

## Issues and corrections

The author welcomes corrections, replications, and extensions. Please open a GitHub issue for any factual or methodological concern.
