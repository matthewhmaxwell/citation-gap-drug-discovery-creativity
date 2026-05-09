# MISSING_ARTIFACTS.md

**Repository:** citation-gap-drug-discovery-creativity
**Release:** v1.0-arxiv-preprint
**Date:** 2026-05-09

---

This file is an honest accounting of artifacts referenced in `paper.md` (the arXiv preprint) but not yet committed to this repository as of v1.0.

## What is in v1.0

- `paper.md` — main paper (~22,500 words across 13 sections plus references)
- `figures/` — four standalone SVG figures matching those embedded inline in the paper
- `citation_network_analysis.md` — n=100 systematic survey methodology and findings, plus Section 8 reporting the bibliometric extension
- `bibliometric_findings.md` (v1), `bibliometric_findings_v2.md`, `bibliometric_findings_v3.md` — the three iterations of the bibliometric extension at scale, with v3 as the final calibrated headline
- `bibliometric_extension/` — execution specifications and (where applicable) scripts for the bibliometric corpus build
- `philosophical_accounting.md` — substantive-vs-decorative philosophical apparatus accounting for the paper's framework apparatus
- `novel_prediction_operationalization.md` — operationalization of Lakatosian "novel prediction" for P1's Programme-Progressivity Tracker, with six worked examples
- `preregistered_matrix_predictions.md` — held-out validation on 8 drug-discovery AI systems
- This file

## What `paper.md` references but is NOT in v1.0

The following supplementary artifacts are referenced in the paper's Acknowledgments and Section 1.5 but are not yet committed to this repository. They are planned for inclusion in v1.1.

### Architectural hypothesis specifications

- `proposals.md` — full hypothesis specifications at depth for P1 through P6
- `p1_implementation.md` — engineering-grade implementation specification for P1 (Wiggins/Lakatos/Levin neurosymbolic core)
- `p2_implementation.md` — engineering-grade implementation specification for P2 (structure-mapping substrate)
- `p3_implementation.md` — engineering-grade implementation specification for P3 (field-aware neurosymbolic)
- `p4_implementation.md` — engineering-grade implementation specification for P4 (constraint-engineering substrate)
- `p5_implementation.md` — engineering-grade implementation specification for P5 (stigmergic distributed substrate)
- `p6_implementation.md` — engineering-grade implementation specification for P6 (incubation-aware architecture)

### Matrix artifacts

- `matrix_populated.md` — full populated 31 × 14 matrix with per-cell rationale narratives
- `matrix_drilldown.md` — drill-down treatment for high-leverage Type 1 EMPTY cells
- `matrix_data.json` — full matrix data including per-cell rationales (machine-readable)
- `matrix_data_compact.json` — compact matrix data (cell statuses + short rationales)
- `matrix_heatmap.html` — interactive matrix visualization

### Review and validation artifacts

- `multidisciplinary_review.md` — seven-discipline structured self-review of the work
- `adversarial.md` — strongest-hostile-reading adversarial analysis
- `experiments.md` — eighteen designed validation experiments (three per hypothesis)

## Why these are not in v1.0

The repository is being released to coincide with arXiv preprint submission. The author (single author, AIMR) prioritized verifying that committed artifacts are accurate, current, and consistent with the paper's calibrated claims rather than rushing all referenced supplementary materials into the v1.0 release. Several of the missing artifacts exist in earlier project state but require an audit pass before public release to ensure they reflect post-Block-39 citation corrections and post-Block-40 framing calibration.

## Plan for v1.1

Target date: within 30 days of v1.0.

The v1.1 release will add the missing artifacts above, with each verified against the current paper.md framing. If any referenced artifact is determined not to exist or to require substantial reconstruction, the paper.md cross-references will be updated to reflect this honestly rather than restored as if the artifact were available. Honesty about what supplementary material backs the paper is more important than completeness of supplementary material.

## How this affects readers

A reader of v1.0 has access to the empirical core of the work: the paper itself, the citation gap measurement at both n=100 survey scale and 53,792-paper bibliometric scale, the philosophical accounting, the PPT operationalization with six worked examples, and the held-out validation results. The reader does not have access to the full hypothesis-specification depth for P1 through P6, the matrix-population narratives, or the adversarial and multidisciplinary review documents.

Readers needing those artifacts before v1.1 ships should contact the author directly (correspondence link in `paper.md` front matter).

## Cite as

```
Maxwell, M.H. (2026). The Citation Gap Between Drug-Discovery AI and Creativity Research:
A 53,792-Paper Bibliometric Analysis with Architectural Hypotheses. arXiv:[INSERT ID].
American Institute for Medical Research (AIMR). v1.0 release: [INSERT DATE].
Some supplementary artifacts pending in v1.1; see MISSING_ARTIFACTS.md.
```
