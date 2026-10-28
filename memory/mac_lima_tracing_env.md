---
name: mac-lima-tracing-env
description: The Mac now CAN run v1's trace phase — Lima VM "caruca" (Ubuntu 24.04) set up 2026-09-03; full ls pipeline verified end to end
metadata:
  type: project
---

As of 2026-09-03 the Mac has a working v1 tracing environment, so "trace on a
provisioned host, analyze locally" no longer forces a CloudLab/remote box when
working from the Mac (the WSL PC still cannot trace — see [[dev-machine-paths]]).

- Lima VM named `caruca`: Ubuntu 24.04, 8 vCPU / 8 GiB / 30 GiB, created with
  `--mount-writable`, so the Mac home dir (and the v1 repo at
  `~/dev/stevens/caruca`) is read-write inside the VM at the same path.
  Enter with `limactl shell caruca`.
- Linux venv at `~/caruca-venv` **inside the VM** (VM-local disk, editable
  install of v1). The repo's `.venv`/`.venv-llm` are Darwin-only.
- **The guest home is NOT the mounted Mac home.** Inside the VM, `$HOME` is
  `/home/tirandagan.guest`; the Mac home is mounted separately at its own
  `/Users/tirandagan` path. So `~/caruca-venv` is guest-local while the v1
  checkout is read through the shared mount. Consequence when scripting from
  the Mac: `limactl shell caruca -- test -x "$HOME/caruca-venv/bin/caruca"`
  **falsely reports missing**, because the outer shell expands `$HOME` to
  `/Users/tirandagan` before Lima ever sees it. Quote the tilde or wrap in
  `bash -lc` so expansion happens guest-side. Verified 2026-09-08.
- Critical fix applied and persisted (`/etc/sysctl.d/99-caruca-userns.conf`):
  `kernel.apparmor_restrict_unprivileged_userns=0`. Without it every traced
  invocation fails silently (rc=1, zero traces, stderr `unshare: write failed
  /proc/self/uid_map`).
- Verified end to end for `ls`: trace → `outputs/ls.json` (682 configs, 594
  rc==0, 17,512 strace events), annotate → `save/ls.json`. The fresh annotation
  differs from the committed one (4 cases vs 6; some `stateless` → `non-pure`),
  consistent with v1's recent "fix parallelizability class classification"
  commit postdating the committed file.
- Full operating instructions (macOS/Lima, WSL2, and native-Linux paths):
  `ai_docs/docs/caruca_v1 pipeline instructions.md` in this repo.
- 2026-10-13: Claude Code CLI 2.1.296 is installed in this VM (guest home, native installer) for the
  naive Claude Code arm; see [[project_naive_claude_code_arm]].

**2026-10-27:** `binwalk` 2.3.4+dfsg1-5 (with `python3-binwalk`) was apt-installed in the `caruca` VM for
task 018's tracing, the same package the naive agent's image has.

**Watching a running job (observed 2026-10-27).** Jobs started from the Mac by a Claude Code session run as
`limactl shell caruca bash -lc '...'` under the VM's sshd — not in tmux/screen (no tmux server was running), so
there is no session to attach. The task 019 `caruca_side/refused_share.py` runs pipe their stdout through
`grep -v 'it/s\|%|' | tail -1`, so nothing prints until the end; the live view is v1's `tracer.log`, which the
tracer writes into the job's working folder (a `mktemp -d` under `/tmp`). Find it with
`ls -l /proc/<python pid>/fd | grep tracer.log`; each started test run is a `strace invocation:` line.
`tmux`, `htop` and `strace` are installed in the VM; `kernel.yama.ptrace_scope` is 1, so attaching strace to an
existing process needs `sudo`.
