#!/bin/bash
# Runs in the pash VM (copied to ~/t024/rerun/batch.sh). The rerun's whole batch: 86 scripts, bash first in
# every repeat, one instrumented pass and three timed repeats. No folder-decides controls (the first run's
# controls on spell stand; brief_caruca_expanded_rerun.md asks for none).
R=/Users/tirandagan/dev/stevens/caruca_v2/naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/run_koala_caruca_all.py
cd ~/t024/rerun
python3 $R batch --no-controls --phase main --repeats 3 \
  --sets bash pash-own caruca-pash-all caruca-main-all pash-own-copy --script $(cat ids.txt)
