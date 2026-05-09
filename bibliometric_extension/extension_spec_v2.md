# Bibliometric Extension v2 Specification: Broader Corpus

**Purpose.** Settle the corpus-boundary question identified by the third hostile-reviewer pass. The first bibliometric extension (executed 2026-05-09; results in `bibliometric_findings.md`) found 13 corpus papers (~0.04%) citing creativity-research figures across a strictly-defined drug-discovery AI corpus of 30,935 papers. The hostile reviewer identified the strict corpus boundary as the work's most vulnerable point: it excludes the broader chemistry-AI methodology layer (molecular ML, autonomous chemical discovery, retrosynthesis, generative chemistry, cheminformatics) that drug-discovery AI imports its methods *from*. The first run's own co-citation analysis surfaced two real bridges (Coley et al. 2019; Schwaller et al. 2020 — both Angewandte Chemie) that fall *outside* the strict corpus due to "chemistry" or "autonomous discovery" framing rather than "drug discovery." A hostile cheminformatics reviewer can argue that excluding these papers and adjacent literature lets the strict corpus produce the architectural-impoverishment finding by definitional artifact.

**This v2 specification settles the question by re-running all five analyses against a broader corpus that includes the methodology-layer literature drug-discovery AI imports from.** Goal: produce a definitive empirical result that does not depend on the contested corpus boundary. If the broader corpus shows substantially more engagement, the architectural-impoverishment inference for the methodology layer must be revised. If the broader corpus shows the same essential pattern, the inference is robust to the boundary choice.

**Key v1 spec adjustments learned and now incorporated:**

- The 30-figure set is fixed (eleven original + nineteen extensions; same as v1).
- Drug-discovery-AI canonical set for analysis 3.2 is now specified explicitly (see Section 3 below).
- Forward-citation analysis (3.4) uses OpenAlex `group_by` rather than full citer pagination.
- Fuzzy concept scan is now a required component of analysis 3.5 with a fixed term list.
- Disambiguation passes for common-name authors are pre-specified.

**Output.** Three deliverables: (1) revised five-analysis suite against the broader corpus; (2) explicit comparison table of v1 (strict drug-discovery) vs v2 (broader chemistry-AI methodology) results; (3) findings document `bibliometric_findings_v2.md` that supersedes or supplements `bibliometric_findings.md` depending on what the comparison shows.

---

## 1. The 30-figure set (unchanged from v1)

Eleven original figures: Geraint Wiggins, Margaret Boden, Douglas Hofstadter, Imre Lakatos, Graham Wallas, Mihaly Csikszentmihalyi, Dedre Gentner, Gilles Fauconnier and Mark Turner (joint), Ronald Finke and Thomas Ward and Steven Smith (joint), Arthur Koestler, Michael Levin.

Nineteen extensions across thirty-four total individuals: Herbert Simon, Allen Newell, Teresa Amabile, Robert Sternberg, Donald Campbell, Dean Keith Simonton, Donald Schön, Christopher Alexander, Genrich Altshuller, Donald Stokes, Edwin Hutchins, Andy Clark and David Chalmers (joint), Bruno Latour, Karin Knorr-Cetina, Thomas Kuhn, Paul Feyerabend, Stuart Kauffman, James C. Kaufman, Mark Runco.

Use the canonical-papers list from v1 raw data (`canonical_papers.json` at `./bibliometrics/raw/canonical_papers.json`). The disambiguation work has been done. 156 canonical works total.

---

## 2. The broader corpus definition

The v1 strict drug-discovery corpus required title or abstract to contain at least one drug-discovery term AND at least one AI term. The v2 broader corpus expands the drug-discovery side of the conjunction to include the methodology-layer literature drug-discovery AI actually imports.

**Primary v2 corpus filter:**

OpenAlex papers that match all of:
- Published 2017-01-01 through 2026-05-09 (same as v1)
- English language (same as v1)
- Title or abstract contains at least one term from EITHER:
  - **Drug-discovery terms (v1 set, retained):** "drug discovery", "drug design", "drug repurposing", "molecular generation", "de novo design", "virtual screening", "ADMET prediction", "lead optimization", "binding affinity prediction", "compound generation"
  - **OR Chemistry-AI methodology terms (v2 expansion):** "molecular machine learning", "autonomous chemistry", "autonomous chemical discovery", "autonomous synthesis", "retrosynthesis", "synthetic chemistry AI", "generative chemistry", "molecular property prediction", "chemoinformatics", "cheminformatics", "molecular representation learning", "chemical foundation model", "molecular foundation model", "reaction prediction", "self-driving laboratory", "self-driving lab", "autonomous laboratory"
- AND title or abstract contains at least one AI term (v1 set, retained): "deep learning", "machine learning", "artificial intelligence", "neural network", "transformer", "graph neural network", "diffusion model", "generative model", "foundation model", "large language model", "LLM", "agent", "agentic"

This expansion is a defended scope decision, not unbounded scope creep. Each added term is part of the methodology substrate from which drug-discovery AI imports — molecular ML and chemoinformatics produce property predictors used in drug discovery; autonomous chemistry produces autonomous-lab platforms applied to drug discovery; retrosynthesis is the synthetic-chemistry AI subdomain whose methods drug-discovery AI uses; foundation models are increasingly the substrate. The expanded terms are not "AI for chemistry generally" — they're the specific methodology subdomains the third reviewer correctly identified as constitutive of drug-discovery AI methodology.

**Estimated corpus size.** v1 was 30,935 papers. v2 should be substantially larger; expect 50,000-150,000 papers depending on overlap. Use OpenAlex `meta.count` to confirm before retrieval.

**Save corpus as** `bibliometrics_v2/raw/primary_corpus_v2.parquet` with the same schema as v1: paper IDs, titles, abstracts where available, reference lists, citation counts, venues, dates.

**Also retain v1 corpus in place** for direct comparison. Do not overwrite v1 files.

---

## 3. The drug-discovery-AI canonical set for analysis 3.2 (now specified)

The v1 spec did not specify which papers count as "drug-discovery AI canonical" for the co-citation analysis; v1 picked top-cited corpus papers plus REINVENT 2.0. For v2, fix the list to ensure reproducibility and to include canonical papers from the v2 expanded scope:

**Drug-discovery AI canonical (v1 set, 12 papers):**
- REINVENT 2.0 (Blaschke et al. 2020, OpenAlex `W3094686696`)
- Molecular Docking Shifting Paradigms (Pinzi & Rastelli 2019, `W2971801381`)
- The rise of deep learning in drug discovery (Chen et al. 2018, `W2790808809`)
- Generating Focused Molecule Libraries with RNN (Segler et al. 2017, `W2578240541`)
- DeepDTA: deep drug-target binding affinity (Öztürk et al. 2018, `W2785947426`)
- Molecular de-novo design through deep RL (Olivecrona et al. 2017, `W2610148085`)
- Deep RL for de novo drug design (Popova et al. 2018, `W2773987374`)
- Computational approaches streamlining drug discovery (Sadybekov & Katritch 2023, `W4367049415`)
- GraphDTA: predicting drug-target binding affinity with GNN (Nguyen et al. 2020, `W3096561213`)
- Concepts of AI for Computer-Assisted Drug Discovery (Gupta et al. 2019, `W2959938226`)
- KDEEP: Protein-Ligand Absolute Binding Affinity Prediction (Jiménez et al. 2018, `W2784213390`)
- Machine learning in chemoinformatics and drug discovery (Lo et al. 2018, `W2801991413`)

**Chemistry-AI methodology canonical (v2 additions, 10 papers — to be confirmed by the executor):**

The executor should identify ten additional canonical papers in the v2 expanded scope. Selection rules:
- Top-cited in v2 corpus but not v1 corpus (i.e., papers that entered the corpus due to v2 expansion).
- Span the methodology subdomains: molecular ML, autonomous chemistry, retrosynthesis, generative chemistry foundation models, self-driving labs.
- Include any of these specifically if found via search:
  - Coley et al. 2019, "Autonomous Discovery in the Chemical Sciences Part II: Outlook" (Angewandte Chemie)
  - Schwaller et al. 2020, "Molecular Machine Learning: The Future of Synthetic Chemistry?" (Angewandte Chemie)
  - Coley et al. 2019, "RDChiral" or other Coley-canonical retrosynthesis work
  - Schwaller et al., "Molecular Transformer" or similar reaction-prediction work
  - Burger et al. 2020, "A mobile robotic chemist" (Nature; the autonomous-laboratory anchor)
  - Boiko et al. 2023, "Autonomous chemical research with large language models" (Coscientist)
  - M. Bran et al. 2024, "Augmenting large language models with chemistry tools" (ChemCrow)
  - AlphaFold (Jumper et al. 2021) if not in v1
  - RFdiffusion (Watson et al. 2023) if not in v1

The executor should document the final 22-paper drug-discovery-AI-and-methodology canonical set with rationale, selecting the top 10 from candidates above based on citation count and methodological centrality. This list becomes the "right side" of co-citation pair queries for analysis 3.2.

---

## 4. The five analyses (revised for v2)

### 4.1 Direct citation analysis (analysis 3.1)

For each of the 156 canonical creativity works, count v2-corpus papers that cite it (via OpenAlex `referenced_works`).

**Output:** Per-figure-group counts; per-canonical-work counts; list of all v2-corpus papers citing any creativity-research figure with full metadata (title, year, venue, DOI, abstract, which figure(s) cited). Save as `bibliometrics_v2/processed/direct_citation_v2_*.csv`.

**Critical comparison output:** A table comparing v1 vs v2 results, structured as:

| figure_group | v1 corpus citations | v2 corpus citations | papers in v2 not in v1 |
|---|---|---|---|

This table is the single most important deliverable of the v2 run. It directly addresses the third reviewer's objection.

### 4.2 Co-citation analysis (analysis 3.2)

Same as v1 methodology, but using the 22-paper v2 canonical set (12 v1 drug-discovery + 10 v2 chemistry-AI methodology). For each (creativity-canonical × DD/methodology-canonical) pair, count co-citing papers across all OpenAlex.

**Output:** 156 × 22 = 3,432 pair counts. Bridging papers list (papers that co-cite at least one creativity figure with at least one DD/methodology canonical). Save as `bibliometrics_v2/processed/co_citation_v2_*.csv`.

**Specifically check:** Are Coley 2019 and Schwaller 2020 now in the v2 primary corpus? The hypothesis is yes (they should match "autonomous chemistry" or "molecular machine learning"). Confirm and report.

### 4.3 Topic-modeling community separation (analysis 3.3)

Run BERTopic on the union of:
- A 5,000-paper random sample of the v2 corpus
- The full computational-creativity tertiary corpus from v1 (2,625 papers; preserved at `./bibliometrics/raw/cc_corpus.parquet`)

Compare to v1 topic-modeling output. Test whether v2 corpus produces shared topics with computational-creativity that v1 did not.

**Output:** Topic assignments; community-share table; comparison narrative against v1. Save as `bibliometrics_v2/processed/topic_modeling_v2_*.csv`.

### 4.4 Forward-citation share (analysis 3.4)

For each canonical creativity work (≥50 global cites, ≤2021 publication), use OpenAlex `group_by` to compute share of citers in v2 corpus directly (avoiding pagination).

**Output:** Per-canonical-work forward-citation summary with v2-corpus share. Compare to v1 share. Save as `bibliometrics_v2/processed/forward_citation_v2.csv`.

### 4.5 Counterexample classification + fuzzy scan (analysis 3.5)

**Counterexample classification:** For all v2-corpus papers citing any creativity-research figure (output of 4.1), classify by:

- Paper class: drug-discovery-AI primary | chemistry-AI methodology primary | survey/position adjacent | tangential corpus member
- Engagement depth: substantive | passing

The "chemistry-AI methodology primary" class is new in v2. Examples: Coley 2019, Schwaller 2020, Burger et al. 2020, Coscientist, ChemCrow if they are in the v2 corpus and cite any creativity figure.

**Fuzzy concept scan:** Same term list as v1 (paradigm shift, structure-mapping, TAME, actor-network, bisociation, paradigm-shift, etc.) applied to v2 corpus titles + abstracts. Compare to v1 hit counts.

**Output:** Counterexample list with classifications; fuzzy concept hit counts with v1/v2 comparison. Save as `bibliometrics_v2/processed/counterexample_v2.csv` and `bibliometrics_v2/processed/fuzzy_scan_v2.csv`.

---

## 5. The comparison framework

The single most important output of v2 is the v1 vs v2 comparison. Structure it as:

| Metric | v1 (strict drug-discovery) | v2 (broader chemistry-AI methodology) | Change | Implication |
|---|---|---|---|---|
| Corpus size | 30,935 | (TBD) | (TBD) | scope of v2 expansion |
| Direct citations | 13 papers (~0.04%) | (TBD) | (TBD) | does the citation gap survive? |
| Substantive engagements | 3 (all at biology-AI-philosophy frontier) | (TBD) | (TBD) | are there now methodology-layer substantive engagements? |
| Figures with non-zero corpus citations | 7 of 30 | (TBD) | (TBD) | does any extended-set figure newly appear? |
| Fuzzy "paradigm shift" hits | 300 abstracts, 0 Kuhn citations | (TBD) | (TBD) | does parallel-vocabulary pattern hold? |
| Coley 2019 / Schwaller 2020 in primary corpus? | No | (TBD) | (TBD) | is the boundary leakage closed? |

**Three possible v2 outcomes the executor should plan for:**

**Outcome A: v2 reproduces v1 pattern at scale.** Direct citations remain ~0.04% or lower (proportional to corpus growth); substantive engagements remain concentrated at frontier; the architectural-impoverishment inference holds across the broader methodology layer too. This would settle the corpus-boundary objection in the work's favor.

**Outcome B: v2 reveals substantially more engagement at the chemistry-AI methodology layer.** Coley, Schwaller, and additional similar papers are now in the corpus; substantive engagements rise meaningfully (say, 10x or more). This would weaken the architectural-impoverishment inference for methodology specifically — though it might still hold for drug-discovery-self-labeled methodology.

**Outcome C: v2 produces a mixed picture.** Some new engagement at chemistry-AI methodology layer, but still proportionally tiny; substantive engagements still concentrated at frontier or at narrow methodology sub-domains. This is the most likely outcome given the v1 evidence, and would calibrate the inference rather than confirming or denying it.

**The executor should explicitly test each hypothesis** rather than treating v2 as confirmation of v1. If outcome B emerges, surface it clearly; do not minimize.

---

## 6. Reproducibility requirements (same as v1)

1. All API queries persisted as Python code in `bibliometrics_v2/scripts/`.
2. All raw API responses saved as JSON or Parquet in `bibliometrics_v2/raw/`.
3. All processed analyses saved as CSV/Parquet in `bibliometrics_v2/processed/`.
4. One executable script `bibliometrics_v2/run_full_analysis.sh` that runs everything end-to-end.
5. **Findings document `bibliometric_findings_v2.md`** structured around the comparison framework above.

The v2 work should be additive, not replacement. v1 raw data and scripts remain in `bibliometrics/`; v2 work goes in `bibliometrics_v2/`.

---

## 7. Honest acknowledgment of v2 limits

The v2 expansion still has limits:

- **Boundary still has to stop somewhere.** v2 expands to chemistry-AI methodology that drug-discovery AI imports. It does not include "all AI for chemistry," "all AI for science," or "all generative AI." A hostile reviewer could argue v2 boundary is still defended too narrowly. The defense: the v2 expansion is principled (limited to methodology subdomains drug-discovery AI imports from); further expansion would dilute the drug-discovery focus. State this defense explicitly in the findings.

- **OpenAlex coverage gaps.** Same as v1. Some venues underweighted; non-English papers absent; book citations undercounted; ~27% of v1 corpus had no `referenced_works`. v2 will have similar gaps. Quantify them.

- **Same author throughout.** v2 is the same author selecting the same 30-figure set, designing the broader corpus criteria, and executing/interpreting results. This is a permanent feature of the work. Acknowledge.

- **The v2 expansion was triggered by a specific reviewer objection.** This is itself worth noting transparently. v2 is not a neutral robustness check; it is a directed response to "the strict corpus boundary excludes chemistry-AI methodology." The findings document should say so.

---

## 8. Specific instructions for Claude Code

You have access to bash, file creation, and Python execution. Required libraries: `pyalex`, `semanticscholar`, `pandas`, `numpy`, `bertopic` or `top2vec`, plus standard scientific Python.

**Step 1: Set up workspace.** Create `bibliometrics_v2/` directory structure with subdirectories `scripts/`, `raw/`, `processed/`, `outputs/`. Do not modify or overwrite the v1 `bibliometrics/` directory.

**Step 2: Build v2 corpus.** Construct the OpenAlex query per Section 2 above. Use `meta.count` first to confirm corpus size before full retrieval. Retrieve full corpus metadata with reference lists. Save as `bibliometrics_v2/raw/primary_corpus_v2.parquet`.

**Step 3: Confirm or expand the 22-paper canonical set.** Identify the 10 v2 chemistry-AI methodology canonical papers per Section 3 rules. Save as `bibliometrics_v2/raw/dd_and_methodology_canonical_papers.json`.

**Step 4: Run the five analyses against v2 corpus.** Use the v1 scripts as templates where possible, modifying for v2 corpus. Document any methodology refinements.

**Step 5: Produce the v1 vs v2 comparison framework.** This is the central deliverable. Save as `bibliometrics_v2/processed/v1_vs_v2_comparison.csv` and integrate into the findings document.

**Step 6: Write `bibliometric_findings_v2.md`.** Structure: Executive summary; Key v1 vs v2 comparison; Per-analysis findings; Outcome interpretation (A, B, or C from Section 5); Coley/Schwaller status; Additional bridges discovered; Honest limits; Recommended downstream uses for paper integration.

**Step 7: Save complete deliverable bundle.** When complete, the `bibliometrics_v2/` directory should contain everything needed to re-run or extend.

The estimated runtime is comparable to v1 (hours to a day depending on API rate limits and the v2 corpus size). The v2 corpus is larger; budget accordingly.

When complete, return:
1. The `bibliometrics_v2/` directory tree as a summary.
2. The `bibliometric_findings_v2.md` file as the primary deliverable.
3. The v1 vs v2 comparison table inline.
4. Outcome classification (A, B, or C) with supporting evidence.
5. A short note (3-5 sentences) on anything you'd recommend adjusting in this spec if the work were to be repeated.

---

## 9. What I will do with the results

If outcome A: integrate v2 findings as a definitive extension of `citation_network_analysis.md` Section 8 and `paper.md` Section 1.2; note that the corpus-boundary objection has been empirically tested and the pattern holds. The third reviewer's Objection 1 substantially closes.

If outcome B: substantively revise the architectural-impoverishment inference. Acknowledge that chemistry-AI methodology layer engagement was previously masked by strict corpus boundary. Tighten the "core methodology" language to mean "drug-discovery-self-labeled methodology." Calibrate the empirical claim accordingly. The third reviewer's Objection 1 lands and the work absorbs the correction.

If outcome C: integrate the calibrated finding (some new engagement, but still proportionally small). Update the paper to report the v1 vs v2 comparison directly. Reframe "core methodology" to be explicit about scope. Acknowledge that the boundary choice is a defended scope decision rather than an empirical neutral.

In any case: integrate the findings honestly. If outcome A reveals patterns that complicate the work, integrate them. If outcome B requires substantive revision, do it. The point of v2 is to settle the question, not to confirm v1.
