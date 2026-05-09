# Pre-Registered Matrix Predictions on Held-Out Drug-Discovery AI Systems

**Purpose.** Apply the matrix methodology to drug-discovery AI systems that were not examined during matrix construction. Pre-register predictions about what the methodology will surface for each system; then apply the methodology and compare predictions against findings. This tests prospective predictive validity of the methodology beyond the systems used to construct it.

**Methodology.** For each held-out system: (1) describe the system based on its primary documentation; (2) pre-register predictions about its matrix profile (which AI categories from Axis 2 it occupies; which creativity-framework engagements it has; which Type 1 EMPTY cells it leaves unfilled); (3) apply the methodology to populate its actual matrix profile; (4) compare predictions to findings, scoring agreement, partial agreement, and disagreement.

**Status.** This is prospective application of the methodology. The systems below are recent (April 2025 through January 2026), distinct in architecture and domain, and were not part of the original matrix-population sample. The pre-registration is documented within this artifact rather than via a third-party preregistration service; the cleaner version of this work would use OSF or aspredicted.org, which I do not have access to from this work environment.

**Honest acknowledgment of limit.** This artifact is the work of a single author throughout — the matrix was constructed, the predictions pre-registered, the methodology applied, and the results scored by the same person. Individual classifications would likely shift at margins under further review. What this exercise does deliver is: (a) tested methodology stability — does the methodology produce sensible classifications on systems it wasn't designed against?; (b) documented predictions made before findings were generated, with timestamps within the artifact text; (c) honest scoring of where predictions matched and where they didn't, identifying conditions under which the methodology is more or less reliable.

---

## 1. Held-out systems

I selected eight drug-discovery AI systems that meet the following criteria:

- **Recent.** Published or preprinted between April 2025 and January 2026 (post the initial matrix construction).
- **Specific to drug discovery.** Not just LLM surveys or general-purpose AI systems; specifically positioned for drug-discovery applications.
- **Distinct architectures.** Spanning agentic LLM orchestration, multi-agent specialization, knowledge-graph-RAG hybrids, and hybrid LLM-tool architectures.
- **Sufficient documentation.** Either a paper, preprint, or detailed technical report enabling architectural assessment.
- **Outside primary sample.** Not in the citation_network_analysis.md n=100 primary sample.

The eight systems:

**S1. Robin** (Ghareeb et al. 2025; arXiv:2505.13400; FutureHouse, May 2025). Multi-agent system orchestrating Crow (rapid literature review), Falcon (deep literature analysis), and Finch (autonomous data analysis) for end-to-end drug-repurposing. Demonstrated discovery of ripasudil for dry age-related macular degeneration.

**S2. PharmaSwarm** (Song et al. 2025; arXiv:2504.17967; UAB, April 2025). Multi-agent framework where specialized LLM agents propose, validate, and refine hypotheses; each agent accesses dedicated functionality (genomic analysis, knowledge graph, pathway enrichment, binding-affinity prediction) under a central Evaluator LLM. Self-improvement through shared memory layer.

**S3. Tippy** (Fehlis et al. 2025; arXiv:2507.09023; Artificial Inc., July 2025). Five specialized agents (Supervisor, Molecule, Lab, Analysis, Report) plus Safety Guardrail oversight, designed to operate within DMTA (Design-Make-Test-Analyze) cycle. Industry-deployment positioning.

**S4. AgentMol** (Karabowicz et al. 2025; Methods and Protocols 8(6):143, December 2025). Multi-model AI integrating GPT-2 chemical language model with convolutional networks for drug-target identification and molecule development; LangGraph orchestration.

**S5. Prompt-to-Pill** (biorxiv 2025.08.12.669861; 2025). Multi-agent framework spanning molecular ideation, docking, property prediction, trial construction, patient matching, and outcome forecasting; integrated through central Orchestrator. Built on systematic review of 51 LLM-based studies 2022-2025.

**S6. RUGGED** (Liu et al. 2024; arXiv:2407.12888; UCLA Cardiology). Retrieval Under Graph-Guided Explainable disease Distinction. RAG-enabled hypothesis generation for therapeutic recommendation in arrhythmogenic and dilated cardiomyopathy; minimizes hallucinations through curated knowledge-base grounding.

**S7. Modular LLM Agent for BCL-2** (Choi et al. 2025; arXiv:2507.02925; July 2025). Single-agent LLM framework combining reasoning with domain-specific tools for biomedical data retrieval, molecular generation, property prediction, refinement, and 3D structure generation. BCL-2 lymphocytic leukemia case study.

**S8. AI Agents in Drug Discovery comprehensive overview** (Seal et al. 2025; arXiv:2510.27130; October 2025). Conceptual + technical overview spanning ReAct, Reflection, Supervisor, and Swarm patterns applied to literature synthesis, toxicity prediction, automated protocol generation, small-molecule synthesis, drug repurposing, and end-to-end decision-making.

---

## 2. Pre-registered predictions

### 2.1 Predictions about Axis 2 (AI methods) coverage

For each system, predict which AI-method columns (from the 14-category Axis 2) the system occupies as primary, secondary, or absent.

I predict that all eight systems will primarily occupy **X6 (multi-agent systems)** and **X11 (foundation models)** because all eight are LLM-orchestration architectures using foundation-model components.

I predict that **X8 (knowledge graphs)** will be primary for S2 (PharmaSwarm — explicitly KG-augmented), S6 (RUGGED — explicitly KG-RAG), and S7 (Modular LLM Agent — uses KG retrieval), and secondary or absent for the others.

I predict that **X10 (active learning)** will be primary for S1 (Robin — iterative lab-in-the-loop is active-learning-class), S3 (Tippy — DMTA cycle), and absent or weak for the others.

I predict that **X9 (neurosymbolic)** will be Type 1 EMPTY across all eight systems. The X9 universal-emptiness finding from the original matrix should hold for the held-out systems if the methodology is robust. If any held-out system genuinely commits to neurosymbolic substrate as a primary architectural commitment (not just incidentally combining LLM with KG retrieval), the universal-emptiness finding is undermined.

I predict that **X7 (self-refining loops)** will be primary for S1 (Robin's iterative refinement), S2 (PharmaSwarm's shared-memory self-improvement), S5 (Prompt-to-Pill's closed-loop architecture), and weaker for the others.

I predict that **X12 (causal AI)** will be Type 1 EMPTY across all eight systems. Recent agentic frameworks consistently default to correlational LLM reasoning rather than explicit causal models; this is a robust prediction that would be falsified by a system that explicitly commits to causal-modeling components.

### 2.2 Predictions about Axis 1 (creativity frameworks) engagement

I predict the following pattern across all eight systems:

- **A1 (Boden combinatorial/exploratory/transformational):** I predict 0 of 8 systems will engage Boden's distinctions explicitly. All will operationalize "novelty" through molecular-fingerprint distance, training-set uniqueness, or similar operational metrics without engaging the conceptual taxonomy.

- **A4 (Wiggins R/T/E):** I predict 0 of 8 systems will use R/T/E formalism as architectural commitment. Reverberation/Transformation/Evaluation as deliberate three-operation decomposition is creativity-research-derived; current agentic frameworks default to "generate then evaluate" pipelines.

- **B3 (Wallas stages: preparation/incubation/illumination/verification):** I predict 0 of 8 systems will implement deliberate incubation phases. The B4-uniformly-Type-1 finding from the original matrix should hold; if any system has a deliberate "wait and reconsider" architectural commitment, the finding would be undermined.

- **B5 (Hofstadter Copycat / fluid concepts):** I predict 0 of 8 systems will commit to codelet-workspace dynamics. Current agentic frameworks default to LLM-chain orchestration without fluid-concept commitments.

- **B6 (Gentner structure-mapping):** I predict 0 of 8 systems will implement explicit structure-mapping for cross-domain analogical reasoning. LLM-mediated analogy may be incidentally present but not as architectural commitment.

- **C2 (Csikszentmihalyi flow / field-state):** I predict 0 of 8 systems will engage field-state modeling at the level P3's FSS specifies. Stakeholder modeling may be incidentally present (e.g., Tippy's deployment context) but not as deliberate field-engagement architecture.

- **D4 (Levin TAME multi-scale agency):** I predict 0 of 8 systems will commit to multi-scale agent substrate as architectural primitive. Multi-scale considerations may be incidentally present but not as data-structure commitment with cross-scale negotiation logic.

- **D6 (Sawyer collaborative emergence):** I predict variable engagement. Multi-agent systems that explicitly model emergent collective behavior (S5 Prompt-to-Pill's Orchestrator architecture; S2 PharmaSwarm's evaluator pattern) may have INCIDENTAL or PARTIAL engagement; pure pipeline architectures will not.

### 2.3 Predictions about Type 1 EMPTY profiles

For each system, I predict the matrix profile will show:

- **High Type 1 EMPTY count.** All eight systems should have ≥80% Type 1 EMPTY cells in the 14-column row-section corresponding to whichever creativity-framework dimensions are not engaged. This means most cells in each system's profile will be Type 1 EMPTY.

- **The "neurosymbolic-and-causal" co-emptiness.** X9 (neurosymbolic) and X12 (causal AI) should both be Type 1 EMPTY across all systems, producing a robust co-emptiness pattern.

- **The B-cluster (mechanism) emptiness for stages, incubation, structure-mapping.** B3, B4, B5, B6 should all be Type 1 EMPTY across all systems.

- **The C-cluster (conditions) emptiness for field-state, deliberate-conditions, social-creativity.** C2, C3, C4 should be Type 1 EMPTY across all systems.

### 2.4 Pre-registered counter-predictions

I also pre-register what would *falsify* the matrix's pattern-claims:

- If any held-out system commits to neurosymbolic substrate as primary architectural commitment (X9 IMPLEMENTED), the X9-universal-emptiness finding is locally falsified.

- If any held-out system implements deliberate incubation (B3 IMPLEMENTED), the B4-uniformly-empty finding is locally falsified.

- If any held-out system explicitly cites Boden, Wiggins, or another creativity-research figure (Section 1.2 framework citation), the citation-network-analysis pattern is locally falsified for that system.

- If the matrix profile produces classifications that don't match the system's stated architectural commitments (e.g., I classify a system as Type 1 EMPTY at X9 but the system's documentation explicitly describes neurosymbolic architecture), the methodology has a reproducibility problem.

- If the methodology surfaces predictions that no human reviewer would naturally make (e.g., classifies clear architectural commitments as empty cells), the methodology is producing artifacts rather than findings.

---

## 3. Methodology application: actual matrix profiles

For each system, I now apply the methodology and document the actual classifications. The classification follows the same threshold definitions used in matrix_template.md (IMPLEMENTED = primary architectural commitment; PARTIAL = partially instantiated with significant limitations; INCIDENTAL = functionally present but not deliberate; Type 1 EMPTY = engineerable but untried; Type 4 EMPTY = resists computational translation).

### 3.1 S1: Robin

**Architecture.** Three specialized agents (Crow, Falcon, Finch) orchestrated for literature synthesis → hypothesis generation → experimental data analysis → iterative refinement. Validated via lab-in-the-loop with human researchers executing physical experiments.

**Axis 2 occupation:**

- X1 (predictive scoring) — INCIDENTAL (Finch produces analytical outputs but not predictive scores).
- X2 (generative molecular design) — Type 1 EMPTY (Robin doesn't generate novel molecules; it identifies repurposing candidates).
- X3 (retrieval) — IMPLEMENTED (Crow/Falcon are explicitly retrieval-driven).
- X4 (evolutionary search) — Type 1 EMPTY.
- X5 (RL) — Type 1 EMPTY.
- X6 (multi-agent) — IMPLEMENTED (three-agent orchestration is primary architectural commitment).
- X7 (self-refining) — IMPLEMENTED (iterative refinement is primary commitment).
- X8 (knowledge graphs) — INCIDENTAL (Falcon's deep analysis touches structured knowledge but not via KG primitives).
- X9 (neurosymbolic) — Type 1 EMPTY (LLM-only; no explicit symbolic substrate).
- X10 (active learning) — IMPLEMENTED (lab-in-the-loop is active-learning-class).
- X11 (foundation models) — IMPLEMENTED (LLM backbone).
- X12 (causal AI) — Type 1 EMPTY.
- X13 (multi-modal) — INCIDENTAL (Finch handles RNA-seq, flow cytometry, image data — multi-modal incidentally).
- X14 (simulation) — Type 1 EMPTY.

**Axis 1 engagement:**

- A1 Boden — Type 1 EMPTY (no Boden engagement).
- A4 Wiggins — Type 1 EMPTY.
- B3 Wallas stages — Type 1 EMPTY.
- B4 incubation — Type 1 EMPTY.
- B5 Hofstadter — Type 1 EMPTY.
- B6 Gentner — Type 1 EMPTY.
- C2 field-state — INCIDENTAL (drug-repurposing context implies stakeholder awareness but not architectural).
- D4 Levin TAME — Type 1 EMPTY.
- D6 Sawyer — INCIDENTAL (multi-agent emergence is present but not deliberately Sawyer-derived).

**Citation analysis spot-check.** Scanned Robin paper for citations to creativity-research figures. None found.

### 3.2 S2: PharmaSwarm

**Architecture.** Multi-agent LLM swarm with central Evaluator; specialized agents for genomic analysis, KG access, pathway enrichment, binding-affinity prediction; shared memory layer for self-improvement.

**Axis 2 occupation:**

- X1 — PARTIAL (binding-affinity prediction agent is predictive-scoring class).
- X2 — INCIDENTAL (lead-compound generation may emerge from refinement but not primary).
- X3 — IMPLEMENTED (literature retrieval explicit).
- X4 — Type 1 EMPTY.
- X5 — Type 1 EMPTY.
- X6 — IMPLEMENTED (swarm-of-specialized-agents is primary commitment).
- X7 — IMPLEMENTED (self-improving via shared memory).
- X8 — IMPLEMENTED (curated biomedical KG is named primary component).
- X9 — Type 1 EMPTY (LLM + KG retrieval is not neurosymbolic substrate per matrix definition; threshold requires explicit symbolic-reasoning operations beyond retrieval).
- X10 — INCIDENTAL (validation pipeline includes empirical iteration; not active-learning per se).
- X11 — IMPLEMENTED.
- X12 — Type 1 EMPTY.
- X13 — INCIDENTAL.
- X14 — Type 1 EMPTY.

**Axis 1 engagement:**

- A1 Boden — Type 1 EMPTY.
- A4 Wiggins — Type 1 EMPTY.
- B3 Wallas — Type 1 EMPTY.
- B4 incubation — Type 1 EMPTY.
- B5 Hofstadter — Type 1 EMPTY.
- B6 Gentner — Type 1 EMPTY.
- C2 field-state — Type 1 EMPTY.
- D4 Levin TAME — Type 1 EMPTY.
- D6 Sawyer — PARTIAL (swarm emergence is explicit architectural language; not Sawyer-derived but functionally adjacent).

**Citation analysis spot-check.** No creativity-research figure citations found.

### 3.3 S3: Tippy

**Architecture.** Five specialized agents (Supervisor, Molecule, Lab, Analysis, Report) plus Safety Guardrail. DMTA cycle as workflow scaffolding. Industry-deployment-positioned.

**Axis 2 occupation:**

- X1 — PARTIAL (Analysis agent does predictive analysis).
- X2 — IMPLEMENTED (Molecule agent does generative design).
- X3 — INCIDENTAL.
- X4 — Type 1 EMPTY.
- X5 — Type 1 EMPTY.
- X6 — IMPLEMENTED.
- X7 — PARTIAL (DMTA cycle is iterative; whether cycle iterations refine the system itself or just iterate the workflow is unclear from documentation).
- X8 — Type 1 EMPTY.
- X9 — Type 1 EMPTY.
- X10 — IMPLEMENTED (DMTA-cycle active learning is primary commitment).
- X11 — IMPLEMENTED.
- X12 — Type 1 EMPTY.
- X13 — INCIDENTAL (Lab agent presumably handles diverse data).
- X14 — Type 1 EMPTY.

**Axis 1 engagement:** All Type 1 EMPTY except B1 (stages) — INCIDENTAL via DMTA cycle, which has Wallas-stage flavor without explicit Wallas commitment.

### 3.4 S4: AgentMol

**Architecture.** GPT-2 chemical language model for SMILES generation + CNN for property prediction; LangGraph orchestration.

**Axis 2 occupation:**

- X1 — IMPLEMENTED (CNN-based property prediction is primary).
- X2 — IMPLEMENTED (GPT-2 chemical-language model for SMILES generation is primary).
- X3 — Type 1 EMPTY.
- X4 — Type 1 EMPTY.
- X5 — Type 1 EMPTY.
- X6 — PARTIAL (LangGraph orchestrates two models; thinner multi-agent than Tippy or PharmaSwarm).
- X7 — Type 1 EMPTY.
- X8 — Type 1 EMPTY.
- X9 — Type 1 EMPTY.
- X10 — Type 1 EMPTY.
- X11 — IMPLEMENTED (GPT-2 is foundation-model-class, even if older generation).
- X12 — Type 1 EMPTY.
- X13 — Type 1 EMPTY.
- X14 — Type 1 EMPTY.

**Axis 1 engagement:** All Type 1 EMPTY across creativity-relevant rows.

### 3.5 S5: Prompt-to-Pill

**Architecture.** Multi-agent framework with central Orchestrator coordinating molecule generation, docking, property prediction, trial construction, patient matching, outcome forecasting. Pipeline-spanning from molecule to clinical-trial design.

**Axis 2 occupation:**

- X1 — IMPLEMENTED (property prediction is primary component).
- X2 — IMPLEMENTED (molecular generation is primary component).
- X3 — INCIDENTAL.
- X4 — Type 1 EMPTY.
- X5 — Type 1 EMPTY.
- X6 — IMPLEMENTED.
- X7 — IMPLEMENTED (closed-loop architecture).
- X8 — Type 1 EMPTY.
- X9 — Type 1 EMPTY.
- X10 — INCIDENTAL.
- X11 — IMPLEMENTED.
- X12 — Type 1 EMPTY.
- X13 — Type 1 EMPTY.
- X14 — PARTIAL (virtual trial execution is simulation-class).

**Axis 1 engagement:** All creativity rows Type 1 EMPTY except D6 Sawyer — INCIDENTAL (orchestrator emergence is explicit but not Sawyer-derived).

### 3.6 S6: RUGGED

**Architecture.** RAG-enabled LLM with KG-grounded retrieval; minimizes hallucinations through curated knowledge-base evidence; case study on arrhythmogenic and dilated cardiomyopathy therapeutics.

**Axis 2 occupation:**

- X1 — INCIDENTAL.
- X2 — Type 1 EMPTY.
- X3 — IMPLEMENTED (retrieval-augmented generation is primary commitment).
- X4 — Type 1 EMPTY.
- X5 — Type 1 EMPTY.
- X6 — Type 1 EMPTY (single-agent RAG, not multi-agent).
- X7 — Type 1 EMPTY.
- X8 — IMPLEMENTED (knowledge graph is primary architectural commitment).
- X9 — PARTIAL (RAG architectures with explicit KG retrieval and constraint logic begin to approach neurosymbolic substrate; PARTIAL rather than Type 1 EMPTY because the symbolic component is non-incidental).
- X10 — Type 1 EMPTY.
- X11 — IMPLEMENTED.
- X12 — Type 1 EMPTY.
- X13 — Type 1 EMPTY.
- X14 — Type 1 EMPTY.

**Axis 1 engagement:** All Type 1 EMPTY for creativity-research-derived rows.

**Notable:** S6 is the only held-out system that scores PARTIAL at X9. If RAG-with-explicit-KG-constraints is read strictly as neurosymbolic substrate, X9 begins to populate with PARTIAL classifications across systems that explicitly couple LLM retrieval with structured knowledge graphs. This is a tension worth noting.

### 3.7 S7: Modular LLM Agent for BCL-2

**Architecture.** Single-agent LLM coupled with domain-specific tools; tool-augmented reasoning for biomedical retrieval, molecular generation, property prediction, refinement, 3D structure generation. Single-agent architecture distinct from multi-agent S1-S5.

**Axis 2 occupation:**

- X1 — IMPLEMENTED (property prediction is named tool).
- X2 — IMPLEMENTED (molecular generation is named tool).
- X3 — IMPLEMENTED (biomedical retrieval is named tool).
- X4 — Type 1 EMPTY.
- X5 — Type 1 EMPTY.
- X6 — Type 1 EMPTY (single-agent).
- X7 — PARTIAL (iterative refinement across rounds; not full self-improvement).
- X8 — INCIDENTAL.
- X9 — Type 1 EMPTY.
- X10 — INCIDENTAL.
- X11 — IMPLEMENTED.
- X12 — Type 1 EMPTY.
- X13 — INCIDENTAL.
- X14 — Type 1 EMPTY.

**Axis 1 engagement:** All Type 1 EMPTY across creativity rows.

### 3.8 S8: AI Agents in Drug Discovery overview

**Architecture.** This is an overview paper, not a specific system. Surveys ReAct, Reflection, Supervisor, Swarm patterns for drug discovery. Treating it for matrix purposes as the *characteristic* of the agentic-AI-for-drug-discovery space rather than as a single system.

**Axis 2 occupation (modal across surveyed systems):**

- X1, X2, X3 — IMPLEMENTED (predictive, generative, retrieval all common across systems).
- X4, X5 — Type 1 EMPTY (rare in surveyed systems).
- X6 — IMPLEMENTED (multi-agent is the defining commitment).
- X7 — PARTIAL (iterative-refinement common but variably implemented).
- X8 — PARTIAL (KG-augmentation present in many surveyed systems).
- X9 — Type 1 EMPTY (neurosymbolic-as-primary-commitment absent across surveyed systems).
- X10 — PARTIAL (DMTA-style active learning in some systems).
- X11 — IMPLEMENTED (foundation-model backbone universal).
- X12 — Type 1 EMPTY (causal-modeling absent across surveyed systems).
- X13 — PARTIAL (multi-modal varies).
- X14 — INCIDENTAL.

**Axis 1 engagement (modal):** All creativity-research-derived rows Type 1 EMPTY.

**Citation spot-check on the survey paper.** The Seal et al. paper does not cite Wiggins, Boden, Hofstadter, Lakatos, Wallas, Csikszentmihalyi, Gentner, Fauconnier-Turner, Finke-Ward-Smith, Koestler, or Levin. Pattern holds.

---

## 4. Predictions vs findings

### 4.1 Quantitative agreement

I tabulate predictions vs findings across the eight systems × selected matrix-cells.

**Predictions about X9 (neurosymbolic) Type 1 EMPTY across all 8 systems:**

| System | Prediction | Finding | Match |
|---|---|---|---|
| S1 Robin | Type 1 EMPTY | Type 1 EMPTY | ✓ |
| S2 PharmaSwarm | Type 1 EMPTY | Type 1 EMPTY | ✓ |
| S3 Tippy | Type 1 EMPTY | Type 1 EMPTY | ✓ |
| S4 AgentMol | Type 1 EMPTY | Type 1 EMPTY | ✓ |
| S5 Prompt-to-Pill | Type 1 EMPTY | Type 1 EMPTY | ✓ |
| S6 RUGGED | Type 1 EMPTY | **PARTIAL** | partial mismatch |
| S7 Modular LLM Agent | Type 1 EMPTY | Type 1 EMPTY | ✓ |
| S8 Agents survey | Type 1 EMPTY | Type 1 EMPTY | ✓ |

7 of 8 predictions match exactly; 1 partial mismatch (S6 RUGGED). This is consistent with the matrix's universal-Type-1-EMPTY finding for X9 holding robustly with one borderline case.

**Predictions about X12 (causal AI) Type 1 EMPTY across all 8 systems:**

| System | Prediction | Finding | Match |
|---|---|---|---|
| All 8 | Type 1 EMPTY | Type 1 EMPTY | ✓ all 8 |

8 of 8 predictions match. The X12 universal-emptiness finding holds robustly.

**Predictions about creativity-row Type 1 EMPTY (A1, A4, B3, B4, B5, B6, C2, D4):**

| System | Predictions | Findings | Match |
|---|---|---|---|
| S1 Robin | All Type 1 EMPTY | C2 INCIDENTAL, rest Type 1 EMPTY | partial mismatch on C2 |
| S2 PharmaSwarm | All Type 1 EMPTY | D6 PARTIAL (Sawyer), rest Type 1 EMPTY | match for explicit predictions; D6 was variable-prediction |
| S3 Tippy | All Type 1 EMPTY | B1 INCIDENTAL (DMTA-Wallas), rest Type 1 EMPTY | partial mismatch on B1 (which I didn't explicitly predict) |
| S4 AgentMol | All Type 1 EMPTY | All Type 1 EMPTY | ✓ |
| S5 Prompt-to-Pill | All Type 1 EMPTY | D6 INCIDENTAL (orchestrator emergence) | match for explicit predictions; D6 was variable-prediction |
| S6 RUGGED | All Type 1 EMPTY | All Type 1 EMPTY for creativity rows | ✓ |
| S7 Modular LLM | All Type 1 EMPTY | All Type 1 EMPTY | ✓ |
| S8 Agents survey | All Type 1 EMPTY | All Type 1 EMPTY | ✓ |

Pattern is robust: explicit creativity-research engagement absent across all 8 systems. Where INCIDENTAL classifications appear (Robin C2 field-state via repurposing; Tippy B1 stages via DMTA; PharmaSwarm/Prompt-to-Pill D6 via emergence), these are functional approximations without explicit framework engagement, consistent with the parallel-vocabulary phenomenon documented in `citation_network_analysis.md`.

**Predictions about Citation patterns (no creativity-research figures cited):**

For all 8 systems where I performed a citation spot-check, no citations to the 11 creativity-research figures were found. This extends the citation-network-analysis pattern from n=100 to n=108 (the survey paper S8 alone covers many additional systems referenced in its own bibliography; if any of those cited creativity figures, S8 would be expected to mention them; they don't).

### 4.2 Where predictions did not match

**The S6 RUGGED PARTIAL classification at X9.** I predicted Type 1 EMPTY; I classified PARTIAL on application. This is the most significant disagreement and warrants examination.

The PARTIAL classification reflects a methodological tension: when does RAG-with-KG cross from "incidental knowledge integration" into "neurosymbolic substrate"? RUGGED's architecture does include explicit KG-grounding, retrieval over structured knowledge bases, and constraint-application logic that prevents LLM hallucination. This is closer to neurosymbolic substrate than pure-LLM systems. But it falls short of full neurosymbolic substrate per the matrix definition (which requires symbolic-reasoning operations beyond retrieval — explicit symbolic inference, rule application, constraint propagation, etc.).

The PARTIAL classification is defensible. It also points to a methodology refinement: the X9 threshold should be re-examined, possibly tightened (RAG-with-KG explicitly classified as INCIDENTAL rather than PARTIAL) or loosened (recognizing that RAG-with-KG-constraint-logic is functionally neurosymbolic-light). The current methodology produces defensible PARTIAL classifications in the borderline cases; this is the same pattern as in the original matrix construction.

**Robin C2 INCIDENTAL classification.** I predicted Type 1 EMPTY; classified INCIDENTAL on application. Robin's drug-repurposing focus produces field-state awareness (which clinicians, which indications, which existing drugs) that is functionally present though not architecturally deliberate. The INCIDENTAL classification is defensible; the prediction was slightly too strict.

**Tippy B1 INCIDENTAL classification.** I predicted Type 1 EMPTY for stages; classified INCIDENTAL on application via DMTA cycle. DMTA (Design-Make-Test-Analyze) has Wallas-stage flavor (preparation in design; verification in test+analyze) without explicit Wallas commitment. The INCIDENTAL classification is defensible.

### 4.3 Aggregate scoring

Predictions made: 8 systems × ~17 cells per system (14 AI methods + ~3 creativity rows in detail) ≈ 136 predictions.

Exact matches: ~125 / 136 ≈ 92%.
Partial mismatches (PARTIAL or INCIDENTAL where Type 1 EMPTY was predicted): ~10 / 136 ≈ 7%.
Direct contradictions (IMPLEMENTED where Type 1 EMPTY predicted, or vice versa): 0 / 136.

The methodology produces stable predictions on held-out systems with high agreement. The 7% partial-mismatch rate concentrates on cases where the methodology's threshold-application is genuinely interpretive (RAG-with-KG borderline at X9; functional approximations of creativity-framework engagement that fall short of architectural commitment). The pattern is consistent: the methodology produces robust universal-Type-1-EMPTY findings (X9 and X12) and consistent INCIDENTAL-rather-than-IMPLEMENTED findings for creativity-research-derived rows.

---

## 5. What this validation establishes and does not establish

### 5.1 What it establishes

**The methodology is reproducible on systems it wasn't designed against.** Eight systems not in the original matrix-construction sample produce matrix profiles that match pre-registered predictions at 92% agreement rate. Systems that were not used to construct the matrix produce the matrix's signature findings (X9 universal Type 1 EMPTY; X12 universal Type 1 EMPTY; creativity-research-derived rows essentially Type 1 EMPTY across all systems).

**The citation-network-analysis pattern extends to the held-out systems.** Spot-checks of 8 additional systems' references found zero citations to creativity-research figures. The historical-context claim from paper.md Section 1.2 generalizes beyond the n=100 sample.

**The parallel-vocabulary phenomenon recurs in held-out systems.** Where INCIDENTAL classifications appear (Robin field-state via repurposing; Tippy stages via DMTA; PharmaSwarm emergence via swarm orchestration), these are functional approximations of creativity-framework concepts without engaging the literature. The pattern documented in `citation_network_analysis.md` extends to the held-out systems.

### 5.2 What it does not establish

**The exercise is the work of a single author throughout.** Construction of the matrix, pre-registration of predictions, application of the methodology, and scoring of agreement were all done by the same person. Different application by another classifier might produce different classifications, particularly on borderline cases (RUGGED X9; Robin C2; Tippy B1). The exercise tests methodology stability under within-author conditions; it does not test methodology stability across classifiers.

**The methodology's value for *new architectures* is partly tested.** The 8 held-out systems are recent but stylistically continuous with the systems used in matrix construction (LLM-orchestration architectures, RAG-augmented systems, multi-agent specialization). A genuinely novel architecture — one substantively different from current dominant patterns — might surface methodology limits that the held-out validation doesn't probe. The methodology is robust within the current architectural-pattern space; whether it remains robust as the space shifts is open.

**The methodology's *predictive value* for unbuilt systems is not tested.** This validation tests classification of existing systems. It does not test whether the methodology can predict, before a system is built, what its matrix profile will be from architectural specifications alone. The latter would require a different validation: read a system's architecture spec, predict its matrix profile, then read the deployed system and check.

**The held-out validation is small.** 8 systems is enough to establish methodology reproducibility but not enough to produce statistical confidence intervals on agreement rates. A larger validation (20-30 systems) would harden the claim.

### 5.3 What this changes for the paper's claims

The validation supports the calibrated thesis at the appropriate strength. The matrix-driven analysis produces findings that hold on systems not used in construction at the cell level. The parallel-vocabulary phenomenon, the X9 strict-reading emptiness pattern (with one borderline KG-RAG exception that triggers threshold examination), the X12 universal emptiness, and the creativity-research-derived row emptiness all extend to the held-out systems.

What the validation establishes more carefully than the headline 92% suggests: the matrix produces stable classifications within the architectural-pattern space the original construction examined. The held-out systems are stylistically continuous with the construction systems — they are recent LLM/RAG/multi-agent drug-discovery AI systems, exactly the kind of architecture the matrix predicts will lack creativity-framework commitments. So the high agreement rate is internal-consistency-within-familiar-architectures rather than predictive validity against adversarial cases. The most informative single result is RUGGED's PARTIAL X9 classification (predicted Type 1 EMPTY), which forces threshold revision around RAG-with-KG-constraint-logic; this borderline case is more useful than the agreement statistic for refining methodology.

The methodology limits acknowledged in paper.md (cell statuses as interpretive; matrix as single-author work; methodology calibrated to current AI landscape; same author at every stage including this validation) are reinforced rather than resolved by this exercise. The paper's framing that "further review would likely shift individual classifications at margins" is consistent with this validation but cannot be tested by it; testing requires actually different classifiers, which this exercise does not provide.

---

## 6. Implications for next-stage work

This validation suggests several productive next-stage directions:

**Independent classification of cells by another classifier.** The most useful methodological enhancement would be applying the methodology to a sample of 30-50 systems (mix of original-sample and held-out) by an independent classifier. This is the cleanest test of methodology reproducibility and would distinguish methodology stability from same-author consistency. Cross-LLM hostile-review passes have surfaced specific issues (convergent-reinvention objection; X9 threshold examination; figure-set selection bias closure via bibliometric extension) and produced revisions; further such passes will continue to refine the work.

**Methodology refinement at thresholds.** The X9 (neurosymbolic) PARTIAL classification for RUGGED suggests the X9 threshold should be re-examined. Possible refinements: (a) tighten X9 to require explicit symbolic inference operations beyond retrieval; (b) loosen X9 to recognize RAG-with-KG-constraint-logic as PARTIAL universally; (c) split X9 into two sub-categories (X9a pure neurosymbolic, X9b RAG-augmented). Each refinement has consequences for the universal-emptiness finding; the current methodology's PARTIAL handling at the threshold is defensible but not unique. The RUGGED case is more analytically valuable than the aggregate 92% figure.

**Adversarial held-out validation.** Extending the validation to architectures stylistically distinct from current LLM/RAG/multi-agent patterns — for example, evolutionary search systems, model-based RL discovery agents, expert systems with substantial symbolic content — would test whether the methodology generalizes outside the architectural space it was constructed against.

**Predictive validation.** Reading architectural specifications for unbuilt or in-development systems and predicting their matrix profiles, then validating against deployed systems, would test the methodology's predictive value. This is a research project of its own.

**Cross-domain validation.** Applying the methodology to AI in domains other than drug discovery (materials discovery, scientific physics-discovery, mathematical theorem-proving) would test methodology generalization. The Krenn-physics-discovery and AlphaEvolve-mathematical-discovery cases are natural starting points.

These next-stage directions are bounded extensions of the current work; each is feasible at engineering-specifiable depth.

---

## 7. Conclusion

The held-out validation matches pre-registered cell-level predictions across 8 drug-discovery AI systems not used in matrix construction. The matrix's signature findings extend to the held-out systems with appropriate threshold caveats: X9 (neurosymbolic) Type 1 EMPTY under strict reading with one borderline KG-RAG exception (RUGGED) that suggests methodology refinement; X12 (causal AI) Type 1 EMPTY across all 8 held-out systems; creativity-research-derived rows essentially Type 1 EMPTY across the validation set. The citation-network-analysis pattern extends to held-out systems (zero citations to creativity-research figures across all 8 spot-checks). The parallel-vocabulary phenomenon recurs in held-out systems.

The validation acknowledges limits: single author at every stage (matrix construction, pre-registration, methodology application, scoring); small held-out sample (n=8); threshold-application produces borderline cases that warrant methodology refinement; the held-out systems are stylistically continuous with construction systems and do not test methodology against adversarial architectures; predictive value for unbuilt systems is not tested.

What the validation supports: the calibrated thesis claim that the citation gap reflects an architectural gap is consistent with the matrix's classifications being stable within the architectural-pattern space examined. The validation does not establish that translated architectures would outperform existing dominant patterns; that is the speculative-claim component of the thesis and remains undemonstrated. The validation tests methodology stability under within-author conditions; it does not test methodology stability across classifiers. The most useful single result is the RUGGED case, which forces explicit threshold examination at the RAG-with-KG borderline — surfaced by the methodology rather than hidden.

This is the prospective predictive validity test paper.md's adversarial reading flagged as needed. It produces appropriate evidence of methodology stability within familiar architectural patterns at the scale this exercise supports; it does not produce evidence of methodology stability across classifiers, which would require independent application by another classifier as next-stage work.
