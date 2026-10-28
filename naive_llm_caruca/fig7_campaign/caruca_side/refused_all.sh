#!/usr/bin/env bash
# Run refused_share.py for every Fig. 7 command in the caruca VM (task 019, 3.3 c, e). Skips commands whose
# refused/<cmd>.json exists. `kill` runs in its own user and process namespace with the script as its process 1:
# v1 generates `kill - HUP -1`, and -1 means every process the user owns (the tracer, the shell, the VM session);
# kill -1 never signals process 1 and cannot leave the namespace. A watchdog there resumes processes that
# `kill -s STOP 0` stops (refused_share.py, KILL_WATCHDOG).
#   ./refused_all.sh            (from the Mac; runs in the background-safe way, one command at a time)
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$HERE/refused"
for c in $(grep -v '^#' "$HERE/../commands.txt" | cut -f1); do
  [ -s "$HERE/refused/$c.json" ] && { echo "skip $c"; continue; }
  W=""; [ "$c" = kill ] && W="unshare --user --map-root-user --pid --fork --mount-proc env KILL_WATCHDOG=1"
  echo "== $c $(date +%H:%M:%S)"
  limactl shell caruca -- bash -lc "cd \$(mktemp -d) && timeout 3600 $W ~/caruca-venv/bin/python -I '$HERE/refused_share.py' '$c' '$HERE/refused/$c.json' 2>&1 | grep -v 'it/s\|%|' | tail -1"
done
echo "done $(date +%H:%M:%S)"
