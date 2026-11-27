#!/usr/bin/env bash
# Converts more of Caruca's commands into PaSh's current Python annotation format, one command at a time,
# by calling Caruca's own run_pash_py.sh (branch pash-python-annotations) inside the Lima VM "caruca".
# A failing command is logged and skipped; the rest continue.
#   trace_batch.sh VM LANE GRAMMAR MAX_COUNT CMD...   (one lane per VM, so each trace has 8 cores as the first eight did)
vm=$1 lane=$2 grammar=$3 maxc=$4; shift 4
here=$(cd "$(dirname "$0")" && pwd)
log=$here/logs/$lane.log
status=$here/logs/status.tsv
for cmd in "$@"; do
  start=$(date +%s)
  echo "$(date '+%F %T') START $cmd $grammar max-count $maxc" | tee -a "$log"
  if limactl shell "$vm" bash -lc "cd /Users/tirandagan/dev/stevens/caruca/caruca && source .venv-linux/bin/activate && ./run_pash_py.sh --grammar $grammar --max-count $maxc $cmd" >> "$log" 2>&1; then
    res=ok
  else
    res="failed($?)"
  fi
  end=$(date +%s)
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$(date '+%F %T')" "$lane" "$cmd" "$grammar" "$res" "$((end-start))" >> "$status"
  echo "$(date '+%F %T') END $cmd $grammar: $res in $((end-start)) s" | tee -a "$log"
done
echo "$(date '+%F %T') LANE $lane DONE" | tee -a "$log"
