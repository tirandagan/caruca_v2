#!/usr/bin/env bash
# Make a fresh run VM: clone naive-golden, start it, copy the package in fresh from this folder,
# install the in-VM helper and the welcome message. One clone per run.
#
#   ./new_run_vm.sh <name>            e.g. ./new_run_vm.sh naive-run-sed-v2
#   GOLDEN=other-image ./new_run_vm.sh <name>
set -euo pipefail
NAME="${1:?usage: new_run_vm.sh <new-vm-name>}"
GOLDEN="${GOLDEN:-naive-golden}"
HERE="$(cd "$(dirname "$0")" && pwd)"

if limactl list -q | grep -qx "$NAME"; then echo "error: a VM named $NAME already exists" >&2; exit 1; fi
limactl list -q | grep -qx "$GOLDEN" || { echo "error: golden image $GOLDEN does not exist; see README 'Building the golden image'" >&2; exit 1; }
if [ "$(limactl list "$GOLDEN" --format '{{.Status}}')" = "Running" ]; then
  echo "== stopping $GOLDEN (clone needs it stopped)"; limactl stop "$GOLDEN"
fi

echo "== cloning $GOLDEN -> $NAME"
limactl clone "$GOLDEN" "$NAME" --tty=false
echo "== starting $NAME"
limactl start "$NAME" --tty=false

echo "== copying the package fresh from $HERE"
"$HERE/sync_to_vm.sh" "$NAME"

echo "== installing helper and welcome"
limactl copy "$HERE/vm/naive-run" "$NAME:/tmp/naive-run"
limactl copy "$HERE/vm/naive-watch.py" "$NAME:/tmp/naive-watch.py"
limactl copy "$HERE/vm/exec-log.bt" "$NAME:/tmp/exec-log.bt"
limactl copy "$HERE/vm/bashrc-welcome.sh" "$NAME:/tmp/bashrc-welcome.sh"
limactl shell "$NAME" -- bash -lc '
  set -e
  mkdir -p ~/bin && mv /tmp/naive-run ~/bin/naive-run && mv /tmp/naive-watch.py ~/bin/naive-watch.py && mv /tmp/exec-log.bt ~/bin/exec-log.bt && chmod +x ~/bin/naive-run ~/bin/naive-watch.py
  grep -q "naive-arm welcome" ~/.bashrc || cat /tmp/bashrc-welcome.sh >> ~/.bashrc
  rm -f /tmp/bashrc-welcome.sh
  rm -rf ~/naive-arm/output/* ~/naive-arm/runs ~/runs/*
  # start with no session history: whatever ~/.claude/projects holds at collection time is from this clone
  rm -rf ~/.claude/projects/*
  echo "claude: $(claude --version)"
  claude auth status 2>/dev/null | grep -q "\"loggedIn\": true" && echo "signed in: yes" || echo "signed in: NO — sign in to the golden image first (README: Sign in once), or run claude and /login in this clone"
  ls ~/.claude/CLAUDE.md 2>/dev/null && echo "WARNING: global CLAUDE.md present" || echo "global CLAUDE.md: none"
'
echo
echo "== ready. Enter with:   limactl shell $NAME"
