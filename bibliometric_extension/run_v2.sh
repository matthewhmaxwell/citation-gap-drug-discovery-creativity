#!/usr/bin/env bash
# v2 end-to-end runner. Each step writes to raw/, processed/, or outputs/.
# Re-running an individual step doesn't require re-running all of them.

set -euo pipefail
cd "$(dirname "$0")"

PY=".venv/bin/python"
mkdir -p raw processed outputs

step="${1:-all}"

run_step1() { echo "==> Step 1: probe v2 corpus size"; $PY -m scripts.probe_corpus_v2 2>&1 | tee outputs/probe_corpus_v2.log; }
run_step2() { echo "==> Step 2: retrieve v2 corpus";  $PY -m scripts.retrieve_v2_corpus 2>&1 | tee outputs/retrieve_v2_corpus.log; }
run_step3() { echo "==> Step 3: confirm Coley/Schwaller status"; $PY -m scripts.check_coley_schwaller 2>&1 | tee outputs/check_coley_schwaller.log; }
run_step4() { echo "==> Step 4: pick v2 canonical set"; $PY -m scripts.pick_v2_canonicals 2>&1 | tee outputs/pick_v2_canonicals.log; }
run_step5() {
    echo "==> Step 5: 3.1 direct citation"; $PY -m scripts.analysis_3_1_v2 2>&1 | tee outputs/analysis_3_1_v2.log
    echo "==> Step 5: 3.2 co-citation (cross-OpenAlex; needs budget)"; $PY -m scripts.analysis_3_2_v2 2>&1 | tee outputs/analysis_3_2_v2.log || echo "WARN: 3.2 cross-OpenAlex hit budget cap; falling back to within-corpus"
    echo "==> Step 5: 3.2 within-corpus substitute"; $PY -m scripts.analysis_3_2_v2_within_corpus 2>&1 | tee outputs/analysis_3_2_v2_within_corpus.log
    echo "==> Step 5: 3.4 forward citation"; $PY -m scripts.analysis_3_4_v2 2>&1 | tee outputs/analysis_3_4_v2.log
    echo "==> Step 5: 3.5 counterexample + fuzzy"; $PY -m scripts.analysis_3_5_v2 2>&1 | tee outputs/analysis_3_5_v2.log
    echo "==> Step 5: 3.3 topic modeling"; $PY -m scripts.analysis_3_3_v2 2>&1 | tee outputs/analysis_3_3_v2.log
}
run_step6() {
    echo "==> Step 6: build v1 vs v2 comparison + render findings"
    $PY -m scripts.build_comparison_table 2>&1 | tee outputs/build_comparison_table.log
    $PY -m scripts.render_findings_v2 2>&1 | tee outputs/render_findings_v2.log
}

case "$step" in
    all)        run_step1; run_step2; run_step3; run_step4; run_step5; run_step6 ;;
    step1)      run_step1 ;;
    step2)      run_step2 ;;
    step3)      run_step3 ;;
    step4)      run_step4 ;;
    step5)      run_step5 ;;
    step6)      run_step6 ;;
    *) echo "unknown: $step"; exit 1 ;;
esac

echo "Done. See bibliometric_findings_v2.md."
