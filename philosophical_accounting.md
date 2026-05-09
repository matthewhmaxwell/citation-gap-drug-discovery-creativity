# Substantive-vs-Decorative Philosophical Accounting

**Purpose:** For each major philosophical commitment the proposals invoke, distinguish what engineering content the apparatus actually delivers from what the apparatus does as positioning. This is internal-discipline work for the paper's honesty: when the proposals invoke Lakatos, Levin, Bourdieu, or other philosophical apparatus, the question is what work the apparatus does at the level of system specifications versus what it does as legitimacy framing.

**Position before reading.** Philosophical apparatus in proposal documents tends to operate at multiple levels simultaneously. At the substrate level, an apparatus specifies architecture (component decomposition, data structures, processing logic). At the framing level, it provides intellectual lineage and connects the work to existing conversations. At the legitimacy level, it grounds claims by connecting to recognized intellectual authorities. The honest accounting is not that one level is good and another bad — all three are doing work — but that they should be tracked separately so the engineering content isn't conflated with the positioning content.

**Methodological commitment.** For each apparatus examined: identify the specific architectural commitments that derive from the apparatus and could not be derived from a thinner formulation; identify the apparatus elements that are doing positioning rather than specification work; report the substantive-decorative split honestly.

---

## 1. Lakatos and the protective belt

### 1.1 Where Lakatos appears in the proposals

Lakatosian apparatus appears prominently in P1 (PPT — programme-progressivity tracker; protective-belt structure around hard-core commitments; programme-vs-degenerative-revision classification) and is referenced more lightly in P3 (TCI engages programme-state in human-AI hybrid reasoning) and P4 (constraint-revision distinguished from constraint-violation in CFS protective belt logic).

### 1.2 What Lakatos does substantively

The protective-belt-vs-hard-core distinction is engineering content. P1's PPT data structures explicitly represent (a) hard-core commitments that cannot be revised without abandoning the programme, (b) protective-belt elements that can be revised in response to anomaly without abandoning the programme, and (c) the temporal sequence of revisions to the protective belt. The data structures and the operations on them are specifically Lakatosian; a non-Lakatosian alternative would not produce the same architecture.

The progressive-vs-degenerative distinction is engineering content for output classification. PPT's main output is a classification of programme states: progressive (revisions predict and accommodate novel facts), degenerative (revisions only accommodate known anomalies), or undetermined. The classification logic uses Lakatosian criteria operationalized into specific predicates. Without the Lakatosian distinction, the proposals would lose their distinctive output type (programme-progressivity classification) and would default to standard ML-system outputs (predictions, scores, generated candidates). The Lakatosian apparatus produces a *kind of output* that differs from what current AI systems produce; this is substantive.

The novel-prediction criterion for progressivity is engineering content but partial. Lakatos's specific criterion for progressive programmes — that they predict novel facts — operationalizes to a structured space of biomedical-discovery predictions (specific candidate-property predictions, mechanism-claim predictions, dose-response predictions). The operationalization itself is non-trivial and is a methodological contribution (the planned `novel_prediction_operationalization.md` artifact develops this). Where the operationalization succeeds, Lakatos is doing substantive engineering work. Where it fails — where "novel prediction" doesn't have a clean operational definition for biomedical discovery — Lakatos is providing motivation rather than specification.

### 1.3 What Lakatos does decoratively

Programme-progressivity classification applied to entire research programmes (across labs, across decades, across multiple investigators) is positioning rather than engineering. The proposals use Lakatosian language for *system-level* programme tracking (a lab's drug-discovery programme; a research group's mechanism-claim programme), but the methodology developed in P1's PPT operates on individual concept-evolution traces rather than across-investigator-and-multi-year programme dynamics. The concept-evolution traces are substantive; the larger programme-level claims are positioning.

Sociological framing of "research programmes" as Lakatosian objects is decorative. When the proposals describe what a Lakatosian programme is — a constellation of researchers committed to specific hard-core assumptions, working out the protective belt, defending against anomalies — the description is providing intellectual context rather than specifying system architecture. The architectural commitments could be made under a thinner vocabulary (e.g., "tracked-belief structures with revision histories") without losing engineering content. The Lakatosian framing makes the work *legible* to philosophers of science and to readers familiar with the literature; it does not change what the system actually does.

The "field-state assessment" claims in P1 and P3 are partly substantive and partly decorative. Some elements (tracking what claims a field has revised in response to which experimental findings; tracking which protective-belt revisions failed to accommodate anomalies) are operationalizable and do engineering work. Other elements (judging whether a field as a whole is in a Lakatosian-progressive state) require subjective synthesis that the system does not actually perform; the language of "field state" implies an architectural capability the proposals do not deliver.

### 1.4 The honest split for Lakatos

Substantive: protective belt vs. hard core data structures; progressive vs. degenerative output classification at the concept-evolution-trace level; revision-history tracking; novel-prediction operationalization where it succeeds.

Decorative: programme-level claims at lab-or-investigator-level scope; field-state-as-Lakatosian-object framing; sociological context that motivates the work without specifying the architecture.

The proposals could be re-framed without losing engineering content if "Lakatosian programme tracking" were renamed "tracked-belief revision history with novelty classification." Doing so would lose intellectual lineage and reader-recognition without changing what the system does. The decision to keep Lakatosian framing is a positioning choice that has a cost (apparatus that doesn't fully deliver the architecture it implies) and a benefit (intellectual context that connects the work to existing literature on scientific change).

---

## 2. Levin and TAME

### 2.1 Where Levin/TAME appears in the proposals

TAME (Technological Approach to Mind Everywhere; Levin 2022, 2023) appears centrally in P1 (MSAS — multi-scale agent substrate; CSNP — cross-scale negotiation protocol) and is referenced lightly across other proposals where multi-scale considerations matter.

### 2.2 What Levin/TAME does substantively

The multi-scale agent substrate is engineering content. P1's MSAS specifies that the system represents biological systems as nested agents at multiple scales (molecular agents, cellular agents, tissue agents, organismal agents, population agents) where each scale has its own competence boundary, problem-solving repertoire, and goal-state representation. The data structures (agent-at-scale-S has goals G_S, has competence C_S, has internal-model-of-other-scale-agents M_S) are TAME-derived; a non-TAME alternative (e.g., reductionist hierarchical decomposition without agent-level commitments) would produce different data structures.

The cross-scale negotiation protocol is engineering content. P1's CSNP specifies how candidate molecules' actions at one scale (a molecular intervention) negotiate with competing goal-states at other scales (cellular homeostasis, tissue function, organismal viability, population-level evolutionary pressure). The negotiation logic produces specific outputs (cross-scale conflict surfacing; conflict-resolution candidates; conflict-prediction ahead of wet-lab investment) that current drug-discovery AI systems do not produce. This is a specific kind of output that derives from TAME's multi-scale agent commitments. Without TAME, the proposals would not produce this kind of output, and the engineering content would be lost.

The agential framing for non-conscious systems is partial substantive content. TAME's commitment that biological agents at non-cognitive scales (e.g., cells, gene-regulatory networks) have goal-state representations that can be modeled symbolically does work in the architecture: it justifies including symbolic representations of non-conscious-system goals (a cell's homeostatic targets; a gene-regulatory network's stable attractors). The substantive engineering claim is that these symbolic representations are useful for cross-scale conflict prediction, not that the underlying systems are literally agentive in the philosophical sense. Where TAME is read as engineering ontology — commitments that produce specific data structures and operations — it does substantive work. Where TAME is read as philosophical commitment — claims about whether cells *really are* agents — it does positioning work.

### 2.3 What Levin/TAME does decoratively

Generalization beyond biological systems to "intelligence wherever it is" is decorative. TAME's full philosophical scope includes claims about cognition in unconventional substrates (xenobots, gene-regulatory networks, evolution itself), consciousness, panpsychism-adjacent territory. The proposals do not engineer any of this; they engineer specific multi-scale conflict-surfacing for drug-discovery applications. Citing TAME in its full scope provides intellectual lineage but exceeds what the proposals deliver. A more disciplined positioning would cite Levin's specific multi-scale-modeling contributions (e.g., Levin 2023 on multi-scale competency architecture) without invoking TAME's broader claims.

The "cognitive light cones" framing is decorative. Levin's cognitive-light-cone construct (the temporal and spatial scope of an agent's predictive and goal-pursuing capabilities) is evocative and connects multi-scale agency to information-theoretic ideas. The proposals do not engineer light-cone-tracking; they engineer specific cross-scale conflict negotiation. Using "cognitive light cones" framing in proposal text is intellectual gesture rather than architectural specification.

### 2.4 The honest split for Levin/TAME

Substantive: multi-scale agent substrate as data-structure commitment; cross-scale negotiation protocol as output-generating logic; symbolic representation of non-conscious-system goals where useful for conflict prediction.

Decorative: TAME's full philosophical scope (intelligence wherever it is; consciousness claims; substrate-independence claims); cognitive-light-cones framing as gestural rather than operational; agential ontology read as philosophical commitment rather than engineering ontology.

The proposals are bitter-lesson-vulnerable on the multi-scale-agency commitment. If a sufficiently scaled multi-modal foundation model implicitly represents cross-scale dynamics (because its training data includes cross-scale measurements), it might produce equivalent conflict-prediction without explicit multi-scale agent commitments. The honest framing: TAME's substantive engineering content is testable against bitter-lesson alternatives; the decorative content is positioning that doesn't change what's being tested.

---

## 3. Bourdieu and field theory

### 3.1 Where Bourdieu appears in the proposals

Bourdieusian field theory appears prominently in P3 (FSS — field-state substrate; CRE — competition-and-recognition engine; CTL — capital-tracking layer; TCI — translator-critic interface) and is referenced lightly in P5 (collective-intelligence claims about distributed-substrate dynamics).

### 3.2 What Bourdieu does substantively

Field-state substrate as data structure is partial substantive content. P3's FSS specifies that the system represents the drug-discovery field as a structured space of positions (academic researchers, pharma R&D, regulatory bodies, payers, patient advocacy groups), capital types (scientific reputation, institutional backing, regulatory standing, financial resources), and competitive dynamics among positions. Where this representation drives specific operations (e.g., FSS data feeds into TCI's translator-critic-interface logic; CRE's competition-and-recognition outputs are derived from FSS state), the apparatus is doing engineering work. The data structures could be specified without Bourdieusian framing (e.g., "stakeholder-position graph with weighted resource flows"), but the specific representational choices reflect Bourdieusian commitments — capital-as-multi-typed; field-as-relational-position-space; recognition-as-symbolic-capital — that thinner alternatives would not produce.

Capital-tracking layer is partial substantive content. CTL tracks how candidate research outputs (papers, patents, FDA submissions, trial registrations) generate or consume different capital types within the field, and how capital accumulation affects field positions over time. The operational specifications (capital flows; capital conversions; capital depreciation rates) are engineering content. The Bourdieusian apparatus is producing specific data-tracking commitments that thinner formulations would not produce.

### 3.3 What Bourdieu does decoratively

The full Bourdieusian theoretical apparatus (habitus, doxa, illusio) is decorative. P3 invokes Bourdieusian language at several points where the underlying engineering content is thinner. "The system tracks the field's habitus around mechanism-claim acceptance" is gestural; what the system actually does is track which mechanism claims have been accepted by which institutional actors and at what rate. Habitus implies dispositional commitments below the level of explicit belief that the system does not actually represent.

Sociological framing of drug-discovery as a field-of-power is decorative. When the proposals describe the drug-discovery landscape as a Bourdieusian field with competing actors deploying capital-types in pursuit of position, the description provides intellectual context. The architectural commitments do not require this framing; they require representations of stakeholders, resources, and competitive dynamics that thinner formulations would also produce.

The connection to broader STS-and-sociology-of-science literature is decorative. Bourdieusian framing connects the work to traditions in science studies (Knorr-Cetina, Latour, Galison) that motivate field-engagement as relevant to drug-discovery decisions. The connection is intellectually productive (it justifies why field-engagement matters) but does not specify the architecture.

### 3.4 The honest split for Bourdieu

Substantive: field-as-relational-position-space data structure; capital-as-multi-typed tracking commitments; competition-and-recognition operational logic.

Decorative: habitus / doxa / illusio language as architectural specification (it isn't); full STS context as motivation; sociological framing as positioning.

The proposals could be re-framed under thinner sociological vocabulary (e.g., "stakeholder-position-and-resource-flow graph") without losing engineering content. Doing so would lose intellectual lineage to STS and field theory. The decision to keep Bourdieusian framing is a positioning choice that connects the work to existing conversations in STS at the cost of apparatus that doesn't fully specify architecture.

---

## 4. Wiggins and computational creativity

### 4.1 Where Wiggins appears in the proposals

Wiggins's R/T/E formalism (Reverberation/Transformation/Evaluation; Wiggins 2006) appears centrally in P1 (the SRS — symbolic reasoning substrate — uses R/T/E as its operational structure) and is referenced across proposals where Boden-via-Wiggins creativity-mode commitments matter.

### 4.2 What Wiggins does substantively

The R/T/E formalism is substantively architectural. SRS in P1 specifies three distinct operations: Reverberation (generating candidate moves within the existing concept space), Transformation (revising the concept space itself), and Evaluation (judging candidate moves against criteria the system can articulate). The three-operation decomposition is Wiggins-derived and produces specific architecture (Reverberation maps to NGIS calls within a fixed concept space; Transformation maps to PPT-driven revisions of the space's hard-core or protective-belt; Evaluation maps to PPT criteria-application). Without the R/T/E decomposition, the proposals would default to undifferentiated "generation" + "ranking" architecture that current AI systems produce.

The combinatorial / exploratory / transformational mode distinction (Boden via Wiggins) is substantively architectural. The proposals' SRS supports all three modes (combinatorial moves within the space; exploratory moves toward space boundaries; transformational moves that revise the space). Different modes invoke different components (combinatorial → NGIS within fixed concept space; exploratory → NGIS + PPT for boundary detection; transformational → PPT-driven space revision). The mode-distinguishing logic is engineering content; without it, the proposals would not differentiate kinds of creativity output.

### 4.3 What Wiggins does decoratively

Wiggins's specific formalism notation (the algebraic R/T/E definitions) is decorative for engineering purposes. The proposals operate at the architectural level (component names, operations, data flow) where Wiggins's formal notation is not essential. The engineering content survives in pseudocode or system-architecture diagrams; the formal notation is intellectual provenance.

Connections to non-medical computational-creativity work (music, narrative, mathematics, poetry) are decorative for medical-discovery applications. Wiggins's broader contributions include creativity research in diverse domains; the proposals operate specifically in drug-discovery space. Citing the broader work positions the proposals in computational creativity but does not specify medical-discovery architecture.

### 4.4 The honest split for Wiggins

Substantive: R/T/E three-operation decomposition as architectural commitment; combinatorial/exploratory/transformational mode distinction as engineering content for differentiating output kinds.

Decorative: formal notation as intellectual provenance rather than architectural necessity; non-medical computational-creativity context as positioning.

The proposals' Wiggins commitments are likely the most substantive of the philosophical apparatus. R/T/E and the Boden-via-Wiggins mode distinction directly produce architectural commitments that thinner formulations would not produce. The decorative content is minimal (formal notation; non-medical context); the substantive content is high.

---

## 5. Hofstadter / FARG / Copycat

### 5.1 Where Hofstadter appears in the proposals

Hofstadter-Mitchell Copycat architecture appears prominently in P2 (SNBC — slip-network bond constraints; CWGE — codelet workspace global execution) and is referenced where fluid-concept dynamics and analogical-flexibility matter.

### 5.2 What Hofstadter / Copycat does substantively

The codelet workspace is engineering content. P2's CWGE specifies that the system uses a workspace where small (codelet-level) operations compete for execution time based on dynamic salience, with global state evolving as codelets succeed or fail at sub-tasks. The codelet-level architecture produces specific dynamics (parallel-processing without explicit synchronization; emergent coherent-pattern-detection from local operations; failure-mode resilience through codelet diversity) that monolithic neural architectures do not produce. The architectural commitment is Hofstadter-derived; without it, the proposals would default to either (a) large-monolithic-model architectures or (b) sequential-pipeline architectures, neither of which produces the same dynamics.

The slip-network bond structure is engineering content. SNBC specifies that the system represents concepts as nodes with weighted, dynamically-adjustable connections to related concepts (the "slip-net"). The bond weights respond to context (a "lock" concept's bonds to "key" and "secure" strengthen in security context; weaken in piano-tuning context). The bond-adjustment logic is engineering content that produces fluid-concept behavior; thinner alternatives (fixed concept embeddings; static knowledge graphs) would not produce the same behavior.

### 5.3 What Hofstadter / Copycat does decoratively

The full Copycat philosophical commitments (consciousness as emergent from codelet swarm; analogy as the central cognitive mechanism) are decorative. The proposals engineer specific codelet-and-slip-net dynamics for analogical drug-discovery moves, not consciousness or general cognition. Citing FARG/Copycat in its full philosophical scope provides intellectual lineage but exceeds what the proposals deliver.

Connections to letter-string analogies (Copycat's original domain) are decorative for drug-discovery applications. The architectural commitments transfer (codelets, slip-nets, workspace dynamics); the specific letter-string-analogy applications do not.

### 5.4 The honest split for Hofstadter / Copycat

Substantive: codelet workspace dynamics as engineering content; slip-network bond structure as data-structure commitment; emergent-coherent-pattern-detection logic.

Decorative: consciousness-from-codelet-swarm philosophical commitment; letter-string-analogy specific applications; FARG-as-research-program intellectual lineage.

---

## 6. Engelbart and IA tradition

### 6.1 Where Engelbart appears in the proposals

Engelbart's Intelligence Augmentation tradition appears in P3 (TCI — translator-critic interface for human-AI hybrid reasoning) and is invoked across proposals where human-in-loop framing matters.

### 6.2 What Engelbart does substantively

Limited substantive engineering content. TCI's specifications include human-system interaction protocols (when the system pauses for human input; what kinds of decisions go to humans vs. autonomous resolution; how human inputs propagate back into system state). The architectural commitment that humans are *agents* in the system rather than *users* of the system has thin engineering implications: it requires the system to model human-agent state alongside AI-agent state, and to design interaction protocols that respect human-agent constraints (cognitive load, attention budgets, recognition latency).

### 6.3 What Engelbart does decoratively

Most invocations of Engelbart in the proposals are decorative. The IA tradition (Augment-Doug Engelbart; Bush's "As We May Think"; Licklider's man-computer-symbiosis) provides intellectual lineage for human-AI hybrid framing without specifying particular architecture. The proposals could specify TCI architecture under contemporary human-in-the-loop ML language without losing engineering content.

The contrast with "AI replacement" framing is decorative. The proposals position themselves against pure-autonomy AI framings (e.g., AI Scientist 2024; full Coscientist autonomy) by invoking Engelbart's IA-as-amplification commitment. The positioning is intellectually productive but does not change the architectural specifications.

### 6.4 The honest split for Engelbart

Substantive: human-as-agent-not-user data-structure commitment in TCI; interaction-protocol specifications grounded in human-agent constraints.

Decorative: IA-tradition intellectual lineage; positioning against pure-autonomy AI framings; broader Engelbart corpus citations.

The proposals' Engelbart content is mostly decorative. Substantive engineering content for human-AI hybrid is thin; the proposals would benefit from more concrete human-in-the-loop ML literature engagement (e.g., Wang et al. 2019 on human-AI-team coordination; Bansal et al. 2021 on human-AI complementarity) where the engineering content is denser.

---

## 7. Aggregate substantive-vs-decorative split

### 7.1 By apparatus

| Apparatus | Substantive content | Decorative content | Net rating |
|---|---|---|---|
| Wiggins R/T/E | High (architectural commitments directly derive) | Low (formal notation; non-medical context) | Mostly substantive |
| Hofstadter Copycat | High (codelet/slip-net dynamics) | Medium (philosophical scope; letter-string applications) | Mostly substantive |
| Levin TAME | Medium (multi-scale agent + CSNP) | Medium (broader TAME claims; cognitive light cones) | Substantive at core, decorative at edges |
| Lakatos | Medium (PPT data structures + classification logic) | High (programme-level claims at field scope; sociological framing) | Substantive at concept-trace level, decorative at field level |
| Bourdieu | Medium (FSS data structures + capital tracking) | High (habitus/doxa/illusio language; STS context) | Substantive at data-structure level, decorative at theoretical-apparatus level |
| Engelbart | Low (thin TCI commitments) | High (IA-tradition intellectual lineage; positioning) | Mostly decorative |

### 7.2 The overall picture

The proposals contain substantial engineering content derived from philosophical apparatus, and substantial positioning content grounded in the same apparatus. The honest accounting for the paper:

- The thesis ("AI approaches to drug discovery are unnecessarily limited because creativity research has not been translated") does not depend on the philosophical apparatus being uniformly substantive. It depends on enough of the apparatus producing engineering content that the translation claim is not vacuous. The substantive content tabulated above is enough to support this.

- The proposals' value claims (specific architectural commitments derive from specific frameworks; the architectures produce distinctive outputs that current AI does not produce) depend on the substantive content of the apparatus, not the decorative content. Where the apparatus is mostly decorative (Engelbart in TCI), the value claim is correspondingly weaker.

- The bitter-lesson question (Section 11.4) operates on the substantive content. Whether the proposals' Wiggins-derived R/T/E decomposition, Hofstadter-derived codelet-workspace dynamics, Levin-derived multi-scale agent substrate, etc., produce better drug-discovery outcomes than scaled foundation-model alternatives is the testable bet. The decorative content is positioning that doesn't change what's being tested.

- A critical reviewer can say the proposals' philosophical apparatus has decorative content. They can also say the substantive content is non-trivial. The honest framing is that the proposals do both engineering work and positioning work, that the engineering work is what matters for the testable claims, and that the positioning work is what makes the work *legible* to the relevant intellectual communities at the cost of apparatus that doesn't fully deliver the architecture it implies.

### 7.3 What this accounting changes for the paper

The accounting tabulated here informs but does not require restructuring of paper.md. The paper's value claims rest on substantive engineering content (matrix as diagnostic instrument; six proposals with engineering specs; citation-network analysis grounding the historical-context claim). The philosophical apparatus is invoked to ground the architectural commitments in established literature, but the testable claims do not require the full philosophical apparatus to be uniformly substantive.

The paper should — and the sharpening pass already does — be honest about the limitations the apparatus has. Section 1.4 (author positioning) acknowledges that the matrix's narrative findings reflect interpretive judgment. Section 11 acknowledges the philosophical-apparatus limitations indirectly. This artifact (`philosophical_accounting.md`) makes the substantive-vs-decorative split explicit, allowing readers who want detail to see the accounting and allowing the paper to compress to the engineering content where appropriate.

The paper's abstract already says: "Some philosophical apparatus the proposals invoke (Lakatos applied to field-state claims; Levin TAME as architectural substance) does engineering work in some places and serves positioning in others; the accounting is partial." This artifact is the partial-accounting fulfillment.

---

## 8. Conclusion

The proposals deliver substantial engineering content from Wiggins R/T/E, Hofstadter Copycat, and Levin TAME multi-scale agent substrate. They deliver moderate engineering content from Lakatos PPT (at concept-trace level) and Bourdieu FSS (at data-structure level). They deliver thin engineering content from Engelbart IA (TCI specifications are mostly thin).

The decorative content is real. Programme-level Lakatosian claims, full TAME philosophical scope, Bourdieusian habitus/doxa/illusio language, and Engelbart-tradition intellectual lineage do positioning work without specifying additional architecture. Acknowledging the decorative content explicitly is the honest move.

The thesis claim ("AI approaches to drug discovery are unnecessarily limited because creativity research has not been translated") does not require uniformly substantive apparatus. It requires enough substantive engineering content to make the translation claim non-vacuous. The substantive content tabulated above is sufficient. The decorative content is what makes the work legible to intellectual communities that recognize the apparatus; legibility has value but isn't the same as engineering content, and the accounting maintains this distinction.

This is the methodology accounting the paper says exists. It supports rather than undermines the thesis: it shows what the apparatus delivers and what it does not, allowing the testable claims to rest on the engineering content rather than on the full philosophical scope.
