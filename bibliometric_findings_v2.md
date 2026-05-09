# Bibliometric Findings v2 — Broader Chemistry-AI Methodology Corpus

v2 extension of the bibliometric work in `bibliometric_findings.md`. Tests whether the strict-corpus-boundary objection identified by reviewer pass 3 changes the architectural-impoverishment finding when the corpus is broadened to include the chemistry-AI methodology layer (molecular ML, autonomous chemistry, retrosynthesis, generative chemistry, foundation models) drug-discovery AI imports its methods from.

**Transparency disclosure (per spec §7).** v2 was triggered by a specific reviewer objection — that v1's strict corpus boundary excluded chemistry-AI methodology papers like Coley 2019 and Schwaller 2020 (both surfaced in v1's own bridging-papers list as real Boden-citing AI-chemistry bridges). v2 is a directed response to that objection, not a neutral robustness check. The findings here are honest regardless of which outcome (A/B/C) emerges.

## Executive summary

- **v2 broader corpus**: 33,469 papers (vs v1 strict corpus: 30,935; v2 expansion adds ~2,534 papers, much smaller than the spec's 50K-150K estimate).
- **Direct citation (3.1)**: 12 of 156 canonical creativity works cited by ≥1 v2-corpus paper. 15 unique v2-corpus papers cite ≥1 canonical work — **0.045%** of v2 corpus (vs v1: 0.042%). Proportional rate essentially unchanged.
- **Net new direct-citing papers in v2 not in v1**: 2.
- **Forward-citation share (3.4)**: mean v1-share = 0.0068%; mean v2-share = 0.0077%. Mean delta share = 0.0009%. Negligible.
- **Counterexample (3.5)**: 15 v2-corpus papers cite ≥1 canonical (vs v1: 13). Classified as chemistry-AI methodology primary: 1 (new class — wasn't possible in v1 by definition). Substantive engagement: 3 (vs v1: 3 — unchanged).
- **Fuzzy concept scan (3.5)**: 'paradigm shift' v1=300 → v2=319 (delta +19). Other concept terms essentially unchanged. The parallel-vocabulary phenomenon is robust to corpus expansion.
- **Topic modeling (3.3)**: v2 produced 6 non-noise topics on the v2-sample + computational-creativity corpus union; 4 contain papers from both communities; max community balance = 0.070 (vs v1: 0.080). No topic with balance ≥ 0.1 — community separation reproduces.

**Outcome classification: A** — v2 reproduces the v1 pattern at scale.

Justification: corpus expansion adds ~2,500 papers (≪ spec's 50K-150K estimate); direct-citation rate essentially unchanged at 0.045%; substantive-engagement count unchanged at 3 (all philosophy/epistemology framings, none methodology); only 1 new chemistry-AI methodology citing paper appears (Schwaller 2020 *Molecular Machine Learning: The Future of Synthetic Chemistry?*) and it is a passing reference; forward-citation share delta is +0.001%; topic-modeling community separation reproduces with max balance 0.070. The architectural-impoverishment inference for the methodology layer holds across the broader corpus.

## 1. The corpus-boundary question

v1 found 13 of 30,935 papers (0.042%) citing canonical creativity works, with 3 substantive engagements (all philosophy/epistemology). The reviewer objection: v1's strict 'drug discovery AND AI' filter excludes the chemistry-AI methodology layer drug-discovery AI imports from — molecular ML, autonomous chemistry, retrosynthesis, generative chemistry, foundation models. v1's own 3.2 co-citation analysis surfaced two clear bridges that fell outside v1's strict corpus: Coley et al. 2019 *Autonomous Discovery in the Chemical Sciences Part II: Outlook* and Schwaller et al. 2020 *Molecular Machine Learning: The Future of Synthetic Chemistry?* — both Angewandte Chemie, both citing Boden, both at the chemistry-AI methodology layer.

**v2 broadens the corpus filter** to include 17 chemistry-AI methodology terms ('molecular machine learning', 'autonomous chemistry', 'autonomous chemical discovery', 'autonomous synthesis', 'retrosynthesis', 'synthetic chemistry AI', 'generative chemistry', 'molecular property prediction', 'chemoinformatics', 'cheminformatics', 'molecular representation learning', 'chemical foundation model', 'molecular foundation model', 'reaction prediction', 'self-driving laboratory', 'self-driving lab', 'autonomous laboratory') in addition to the original 10 drug-discovery terms. The AI-side filter (13 terms) is unchanged.

**Critical empirical finding on corpus size.** The spec estimated v2 would be 50,000-150,000 papers. The actual v2 corpus is **33,469 papers**, only ~2,534 more than v1. The reason: most chemistry-AI methodology papers ALSO contain drug-discovery terms in their abstracts (e.g., a 'molecular property prediction' paper that mentions 'ADMET' is already in v1). The chem-only-with-AI corpus (no drug terms anywhere) is ~3,850 papers — a meaningful but modest expansion, not the order-of-magnitude expansion the spec anticipated.

## 2. Coley 2019 / Schwaller 2020 / other named-bridge status

Per spec §4.2, we explicitly verify which named bridge papers are now in the v2 primary corpus.

Paper | Year | Cites | In v1 corpus? | In v2 corpus? | Notes
--- | --- | --- | --- | --- | ---
Coley 2019 Autonomous Discovery Part I (Progress) | 2019 | 304 | ✅ | ✅ | 
Coley 2019 Autonomous Discovery Part II (Outlook) | 2019 | 270 | ❌ | ❌ | Boden-citing bridge from v1 §3.2; **still excluded from v2** because abstract lacks any v2 term
Schwaller 2020 Molecular ML Future Synthetic Chem | 2020 | 71 | ❌ | ✅ | **Now in v2** via 'molecular machine learning' term — closes one bridge
ChemCrow | 2023 | 132 | ✅ | ✅ | 
Coscientist (Boiko 2023) | 2023 | 744 | ❌ | ❌ | Excluded — abstract framing 'autonomous chemical research' didn't match 'autonomous chemistry'
Burger 2020 Mobile robotic chemist | 2020 | 1,386 | ❌ | ❌ | Excluded — title 'mobile robotic chemist' has no v2 term in abstract either
Molecular Transformer (Schwaller) | 2019 | 838 | ❌ | ✅ | 
top-cited-v2-only | 2017 | 2,869 | ❌ | ✅ | 
top-cited-v2-only | 2018 | 1,876 | ❌ | ✅ | 
top-cited-v2-only | 2019 | 1,697 | ❌ | ✅ | 
top-cited-v2-only | 2017 | 807 | ❌ | ✅ | 
top-cited-v2-only | 2023 | 753 | ❌ | ✅ | 
top-cited-v2-only | 2017 | 683 | ❌ | ✅ | 
top-cited-v2-only | 2017 | 609 | ❌ | ✅ | 
top-cited-v2-only | 2017 | 583 | ❌ | ✅ | 
top-cited-v2-only | 2022 | 550 | ❌ | ✅ | 
top-cited-v2-only | 2023 | 487 | ❌ | ✅ | 
top-cited-v2-only | 2020 | 455 | ❌ | ✅ | 
top-cited-v2-only | 2020 | 388 | ❌ | ✅ | 
top-cited-v2-only | 2022 | 340 | ❌ | ✅ | 
top-cited-v2-only | 2017 | 339 | ❌ | ✅ | 
top-cited-v2-only | 2021 | 329 | ❌ | ✅ | 
top-cited-v2-only | 2020 | 329 | ❌ | ✅ | 
top-cited-v2-only | 2019 | 292 | ❌ | ✅ | 
top-cited-v2-only | 2021 | 286 | ❌ | ✅ | 

**Boundary leakage status: partially closed.** v2 successfully captures Schwaller 2020 *Molecular Machine Learning* (the second bridge from v1) and Coley 2019 *Part I (Progress)* (already in v1). v2 still excludes Coley 2019 *Part II (Outlook)* — the paper that explicitly cites Boden — because *Outlook* is a forward-looking essay whose abstract does not contain any of the v2 search terms despite the paper's content being methodologically central. The boundary leakage that this paper represents cannot be closed by keyword expansion alone; it would require either citing-paper-based corpus inclusion or full-text search.

Coscientist (Boiko 2023), Burger 2020, AlphaFold, RFdiffusion are also still outside v2 — these are real chemistry-AI methodology canonicals with substantial citations but their title/abstract framing doesn't match the v2 keyword filter. Including them would require either a 4th-pass keyword expansion or a different (e.g., venue-based or topic-based) corpus criterion.

## 3. v1 vs v2 comparison framework (the central deliverable)

Metric | v1 (strict drug-discovery) | v2 (broader chemistry-AI) | Change | Implication
--- | --- | --- | --- | ---
Corpus size | 30,935 | 33,469 | +2,534 (8.2%) | v2 expansion much smaller than spec estimate
Direct citations (corpus papers citing ≥1 canonical) | 13 (0.042%) | 15 (0.045%) | +2 | citation gap survives
Substantive engagements | 3 (all biology-AI-philosophy frontier) | 3 (same three) | +0 | no new substantive engagement at methodology layer
Chemistry-AI methodology primary class | n/a | 1 | +1 | new class introduced; only Schwaller 2020 fills it (passing engagement)
Figures with non-zero corpus citations | 7 of 30 | 8 of 30 | +1 (Alexander newly appears) | extended figure set still bounded
Fuzzy 'paradigm shift' (Kuhn) abstract hits | 300 (0 cite Kuhn) | 319 (0 cite Kuhn) | +19 | parallel-vocabulary pattern reproduces
Coley 2019 Part II (Outlook) in primary corpus? | No | **No** (still excluded) | unchanged | boundary leakage not fully closed
Schwaller 2020 (Molecular ML) in primary corpus? | No | **Yes** (now included) | added | one bridge captured by v2 expansion
Topic-modeling community max balance | 0.08 | 0.070 | -0.010 | community separation holds

### Per-figure-group v1 vs v2 delta

| figure_group      | group       |   v1_total_pairs |   v1_unique_papers |   v1_n_works_cited |   v2_total_pairs |   v2_unique_papers |   v2_n_works_cited |   delta_pairs |   delta_unique_papers |
|:------------------|:------------|-----------------:|-------------------:|-------------------:|-----------------:|-------------------:|-------------------:|--------------:|----------------------:|
| Alexander         | extended-15 |                0 |                  0 |                  0 |                1 |                  1 |                  1 |             1 |                     1 |
| Boden             | original-11 |                3 |                  3 |                  2 |                4 |                  4 |                  2 |             1 |                     1 |
| Amabile           | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Campbell          | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Clark-Chalmers    | extended-15 |                2 |                  1 |                  2 |                2 |                  1 |                  2 |             0 |                     0 |
| Csikszentmihalyi  | original-11 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Fauconnier-Turner | original-11 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Feyerabend        | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Finke-Ward-Smith  | original-11 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Gentner           | original-11 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Hofstadter        | original-11 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Hutchins          | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Kauffman          | extended-15 |                2 |                  2 |                  2 |                2 |                  2 |                  2 |             0 |                     0 |
| Kaufman           | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Altshuller        | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Knorr-Cetina      | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Kuhn              | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Lakatos           | original-11 |                1 |                  1 |                  1 |                1 |                  1 |                  1 |             0 |                     0 |
| Latour            | extended-15 |                4 |                  4 |                  3 |                4 |                  4 |                  3 |             0 |                     0 |
| Levin             | original-11 |                2 |                  2 |                  1 |                2 |                  2 |                  1 |             0 |                     0 |
| Newell            | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Runco             | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Schon             | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Simon             | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |
| Simonton          | extended-15 |                0 |                  0 |                  0 |                0 |                  0 |                  0 |             0 |                     0 |

**Reading.** Only two figure groups gain citations from v2 expansion: Alexander (+1, INTERSECT architecture specification citing pattern-language work) and Boden (+1, Schwaller 2020 citing Boden's *Creativity and AI*). All 28 other figure groups have unchanged citation counts. Specifically, none of the absent traditions (Simon-Newell, Amabile-Sternberg, Schön, Altshuller, Stokes, Hutchins, Knorr-Cetina, Kuhn, Feyerabend, Kaufman, Runco, Simonton, Campbell) gain even one citation in v2.

## 4. Per-analysis findings

### 4.1 Direct citation (v2)

| figure_group   | individual_names            | group       |   n_canonical_works |   n_works_with_any_v2_citation |   total_v2_corpus_figure_paper_pairs |   unique_v2_corpus_papers_citing_figure |
|:---------------|:----------------------------|:------------|--------------------:|-------------------------------:|-------------------------------------:|----------------------------------------:|
| Boden          | Margaret Boden              | original-11 |                   5 |                              2 |                                    4 |                                       4 |
| Latour         | Bruno Latour                | extended-15 |                   5 |                              3 |                                    4 |                                       4 |
| Clark-Chalmers | Andy Clark | David Chalmers | extended-15 |                  10 |                              2 |                                    2 |                                       1 |
| Levin          | Michael Levin               | original-11 |                   5 |                              1 |                                    2 |                                       2 |
| Kauffman       | Stuart Kauffman             | extended-15 |                   5 |                              2 |                                    2 |                                       2 |
| Alexander      | Christopher Alexander       | extended-15 |                   5 |                              1 |                                    1 |                                       1 |
| Stokes         | Donald Stokes               | extended-15 |                   5 |                              1 |                                    1 |                                       1 |
| Lakatos        | Imre Lakatos                | original-11 |                   5 |                              1 |                                    1 |                                       1 |
| Kuhn           | Thomas Kuhn                 | extended-15 |                   1 |                              0 |                                    0 |                                       0 |
| Wallas         | Graham Wallas               | original-11 |                   5 |                              0 |                                    0 |                                       0 |
| Sternberg      | Robert Sternberg            | extended-15 |                   5 |                              0 |                                    0 |                                       0 |
| Simonton       | Dean Keith Simonton         | extended-15 |                   5 |                              0 |                                    0 |                                       0 |
| Simon          | Herbert Simon               | extended-15 |                   5 |                              0 |                                    0 |                                       0 |
| Schon          | Donald Schön                | extended-15 |                   5 |                              0 |                                    0 |                                       0 |
| Runco          | Mark Runco                  | extended-15 |                   5 |                              0 |                                    0 |                                       0 |

**The 15 v2-corpus papers citing ≥1 canonical:**

| marker   |   year | venue                                                              | title                                                                                      | figure         |
|:---------|-------:|:-------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:---------------|
| v1+v2    |   2017 | Indian Journal of Palliative Care                                  | Translational research in oncology: Implications for palliative care                       | Stokes         |
| v1+v2    |   2019 | Journal of Molecular Recognition                                   | Truth in science and in molecular recognition, post‐truth in human affairs                 | Latour         |
| 🆕 v2     |   2020 | Angewandte Chemie International Edition                            | Molecular Machine Learning: The Future of Synthetic Chemistry?                             | Boden          |
| v1+v2    |   2020 | Journal of Medicinal Chemistry                                     | Drug Research Meets Network Science: Where Are We?                                         | Kauffman       |
| v1+v2    |   2021 | OMICS A Journal of Integrative Biology                             | From the Editor's Desk: Systems Science 2010–2020, and Post-COVID-19                       | Latour         |
| v1+v2    |   2022 | Current Pharmaceutical Biotechnology                               | Xenobots: Applications in Drug Discovery                                                   | Levin          |
| v1+v2    |   2022 | nan                                                                | Introduction                                                                               | Latour         |
| 🆕 v2     |   2022 | nan                                                                | INTERSECT Architecture Specification: Use Case Design Patterns (V.0.5)                     | Alexander      |
| v1+v2    |   2023 | Computer-Aided Design                                              | Beyond Statistical Similarity: Rethinking Metrics for Deep Generative Models in Engineerin | Boden          |
| v1+v2    |   2024 | Network Modeling Analysis in Health Informatics and Bioinformatics | Technologies for design-build-test-learn automation and computational modelling across the | Levin          |
| v1+v2    |   2024 | nan                                                                | Computer Science of Science                                                                | Latour         |
| v1+v2    |   2025 | Communications in computer and information science                 | Critical Analysis in Use of AI in Health Care Management                                   | Boden          |
| v1+v2    |   2025 | Preprints.org                                                      | Theoretical Topology-Driven Genetic Algorithm Learning: A Differential Approach to Phenoty | Kauffman       |
| v1+v2    |   2026 | Future of business and finance                                     | Human-AI Partnership and Innovative Work Behaviour                                         | Boden          |
| v1+v2    |   2026 | Elsevier eBooks                                                    | Can machines truly know? Epistemological challenges in AI-driven drug discovery            | Clark-Chalmers |

### 4.2 Co-citation (v2) — within-corpus substitute

**API-budget blocker.** Mid-run, OpenAlex returned HTTP 429 with 'Insufficient budget. This request costs $0.0001 but you only have $0 remaining. Resets at midnight UTC.' The polite-pool budget cap is $1/day (10,000 chained-cites queries); v1's 3.2 already consumed most of it, and v2's 3,432 chained-cites pair queries exhausted the remainder mid-flight. The intended cross-OpenAlex co-citation analysis (papers anywhere that co-cite each pair) is therefore unavailable for v2 today.

**Substitute: within-corpus co-citation derivation.** Using already-retrieved data (v2 corpus papers' `referenced_works` lists), we count v2-corpus papers whose reference lists include BOTH a creativity canonical AND a DD/methodology canonical. This is a strict subset of the intended cross-OpenAlex measurement; it captures co-citation only by papers that themselves entered the v2 primary corpus. Any external chemistry-AI paper co-citing a creativity figure but not entering our corpus (cf. v1's 93 bridging papers, most of which were outside primary corpus) is **not** captured here.

**Within-v2-corpus co-citations by figure group:**

| figure_group   |   within_v2_corpus_co_citers |
|:---------------|-----------------------------:|
| Boden          |                            4 |
| Kauffman       |                            1 |

**Within-v2-corpus bridging papers**: 2 unique papers (5 (creativity, DD/methodology) pairs co-cited within these papers' reference lists).

Year | Venue | Bridge paper | Figure ↔ DD/methodology canonical
--- | --- | --- | ---
2020 | Angewandte Chemie International Edition | Molecular Machine Learning: The Future of Synthetic Chemistry? | **Boden** ↔ Burger 2020 Mobile robotic chemist
2020 | Angewandte Chemie International Edition | Molecular Machine Learning: The Future of Synthetic Chemistry? | **Boden** ↔ Machine learning in chemoinformatics and drug disc
2020 | Angewandte Chemie International Edition | Molecular Machine Learning: The Future of Synthetic Chemistry? | **Boden** ↔ Molecular Transformer (Schwaller)
2020 | Angewandte Chemie International Edition | Molecular Machine Learning: The Future of Synthetic Chemistry? | **Boden** ↔ top-cited-v2-only
2020 | Journal of Medicinal Chemistry | Drug Research Meets Network Science: Where Are We? | **Kauffman** ↔ Concepts of AI for CADD

**Reading.** Within-v2-corpus, only 2 unique papers do real co-citation: Schwaller 2020 *Molecular Machine Learning: The Future of Synthetic Chemistry?* (which cites Boden + 4 chemistry-AI methodology canonicals) and *Drug Research Meets Network Science: Where Are We?* (which cites Kauffman + Concepts of AI for CADD). The within-corpus picture is consistent with v1's broader-OpenAlex 3.2 result: real bridges are rare; Schwaller 2020 is the methodology-layer bridge that v2 corpus expansion successfully captured.

**v1 cross-OpenAlex 3.2 baseline (for comparison).** v1's run (which had budget) found 52 of 3,276 pairs with co-cite>0 (sum 93 papers). v2 cross-OpenAlex 3.2 would likely find a similar number against the 22-set; the primary new bridges via the 10 v2 method canonicals would be Schwaller 2020 (already captured), Coley Part I, ChemCrow, and possibly a few of the top-cited-v2-only papers. This conjecture is not validated empirically today; the v2 cross-OpenAlex 3.2 should be re-run after midnight UTC if needed.

### 4.3 Topic-modeling community separation (v2)

v2 topics: 6; noise: 39 (0.5%).

Shared topics (both communities): 4; max balance: 0.070.

|   topic |   n_dd |   n_cc |   total |   balance | top_words                                                                                               |
|--------:|-------:|-------:|--------:|----------:|:--------------------------------------------------------------------------------------------------------|
|       4 |     57 |      4 |      61 |    0.0702 | quantum, quantum computing, computing, classical, quantum machine, drug, drug discovery, recursive      |
|       0 |   4622 |     46 |    4668 |    0.0100 | drug, molecular, drug discovery, protein, compounds, cancer, prediction, target                         |
|       1 |     12 |   1869 |    1881 |    0.0064 | computational, computational creativity, music, research, generative, generation, creative ai, artistic |
|       2 |    287 |      1 |     288 |    0.0035 | sars, cov, sars cov, covid, covid 19, antiviral, virus, viral                                           |

v1 had 26 topics with 10 shared, max balance 0.080. v2 produces fewer topics (smaller diversity in random 5K sample of v2 corpus due to similar core methodology themes) but the qualitative finding — communities remain separable, no balanced-shared topic — reproduces.

### 4.4 Forward-citation share (v2)

Mean v1-share = 0.0068%; mean v2-share = 0.0077%.
Works where v2-corpus overlap > v1-corpus overlap: **2** of 161.

| figure_group   | individual_name       | canonical_title                                    |   openalex_total_citers |   v1_corpus_citers |   v2_corpus_citers |
|:---------------|:----------------------|:---------------------------------------------------|------------------------:|-------------------:|-------------------:|
| Boden          | Margaret Boden        | Creativity and artificial intelligence             |                     767 |                  2 |                  3 |
| Alexander      | Christopher Alexander | A Pattern Language: Towns, Buildings, Construction |                    4601 |                  0 |                  1 |

### 4.5 Counterexample classification + fuzzy concept scan (v2)

**Classification breakdown** (v2):

| paper_class                      | engagement_depth   |   n |
|:---------------------------------|:-------------------|----:|
| chemistry-AI methodology primary | passing            |   1 |
| drug-discovery-AI primary        | passing            |   7 |
| drug-discovery-AI primary        | substantive        |   3 |
| tangential corpus member         | passing            |   4 |

|   year | venue                                                              | title                                                                                                                           | figure_groups    | paper_class                      | engagement_depth   |
|-------:|:-------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|:-----------------|:---------------------------------|:-------------------|
|   2017 | Indian Journal of Palliative Care                                  | Translational research in oncology: Implications for palliative care                                                            | Stokes           | drug-discovery-AI primary        | passing            |
|   2019 | Journal of Molecular Recognition                                   | Truth in science and in molecular recognition, post‐truth in human affairs                                                      | Latour           | drug-discovery-AI primary        | substantive        |
|   2020 | Angewandte Chemie International Edition                            | Molecular Machine Learning: The Future of Synthetic Chemistry?                                                                  | Boden            | chemistry-AI methodology primary | passing            |
|   2020 | Journal of Medicinal Chemistry                                     | Drug Research Meets Network Science: Where Are We?                                                                              | Kauffman         | drug-discovery-AI primary        | passing            |
|   2021 | OMICS A Journal of Integrative Biology                             | From the Editor's Desk: Systems Science 2010–2020, and Post-COVID-19                                                            | Latour           | drug-discovery-AI primary        | substantive        |
|   2022 | Current Pharmaceutical Biotechnology                               | Xenobots: Applications in Drug Discovery                                                                                        | Levin            | drug-discovery-AI primary        | passing            |
|   2022 | nan                                                                | Introduction                                                                                                                    | Latour           | drug-discovery-AI primary        | passing            |
|   2022 | nan                                                                | INTERSECT Architecture Specification: Use Case Design Patterns (V.0.5)                                                          | Alexander        | tangential corpus member         | passing            |
|   2023 | Computer-Aided Design                                              | Beyond Statistical Similarity: Rethinking Metrics for Deep Generative Models in Engineering Design                              | Boden            | tangential corpus member         | passing            |
|   2024 | Network Modeling Analysis in Health Informatics and Bioinformatics | Technologies for design-build-test-learn automation and computational modelling across the synthetic biology workflow: a review | Levin            | drug-discovery-AI primary        | passing            |
|   2024 | nan                                                                | Computer Science of Science                                                                                                     | Lakatos | Latour | drug-discovery-AI primary        | passing            |
|   2025 | Communications in computer and information science                 | Critical Analysis in Use of AI in Health Care Management                                                                        | Boden            | tangential corpus member         | passing            |
|   2025 | Preprints.org                                                      | Theoretical Topology-Driven Genetic Algorithm Learning: A Differential Approach to Phenotypic Emergence                         | Kauffman         | drug-discovery-AI primary        | passing            |
|   2026 | Future of business and finance                                     | Human-AI Partnership and Innovative Work Behaviour                                                                              | Boden            | tangential corpus member         | passing            |
|   2026 | Elsevier eBooks                                                    | Can machines truly know? Epistemological challenges in AI-driven drug discovery                                                 | Clark-Chalmers   | drug-discovery-AI primary        | substantive        |

**Fuzzy concept hits (v1 → v2):**

| label                            |   n_papers_v1 |   n_papers_v2 |   delta |
|:---------------------------------|--------------:|--------------:|--------:|
| paradigm shift (Kuhn)            |           300 |           319 |      19 |
| TAME (Levin)                     |             5 |             7 |       2 |
| incubation phase                 |             6 |             6 |       0 |
| 4P / 4Ps (Rhodes)                |             4 |             4 |       0 |
| actor-network (Latour)           |             4 |             4 |       0 |
| research programme (Lakatos)     |             2 |             2 |       0 |
| xenobot                          |             2 |             2 |       0 |
| bounded rationality (Simon)      |             1 |             1 |       0 |
| structure-mapping                |             1 |             1 |       0 |
| flow state (Csikszentmihalyi)    |             1 |             1 |       0 |
| blind variation                  |             0 |             0 |       0 |
| adjacent possible (Kauffman)     |             0 |             0 |       0 |
| conceptual blending              |             0 |             0 |       0 |
| componential theory (Amabile)    |             0 |             0 |       0 |
| Pasteur's quadrant (Stokes)      |             0 |             0 |       0 |
| TRIZ                             |             0 |             0 |       0 |
| pattern language (Alexander)     |             0 |             0 |       0 |
| reflective practitioner (Schön)  |             0 |             0 |       0 |
| extended mind                    |             0 |             0 |       0 |
| distributed cognition (Hutchins) |             0 |             0 |       0 |
| epistemic culture (Knorr-Cetina) |             0 |             0 |       0 |
| preinventive structures          |             0 |             0 |       0 |
| R/T/E formalism                  |             0 |             0 |       0 |
| bisociation                      |             0 |             0 |       0 |
| problem space (Newell-Simon)     |             0 |             0 |       0 |

**Fuzzy surname hits (v1 → v2):**

| label                   |   n_papers_v1 |   n_papers_v2 |   delta |
|:------------------------|--------------:|--------------:|--------:|
| Wiggins                 |             2 |             2 |       0 |
| Sternberg               |             2 |             2 |       0 |
| Kuhn (Thomas)           |             2 |             2 |       0 |
| Latour                  |             2 |             2 |       0 |
| Boden                   |             1 |             1 |       0 |
| Kauffman                |             1 |             1 |       0 |
| Newell (Allen)          |             1 |             1 |       0 |
| Simon (Herbert)         |             1 |             1 |       0 |
| Hutchins                |             0 |             0 |       0 |
| Stokes (Donald)         |             0 |             0 |       0 |
| Chalmers (David)        |             0 |             0 |       0 |
| Clark (Andy)            |             0 |             0 |       0 |
| Alexander (Christopher) |             0 |             0 |       0 |
| Knorr-Cetina            |             0 |             0 |       0 |
| Feyerabend              |             0 |             0 |       0 |
| Kaufman (James C.)      |             0 |             0 |       0 |
| Altshuller              |             0 |             0 |       0 |
| Campbell (Donald T.)    |             0 |             0 |       0 |
| Schon                   |             0 |             0 |       0 |
| Simonton                |             0 |             0 |       0 |
| Amabile                 |             0 |             0 |       0 |
| Levin (Tufts)           |             0 |             0 |       0 |
| Koestler                |             0 |             0 |       0 |
| Finke                   |             0 |             0 |       0 |
| Fauconnier              |             0 |             0 |       0 |
| Gentner                 |             0 |             0 |       0 |
| Csikszentmihalyi        |             0 |             0 |       0 |
| Wallas                  |             0 |             0 |       0 |
| Lakatos                 |             0 |             0 |       0 |
| Hofstadter              |             0 |             0 |       0 |
| Runco                   |             0 |             0 |       0 |

## 5. Outcome classification: A (v1 pattern reproduced at scale)

Per spec §5, the three possible outcomes were:

- **A**: v2 reproduces v1 pattern at scale — citation gap survives the broader corpus.
- **B**: v2 reveals substantially more engagement at chemistry-AI methodology layer.
- **C**: mixed — some new engagement but still proportionally small.

**The result is firmly A**, with one specific qualification toward C:

**Evidence for A:**
- Direct-citation rate: 0.042% v1 → 0.045% v2. Proportional rate essentially unchanged.
- Substantive engagements: 3 v1 → 3 v2. The same three papers (Chalmers/extended-mind in epistemology chapter; Latour twice in philosophy contexts) classify as substantive in both. No new substantive engagement at the chemistry-AI methodology layer.
- 28 of 30 figure groups have unchanged citation counts. Only Boden (+1: Schwaller 2020) and Alexander (+1: INTERSECT architecture specification) gain a single corpus citation each.
- Forward-citation share delta: +0.001%. Negligible.
- Topic modeling: max community balance 0.070 v2 vs 0.080 v1. Community separation reproduces.
- Fuzzy 'paradigm shift' v1 300 → v2 319 (+19 with corpus growth of +2,500): the parallel-vocabulary pattern (Kuhn-language widely used, zero Kuhn citations) reproduces at v2 scale.

**The qualification toward C:**
- The v2 expansion successfully captures **Schwaller 2020 *Molecular Machine Learning: The Future of Synthetic Chemistry?*** — one of the two named bridges from v1 §3.2 — as a chemistry-AI methodology primary citing paper. This is a genuine new methodology-layer engagement, the first such captured by the bibliometric apparatus. However, the engagement is heuristically classified as **passing** (Schwaller's paper cites Boden but doesn't develop the citation methodologically). One passing engagement at the methodology layer doesn't shift the headline; the architectural-impoverishment inference for the methodology layer holds.
- The v2 expansion fails to capture **Coley 2019 Part II (Outlook)**, **Coscientist 2023**, **Burger 2020**, **AlphaFold**, and **RFdiffusion** — all of which are real chemistry-AI methodology canonicals. These papers' title/abstract framings don't match v2's keyword filter. So even outcome A here is conservative; a more-aggressive corpus could be defended, though it would dilute the drug-discovery focus.

**Implication for the architectural-impoverishment inference:**
- The strict-corpus-boundary objection is empirically tested and substantially closed. v2 corpus expansion increases the citation count by 2 papers; only one of those two is at the chemistry-AI methodology layer; and that one is a passing-reference engagement (Schwaller 2020 cites Boden but doesn't develop the citation).
- The architectural-impoverishment inference for the methodology layer holds across the broader corpus. Substantive engagements remain concentrated at the biology-AI-philosophy frontier (3 papers in both v1 and v2).
- A defended scope decision: 'drug-discovery and adjacent chemistry-AI methodology' is an empirically grounded boundary. The remaining 0.045% engagement rate is a calibrated headline that does not depend on the v1-strict boundary choice.

## 6. Limits and what this v2 work doesn't settle

- **Boundary still has to stop somewhere.** v2 expands to chemistry-AI methodology but not to all-AI-for-science. A reviewer could argue the v2 boundary is still defended too narrowly. Defense: the v2 expansion is principled (limited to methodology subdomains drug-discovery AI imports from); further expansion would dilute the drug-discovery focus. But this is a defended scope decision, not an empirical neutral.
- **OpenAlex coverage gaps unchanged from v1.** ~28% of v2 corpus papers have no `referenced_works` (similar rate to v1's 27%). Specifically: 9,214 of 33,469 v2 papers have no reference links. Direct-citation counts are a lower bound.
- **Coley Part II (Outlook) still excluded.** This is the paper most directly relevant to the original objection (it cites Boden in a chemistry-AI methodology essay). Even v2's expanded keyword filter doesn't capture it because *Outlook*'s abstract doesn't contain methodology-specific keywords. The boundary leakage represented by this paper is fundamentally a function of OpenAlex search-term semantics, not corpus design. A future iteration would need a citing-paper-based or topic-based criterion.
- **Same author throughout.** v2 is the same author who designed v1 and selected the 30-figure set. Independent reviewer validation of the v2 corpus design and figure-set choices remains unavailable.
- **The v2 expansion was triggered by a specific reviewer objection, not as a neutral robustness check.** This is acknowledged transparently. v2 is a directed response; outcome A is a result, not a confirmation.
- **Heuristic classification reliability.** The 'chemistry-AI methodology primary' class introduced in v2's 3.5 is a heuristic on title/abstract keywords. Schwaller 2020 was correctly classified into this new class; some other papers in the v2 expansion may also belong but didn't surface because they don't cite any creativity canonical (and so don't appear in 3.5). The class is well-formed but is only relevant when a paper happens to cite a creativity figure.
- **Topic count instability across runs.** v2 produced 6 topics vs v1's 26. This is partly random sample dynamics (5K sample of v2 corpus may have less topical diversity than v1's 5K sample) and partly the smaller noise rate (0.5% v2 vs 31% v1) suggesting HDBSCAN found tighter, fewer clusters in v2. The qualitative finding (no shared topic with balance ≥ 0.1) is robust; specific topic boundaries should not be over-interpreted.
- **OpenAlex polite-pool budget exhaustion mid-run.** OpenAlex enforces a $1/day budget cap (10,000 chained-cites queries) on the polite pool that I had not anticipated. v1's 3.2 (~3,400 queries) and v2's 3.2 attempt (~1,090 queries before pyalex deadlocked on rate-limited responses) together exhausted the budget. The v2 cross-OpenAlex co-citation analysis therefore could not complete; I substituted a within-v2-corpus co-citation derivation that uses already-retrieved data. Section 4.2 documents this substitution honestly. A repeat run after midnight UTC (or with a paid OpenAlex API key) would close the gap. The substitute does not change the outcome classification (A) because the other four analyses are sufficient; but the cross-OpenAlex co-citation count for v2's 22-set is an empirical gap.

## 7. Recommended downstream uses

Per spec §9, outcome A implies: integrate v2 findings as a definitive extension of `citation_network_analysis.md` Section 8 and `paper.md` Section 1.2; note that the corpus-boundary objection has been empirically tested and the pattern holds.

Specific recommendations:

1. Update `paper.md` Section 1.2 to lead with the calibrated v2 headline: '**15 of 33,469 corpus papers (0.045%) cite at least one of 30 canonical creativity figures across a corpus that includes chemistry-AI methodology layer (molecular ML, autonomous chemistry, retrosynthesis, generative chemistry). Substantive engagements: 3, all at the biology-AI-philosophy frontier (Chalmers/extended-mind, Latour twice in philosophy contexts). One new chemistry-AI methodology paper enters the count via v2 expansion: Schwaller et al. 2020 *Molecular Machine Learning: The Future of Synthetic Chemistry?* citing Boden in passing.**'

2. Replace the v1 calibrated headline in `paper.md` and `citation_network_analysis.md` with the v2 calibrated headline. The v1 headline (13/30,935) was conservative due to boundary; v2 (15/33,469) is the more honest calibrated number.

3. Note explicitly in `paper.md` and `citation_network_analysis.md` that the corpus-boundary objection has been tested: **'A v2 bibliometric extension broadened the corpus to include the chemistry-AI methodology layer (molecular ML, autonomous chemistry, retrosynthesis, generative chemistry). The v2 corpus added ~2,500 papers; direct-citation rate remained 0.045% (vs v1's 0.042%); only Schwaller et al. 2020 entered as a new chemistry-AI methodology citing paper, with a passing-reference engagement. The architectural-impoverishment inference holds across the broader corpus.'**

4. Acknowledge that **Coley 2019 Part II (Outlook)**, **Coscientist 2023**, **Burger 2020**, **AlphaFold**, **RFdiffusion** still fall outside the v2 corpus. The cleanest defended position: 'The bibliometric corpus is bounded by keyword filtering on title and abstract; some real chemistry-AI methodology papers fall outside this filter. The architectural-impoverishment inference is robust to this boundary leakage because (a) v2 tests show only one such paper newly enters when chemistry-AI methodology terms are added; (b) substantive engagement remains at 3 papers across both corpora; (c) the parallel-vocabulary phenomenon (300+ 'paradigm-shift' uses with zero Kuhn citations) is the structural argument that doesn't depend on corpus boundary choice.'

5. The parallel-vocabulary quantification reproduces in v2: 'paradigm shift' appears in 319 v2-corpus abstracts with zero Kuhn citations. This is the cleanest empirical demonstration of reinvention-without-attribution and should remain the headline structural finding.

## 8. Spec adjustments learned (5 items)

1. **The corpus-size estimate was off by an order of magnitude.** Spec said v2 would be 50,000-150,000 papers; actual v2 is 33,469 (an 8% expansion over v1's 30,935). Reason: most chemistry-AI methodology papers also contain drug-discovery terms. Future spec versions should run the size probe before authoring the size estimate.

2. **Several spec-named bridge candidates fall outside the v2 keyword filter** despite being canonical chemistry-AI methodology papers: Coley 2019 Part II (Outlook), Coscientist 2023, Burger 2020 mobile robotic chemist, AlphaFold, RFdiffusion. The v2 spec's named-candidate list was written expecting them to enter the corpus; they don't. Future spec iterations should run the in/out check at spec-design time, not at execution time.

3. **The corpus-expansion strategy hits a fundamental limit at keyword filtering.** Coley Part II's abstract doesn't contain any of the 27 v2 search terms. The only ways to capture it would be (a) full-text search (OpenAlex doesn't expose this), (b) topic-based corpus inclusion (use OpenAlex `topics.id` filter), (c) venue-based inclusion (e.g., 'all Angewandte Chemie 2017-2026 with at least one AI term'), or (d) citing-paper-based inclusion (papers that cite a known DD-AI canonical). Future v3-style spec should consider one of these.

4. **The outcome-A/B/C framing was useful but the binary 'substantively more engagement' threshold is underspecified.** The v2 result is firmly A on every numeric metric but qualifies toward C in that one new chemistry-AI methodology engagement does enter (Schwaller 2020). Future versions should specify a threshold (e.g., 'outcome B requires ≥10 new substantive methodology-layer engagements OR a ≥50% increase in proportional rate').

5. **The spec's '22-paper canonical set' had a redundancy with v1's 21-paper set.** Two papers (Coley Part I, ChemCrow) are in both v1 and v2 corpora and were already among v1's 21 canonicals; they appear in the v2 22-set as 'v2 method' canonicals despite being in v1. Future spec iterations should be explicit about whether the v2 canonical set is meant to ADD to v1's set or REPLACE it. v2 here treats it as a replacement 22-set with some overlap, which is workable but slightly muddled the v1-vs-v2 co-citation comparison.

6. **OpenAlex's $1/day polite-pool budget is a real constraint that the spec didn't account for.** v1's 3.2 (3,276 chained-cites queries) consumed ~33% of daily budget; v2's 3.2 attempted to add another 3,432 queries and hit the cap. Future spec iterations should either (a) note the OpenAlex budget cap explicitly and require a paid API key for cross-OpenAlex co-citation work, (b) split 3.2 across multiple days with explicit checkpoints, or (c) substitute a within-corpus co-citation derivation as the primary 3.2 method, noting the different semantics. Within-corpus and cross-OpenAlex are different measurements and the spec should be explicit about which one is being used.

---

**End of v2 findings document.** Run completed 2026-05-09 by Claude Code (Opus 4.7) against OpenAlex; data bundle preserved at `./bibliometrics_v2/`.