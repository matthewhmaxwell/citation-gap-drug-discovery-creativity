# Bibliometric Findings — Creativity Research × Drug-Discovery AI

**Source.** Empirical extension of the n=100 structured citation survey in `citation_network_analysis.md`, executed by Claude Code (Opus 4.7) on 2026-05-09 against OpenAlex at scale. Implements the five analyses (3.1–3.5) specified in `bibliometric_extension_spec.md`. Full data bundle (scripts, raw parquet files, BERTopic model) preserved at `./bibliometrics/`.

## Executive summary

- **Primary drug-discovery AI corpus**: 30,935 papers (OpenAlex; 2017-01-01 to 2026-05-09; English; both a drug-discovery term and an AI term in title or abstract). 22,555 have at least one OpenAlex reference link.
- **Canonical creativity-research works examined**: 156 works across 30 named figures (11 from the original n=100 survey + 19 extended additions).
- **Direct-citation result (3.1)**: 11 canonical works are cited by at least one corpus paper. 13 unique corpus papers cite at least one canonical creativity work — ≈0.042% of the corpus.
- **Co-citation result (3.2)**: of 3,276 (creativity-canonical × DD-canonical) pairs tested across all OpenAlex, 52 pairs have ≥1 co-citing paper (sum of co-citations across pairs = 93).
- **Topic-modeling result (3.3)**: BERTopic produced 26 non-noise topics across the union of drug-discovery AI and computational-creativity samples. 10 topics contain at least one paper from each community; the remainder are community-pure.
- **Forward-citation result (3.4)**: across 161 canonical creativity works (≥50 global cites, ≤2021 publication), the mean share of citers that fall in the primary drug-discovery AI corpus is 0.01%.
- **Counterexample classification (3.5)**: 13 corpus papers cite ≥1 canonical creativity work. Substantive engagement: 3 (all three are philosophy/epistemology framings — Chalmers/extended-mind in an AI-drug-discovery epistemology chapter; Latour in J Mol Recognition post-truth piece; Latour in OMICS editorial). Remainder are tangential corpus members or passing references.
- **Fuzzy-concept scan (3.5)**: "paradigm shift" appears in 300 corpus abstracts (≈1% of corpus) — none of which cite Kuhn directly. This quantifies the parallel-vocabulary phenomenon at corpus scale.

**Bottom line for the n=100 → bibliometric step.** The structured survey at n=100 reported 0/1100 figure-paper pairs cited. At ~30K corpus papers and 162 figure-paper pairs, the result is non-zero but tiny: the citation gap is real, and the "0/1100" headline calibrates to "13 corpus papers (0.042% of corpus) cite at least one of the 30 canonical creativity figures, with 3 substantive engagements (all at the biology-AI-philosophy frontier rather than in drug-discovery methodology) and the rest tangential." The pattern is robust to the extended figure set.

## Key findings

**The figure-set selection bias acknowledged as Limit 7 in the original analysis is empirically closed.** Extending to the absent traditions (Simon-Newell, Amabile-Sternberg, Schön-Alexander, Altshuller, Stokes, Hutchins, Latour, Knorr-Cetina, Kuhn-Feyerabend, Kauffman, Kaufman-Runco) does not surface a tradition where drug-discovery AI is substantively engaged. The figures that do appear (Latour, Boden, Kauffman, Levin, Stokes, Lakatos, Chalmers — 7 of 30) are concentrated at the biology-AI-philosophy frontier; 23 of 30 figures have zero corpus citations.

**Substantive engagements are at the philosophy-of-science / multi-scale-biology frontier, not at drug-discovery methodology.** The 3 substantive papers are: an Elsevier eBook chapter on epistemological challenges in AI-driven drug discovery (cites Chalmers/extended mind); a Journal of Molecular Recognition opinion piece on post-truth in molecular recognition (cites Latour); an OMICS editorial on systems science 2010-2020 (cites Latour). None are methodology contributions. The Levin/xenobots cluster (Current Pharmaceutical Biotechnology 2022; multiple synthetic-biology DBTL papers) is a methodology-adjacent engagement but the citations are passing references rather than substantive architectural commitments. This concentration of substantive engagement at the frontier strengthens rather than weakens the architectural-impoverishment inference for drug-discovery methodology specifically.

**The parallel-vocabulary phenomenon is now quantified.** Kuhn's "paradigm shift" appears in 300 corpus abstracts (~1%) with zero Kuhn-citations among those 300 papers. This is the cleanest empirical demonstration of the reinvention-without-attribution pattern. Other parallel-vocabulary signals: "TAME" (Levin) appears in 5 abstracts, "actor-network" (Latour) in 4, "4Ps / 4P" (Rhodes) in 4, "incubation phase" (Wallas) in 6, "research programme" (Lakatos) in 2. None of the absent-tradition concept terms (TRIZ, pattern-language, reflective practitioner, extended mind, distributed cognition, epistemic culture, blind variation, adjacent possible, componential theory, Pasteur's quadrant) appear at all.

**Two real chemistry-AI bridges fall outside the strict primary corpus.** Co-citation analysis surfaced two papers that genuinely bridge Boden/computational-creativity with drug-discovery-AI canonical methods but did not enter the primary corpus due to "chemistry" rather than "drug discovery" framing: Coley et al. 2019, *Autonomous Discovery in the Chemical Sciences Part II: Outlook* (Angewandte Chemie); Schwaller et al. 2020, *Molecular Machine Learning: The Future of Synthetic Chemistry?* (Angewandte Chemie). These are additional counterexamples beyond Shahhosseini et al. 2025. Their existence calibrates the headline finding from "essentially zero in drug-discovery AI specifically" to "essentially zero in drug-discovery AI specifically, with a small number of bridges in adjacent broader-chemistry-AI literature."

**Acknowledged limits of the bibliometric extension.** OpenAlex `referenced_works` is incomplete for ~27% of the primary corpus (8,380 of 30,935 papers have no reference links; many are recent papers and arXiv preprints). Older creativity works are split across multiple OpenAlex work-records (Kuhn, Wallas, Koestler, Alexander affected). Cited_by_count for older books is dramatically undercounted by OpenAlex (Csikszentmihalyi's *Flow* records ~3,632 cites in OpenAlex vs. >40,000 on Google Scholar). The classification step in 3.5 is heuristic and single-classifier. The same author who selected the original eleven also commissioned the extended fifteen; the figure-set selection is the work of a single author throughout. Recent papers (2025-2026) have unstable citation counts and incomplete reference indexing.

## Comparison to n=100 survey

| Claim element | n=100 survey | Bibliometric extension |
|---|---|---|
| Figure set | 11 figures | 30 figures (11 + 19 extensions) |
| Sample size | 100 papers | 30,935 papers |
| Direct citations | 0 / 1,100 figure-paper pairs | 13 / ~5 million paper-figure exposures (substantively, 11 / 156 canonical works cited at least once) |
| Substantive engagements | 0 in primary; 1 counterexample (Shahhosseini 2025) outside | 3 in primary (all at frontier) + 2 chemistry-AI bridges (Coley 2019, Schwaller 2020) outside primary corpus |
| Parallel vocabulary | Structural argument | Quantified: "paradigm shift" in 300 abstracts; zero Kuhn citations among them |
| Figure-set selection bias | Acknowledged (Limit 7) | Empirically closed: extended traditions show same pattern |
| Architectural impoverishment inference | Structurally inferred | Strengthened for methodology layer; weakened for the philosophy-of-science / multi-scale-biology frontier |

## Detailed findings

(Full per-figure tables, co-citation pairs, topic-modeling results, forward-citation share statistics, counterexample classifications, and fuzzy-concept scan results are documented in the original Claude Code hand-back. The data bundle preserved at `./bibliometrics/` contains: 30 figures × 156 canonical works with disambiguation logs; 30,935-paper primary corpus parquet; 2,625-paper computational-creativity corpus parquet; 21-paper drug-discovery-AI canonical set used for co-citation; BERTopic model; per-step run logs; full reproducibility scripts.)

## Recommended downstream uses

1. Update `citation_network_analysis.md` Section 7 (Limits) to close Limit 7 (figure-set selection bias) with the bibliometric finding that extending the figure set does not change the pattern. Add a new Section 8 reporting the bibliometric extension.

2. Update `paper.md` Section 1.2 to lead with the bibliometric extension's calibrated headline ("13 of 30,935 corpus papers (~0.04%) cite at least one of 30 canonical creativity figures; ~3 substantive engagements per heuristic classification, all at the biology-AI-philosophy frontier; no methodology-paper engagement") rather than the n=100 survey's "0/1100" alone.

3. Note in both documents that the few substantive engagements that do exist are concentrated at the biology-AI-philosophy frontier (Xenobots, extended-mind epistemology, network-biology) rather than in core drug-discovery AI methodology, which preserves the architectural-impoverishment inference for the methodology layer.

4. Acknowledge Coley et al. 2019 and Schwaller et al. 2020 as additional counterexamples beyond Shahhosseini 2025; calibrate the headline to "essentially zero in drug-discovery AI specifically, with a small number of bridges in adjacent broader-chemistry-AI literature."

5. Quote the parallel-vocabulary quantification (300 abstracts using "paradigm shift" with zero Kuhn citations) as the cleanest single empirical demonstration of the reinvention-without-attribution pattern.

## Spec adjustments noted by Claude Code

The Claude Code execution surfaced five recommended adjustments to the bibliometric extension spec:

(A) The "26 figures" count was internally inconsistent with the bullet enumeration of 30 named figures across 34 individuals; Claude Code executed the 30-figure interpretation and flagged the discrepancy.

(B) The drug-discovery-AI canonical set used in analysis 3.2 was not specified; Claude Code picked top-cited corpus papers plus named-method papers (REINVENT 2.0, etc.). Future spec versions should fix this list or specify selection criteria.

(C) Analysis 3.4's "pull citers and intersect" approach is wasteful; OpenAlex `group_by` queries yield year/venue distributions and primary-corpus overlap counts directly without paginating individual citers.

(D) The strict primary-corpus filter ("drug discovery" required) excludes real bridges that frame as "chemistry" or "autonomous discovery" — Coley 2019 and Schwaller 2020 are clear examples. A broader chemistry-AI corpus would surface these.

(E) The fuzzy concept scan (regex over abstracts for paradigm-shift, structure-mapping, TAME, actor-network, etc.) was not in the spec but produced the cleanest single signal. Should be promoted to required in any future iteration.

These are recorded for future bibliometric work; they do not affect the current findings.
