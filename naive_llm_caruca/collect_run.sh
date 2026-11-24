#!/usr/bin/env bash
# Copy every run folder out of a clone into this package's runs/ and delete the clone.
#   ./collect_run.sh <vm-name> [--keep]        --keep: do not delete the clone
# Each run in the VM (~/runs/<date>_<time>_<vm>_<command>_<version>/) lands here as runs/<same name>/,
# with environment.txt added. The clone's complete Claude Code session store is also saved once, as
# runs/<date>_<time>_<vm>_claude-sessions/, in case a session was started outside naive-run.
# runs/ is never copied into a VM (sync_to_vm.sh stages only the prompts, formats/ and samples/).
# Key scan (task 019): runs billed through OpenRouter had the key in the session's environment, and run
# folders are committed to a public repository. Every collected file is searched for the key in the repo's
# .env (OPENROUTER_API_KEY); any hit is replaced by [REDACTED-OPENROUTER-KEY] before the folder is moved
# into runs/, and listed in that folder's KEY_REDACTED.txt. Since 2026-11-24 the requesty.ai key
# (REQUESTY_API_KEY) is scanned for the same way, redacted as [REDACTED-REQUESTY-KEY].
set -euo pipefail
NAME="${1:?usage: collect_run.sh <vm-name> [--keep]}"
KEEP="${2:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
limactl list -q | grep -qx "$NAME" || { echo "error: no VM named $NAME" >&2; exit 1; }
[ "$(limactl list "$NAME" --format '{{.Status}}')" = "Running" ] || limactl start "$NAME" --tty=false
ENV="$(limactl shell "$NAME" -- bash -lc 'claude --version; lsb_release -ds; uname -m; claude auth status 2>/dev/null | grep -E "subscriptionType|authMethod"' 2>/dev/null || true)"
RUNS="$(limactl shell "$NAME" -- bash -lc 'ls -1 ~/runs 2>/dev/null' 2>/dev/null | tr -d '\r' || true)"
scrub() {   # scrub <folder>: redact both keys in every file under it, list the files in KEY_REDACTED.txt
  scrub_one "$1" OPENROUTER_API_KEY OPENROUTER; scrub_one "$1" REQUESTY_API_KEY REQUESTY
}
scrub_one() {   # scrub_one <folder> <.env variable> <label>
  local KEY; KEY="$(sed -n "s/^$2=//p" "$HERE/../.env" 2>/dev/null | tr -d "\"' \r")"
  [ -n "$KEY" ] && [ "$KEY" != REPLACE_ME ] || return 0
  local hits; hits="$(grep -rlF -- "$KEY" "$1" 2>/dev/null || true)"
  [ -z "$hits" ] && return 0
  printf '%s\n' "$hits" | while read -r F; do
    python3 -c 'import sys; p,k=sys.argv[1],sys.argv[2]; b=open(p,"rb").read(); open(p,"wb").write(b.replace(k.encode(), ("[REDACTED-"+sys.argv[3]+"-KEY]").encode()))' "$F" "$KEY" "$3"
  done
  printf '%s\n' "$hits" | sed "s|$1/||" >> "$1/KEY_REDACTED.txt"
  echo "WARNING: the $3 key appeared in $(printf '%s\n' "$hits" | wc -l | tr -d ' ') file(s) of $(basename "$1"); redacted (KEY_REDACTED.txt)" >&2
}
if [ -z "$RUNS" ]; then echo "(no runs in $NAME)"; else
  for R in $RUNS; do
    if [ -e "$HERE/runs/$R" ]; then echo "skip: runs/$R already collected"; continue; fi
    STAGE="$(mktemp -d)"
    limactl copy -r "$NAME:~/runs/$R" "$STAGE/$R"
    scrub "$STAGE/$R"
    mv "$STAGE/$R" "$HERE/runs/$R"; rmdir "$STAGE"
    printf '%s\n' "$ENV" > "$HERE/runs/$R/environment.txt"
    echo "collected runs/$R:"; find "$HERE/runs/$R" -type f | sort | sed "s|$HERE/||"
  done
fi
# Sessions not started by naive-run (e.g. the sign-in session, or a bare `claude` from the home
# folder) are not in any run folder. Save only those, as runs/<stamp>_<vm>_other-sessions/.
T="$(mktemp -d)"
if limactl copy -r "$NAME:~/.claude/projects" "$T/projects" 2>/dev/null; then
  O="$HERE/runs/$(date +%Y-%m-%d_%H%M%S)_${NAME}_other-sessions"
  find "$T/projects" -name '*.jsonl' | while read -r F; do
    ID="$(basename "$F" .jsonl)"
    if ls "$HERE"/runs/*/transcript_"$ID".jsonl >/dev/null 2>&1; then continue; fi
    SLUG="$(basename "$(dirname "$F")")"; mkdir -p "$O/$SLUG"; cp "$F" "$O/$SLUG/"
  done
  if [ -d "$O" ]; then scrub "$O"; echo "saved sessions not captured by any run as runs/$(basename "$O"):"; find "$O" -type f | sed "s|$HERE/||"; fi
fi
rm -rf "$T"
if [ "$KEEP" = "--keep" ]; then echo "keeping clone $NAME"; else echo "== deleting clone $NAME"; limactl delete -f "$NAME"; fi
