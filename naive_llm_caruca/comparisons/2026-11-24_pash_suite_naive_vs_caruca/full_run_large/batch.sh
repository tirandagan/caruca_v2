#!/bin/bash
# Runs in the pash VM (copied to ~/t024/large/batch.sh). One group of the larger-input run:
#   bash batch.sh A|B [extra sets...]
# bash first in every repeat, one instrumented pass and three timed repeats, each script's input scaled
# by its k from scale.jsonl (pilot). No folder-decides controls (the plan asks for none).
R=/Users/tirandagan/dev/stevens/caruca_v2/naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/run_koala_large.py
g=$1; shift
cd ~/t024/large
python3 $R batch --no-controls --phase group$g --repeats 3 \
  --sets bash pash-own naive-sed2 caruca-pash-all pash-own-copy "$@" \
  --script $(cat ids_group_$(echo $g | tr AB ab).txt)
