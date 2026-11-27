#!/bin/bash
# Runs on the Mac: copies the records of the larger-input run out of the VM into this folder.
dest="$(cd "$(dirname "$0")" && pwd)"
for f in results.jsonl regions.jsonl occurrences.jsonl run_windows.jsonl batch_errors.jsonl batch_progress.txt scale.jsonl commands.jsonl; do
  limactl copy "pash:/home/tirandagan.guest/t024/out_large/$f" "$dest/$f" 2>/dev/null
done
echo "copied: $(wc -l < "$dest/batch_progress.txt" 2>/dev/null) scripts done"
