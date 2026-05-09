#!/usr/bin/env bash
# End-to-end runner. Each step writes to raw/, processed/, or outputs/.
# Re-running an individual step doesn't require re-running all of them.
#
# Usage:  ./run_full_analysis.sh              (runs all)
#         ./run_full_analysis.sh from_step3   (skips canonical-papers build)

set -euo pipefail
cd "$(dirname "$0")"

PY=".venv/bin/python"
mkdir -p raw processed outputs

step="${1:-all}"

run_step1() {
    echo "==> Step 1: build canonical papers list"
    $PY -m scripts.build_canonical_papers   2>&1 | tee outputs/build_canonical_papers.log
    $PY -m scripts.fix_canonical_papers     2>&1 | tee outputs/fix_canonical_papers.log
    $PY -m scripts.fix_canonical_papers_v2  2>&1 | tee outputs/fix_canonical_papers_v2.log
    $PY -m scripts.fix_canonical_papers_v3  2>&1 | tee outputs/fix_canonical_papers_v3.log
}

run_step2() {
    echo "==> Step 2: probe + retrieve primary corpus"
    $PY -m scripts.probe_corpus_size        2>&1 | tee outputs/probe_corpus_size.log
    $PY -m scripts.retrieve_primary_corpus  2>&1 | tee outputs/retrieve_primary_corpus.log
    $PY -m scripts.pick_dd_canonicals       2>&1 | tee outputs/pick_dd_canonicals.log
}

run_step3() {
    echo "==> Step 3: tertiary computational-creativity corpus"
    $PY -m scripts.retrieve_cc_corpus       2>&1 | tee outputs/retrieve_cc_corpus.log
}

run_step4() {
    echo "==> Step 4: 3.1 direct citation"
    $PY -m scripts.analysis_3_1_direct_citation  2>&1 | tee outputs/analysis_3_1.log
    echo "==> Step 4: 3.2 co-citation (long ~15 min)"
    $PY -m scripts.analysis_3_2_co_citation     2>&1 | tee outputs/analysis_3_2.log
    echo "==> Step 4: 3.4 forward citation"
    $PY -m scripts.analysis_3_4_forward_citation 2>&1 | tee outputs/analysis_3_4.log
    echo "==> Step 4: 3.5 counterexample search"
    $PY -m scripts.analysis_3_5_counterexample   2>&1 | tee outputs/analysis_3_5.log
    echo "==> Step 4: 3.3 topic modeling"
    $PY -m scripts.analysis_3_3_topic_modeling   2>&1 | tee outputs/analysis_3_3.log
}

case "$step" in
    all)         run_step1; run_step2; run_step3; run_step4 ;;
    step1)       run_step1 ;;
    step2)       run_step2 ;;
    step3)       run_step3 ;;
    step4)       run_step4 ;;
    from_step3)  run_step3; run_step4 ;;
    from_step4)  run_step4 ;;
    *) echo "unknown step: $step"; exit 1 ;;
esac

echo "Done. See bibliometric_findings.md for the writeup."
