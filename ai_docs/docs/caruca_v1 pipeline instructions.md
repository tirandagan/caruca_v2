# Caruca v1 Pipeline — Operating Instructions

This document explains how to set up and operate the caruca v1 pipeline end to end on macOS
(via a Lima Linux VM), on Windows (via WSL2), or on a native Linux server. It was written after a full verified run of the
pipeline for the target command `ls` (September 2026) and records both the working
commands and the pitfalls discovered along the way.

**Repo:** `/Users/tirandagan/dev/stevens/caruca` (the v1 repo, sibling of `caruca_v2`)

---

## 1. What caruca v1 does

Caruca automatically mines **partial specifications for shell commands** (`ls`, `rm`,
`mkdir`, …) from their natural-language documentation. For each target command the
pipeline produces a JSON *annotation* describing, per syntactic case, what the command
reads, what it writes, and its parallelizability class (`stateless`, `side-effectful`,
`non-pure`, …). These annotations are consumed by downstream systems such as PaSh and
POSH.

The v1 repo layout:

| Path | Purpose |
|---|---|
| `caruca/` | The tool itself (CLI, tracer, annotator, syntax specs) |
| `caruca/src/caruca/pash_syntax_specs/` | Pre-built per-command syntax specs (one `.py` per command) — the pipeline's inputs |
| `caruca/outputs/<cmd>.json` | Trace output per command (created by the trace stage) |
| `caruca/save/<cmd>.json` | Final annotation per command (created by the annotate stage) |
| `eval/` | Scripts for evaluating practical completeness against real-world invocations |
| `benchmarks/` | Benchmark corpora (bsd, busybox, top100, …) |

### Why a Linux environment is required

The tracer (`src/caruca/tracer/tracer.py`) is Linux-only. It:

- shells out to **strace** (`strace -yfo /proc/self/fd/N --trace=%file,%desc,getcwd …`)
  and reads the log back through `/proc/self/fd`;
- wraps every invocation in the bundled **`try`** tool (`src/caruca/scripts/try`),
  which uses **unprivileged user namespaces** (`unshare`) plus
  **overlayfs/mergerfs** to redirect all filesystem writes into a throwaway overlay.

None of that exists on macOS or native Windows, so on those platforms the pipeline
runs inside a Linux environment — a Lima VM on macOS, WSL2 on Windows — playing the
role the CloudLab node plays in `cloudlab-setup.sh`. On a Linux server it runs
directly on the host.

### Isolation model — no snapshots needed

Caruca knows nothing about Lima, WSL, or VMs and does **not** need a clean machine
per run.
Every traced invocation gets its own fresh sandbox: a `TemporaryDirectory` under
`/tmp` populated with fixture files (`ir/environment.py`, `env()` context manager),
executed under `try -D <sandbox>` so that even destructive commands (`rm`) only touch
the overlay. The sandbox is deleted when the invocation finishes. The VM is therefore
a **long-lived reusable host**: build it once, `limactl stop` / `limactl start` it as
needed, rerun the pipeline as often as you like. Worst case after a crashed run is
leftover temp dirs in the VM's `/tmp`, cleared by a VM reboot.

---

## 2. One-time environment setup

Caruca itself always runs on Linux. What differs per platform is how you get a Linux
environment with a copy of the repo in it:

| Your machine | Path | Repo location |
|---|---|---|
| macOS | **2A** — Lima VM | Mac home dir auto-mounted at the same path inside the VM |
| Windows | **2B** — WSL2 (Ubuntu 24.04) | `git clone` inside the WSL filesystem |
| Linux server (headless/"core") | **2C** — native, no VM | `git clone` anywhere on a local filesystem |

Do the platform section that applies, then the **common Linux-side setup (2.3–2.5)**,
which is identical everywhere. Throughout the common steps, `$CARUCA` means the
repo's `caruca/` subdirectory:

- macOS/Lima: `CARUCA=/Users/tirandagan/dev/stevens/caruca/caruca`
- WSL2 / Linux server: `CARUCA=~/caruca/caruca` (or wherever you cloned)

### 2A. Platform setup — macOS (Lima VM)

#### Step 2A.1 — Install Lima (on the Mac)

```sh
brew install lima
```

Verified with Lima 2.2.0 on Homebrew 6.0.18, Apple Silicon (arm64).

#### Step 2A.2 — Create the Ubuntu VM

```sh
limactl start --name=caruca --cpus=8 --memory=8 --disk=30 --mount-writable template:ubuntu-24.04
```

- First run downloads the Ubuntu 24.04 image and boots the VM (a few minutes).
- If an interactive menu appears, choose **"Proceed with the current configuration"**.
- `--mount-writable` mounts your macOS home directory read-write inside the VM **at
  the same path**, so the repo is visible at
  `/Users/tirandagan/dev/stevens/caruca` from inside the VM and all pipeline outputs
  land directly in the repo on the Mac side.
- Ubuntu 24.04 ships Python 3.12, which satisfies caruca's `requires-python >= 3.11`.

Useful lifecycle commands:

```sh
limactl list            # status
limactl shell caruca    # open a shell inside the VM
limactl stop caruca     # stop (state preserved)
limactl start caruca    # start again
```

All subsequent Linux-side commands are run inside `limactl shell caruca`.

### 2B. Platform setup — Windows (WSL2)

#### Step 2B.1 — Install WSL2 with Ubuntu 24.04

In an elevated PowerShell:

```powershell
wsl --install -d Ubuntu-24.04
```

Reboot if prompted, then confirm the distro runs under **WSL 2** — WSL 1 lacks the
real Linux kernel features the tracer needs (ptrace/strace semantics, FUSE,
overlayfs, user namespaces):

```powershell
wsl -l -v          # VERSION column must say 2
wsl --set-version Ubuntu-24.04 2   # only if it says 1
```

#### Step 2B.2 — Clone the repo inside the Linux filesystem

Open the Ubuntu shell and clone the repo somewhere under the Linux home directory —
**not** under `/mnt/c/...`. The Windows drive mounts go through 9p/drvfs, which is
slow and does not reliably support the FUSE/overlay and permission semantics the
sandbox relies on:

```sh
cd ~
git clone <repo-url> caruca
```

WSL2 notes:

- The default WSL2 kernel has AppArmor disabled, so the Ubuntu 24.04 user-namespace
  restriction from step 2.4 usually **does not exist** there — step 2.4 below is
  written to detect this and no-op safely.
- If memory is tight during large traces, raise the WSL2 limit in `%UserProfile%\.wslconfig`
  (`[wsl2]` → `memory=8GB`, `processors=8`) and run `wsl --shutdown` to apply.
- Outputs land in the WSL filesystem; reach them from Windows at
  `\\wsl.localhost\Ubuntu-24.04\home\<user>\caruca\...` if needed.

### 2C. Platform setup — native Linux server (headless)

No VM layer at all — the pipeline runs directly on the host (this is exactly the
CloudLab scenario `caruca/cloudlab-setup.sh` targets).

```sh
cd ~
git clone <repo-url> caruca
```

- Instructions below assume **Ubuntu 24.04 / Debian-family** (apt). Prefer a
  distro whose `python3` is **3.12+**: although `pyproject.toml` declares
  `requires-python >= 3.11`, the tracer uses a PEP 701 nested f-string
  (`tracer/tracer.py`), so the trace stage dies on 3.11. On Ubuntu 22.04 install
  Python 3.12 from deadsnakes (`add-apt-repository ppa:deadsnakes/ppa &&
  apt install python3.12 python3.12-venv`) and substitute `python3.12` in step 2.5.
- On RHEL/Fedora-family, the equivalents are
  `dnf install strace attr fuse mergerfs python3-pip` (mergerfs comes from EPEL on
  RHEL/Rocky/Alma); everything else is identical.
- Root/sudo is required once, for package install and the sysctl in step 2.4. The
  pipeline itself runs unprivileged — its sandboxes use unprivileged user
  namespaces, not root.
- Keep the repo on a local filesystem: `/tmp` sandboxing and overlay mounts behave
  poorly when the working tree is on NFS.

### Common Linux-side setup (all platforms)

Run these inside the VM (`limactl shell caruca`), the WSL2 Ubuntu shell, or the
server shell respectively.

#### Step 2.3 — Install OS packages

```sh
sudo apt-get update
sudo apt-get install -y git python3-venv python3-pip attr mergerfs strace
```

This adapts `caruca/cloudlab-setup.sh` for Ubuntu 24.04: we use the default
`python3-venv` (3.12) instead of `python3.11-venv`, and add `strace` explicitly
(CloudLab images ship it; stock Ubuntu cloud images already had it in our case, but
listing it is harmless).

#### Step 2.4 — Lift Ubuntu's user-namespace restriction (critical!)

Ubuntu 23.10+ (including 24.04) restricts unprivileged user namespaces via AppArmor
by default (`kernel.apparmor_restrict_unprivileged_userns = 1`). With the
restriction in place, **every traced invocation fails silently** with
`return_code: 1`, empty stdout, zero traces, and this stderr buried in the trace
JSON:

```
unshare: write failed /proc/self/uid_map: Operation not permitted
```

Apply the fix only where the knob exists (on WSL2 and most non-Ubuntu kernels it
doesn't, and nothing needs to be done):

```sh
if sysctl kernel.apparmor_restrict_unprivileged_userns >/dev/null 2>&1; then
    echo 'kernel.apparmor_restrict_unprivileged_userns=0' | sudo tee /etc/sysctl.d/99-caruca-userns.conf
    sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
fi
```

The sysctl.d file survives reboots; the `sysctl -w` applies it immediately.

Sanity check on **every** platform (this is the real test that the sandbox will
work): `unshare --user --map-root-user true && echo OK` should print `OK`. If it
fails on a non-Ubuntu server, check `sysctl kernel.unprivileged_userns_clone`
(older Debian: must be 1) or your distro's equivalent hardening knob.

#### Step 2.5 — Create the Linux venv and install caruca

```sh
cd "$CARUCA"          # the repo's caruca/ subdirectory, see table above
python3 -m venv ~/caruca-venv
~/caruca-venv/bin/pip install -e .
```

Notes:

- The venv lives at `~/caruca-venv` on a Linux-local disk, deliberately not in the
  repo. On macOS/Lima this also means it can't collide with the macOS-side `.venv` /
  `.venv-llm` (Darwin binaries, unusable from Linux) and avoids slow virtiofs
  imports; on WSL2/servers it simply keeps build artifacts out of the working tree.
- `-e` (editable install) means the code runs from the repo — edits take effect
  immediately, no reinstall needed.
- All ~70 dependencies (dspy-ai, pydantic, litellm, tiktoken, …) have prebuilt
  manylinux wheels for both x86_64 and aarch64 on Python 3.12; no compilers are
  required.

---

## 3. The pipeline — five stages per target command

Each target command flows through the stages below. Stages 1–2 are inputs that
normally already exist in the repo; stages 3–4 are what you run day-to-day (this is
exactly what `caruca/run.sh` loops over); stage 5 is the evaluation layer.

```
documentation ──(1 syntax-spec, LLM)──▶ syntax spec (.py)
syntax spec ──(2 generate)──▶ concrete invocations
invocations ──(3 trace)──▶ outputs/<cmd>.json   (sandboxed strace traces)
traces ──(4 annotate)──▶ save/<cmd>.json        (the mined specification)
annotations ──(5 eval/)──▶ correctness & completeness results
```

### Stage 1 — Syntax specification (`caruca syntax-spec`)

**What it does:** uses an LLM (dspy → OpenAI) to convert a command's natural-language
documentation (man page) into a machine-readable syntax specification: the grammar of
flags, options, operands, and their types.

**Input:** documentation under `src/caruca/doc_sources/`.
**Output:** a spec module like `src/caruca/pash_syntax_specs/ls.py`.

**Key operational fact:** this is the **only stage that needs an API key**
(`OPENAI_API_KEY` in the environment, read in `src/caruca/llm.py`). The specs for the
PaSh command set are already committed under `pash_syntax_specs/` (and
`posh_syntax_specs/`, `syntax_specs/`), so for normal pipeline runs you skip this
stage entirely and no key is required.

### Stage 2 — Invocation generation (`caruca generate`)

**What it does:** takes the syntax spec from stage 1 and enumerates concrete
invocations to exercise: flag combinations (bounded by `--max-count`), operand
arities (bounded by `--max-arity`), plus systematic variations of stdin
(`--stdin simple|varied|split`) and file content (`--content simple|varied|split`).

**How it uses the prior stage:** the spec defines the space of legal (and some
deliberately illegal) invocations; generation walks that space. You rarely run this
stand-alone — the trace stage invokes generation internally. The useful stand-alone
form is the cost estimate:

```sh
~/caruca-venv/bin/caruca trace --pash --stdin split --content split --length-only <cmd>
```

which prints the number of invocations that a full trace would execute **without
running anything**. (`ls` → 688; `pwd` → 12; `echo` → 96.) Always check this before a
long run.

### Stage 3 — Tracing (`caruca trace`)

**What it does:** executes every generated invocation inside a fresh sandbox, under
`try` (user-namespace + overlay isolation) and `strace` (recording every file open,
read, write, and directory access). It records, per invocation-configuration: the
exact command line, return code, stdout/stderr, and the parsed strace events
(e.g. `['rf', '/etc/ld.so.cache']` = read file).

**How it uses the prior stage:** consumes the generated invocations and the fixture
environments the generator prescribes (which files/dirs exist in the sandbox, their
contents, what's on stdin).

**Run it (in the Linux shell):**

```sh
cd "$CARUCA"
mkdir -p save outputs
~/caruca-venv/bin/caruca trace --pash --stdin split --content split <cmd>
```

**Output:** `outputs/<cmd>.json` — one JSON file, *not* a directory (the `--output`
help text saying "Defaults to outputs/CMD_traces/" is stale). For `ls` this was
~2.8 MB: 682 configs, ~17.5k trace events, a few minutes of wall time with 8 vCPUs.

**Notes:**

- `--pash` selects the simplified PaSh specs; `--posh` selects the POSH ones.
- Non-zero return codes for a minority of configs are **expected** — some generated
  invocations intentionally exercise error paths. What is *not* normal is *every*
  config failing with rc=1 and zero traces: that means the sandbox itself is broken
  (see step 2.4).
- `--parallel N` trades determinism for speed on some commands; the default was fine.
- The isolation backend is selectable via the `CARUCA_ISOLATION_METHOD` env var:
  `try` (default, the vendored overlayfs script), `docker`, or `none`. Everything in
  this document assumes the default `try`.

### Stage 4 — Annotation (`caruca annotate`)

**What it does:** analyzes the trace set and induces the specification: it partitions
the command's behavior into *cases* (predicates over the invocation, e.g. "flag `-n`
present ∧ exactly 1 operand"), and for each case derives the inputs, outputs, and the
parallelizability class (`stateless` / `side-effectful` / `non-pure` / …).

**How it uses the prior stage:** purely a function of `outputs/<cmd>.json` — it
generalizes from the observed strace events across all sandboxed runs. No LLM, no
network, no sandbox needed.

**Run it (same directory):**

```sh
~/caruca-venv/bin/caruca annotate pash <cmd> > save/<cmd>.json
```

Useful flags: `--human` (readable output), `--hide-trivial`,
`--input` (non-default trace location), and the first positional argument selects the
annotation dialect (`pash`, `posh`, `sash`, `shellcheck`).

**Caveat observed in practice:** a fresh `save/ls.json` differed from the previously
committed one (4 cases vs 6; some cases reclassified `stateless` → `non-pure`).
Recent commits on main (`fix parallelizability class classification`, `fix tracer`)
postdate the committed file, so differences against old saved annotations are
expected — but review them before overwriting, and rely on git history to recover
prior versions.

### Stage 5 — Evaluation (`eval/`)

**What it does:** measures the mined specifications against the real world:

- `eval/syntax-spec-correctness.sh`, `eval/cmp_specs.py` — compare mined syntax
  specs against references;
- `eval/llm_correctness.sh` — LLM-related correctness checks (needs the API key);
- `eval/command-invocations.txt`, `eval/union.txt`, `benchmarks/` — corpora of
  command invocations "in the wild" used to score practical completeness;
- `eval/type_stats.py`, `eval/shellcheck/`, `eval/pash-annotations/` — analysis and
  downstream-format checks.

**How it uses the prior stage:** consumes the `save/*.json` annotations (and the
specs) and reports coverage/correctness over the benchmark invocation corpora.

### Batch mode — all commands

`caruca/run.sh` is the whole v1 pipeline over every committed PaSh spec:

```sh
mkdir -p save outputs
for file in src/caruca/pash_syntax_specs/*.py; do
    cmd=$(basename "$file" .py)
    caruca trace --pash --stdin split --content split "$cmd"
    caruca annotate pash "$cmd" > save/"$cmd".json
done
```

Run it in the Linux shell with the venv active
(`source ~/caruca-venv/bin/activate`) from `"$CARUCA"`. Check `--length-only` counts first for
expensive commands before committing to a long batch.

There is also `caruca oracle` — a quick check of whether caruca can produce
annotations for a given command at all.

---

## 4. Verifying a run

After tracing, sanity-check the trace file before annotating:

```sh
~/caruca-venv/bin/python - <<'EOF'
import json
d = json.load(open("outputs/ls.json"))
tot = sum(1 for inv in d for c in inv["configs"])
ok  = sum(1 for inv in d for c in inv["configs"] if c["return_code"] == 0)
tr  = sum(len(c["traces"]) for inv in d for c in inv["configs"])
print(f"invocations: {len(d)}, configs: {tot}, rc==0: {ok}, trace lines: {tr}")
EOF
```

Healthy run (ls): `invocations: 6, configs: 682, rc==0: 594, trace lines: 17512`.

Red flags:

| Symptom | Cause / fix |
|---|---|
| Every config rc=1, 0 traces, stderr `unshare: write failed /proc/self/uid_map` | AppArmor userns restriction — apply step 2.4 |
| `strace: command not found` in stderr | strace missing — step 2.3 |
| `caruca: command not found` | venv not on PATH — use `~/caruca-venv/bin/caruca` or `source ~/caruca-venv/bin/activate` |
| Trace output not found at `outputs/<cmd>_traces/` | Stale help text; the file is `outputs/<cmd>.json` |
| `Please provide an OpenAI API key…` | You invoked stage 1 (`syntax-spec`) or an LLM eval; export `OPENAI_API_KEY` (trace/annotate never need it) |

---

## 5. Quick reference — full cold-start to first annotation

```sh
# --- Get a Linux environment (pick ONE) ---------------------------------
# macOS:
brew install lima
limactl start --name=caruca --cpus=8 --memory=8 --disk=30 --mount-writable template:ubuntu-24.04
limactl shell caruca                          # continue below inside the VM
CARUCA=/Users/tirandagan/dev/stevens/caruca/caruca

# Windows (elevated PowerShell, then open the Ubuntu shell):
#   wsl --install -d Ubuntu-24.04
# Linux server: nothing to do, you are already there.
# WSL2 / server:
#   git clone <repo-url> ~/caruca
#   CARUCA=~/caruca/caruca

# --- Common Linux-side setup (VM / WSL2 / server) -----------------------
sudo apt-get update
sudo apt-get install -y git python3-venv python3-pip attr mergerfs strace
if sysctl kernel.apparmor_restrict_unprivileged_userns >/dev/null 2>&1; then
    echo 'kernel.apparmor_restrict_unprivileged_userns=0' | sudo tee /etc/sysctl.d/99-caruca-userns.conf
    sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
fi
unshare --user --map-root-user true && echo SANDBOX-OK

cd "$CARUCA"
python3 -m venv ~/caruca-venv
~/caruca-venv/bin/pip install -e .
mkdir -p save outputs

# --- The pipeline for one command ---------------------------------------
~/caruca-venv/bin/caruca trace --pash --stdin split --content split --length-only ls   # cost estimate: 688
~/caruca-venv/bin/caruca trace --pash --stdin split --content split ls                 # → outputs/ls.json
~/caruca-venv/bin/caruca annotate pash ls > save/ls.json                               # → the specification
```
