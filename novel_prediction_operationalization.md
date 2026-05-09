# Operationalizing "Novel Prediction" for P1's PPT Progressivity Classification

**Purpose.** Lakatosian programme-progressivity classification depends on the criterion that a progressive programme predicts novel facts and a degenerative programme only accommodates known ones. P1's PPT (programme-progressivity tracker) implements this classification as one of its primary outputs. For the implementation to work, "novel prediction" must be operationalized — turned from philosophical concept into concrete predicates the system can apply to specific biomedical-discovery cases.

This artifact develops the operationalization. Without it, PPT delivers Lakatosian framing without Lakatosian engineering content; with it, PPT delivers a kind of output (programme-progressivity classification with concrete predicates) that no current AI system produces. The artifact is therefore one of the most substantive engineering contributions the paper supports, and the most testable.

**Scope.** I treat biomedical drug-discovery programmes specifically (small-molecule and protein therapeutics; mechanism-claim programmes; target-validation programmes). Other biomedical contexts (devices, diagnostics, surgical innovation) require separate operationalization that I sketch but do not fully develop.

**Status.** This is an operationalization design with worked examples, not a fully validated specification. PPT validation requires implementation against historical biomedical programmes (a planned validation study) and against held-out contemporary programmes (the planned `preregistered_matrix_predictions.md` artifact). The current artifact develops the operationalization to engineering-specifiable depth.

---

## 1. Lakatos's "novel prediction" criterion in the original formulation

### 1.1 Lakatos's text

In *Falsification and the Methodology of Scientific Research Programmes* (Lakatos 1970), the criterion appears in several formulations:

- A research programme is "theoretically progressive" if each modification to the protective belt predicts a novel fact that could not have been predicted from the previous formulation.
- A research programme is "empirically progressive" if some of those novel predictions get confirmed.
- A research programme is "degenerative" if modifications only accommodate already-known anomalies (post-hoc rescues) without producing novel predictions.

The key terms requiring operationalization are: *novel fact*, *prediction*, *modification of the protective belt*, *empirically progressive vs theoretically progressive*, and *degenerative*.

### 1.2 The challenge

Lakatos's criterion has been productively contested in philosophy of science for fifty years. Key challenges:

- "Novel" has multiple defensible readings: temporally novel (the prediction was made before the fact was known); use-novel (the fact was not used to construct the prediction); heuristic-novel (the fact would not have been expected from the previous framework). These readings differ in cases — a fact known historically but not used in constructing a prediction is use-novel but not temporally novel.

- Empirical confirmation has its own complications: how confirmed must a prediction be to count? At what point does a series of partially-confirmed predictions count as "empirically progressive"?

- The protective-belt-vs-hard-core distinction is itself interpretive. Different philosophers of science have read the same programme as having different hard-core elements.

The operationalization for PPT does not need to resolve these philosophical disputes; it needs to commit to specific definitions that produce reproducible classifications, with explicit acknowledgment of the readings that were chosen.

### 1.3 Commitments for PPT operationalization

PPT adopts the following commitments:

- **Use-novelty** rather than temporal-novelty as the primary criterion. A prediction counts as novel if the fact predicted was not used in constructing the framework version that made the prediction. This is the most defensible reading because it doesn't require historical-priority arguments and applies cleanly to AI-generated predictions where temporal sequencing is well-defined.

- **Probabilistic confirmation** rather than binary confirmation. Predictions get confirmation scores in [0,1] based on the strength of supporting evidence; "empirically progressive" requires accumulated confirmation above a threshold (specific threshold to be defined).

- **Explicit hard-core / protective-belt commitments** at programme initialization. The system requires the programme being tracked to specify its hard-core (the commitments that cannot be revised without abandoning the programme) and protective-belt (the commitments that can be revised). Disputes about which elements are hard-core vs protective-belt are resolved at initialization rather than during tracking.

- **Programme-relativity of classifications.** Progressivity vs degenerativity is judged relative to the programme's stated commitments at initialization, not against some absolute standard. A programme that converts to a different framework counts as starting a new programme rather than transforming the existing one.

These commitments are specific enough to support operationalization; they are also acknowledgedly Lakatosian-orthodox in some places and Lakatosian-pragmatic in others. The operationalization is neither the only defensible one nor a controversial reading; it is one principled committee choice.

---

## 2. The structured space of biomedical-discovery predictions

For PPT to classify biomedical programmes, "novel prediction" must be operationalized in biomedical-specific terms. The structured space of biomedical-discovery predictions falls into nine categories.

### 2.1 Candidate-property predictions

A programme that has identified candidate molecules predicts properties of those candidates that can be measured. Examples:

- *Binding-affinity predictions.* The programme predicts that candidate molecule M binds to target T with affinity ≥ K_d threshold under specified conditions.
- *Selectivity predictions.* The programme predicts that candidate molecule M binds to target T but not to off-target T' under specified conditions.
- *ADMET predictions.* The programme predicts that candidate molecule M has specific absorption, distribution, metabolism, excretion, toxicity properties (oral bioavailability ≥ X%; half-life ≥ Y hours; LD50 ≥ Z; specific cytochrome-P450 interaction profile).
- *Synthesizability predictions.* The programme predicts that candidate molecule M is synthesizable via a specific retrosynthetic route at specified yield and cost.

These predictions are use-novel if the framework version making the prediction did not have access to the experimental measurement of the property when the prediction was generated. The operationalization for PPT: track which framework version generated which candidate-property prediction; track which experimental measurements were available at framework-version time; classify as use-novel only if the prediction was generated before the measurement was taken (or before the measurement was made available to the framework).

### 2.2 Mechanism-claim predictions

A programme that has identified a candidate mechanism (e.g., "molecule M acts via inhibition of pathway P at node N") makes predictions about consequences:

- *Downstream-effect predictions.* The programme predicts that intervention via mechanism M produces specific downstream changes (e.g., transcript level of gene G decreases by X-fold; metabolite Z accumulates).
- *Cross-target predictions.* The programme predicts that other molecules acting via the same mechanism produce similar downstream effects.
- *Combinatorial predictions.* The programme predicts how the mechanism interacts with other interventions (synergy, antagonism, no interaction).
- *Resistance/escape predictions.* The programme predicts how target organisms or systems escape the mechanism (specific mutations; specific compensatory pathways).

Use-novelty for mechanism predictions: the framework version asserting the mechanism must have been formulated before the predicted downstream effect was measured. Cross-target predictions are particularly informative — a framework that asserts "molecule M acts via mechanism Φ" predicts that other M' molecules also acting via Φ will produce specific effects; this prediction is use-novel because the framework was formulated for M, not M'.

### 2.3 Dose-response predictions

A programme makes predictions about quantitative dose-response relationships:

- *EC50/IC50 predictions.* The programme predicts the molecular concentration at which 50% of maximal effect is observed in specified assays.
- *Hill-coefficient predictions.* The programme predicts the cooperativity of binding (slope of the dose-response curve).
- *Therapeutic-window predictions.* The programme predicts the ratio between therapeutic and toxic doses.
- *Time-course predictions.* The programme predicts how response evolves over time (acute vs. cumulative; tachyphylaxis vs. desensitization).

These predictions are quantitative; use-novelty operationalizes as the prediction being made before the corresponding experimental measurement.

### 2.4 Patient-stratification predictions

A programme that has identified a mechanism or candidate makes predictions about which patients respond:

- *Biomarker predictions.* The programme predicts that patients with biomarker B respond differently than patients without (specific differential response; magnitude estimate).
- *Genotype-stratification predictions.* The programme predicts that patients with specific genetic variants (SNPs, structural variants, expression patterns) respond differently.
- *Disease-stage predictions.* The programme predicts differential response across disease stages.
- *Comorbidity-stratification predictions.* The programme predicts how the candidate or mechanism interacts with common comorbidities.

These predictions are testable in clinical-trial substratification analysis or in real-world evidence studies; use-novelty applies when the prediction is made before the relevant patient-stratification data is collected.

### 2.5 Repurposing predictions

A programme makes predictions about new indications for known molecules or mechanisms:

- *Indication predictions.* The programme predicts that a molecule with established mechanism Φ will be effective in indication I_2 (when its current indication is I_1) based on mechanism-relevance.
- *Drug-class predictions.* The programme predicts that a class of molecules (defined by mechanism or structure) will be effective in indication I.
- *Cross-indication mechanism predictions.* The programme predicts that the mechanism relevant in one indication is relevant in another.

Use-novelty: the prediction is made for an indication-molecule pair that has not yet been studied empirically.

### 2.6 Trial-outcome predictions

A programme that has produced a candidate makes predictions about clinical-trial outcomes:

- *Phase-1 safety predictions.* The programme predicts specific safety findings in Phase 1 (no dose-limiting toxicity below dose D; specific adverse-event profile).
- *Phase-2 efficacy predictions.* The programme predicts specific efficacy thresholds (response rate ≥ R%; primary-endpoint improvement ≥ X).
- *Phase-3 confirmation predictions.* The programme predicts that the Phase-2 effect-size will replicate in Phase 3.
- *Subgroup predictions.* The programme predicts specific subgroup analyses will show stronger effects.

Use-novelty: the prediction is made before the relevant trial data is collected.

### 2.7 Negative-result predictions

A programme makes predictions that specific candidates or mechanisms will *fail*:

- *Off-target failure predictions.* The programme predicts that molecules with specific off-target binding will fail in vivo despite being effective in vitro.
- *Resistance-emergence predictions.* The programme predicts that specific resistance mechanisms will emerge in clinical use.
- *Subpopulation-failure predictions.* The programme predicts that specific subpopulations will not respond.
- *Mechanism-incompatibility predictions.* The programme predicts that specific mechanism combinations will not be additive or synergistic.

Negative-result predictions are particularly informative for progressivity assessment because they involve specific commitments rather than open-ended success claims. A programme that predicts "molecule M will fail in patients with marker B" makes a more falsifiable claim than "molecule M will work in some patients."

### 2.8 Cross-scale predictions

A programme that has multi-scale agent commitments (P1-relevant) predicts cross-scale effects:

- *Molecule-to-cellular predictions.* The programme predicts how a molecular intervention propagates to cellular phenotypes.
- *Cellular-to-tissue predictions.* The programme predicts how cellular changes manifest at tissue level.
- *Tissue-to-organism predictions.* The programme predicts how tissue changes affect organism-level physiology.
- *Population predictions.* The programme predicts how organism-level changes affect population-level outcomes (e.g., resistance dynamics, prevalence shifts).

These predictions are central to PPT's cross-scale-conflict-surfacing capability. Use-novelty applies at each scale separately: a programme that predicts cellular consequences of a molecular intervention before cellular measurements are taken makes a use-novel cellular prediction.

### 2.9 Discovery-method predictions

A programme makes predictions about which discovery methods will work:

- *Screen-hit predictions.* The programme predicts that specific screening conditions will identify molecules with mechanism Φ.
- *Computational-method predictions.* The programme predicts that specific computational methods (docking, ML scoring, generative models) will produce candidates with specific properties.
- *Assay-development predictions.* The programme predicts that specific assays will distinguish active from inactive molecules.
- *Trial-design predictions.* The programme predicts that specific trial designs (basket trials, adaptive designs, biomarker-stratified designs) will be more efficient than alternatives.

Use-novelty: the prediction is made before the discovery method is tried.

---

## 3. The PPT operationalization

### 3.1 Data structure

PPT maintains for each tracked programme:

- **Programme identifier** (string, unique).
- **Hard-core commitments** (list of structured claims; each claim has assertion, framework-version provenance, immutability flag = True).
- **Protective-belt commitments** (list of structured claims; each claim has assertion, framework-version provenance, revision-history list).
- **Predictions ledger** (list of prediction records; each record has prediction-text, prediction-category-from-Section-2, framework-version provenance, generation-timestamp, status [pending | confirmed | falsified | abandoned], confirmation-evidence-list, falsification-evidence-list).
- **Revision history** (list of revision records; each record has framework-version-from, framework-version-to, revision-type [protective-belt-modification | protective-belt-addition | protective-belt-removal], revision-trigger [anomaly-accommodation | novel-prediction-generation | hard-core-clarification], revision-text, timestamp).
- **Anomaly ledger** (list of anomaly records; each record has anomaly-text, framework-version-when-encountered, response-status [accommodated | unresolved | abandoned], response-revision-id-if-accommodated).

### 3.2 Use-novelty determination

For each prediction record, PPT determines use-novelty as follows:

```
def is_use_novel(prediction_record, framework_version, evidence_corpus):
    # Was the predicted fact already in the evidence corpus when the framework_version
    # that made the prediction was constructed?
    
    fact = extract_fact_from_prediction(prediction_record)
    framework_construction_timestamp = get_framework_timestamp(framework_version)
    
    # Check if fact was empirically established before framework version
    fact_evidence = search_evidence_corpus(fact, evidence_corpus)
    
    if not fact_evidence:
        # Fact has no prior empirical evidence → automatically use-novel
        return True
    
    # Fact has prior evidence: check if it was accessible to framework construction
    earliest_evidence_timestamp = min(e.timestamp for e in fact_evidence)
    
    if earliest_evidence_timestamp > framework_construction_timestamp:
        # Evidence post-dates framework construction → use-novel
        return True
    
    # Evidence pre-dates framework: check if it was used in framework construction
    if fact_evidence in framework_version.training_data_or_explicit_inputs:
        # Fact was used in construction → not use-novel
        return False
    
    # Evidence pre-dates framework but was not used → use-novel
    return True
```

The operationalization requires three traceable items: fact extraction from predictions; evidence-corpus search; framework-construction provenance. Each is feasible at engineering specification level:

- **Fact extraction from predictions** uses structured templates per prediction category from Section 2. A binding-affinity prediction parses to (target, molecule, affinity_threshold, conditions) and the fact corresponding to it is the empirically-measured affinity of that molecule against that target under those conditions. Templates are defined per category.

- **Evidence-corpus search** uses structured biomedical databases (BindingDB, ChEMBL, PubChem, ClinicalTrials.gov, drugs.fda.gov) plus literature search through PubMed/Europe-PMC APIs. Evidence-corpus state at a given timestamp can be reconstructed by filtering on entry-creation-date.

- **Framework-construction provenance** requires the system to track which inputs the framework version used. For ML-component-derived predictions, this is the training data provenance (when components were trained, what data was available). For symbolic-component-derived predictions, this is the explicit input commitments at framework version time.

The operationalization has a known limit: the evidence-corpus search can produce false-positives (the corpus contains evidence the framework didn't actually use; the system flags the prediction as not-use-novel when it really was). Reducing false-positives requires explicit framework-input tracking, which adds engineering cost. The current operationalization tolerates some false-positive rate and produces conservative classifications (more predictions classified as not-use-novel than truly were not-use-novel).

### 3.3 Confirmation-status determination

For each prediction record with status = pending, PPT determines confirmation status by searching for empirical evidence that bears on the prediction:

```
def determine_confirmation_status(prediction_record, evidence_corpus):
    fact = extract_fact_from_prediction(prediction_record)
    
    # Search for evidence directly relevant to the fact
    direct_evidence = search_evidence_corpus(fact, evidence_corpus)
    
    if not direct_evidence:
        # No relevant evidence → status remains pending
        return 'pending', None, None
    
    # Score evidence relevance and direction
    confirming_evidence = [e for e in direct_evidence if confirms(e, prediction_record)]
    falsifying_evidence = [e for e in direct_evidence if falsifies(e, prediction_record)]
    
    confirmation_score = compute_confirmation_score(
        confirming_evidence, falsifying_evidence, prediction_record
    )
    
    if confirmation_score >= CONFIRMATION_THRESHOLD:
        return 'confirmed', confirming_evidence, confirmation_score
    elif confirmation_score <= -CONFIRMATION_THRESHOLD:
        return 'falsified', falsifying_evidence, confirmation_score
    else:
        return 'pending_with_evidence', direct_evidence, confirmation_score
```

The CONFIRMATION_THRESHOLD is a tunable parameter; reasonable starting value is 0.7 for confirmation and -0.7 for falsification, with tunable values for different prediction categories. Confirmation-score computation depends on prediction category:

- For *binding-affinity predictions*, confirmation requires direct K_d/K_i measurement within ±2-fold of predicted value; falsification requires measurement >10-fold off prediction.
- For *mechanism-claim predictions*, confirmation requires intervention experiments (CRISPR perturbation, pharmacological rescue, etc.) that show predicted causal structure; falsification requires interventions that do not show predicted structure.
- For *trial-outcome predictions*, confirmation requires trial reaching predicted endpoint at predicted effect size with appropriate power; falsification requires trial reaching different endpoint or failing to reach the predicted endpoint with appropriate power.
- (And similar category-specific definitions for the other categories.)

### 3.4 Progressivity classification

Given the predictions ledger and revision history, PPT classifies the programme:

```
def classify_progressivity(programme):
    use_novel_predictions = filter_use_novel(programme.predictions)
    
    if len(use_novel_predictions) == 0:
        return 'theoretically_stagnant'  # No novel predictions made
    
    confirmed_use_novel = [p for p in use_novel_predictions if p.status == 'confirmed']
    falsified_use_novel = [p for p in use_novel_predictions if p.status == 'falsified']
    pending_use_novel = [p for p in use_novel_predictions if p.status.startswith('pending')]
    
    # Theoretically progressive: programme makes use-novel predictions
    if len(use_novel_predictions) >= MIN_NOVEL_PREDICTIONS_THRESHOLD:
        theoretically_progressive = True
    else:
        theoretically_progressive = False
    
    # Empirically progressive: confirmed use-novel predictions exceed threshold
    if len(confirmed_use_novel) / max(len(use_novel_predictions), 1) >= EMPIRICAL_PROGRESSIVITY_THRESHOLD:
        empirically_progressive = True
    else:
        empirically_progressive = False
    
    # Degenerative: revisions only accommodate anomalies without producing novel predictions
    revision_to_novel_prediction_ratio = (
        len(programme.revisions_with_novel_predictions) / 
        max(len(programme.revisions), 1)
    )
    
    if revision_to_novel_prediction_ratio < DEGENERATIVE_THRESHOLD:
        degenerative = True
    else:
        degenerative = False
    
    # Final classification
    if theoretically_progressive and empirically_progressive:
        return 'progressive'
    elif theoretically_progressive and not empirically_progressive:
        return 'theoretically_progressive_empirically_pending'
    elif degenerative:
        return 'degenerative'
    else:
        return 'undetermined'
```

The thresholds (MIN_NOVEL_PREDICTIONS_THRESHOLD, EMPIRICAL_PROGRESSIVITY_THRESHOLD, DEGENERATIVE_THRESHOLD) are tunable parameters. Reasonable starting values:

- MIN_NOVEL_PREDICTIONS_THRESHOLD = 3 (a programme must make at least 3 use-novel predictions to be theoretically progressive — fewer would not distinguish progressive from accidental).
- EMPIRICAL_PROGRESSIVITY_THRESHOLD = 0.30 (at least 30% of use-novel predictions must be confirmed for the programme to be empirically progressive — the threshold is relatively low because confirmation lag is high in biomedical contexts).
- DEGENERATIVE_THRESHOLD = 0.20 (fewer than 20% of revisions producing novel predictions classifies as degenerative — i.e., more than 80% of revisions are anomaly-accommodation rather than novel-prediction-generation).

### 3.5 Output format

PPT outputs for a tracked programme include:

- **Classification:** one of {progressive, theoretically_progressive_empirically_pending, degenerative, theoretically_stagnant, undetermined}.
- **Evidence summary:** counts of predictions per category; counts of confirmed / falsified / pending predictions; revisions and their types.
- **Specific predictions list:** each pending prediction with (a) its content, (b) its use-novelty status, (c) any pending evidence, (d) what would confirm or falsify it.
- **Revision narrative:** chronological list of revisions with classification (anomaly-accommodation vs novel-prediction-generation) and the predictions each revision generated.

The classification is the high-level output; the specific-predictions list and revision narrative are the operational outputs that allow human decision-makers to act on the classification (e.g., decide whether to continue investing in a programme classified as degenerative; decide which pending predictions to test next to resolve a programme's classification).

---

## 4. Worked example: applying PPT to the imatinib programme

### 4.1 Programme specification

The imatinib programme (1992-2001 development; see Druker et al. 2001 for the foundational clinical paper) is a useful worked example because it has clear hard-core commitments, well-documented protective-belt revisions, and a known outcome.

**Hard-core commitments** (specified at programme initialization):

- Chronic myeloid leukemia (CML) is driven by the BCR-ABL fusion protein.
- BCR-ABL has constitutively active tyrosine-kinase activity.
- Pharmacological inhibition of BCR-ABL kinase activity will normalize CML cells.

**Protective-belt commitments** (specified at programme initialization):

- A small-molecule kinase inhibitor with appropriate selectivity can be developed.
- The inhibitor will distinguish BCR-ABL from related kinases (Bcr-Abl-selective binding).
- Resistance mechanisms can be managed pharmacologically.

### 4.2 Predictions made

Across the imatinib development programme:

1. *Binding-affinity prediction.* "Compound STI571 binds BCR-ABL kinase domain with K_d in the low-nanomolar range." Use-novel (compound was synthesized to have this property; measurement post-dated synthesis). Confirmed.

2. *Selectivity prediction.* "STI571 will distinguish BCR-ABL from related Src-family kinases sufficiently to avoid off-target toxicity." Use-novel. Confirmed (with caveats — STI571 also inhibits c-KIT and PDGFR-α, but at similar potency; this opens additional indications rather than producing toxicity).

3. *Cellular-effect prediction.* "STI571 will normalize BCR-ABL-positive cells without affecting normal hematopoietic cells." Use-novel. Confirmed.

4. *Phase-1 prediction.* "STI571 in CML patients will produce hematologic responses at tolerable doses." Use-novel. Confirmed.

5. *Indication-extension prediction.* "STI571's c-KIT inhibition will be effective in gastrointestinal stromal tumors (GISTs) where c-KIT is constitutively active." Use-novel (made later in programme). Confirmed.

6. *Mechanism-extension prediction.* "Other kinases driven by similar fusion proteins or activating mutations will be amenable to similar pharmacological strategies." Use-novel. Confirmed (subsequent kinase inhibitors: gefitinib, erlotinib, dasatinib, nilotinib, etc.).

7. *Resistance-emergence prediction.* "Resistance will emerge through point mutations in the BCR-ABL kinase domain that disrupt drug binding without disrupting catalytic activity." Use-novel. Confirmed (T315I and other resistance mutations).

8. *Resistance-mitigation prediction.* "Second-generation kinase inhibitors with binding modes different from STI571 will be effective against STI571-resistant mutations." Use-novel. Confirmed (dasatinib, nilotinib).

### 4.3 Revisions and their types

The imatinib programme had several protective-belt revisions:

- *Revision 1.* From "STI571 will be selective for BCR-ABL" to "STI571 inhibits BCR-ABL, c-KIT, PDGFR-α at similar potency, and the latter two activities open additional indications." Revision-type: novel-prediction-generation (predicted GIST efficacy; confirmed).

- *Revision 2.* From "STI571 will be effective long-term" to "Resistance via T315I requires alternative inhibitors." Revision-type: anomaly-accommodation (T315I observed clinically), but with novel-prediction-generation (predicted that T315I would be addressable with second-generation inhibitors; confirmed via dasatinib's wider spectrum and ponatinib's T315I-specific activity).

- *Revision 3.* From "Single-agent therapy is sufficient" to "Combination therapy may be required for some resistance phenotypes." Revision-type: anomaly-accommodation; novel predictions about specific combinations are still pending in some cases.

### 4.4 Classification

Applying the PPT classification logic to the imatinib programme:

- Use-novel predictions: 8 (all listed above).
- Confirmed: 8 (all confirmed; some with caveats).
- Falsified: 0.
- Pending: 0 (the programme is mature).

- Theoretically progressive: yes (8 use-novel predictions, well above MIN_NOVEL_PREDICTIONS_THRESHOLD = 3).
- Empirically progressive: yes (8/8 = 100% confirmed, well above EMPIRICAL_PROGRESSIVITY_THRESHOLD = 0.30).
- Degenerative: no (revisions generated novel predictions rather than just accommodating anomalies).

**Final classification: progressive.**

This classification matches the historical assessment of the imatinib programme as one of the most successful targeted-therapy programmes in oncology. PPT's classification is not novel in this case — the programme is widely recognized as successful — but the operationalization shows that the apparatus produces correct classifications on cases where ground truth is established.

### 4.5 What this worked example demonstrates

The imatinib worked example demonstrates that:

- The programme specification (hard-core, protective-belt) is straightforwardly extractable from the literature.
- Predictions are identifiable in the literature and can be assigned categories from Section 2.
- Use-novelty determination is tractable when programme timeline is well-documented.
- Confirmation status is determinable from clinical and laboratory evidence.
- Classification logic produces sensible outputs.

The example also demonstrates a limit: the imatinib programme is well-documented and historically settled. Applying PPT to programmes that are *currently in progress* (where confirmation status is largely pending; where revision history is short; where hard-core commitments may still be evolving) is harder. The classification "theoretically_progressive_empirically_pending" is the expected output for most current programmes; the practical value of PPT is in surfacing which pending predictions, if confirmed or falsified, would change the classification.

---

## 5. A worked example for a degenerative programme: amyloid-cascade hypothesis in Alzheimer's

The amyloid-cascade hypothesis as the dominant explanatory framework for Alzheimer's disease drug-development is a more controversial worked example. Different reviewers will have different readings of its current status; my reading is that it is at minimum *theoretically progressive empirically pending* with some grounds for classifying as *degenerative*.

### 5.1 Programme specification

**Hard-core commitments:**

- Alzheimer's disease pathology is driven by amyloid-β plaques.
- Amyloid-β accumulation is causal of cognitive decline (not just a biomarker).
- Pharmacological reduction of amyloid-β accumulation will produce cognitive benefit.

**Protective-belt commitments (over the programme's history):**

- Amyloid-β monomers are not the toxic species; oligomers or specific aggregates are.
- Earlier intervention (presymptomatic) is required for benefit.
- Specific patient-stratification (APOE4 genotype, biomarker status) is required.
- Multi-target intervention may be required.

### 5.2 Revisions and their types

The amyloid-cascade programme has had numerous revisions:

- *Revision 1.* From "Reducing amyloid plaques will reduce cognitive decline" to "Reducing soluble oligomers (not just plaques) is what matters" after multiple plaque-targeting drugs failed. Revision-type: anomaly-accommodation. Did this revision generate novel predictions? Yes — predicted that drugs targeting oligomers would succeed where plaque-targeting drugs failed. **Status: pending (BAN2401/lecanemab and donanemab show modest effects; some confirmation but limited).**

- *Revision 2.* From "Treatment in symptomatic patients will work" to "Earlier (pre-symptomatic) treatment is required." Revision-type: anomaly-accommodation. Novel-prediction-generation: predicted that pre-symptomatic intervention would show stronger effects. **Status: pending (Alzheimer's prevention trials ongoing; A4 trial showed minimal effect).**

- *Revision 3.* From "Amyloid-β is the primary target" to "Combination with tau-targeting may be required." Revision-type: anomaly-accommodation. Novel-prediction-generation: weak (the prediction is generic; specific combinations not pre-specified).

- *Revision 4.* From "Cognitive scales are appropriate endpoints" to "Biomarker improvements indicate eventual cognitive benefit even when cognitive endpoints don't improve." Revision-type: anomaly-accommodation. Novel-prediction-generation: weak (the revision shifts what counts as success rather than predicting new outcomes).

### 5.3 Predictions and confirmation

Across the programme's history:

1. *Aducanumab/lecanemab cognitive-benefit prediction.* "Anti-amyloid antibodies will produce clinically meaningful cognitive benefit." Use-novel. Status: contested — modest effects observed but clinical-meaningful threshold debated.

2. *Pre-symptomatic intervention prediction.* "Pre-symptomatic intervention will show stronger effects than symptomatic intervention." Use-novel. Status: pending; some trials negative.

3. *Biomarker-improvement-predicts-cognitive-benefit prediction.* "Patients with biomarker improvement will show downstream cognitive benefit." Use-novel. Status: pending.

4. *APOE4-stratification prediction.* "APOE4-positive patients will respond differently than APOE4-negative." Use-novel. Status: confirmed (APOE4-positive at higher risk of ARIA but also at higher rate of disease progression; differential responses observed).

5. *Tau-combination prediction.* "Combining anti-amyloid with anti-tau will be more effective than either alone." Use-novel. Status: pending (combinations under investigation).

### 5.4 Classification

Applying PPT logic:

- Use-novel predictions: 5.
- Confirmed: 1 (APOE4-stratification, with caveats).
- Falsified: 0 (none unambiguously falsified).
- Pending or contested: 4.

- Theoretically progressive: yes (5 use-novel predictions, above MIN_NOVEL_PREDICTIONS_THRESHOLD = 3).
- Empirically progressive: borderline (1/5 = 20%, below EMPIRICAL_PROGRESSIVITY_THRESHOLD = 0.30; and the 1 confirmation has caveats).
- Degenerative: borderline (revisions have generated some novel predictions, but the predictions are mostly weak and have low confirmation rates).

**Final classification: theoretically_progressive_empirically_pending or borderline_degenerative depending on threshold tuning.**

A reviewer applying stricter thresholds (EMPIRICAL_PROGRESSIVITY_THRESHOLD = 0.50) would classify the programme as degenerative; a reviewer applying looser thresholds would classify as theoretically progressive empirically pending. The PPT operationalization makes the classification *transparent* — the threshold parameters are explicit, the predictions are listed, the revision history is documented — so different threshold choices produce different classifications in defensible ways.

### 5.5 What this worked example demonstrates

The amyloid-cascade example demonstrates that:

- PPT can apply to controversial programmes where the classification depends on threshold tuning.
- The operationalization makes the classification reproducible — different reviewers using the same thresholds will get the same classification.
- The transparency about thresholds and predictions allows debate to focus on substantive questions (what is the appropriate empirical-progressivity threshold? are the listed predictions complete? are they correctly assessed for confirmation?) rather than diffuse arguments about whether the programme is "really" progressive.
- The classification is informative for resource-allocation decisions: a programme classified as borderline-degenerative warrants more critical scrutiny on whether continued investment is warranted.

---

## 6. Limits and what the operationalization does not deliver

### 6.1 The use-novelty determination is approximate

The use-novelty determination depends on traceable framework-construction provenance. For ML-component-derived predictions, training data provenance is often partially opaque (training-data manifests are sometimes incomplete; foundation-model-derived predictions inherit all training data of the foundation model). The operationalization tolerates this opacity by classifying conservatively (when in doubt, classify as not-use-novel), but conservative classification underestimates actual progressivity for programmes that use ML components.

### 6.2 Confirmation thresholds are tunable

The CONFIRMATION_THRESHOLD, EMPIRICAL_PROGRESSIVITY_THRESHOLD, and DEGENERATIVE_THRESHOLD are tunable parameters. Different threshold choices produce different classifications. The operationalization makes this transparent rather than hiding it. PPT outputs include the threshold values used; readers can adjust thresholds to see how classifications change.

### 6.3 Programme specification is not automated

PPT requires explicit programme specification (hard-core, protective-belt, programme identifier) at initialization. Specifying programmes is itself interpretive work — different classifiers will draw the hard-core / protective-belt boundary differently. The operationalization does not automate this; it requires human input at programme initialization.

### 6.4 Cross-programme comparison is not handled

PPT classifies individual programmes as progressive vs degenerative. It does not address how to compare two competing programmes' relative progressivity. Multi-programme comparison is a richer Lakatosian-and-post-Lakatosian topic that this operationalization doesn't engage.

### 6.5 The Bayesian framing is implicit, not explicit

A more philosophically sophisticated operationalization would frame use-novelty and confirmation in explicit Bayesian terms (prior probability of the prediction; posterior probability after evidence; Bayes factors for confirmation). The current operationalization uses thresholds rather than continuous Bayesian quantities. A Bayesian-explicit version is feasible and would improve the operationalization; the current version is sufficient for engineering implementation while leaving the Bayesian extension as future work.

### 6.6 What the operationalization does deliver

Despite these limits, the operationalization delivers:

- A specific structured space of biomedical-discovery predictions that PPT can recognize and classify (Section 2).
- A specific use-novelty determination procedure (Section 3.2).
- A specific confirmation-status determination procedure (Section 3.3).
- A specific progressivity-classification procedure (Section 3.4).
- Specific output formats that surface the classification's underlying evidence (Section 3.5).
- Worked examples showing the apparatus operates on real biomedical programmes (Sections 4 and 5).

This is enough for PPT to be implementation-ready. The operationalization can be tested against historical biomedical programmes (further worked examples; calibration of thresholds against historical ground truth) and against contemporary programmes.

### 6.7 PPT produces structured contestability rather than objective classification

A hostile reading of the operationalization, after Sections 6.1 through 6.5, is that PPT solves one problem (operationalizing Lakatosian novel prediction) by relocating discretion into several reviewer-dependent inputs: programme specification at initialization (the hard-core/protective-belt boundary requires interpretive judgment), evidence-corpus completeness (what counts as evidence the framework had access to), confirmation thresholds (each prediction category has its own thresholds requiring calibration), and use-novelty provenance determination (ML-component-derived predictions inherit training-data provenance that is often opaque).

The amyloid-cascade worked example (Section 5) makes this explicit: the classification depends on threshold tuning, with looser thresholds producing "theoretically_progressive_empirically_pending" and stricter thresholds producing "borderline_degenerative." Different reviewers using PPT will produce different classifications on contested programmes. PPT may therefore *reproduce* expert disagreement rather than *resolve* it.

This is not fatal to the operationalization, but it changes what PPT delivers. PPT does not produce objective programme-progressivity classifications; it produces *structured contestability*. The structured-contestability framing has three components:

- **Auditability of disagreement.** When two reviewers using PPT disagree, the disagreement decomposes into specific traceable inputs: which programme specification each used, which evidence corpus each consulted, which threshold parameters each applied, which use-novelty determinations each made. This is a substantial improvement over diffuse disagreement about whether a programme is "really" progressive; it makes the disagreement specific enough to debate.

- **Constraint on legitimate disagreement.** PPT does not allow arbitrary classification. Reviewers using PPT cannot, for example, classify imatinib as degenerative without specifying which predictions were not confirmed and which revisions accommodated anomalies without producing novel predictions. The operationalization constrains what counts as a defensible PPT classification, even when reasonable reviewers disagree within those constraints.

- **Transparency of threshold choices.** PPT's outputs include the threshold values used; classifications travel with their parameter context. Readers can re-run the classification under different thresholds and see how the classification changes. This makes the operationalization *useful for deliberation* rather than *authoritative for adjudication*.

The honest framing for the paper: PPT is not a programme-progressivity classifier in the strong sense (objective classification independent of reviewer judgment). PPT is a structured contestability instrument in the weaker but more defensible sense (specific traceable disagreement, constrained legitimate disagreement space, transparent threshold dependencies). This is what the operationalization actually delivers, and it is what the paper should claim. The earlier framing of PPT as classifying programmes overstates the operationalization's autonomy from reviewer input; the structured-contestability framing matches what the worked examples actually demonstrate.

---

## 7. Implications for the paper's claims

### 7.1 What this artifact strengthens

The thesis claim ("AI approaches to drug discovery are unnecessarily limited because creativity research has not been translated") is strengthened by this artifact. The Lakatosian programme-progressivity-tracking that P1 specifies is now operationalized to engineering-specifiable depth. The translation from Lakatos to PPT is no longer a theoretical commitment; it is concrete enough to implement and test.

The substantive-vs-decorative philosophical accounting (`philosophical_accounting.md`) classified Lakatos's content as "Substantive at concept-trace level, decorative at field level." This artifact concretizes the substantive content. PPT operates at the concept-trace level (programme-specific predictions, programme-specific revisions, programme-specific classifications) — exactly where the philosophical accounting identified substantive engineering content.

The bitter-lesson question (Section 11.4 of paper.md) identified the proposals' value as depending on whether they produce *distinctive outputs that current AI does not produce* and whether *those outputs matter*. PPT's output (programme-progressivity classification with concrete predicates) is one of the proposals' distinctive outputs. This artifact makes that output concrete enough to test against bitter-lesson alternatives.

### 7.2 What this artifact does not deliver

This artifact does not validate PPT against historical or current biomedical programmes systematically. The two worked examples (imatinib, amyloid-cascade) are illustrative rather than systematic. Systematic validation requires applying PPT to a set of historical programmes with known outcomes (e.g., 20-30 historical drug-discovery programmes with documented success/failure trajectories) and showing that PPT's classifications correlate with the known outcomes. This validation is the natural next-stage work.

This artifact does not address the cross-programme comparison problem (Section 6.4) or the Bayesian-framing extension (Section 6.5). Both are honest limits.

This artifact does not specify the classifier-input requirements at programme initialization (the hard-core / protective-belt boundary specification) in detail. Different classifiers will produce different programme specifications; how stable specifications are across classifiers is unmeasured. This is a known limit that requires further engineering work and validation.

### 7.3 The claim this artifact supports

PPT can be specified to engineering depth; the operationalization is concrete enough to implement; the classifications it produces are reproducible-with-disagreement-at-margins (the disagreements being primarily about threshold tuning, which the operationalization makes transparent). The Lakatosian-derived component of the proposals' philosophical apparatus is therefore substantively translatable, not merely decoratively invoked.

This is one specific demonstration of the broader thesis claim that creativity research is translatable to drug-discovery AI architecture. The same demonstration can be developed for the Wiggins R/T/E formalism (P1's SRS), the Hofstadter codelet workspace (P2's CWGE), the Levin multi-scale agency (P1's MSAS), the Geneplore preinventive structures (P2's PSL). Each is a separate operationalization-development project. The current artifact develops one of them in detail, demonstrating that the translation works at engineering-specifiable depth.

The honest framing for the paper: this artifact develops the operationalization for one component of one proposal. Five other major operationalizations remain. Each is similarly tractable; each requires similar artifact-level development. The thesis claim depends on enough of these operationalizations succeeding that translation is non-vacuous; one fully-developed operationalization plus the architectural specifications for five others is sufficient to support the thesis at the level paper.md claims.
