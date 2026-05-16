# Expanding the Method Space of Drug-Discovery AI: Directions from Creativity Research

**Author:** Matthew H. Maxwell
**Affiliation:** American Institute for Medical Research (AIMR)
**Correspondence:** matt@aimronline.org
**License:** CC BY 4.0
**Release:** v1.0 (2026-05-09)

---

## About

This repository accompanies the preprint *Expanding the Method Space of Drug-Discovery AI: Directions from Creativity Research* (Maxwell, 2026).

The paper documents an empirical gap between drug-discovery AI literature and creativity research, infers an architectural gap from that citation gap, and derives six research-derived architectural directions for future drug-discovery AI systems.

The paper makes three claims of progressively weaker evidential strength:

1. **Established (empirical):** at scale, drug-discovery AI literature does not engage substantively with creativity research. Across a 53,792-paper corpus spanning drug-discovery AI, chemistry-AI methodology, protein-AI, materials informatics, and computational chemistry, 22 papers (0.041%) cite any of thirty canonical creativity-research figures. The proportional rate is stable across three corpus iterations of expanding scope.

2. **Plausible (architectural inference):** the citation gap reflects an architectural gap. A structured 31 × 14 matrix maps creativity frameworks against AI approaches in current use, producing 434 cells classified by implementation status. Hybrid neurosymbolic architecture is empty across all 31 sub-clusters under strict reading; held-out validation reproduces the pattern.

3. **Speculative (performance hypothesis):** closing the architectural gap would improve drug-discovery decisions. Six research-derived architectural directions translate the matrix's empty cells into specifiable AI systems. The hypotheses are testable predictions for future work, not demonstrated performance results.

---

## Headline findings

| Finding | Value |
|---|---|
| Corpus size (v3) | 53,792 papers |
| Direct-citation papers | 22 (0.041%) |
| Substantive engagements | 3 (all at biology-AI-philosophy frontier) |
| Figures appearing in corpus | 11 of 30 |
| Citation rate stability | 0.041–0.045% across +74% corpus expansion |
| Kuhn "paradigm shift" abstracts | 411, with zero Kuhn citations |
| Matrix cells | 434 (31 sub-clusters × 14 AI methods) |
| IMPLEMENTED cells | 14 (3.2%) |
| Type 1 EMPTY cells | 188 (43.3%) |
| X9 neurosymbolic | Type 1 EMPTY in all 31 sub-clusters under strict reading |

---

## Repository contents

**Primary deliverable:**
- `paper.md` — main paper (~22,500 words across 13 sections plus references), with four inline figures

**Standalone figures:** `figures/` directory

**Bibliometric analysis:**
- `citation_network_analysis.md`
- `bibliometric_findings.md`, `bibliometric_findings_v2.md`, `bibliometric_findings_v3.md`
- `bibliometric_extension/` (execution specifications and scripts)

**Methodological accounting:**
- `philosophical_accounting.md`
- `novel_prediction_operationalization.md`
- `preregistered_matrix_predictions.md`

**Honest accounting of what's pending:**
- `MISSING_ARTIFACTS.md`
- `RELEASE_NOTES_v1.0.md`

**Release attachments (downloadable from v1.0 release):**
- `bibliometrics_v1.tar.gz`, `bibliometrics_v2.tar.gz`, `bibliometrics_v3.tar.gz`

---

## Reading guide

If you have 10 minutes: read `paper.md` Sections 1.1, 3 (overall + cluster table), 4.1 (X9 finding), and 13 (conclusion).

If you have 30 minutes: add Sections 5 (P1 brief), 11.5 (experimental program), 12 (deployment paths).

If you have 90 minutes: read the full paper.md.

If you want to verify the bibliometric claims: read `bibliometric_findings_v3.md` and the bibliometric data tarballs attached to the v1.0 release.

If you want to evaluate the matrix construction: read `philosophical_accounting.md` and `preregistered_matrix_predictions.md`.

---

## Cite as

```
Maxwell, M.H. (2026). Expanding the Method Space of Drug-Discovery AI:
Directions from Creativity Research. SSRN preprint.
American Institute for Medical Research (AIMR).
```

---

## Contact

Correspondence: matt@aimronline.org
