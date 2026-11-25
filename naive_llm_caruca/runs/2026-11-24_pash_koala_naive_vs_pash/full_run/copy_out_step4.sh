#!/bin/bash
# Runs on the Mac. After each script the batch finishes (batch_progress.txt grows), copies the records
# out of the VM into this folder. Ends when the batch prints STEP4 DONE.
dest="$(cd "$(dirname "$0")" && pwd)"
seen=0
while true; do
  n=$(limactl shell pash -- bash -lc 'wc -l < ~/t024/out/batch_progress.txt 2>/dev/null || echo 0' 2>/dev/null | tr -dc 0-9)
  n=${n:-0}
  if [ "$n" -gt "$seen" ]; then
    for f in results.jsonl run_windows.jsonl batch_errors.jsonl batch_progress.txt; do
      limactl copy "pash:/home/tirandagan.guest/t024/out/$f" "$dest/step4_$f" 2>/dev/null
    done
    last=$(tail -1 "$dest/step4_batch_progress.txt")
    echo "copied after $n scripts (last: $last)"
    seen=$n
  fi
  if limactl shell pash -- bash -lc 'grep -q "STEP4 DONE" ~/t024/full/step4.log' 2>/dev/null; then
    for f in results.jsonl run_windows.jsonl batch_errors.jsonl batch_progress.txt; do
      limactl copy "pash:/home/tirandagan.guest/t024/out/$f" "$dest/step4_$f" 2>/dev/null
    done
    echo "STEP4 DONE: $(wc -l < "$dest/step4_batch_progress.txt") scripts copied"; break
  fi
  if ! limactl shell pash -- bash -lc 'pgrep -f "[s]tep4.sh" >/dev/null' 2>/dev/null; then
    echo "batch process not running (after $n scripts)"; break
  fi
  sleep 20
done
