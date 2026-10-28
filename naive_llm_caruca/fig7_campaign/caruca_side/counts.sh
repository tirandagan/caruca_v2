#!/usr/bin/env bash
# Caruca's test-run counts (task 019, 3.3 b): command lines and traced test runs v1 would make at up to 1, 2
# and 4 options per line, from v1's curated syntax files, with v1's defaults. Uses config_count.py from the
# 2026-10-26 comparison. Output: counts.tsv (command, k, lines, configurations).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PY=~/dev/stevens/caruca/caruca/.venv/bin/python
CC="$HERE/../../comparisons/2026-10-26_syntax_files_vs_v1/scripts/config_count.py"
echo -e "command\tk\tcommand_lines\ttraced_configurations" > "$HERE/counts.tsv"
for c in $(grep -v '^#' "$HERE/../commands.txt" | cut -f1); do
  $PY -I "$CC" caruca.syntax_specs "$c" 1 2 4 2>"$HERE/counts.err.$c" \
    | sed -E "s/^caruca.syntax_specs ([^ ]+) k=([0-9]+): command lines ([0-9,]+)  traced configurations ([0-9,]+)/\1\t\2\t\3\t\4/" | tr -d ',' >> "$HERE/counts.tsv" \
    && rm -f "$HERE/counts.err.$c"
done
