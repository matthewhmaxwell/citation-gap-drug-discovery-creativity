# Bibliometric Extension Specification

**Purpose.** Extend the n=100 structured citation survey from `citation_network_analysis.md` into a formal API-driven bibliometric analysis at scale. The extension addresses two acknowledged limitations of the original survey: (a) sample size (n=100 is sufficient for pattern surfacing but not for statistical confidence intervals); (b) figure-set selection bias (the original eleven figures were selected to represent the matrix's framework clusters and may have missed creativity-relevant traditions where drug-discovery AI does engage with creativity-research-adjacent literature).

**Output.** This spec produces three deliverables: (1) an extended figure-set bibliometric analysis at scale; (2) co-citation and topic-modeling analyses that test whether drug-discovery AI and creativity-research communities are separated in the citation network; (3) a structured findings document at engineering-specifiable depth that I can use to update `citation_network_analysis.md` and Section 1.2 of `paper.md`.

**Constraints.** Solo execution. APIs only — no manual paper-by-paper inspection. Reproducibility-first: all queries must be persisted as code, all results as data files, all analyses as runnable scripts.

---

## 1. The extended figure set

The original eleven figures (Wiggins, Boden, Hofstadter, Lakatos, Wallas, Csikszentmihalyi, Gentner, Fauconnier-Turner, Finke-Ward-Smith, Koestler, Levin) were selected to represent the matrix's framework clusters: ontology (A), mechanism (B), conditions (C), and scope (D). The extended set adds figures from creativity-relevant traditions a hostile reviewer correctly identified as absent from the original selection.

**Original eleven (retained for direct comparability with n=100 survey):**
- Geraint Wiggins (R/T/E formalism; computational creativity)
- Margaret Boden (combinatorial/exploratory/transformational creativity; *The Creative Mind*)
- Douglas Hofstadter (Fluid Analogies Research Group; Copycat; *Gödel Escher Bach*)
- Imre Lakatos (research programmes; protective belt; novel prediction)
- Graham Wallas (preparation/incubation/illumination/verification stages)
- Mihaly Csikszentmihalyi (flow; systems model of creativity)
- Dedre Gentner (structure-mapping theory of analogy)
- Gilles Fauconnier and Mark Turner (conceptual blending)
- Ronald Finke, Thomas Ward, and Steven Smith (Geneplore model; preinventive structures)
- Arthur Koestler (bisociation; *The Act of Creation*)
- Michael Levin (TAME framework; multi-scale agency)

**Extended additions covering absent traditions:**

*Cognitive/AI foundations of creative problem-solving:*
- Herbert Simon (bounded rationality; *Sciences of the Artificial*; design science; problem-space search)
- Allen Newell (problem-space hypothesis; co-author with Simon)

*Componential and applied creativity:*
- Teresa Amabile (componential theory of creativity; intrinsic motivation)
- Robert Sternberg (investment theory; triarchic theory)

*Evolutionary epistemology / creativity-as-selection:*
- Donald Campbell (blind variation and selective retention; evolutionary epistemology)
- Dean Keith Simonton (chance configuration; creative productivity)

*Design theory and reflective practice:*
- Donald Schön (reflective practitioner; *The Reflective Practitioner*)
- Christopher Alexander (pattern language; *A Pattern Language*; *Notes on the Synthesis of Form*)

*Engineering creativity heuristics:*
- Genrich Altshuller (TRIZ; theory of inventive problem solving)

*Use-inspired research framing:*
- Donald Stokes (Pasteur's Quadrant; use-inspired basic research)

*Distributed and embedded cognition relevant to creativity:*
- Edwin Hutchins (cognition in the wild; distributed cognition)
- Andy Clark and David Chalmers (extended mind hypothesis)

*Sociology of scientific knowledge:*
- Bruno Latour (actor-network theory; *Laboratory Life*; *Science in Action*)
- Karin Knorr-Cetina (epistemic cultures)

*Programme-level scientific change (Lakatos-adjacent):*
- Thomas Kuhn (paradigm shifts; *The Structure of Scientific Revolutions*)
- Paul Feyerabend (epistemological anarchism; *Against Method*)

*Adjacent possible / theoretical biology:*
- Stuart Kauffman (adjacent possible; *The Origins of Order*)

*Creativity research synthesis:*
- James C. Kaufman (Four C model; creativity assessment)
- Mark Runco (creativity research methodology; *Creativity Research Handbook*)

**Total extended set: 26 figures** (eleven original + fifteen extensions).

The extended set covers the traditions a hostile reviewer would name: cognitive AI/problem-solving (Simon, Newell), applied creativity (Amabile, Sternberg), evolutionary epistemology (Campbell, Simonton), design theory (Schön, Alexander), engineering heuristics (Altshuller), use-inspired research (Stokes), distributed cognition (Hutchins, Clark-Chalmers), STS (Latour, Knorr-Cetina), programme-level scientific change (Kuhn, Feyerabend), adjacent-possible biology (Kauffman), creativity-research synthesis (Kaufman, Runco).

If formal bibliometrics surfaces any of these as substantively cited in drug-discovery AI literature, the architectural-impoverishment inference weakens — the field may be engaging with creativity-relevant ideas through one of these traditions even though it doesn't engage with the original eleven. If none surface, the architectural-impoverishment inference strengthens — the absence pattern extends across creativity-relevant traditions broadly, not just the framework-cluster-derived eleven.

---

## 2. The drug-discovery AI corpus

The bibliometric analysis must define a corpus of drug-discovery AI literature large enough to produce statistical confidence and well-defined enough to be reproducible.

**Primary corpus definition:**
Papers in OpenAlex that match all of the following:
- Published 2017-01-01 through 2026-05-09 (ten-year window aligned with the deep-learning era post-AlphaFold)
- Include at least two of the following terms in title, abstract, or keywords: "drug discovery", "drug design", "drug repurposing", "molecular generation", "de novo design", "virtual screening", "ADMET prediction", "lead optimization", "binding affinity prediction", "compound generation"
- AND include at least one of: "deep learning", "machine learning", "artificial intelligence", "neural network", "transformer", "graph neural network", "diffusion model", "generative model", "foundation model", "large language model", "LLM", "agent", "agentic"

Estimated corpus size: 10,000-50,000 papers depending on threshold strictness.

**Secondary corpus (agentic AI for science, broader than drug discovery):**
Same date range, terms: "AI scientist", "autonomous laboratory", "self-driving lab", "AI for science", "agentic AI", "Coscientist", "ChemCrow", "AlphaFold", "scientific discovery AI", combined with general AI terms. This serves as a comparison sample for the parallel-vocabulary analysis.

**Tertiary corpus (computational creativity, for community-separation analysis):**
Date range 1995-2026 (longer window because computational creativity has older foundations). Terms: "computational creativity", "creative AI", "creative computing", "AI creativity", "machine creativity", combined with venue filters for ICCC (International Conference on Computational Creativity) and adjacent venues.

---

## 3. Analyses to run

### 3.1 Direct citation analysis

For each of the 26 figures in the extended set, identify their major works in OpenAlex (typically 1-5 papers per figure with thousand-plus citations indicating canonical status). Then for each (figure, paper) pair, count how many papers in the primary drug-discovery AI corpus cite that paper.

**Output:** Matrix (26 figures × max ~130 canonical papers) with citation counts from the primary corpus. Plus aggregate-per-figure counts. Plus citing-paper lists for each figure-paper pair where citations exist (so I can examine specific citing papers).

**Compare to original n=100 result:** The original survey found 0/1100 figure-paper pairs cited across n=100 papers. Formal bibliometrics on the primary corpus (~10K-50K papers) should produce a non-zero but small per-figure citation rate. The pattern of interest: are any figures cited at meaningfully higher rates than the original survey suggested? Particularly in the extended set?

### 3.2 Co-citation analysis

For each figure-pair (creativity-research figure, drug-discovery AI canonical paper), identify whether they are co-cited — appearing in the same reference list in any paper in the broader OpenAlex corpus (not just the drug-discovery AI corpus).

The argument: if creativity-research figures and drug-discovery AI figures are *never* co-cited even in the broader scientific literature, the communities are not just non-bridging in drug-discovery AI specifically; they are structurally separated as research communities. If they are co-cited (in interdisciplinary work, in reviews of AI methodology, etc.), the communities have *some* shared readership even if the drug-discovery AI corpus itself does not show citation.

**Output:** Co-citation count matrix. Plus a list of the top 50-100 papers that co-cite at least one creativity-research figure with at least one drug-discovery AI canonical paper, to surface the bridges that exist.

### 3.3 Topic-modeling community separation

Apply a topic model (BERTopic, Top2Vec, or similar — whichever Claude Code finds easiest with the available APIs) to the union of:
- A 5,000-paper random sample of the primary drug-discovery AI corpus
- A 5,000-paper random sample (or full corpus, whichever is smaller) of computational-creativity literature (tertiary corpus)
- Bridge papers identified in 3.2

**Output:** Topic clusters with paper-to-cluster assignments. Test whether drug-discovery AI papers and computational-creativity papers cluster into distinct topic groups (community separation hypothesis) or whether they share clusters (community overlap hypothesis). Report which topics, if any, contain papers from both communities.

### 3.4 Forward citation of canonical creativity-research works

For each canonical creativity-research paper identified in 3.1, examine its forward citation network:
- How many papers cite it total?
- How many of those papers are in the primary drug-discovery AI corpus?
- What is the temporal pattern (any uptick post-2020? post-2024? post-Shahhosseini 2025?)
- What is the venue distribution?

This is the cleanest single test of the historical-non-bridging claim: if Boden's *The Creative Mind* (and its 2004 second edition) has 5000+ citations across all literature but <5 citations from the primary drug-discovery AI corpus, the claim is empirically grounded.

**Output:** Forward citation table per canonical paper, with drug-discovery AI corpus subset highlighted.

### 3.5 Counterexample search at scale

Building on the Shahhosseini et al. counterexample: search for any paper in the primary corpus that explicitly cites at least one of the 26 figures. If any are found, classify them:
- Is it a drug-discovery AI primary paper? (counterexample to the claim)
- Is it a survey or position piece adjacent to drug-discovery AI? (calibrating evidence for the "essentially zero with isolated bridges" framing)
- Does it use the cited work substantively or in passing? (depth-of-engagement analysis)

**Output:** Counterexample list with classification. Update the headline framing from "essentially zero in drug-discovery AI specifically" to a calibrated statement based on what bibliometrics finds (e.g., "X papers in primary corpus cite at least one creativity-research figure; Y are substantive engagements; Z are passing references").

---

## 4. Reproducibility requirements

All work must be reproducible. Specifically:

1. **All API queries persisted as Python code.** OpenAlex API and Semantic Scholar API are free and have Python client libraries (`pyalex` for OpenAlex; `semanticscholar` for Semantic Scholar). Save query scripts in `bibliometrics/queries/`.

2. **All raw API responses saved as JSON.** The corpus definitions and figure-paper lookups should produce JSON files I can re-examine without re-querying. Save in `bibliometrics/raw/`.

3. **All processed analyses saved as CSV or Parquet.** The citation matrices, co-citation results, topic-modeling outputs should be in tabular form for downstream analysis. Save in `bibliometrics/processed/`.

4. **One executable script that runs everything end-to-end.** `bibliometrics/run_full_analysis.sh` or similar, that invokes the queries, processes results, and produces all output tables.

5. **Findings document.** A structured markdown file `bibliometric_findings.md` summarizing what was found across each of the five analyses (3.1-3.5), with tables, key statistics, and explicit comparison to the original n=100 survey claims. This is the document I'll use to update `citation_network_analysis.md` and Section 1.2 of `paper.md`.

---

## 5. Honest acknowledgment of limits

The extended bibliometric analysis will have its own limits the findings document should address:

- **OpenAlex coverage gaps.** OpenAlex is comprehensive but not perfect — some smaller venues, non-English papers, and older literature may be undercounted. Note the limit and quantify where possible.

- **Citation lag.** Recent papers (2025-2026) may not have accumulated citations yet. The forward-citation-of-creativity-research analysis (3.4) should restrict to papers old enough to have stable citation counts.

- **Conceptual presence still undercounted.** Even at scale, citation analysis cannot detect creativity-relevant ideas used without attribution. The parallel-vocabulary phenomenon documented in `citation_network_analysis.md` remains the structural argument that complements the bibliometric finding.

- **Figure selection still has interpretive boundaries.** The extended 26-figure set is broader than the original eleven but is not exhaustive. A reviewer could still propose figures not in this set. Document the selection logic and note that the set is extensible.

- **Same person constructed both the eleven-figure set and the extended set.** Independent reviewer validation of the figure set itself is unavailable. Acknowledge.

---

## 6. Specific instructions for Claude Code

You have access to bash, file creation, and Python execution. The libraries you'll need can be installed via pip. Internet access for the OpenAlex API and Semantic Scholar API is required.

**Step 1: Set up workspace.** Create `bibliometrics/` directory structure with subdirectories `queries/`, `raw/`, `processed/`, and `outputs/`. Install `pyalex`, `semanticscholar`, `bertopic` or `top2vec`, `pandas`, `numpy`, plus standard scientific Python.

**Step 2: Build canonical-papers list per figure.** For each of the 26 figures, use OpenAlex authorship lookup to identify their top 1-5 canonical works (highest citation count; representative of their major contributions). Save as `bibliometrics/raw/canonical_papers.json`. For ambiguous cases (common surnames; multiple authors with the same name), use ORCID or institutional affiliation to disambiguate. Document disambiguation choices in the findings.

**Step 3: Define and retrieve drug-discovery AI corpus.** Construct the OpenAlex query per Section 2 above. Retrieve the full corpus metadata (paper IDs, titles, abstracts where available, reference lists, citation counts, venues, dates). Save as `bibliometrics/raw/primary_corpus.parquet`. Report the corpus size and any retrieval issues.

**Step 4: Run analyses 3.1 through 3.5 in order.** Each analysis produces processed outputs as specified. Save intermediate results so that re-running a single analysis doesn't require re-querying APIs.

**Step 5: Write `bibliometric_findings.md`.** Structure it with one section per analysis (3.1-3.5), executive summary at the top, honest acknowledgment of limits at the bottom. Include all key tables inline. Explicitly compare findings to the n=100 survey claims in `citation_network_analysis.md` Sections 2-7.

**Step 6: If anything is anomalous, surface it.** If a figure unexpectedly has substantial drug-discovery AI citations, surface this as a finding to investigate rather than burying it. If the primary corpus is unexpectedly small or unexpectedly large, report this. If topic modeling produces unexpected community structure, surface it. The goal is honest empirical findings, not confirmation of the n=100 survey's pattern.

**Step 7: Save everything in a deliverable bundle.** When complete, the `bibliometrics/` directory should contain everything I need to re-run the analysis or to extend it: scripts, raw data, processed data, and the findings document.

The estimated runtime is hours-to-a-day depending on API rate limits and corpus size. Use rate-limiting and caching aggressively to avoid wasted API calls.

---

## 7. What I will do with the results

Once Claude Code produces `bibliometric_findings.md` and the supporting data:

1. I will integrate the findings into `citation_network_analysis.md` as a new Section 8 ("Formal bibliometric extension") that supplements Sections 2-7 (the n=100 survey).

2. I will update Section 1.2 of `paper.md` to cite the bibliometric findings rather than the n=100 survey alone, with the n=100 survey as supporting structured-survey evidence.

3. I will close the figure-set selection bias acknowledgment (current Limit 7 in `citation_network_analysis.md`) by reporting that the extended set was checked and the pattern holds (or doesn't, if findings show otherwise).

4. I will report the calibrated headline finding: not "0/1100 figure-paper pairs in n=100" but the formal-bibliometric equivalent at scale.

5. If the bibliometric findings reveal substantive engagement with any of the extended figures, I will revise the historical-non-bridging argument accordingly. Honest framing requires accepting findings that complicate the original claim if such findings emerge.
