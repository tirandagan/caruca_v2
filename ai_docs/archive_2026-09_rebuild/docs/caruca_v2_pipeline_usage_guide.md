# caruca_v2 — Pipeline Usage Guide

Everything needed to install caruca_v2, run its pipeline end to end, read what it
produces, and recover when a stage fails. The [README](../../README.md) is the short
version; this is the long one.

Every terminal block below is **real captured output** from this repository, not an
illustration. Where a message is quoted from source instead of executed — because
triggering it would have spent money — it says so.

---

## Contents

1. [Installation](#1-installation)
2. [Configuration and the two path rules](#2-configuration-and-the-two-path-rules)
3. [The pipeline, stage by stage](#3-the-pipeline-stage-by-stage)
4. [What a run leaves behind](#4-what-a-run-leaves-behind)
5. [The measurement layer](#5-the-measurement-layer)
6. [Exceptions and how to handle them](#6-exceptions-and-how-to-handle-them)
7. [Controlling cost](#7-controlling-cost)

---

## 1. Installation

### Route A — guided, with Claude Code (recommended)

The repository ships two slash commands. They are ordinary Markdown files in
`.claude/commands/`, so they are readable on their own if you would rather follow them by
hand.

```
/setup_pipeline      prepare and validate this machine
/run_pipeline        walk the pipeline stage by stage
```

`/setup_pipeline` exists because this project runs on at least four machine shapes and
every install recipe differs between them. It detects which one you are on before
proposing anything:

| Profile | Detected by | What it can do |
|---|---|---|
| **A. macOS host** | `uname -s` = `Darwin` | Stages 1, 2, 4 and non-destructive stage 3 natively. Destructive tracing and the v1 side of an annotation diff need the Lima VM. |
| **B. WSL2 under Windows** | `/proc/version` mentions `microsoft` | Linux natively, so v1 runs here directly. |
| **C. Native Linux** | Linux kernel, no WSL or Lima markers | Same as B. The CloudLab / lab-server case. |
| **D. Inside a Linux guest** | Lima markers present | Treated as C, with a note about which side of the shared mount you are on. |

It then asks whether this machine needs the **analysis role** (run the CLI, call the
model) or also the **execution role** (run v1 itself, carry destructive commands), and
validates in four groups: the caruca_v2 install and keys, the v1 checkout, the Linux
execution layer, and writable output roots. It reports the entire table before touching
anything, then fixes failures in dependency order — proposing each command, waiting for
confirmation, and re-validating afterwards.

It handles a machine with **no v1 checkout at all**: it searches for an existing one
before concluding anything is missing, confirms your GitHub access, clones without
forking, and picks a location that satisfies the path rules in §2.

When it finishes it writes a per-machine receipt to `~/.caruca_v2/setup_receipt.json` —
outside the repository, because the working tree is shared between machines — recording
which checks passed. It never writes the API key there.

Here is the environment detection it runs first, on the Mac this guide was written on:

```console
$ uname -s ; grep -qi microsoft /proc/version 2>/dev/null && echo wsl || echo "not wsl"
Darwin
not wsl
```

### Route B — manual

Requires Python 3.12 or newer and [`uv`](https://docs.astral.sh/uv/).

```sh
uv sync
cp .env.example .env      # then fill in the two required values
```

The CLI is then at `.venv/bin/caruca-v2`, or `caruca-v2` with the virtualenv active.

```console
$ .venv/bin/caruca-v2 --help
usage: caruca-v2 [-h]
                 {naive-llm,generate,trace,annotate,metrics,score,sweep} ...

LLM replication of caruca v1's specification-mining pipeline.

positional arguments:
  {naive-llm,generate,trace,annotate,metrics,score,sweep}
    naive-llm           Stage 1 (naive control): a command's documentation in,
                        a v1-DSL syntax specification out, via exactly one
                        few-shot prompt.
    generate            Stage 2: a syntax specification in, the concrete
                        invocations it allows and the environment each needs
                        out.
    trace               Stage 3: run each configuration in a prepared
                        workspace and record what the command did, as a
                        v1-compatible traces file.
    annotate            Stage 4: traces in, one consumer's annotation out.
                        Mirrors v1's own `caruca annotate FORMAT CMD`.
    metrics             Operate on the metrics database.
    score               Harness: argument-by-argument comparison of a
                        generated syntax spec against v1's committed spec or
                        the hand-annotated ground truth. No model call.
    sweep               Harness: run one or more campaign files — (commands ×
                        models × temperatures × samples) over a stage, with
                        ledger resume, budget brakes, the configuration freeze
                        gate, and a per-model comparison rollup.
```

### The v1 checkout

caruca_v2 cannot do anything useful without a caruca v1 checkout to read. v1 is a
**separate, private, unlicensed, fork-restricted** repository at
`https://github.com/binpash/caruca.git`. Clone it if you have access; never fork it, push
it elsewhere, or copy its source into this repository.

```sh
git clone https://github.com/binpash/caruca.git ~/dev/stevens/caruca
cd ~/dev/stevens/caruca/caruca
python3.12 -m venv .venv && .venv/bin/pip install -e .
```

v1's own virtualenv is not optional: every artifact caruca_v2 produces is validated by
running it through **v1's interpreter and v1's pydantic models**, never through an
imitation of the format.

On Linux — inside Lima, WSL2, or on a server — install to `~/caruca-venv` instead, so a
macOS venv and a Linux venv can coexist in a working tree shared across both.

### The Linux execution layer

Needed only for the execution role: running v1's own tracer, or carrying destructive
commands in stage 3.

```sh
sudo apt-get update
sudo apt-get install -y git python3-venv python3-pip attr mergerfs strace

# Ubuntu 23.10+ restricts unprivileged user namespaces. Without this, every traced
# invocation fails SILENTLY: return code 1, empty stdout, zero traces.
if sysctl kernel.apparmor_restrict_unprivileged_userns >/dev/null 2>&1; then
    echo 'kernel.apparmor_restrict_unprivileged_userns=0' | sudo tee /etc/sysctl.d/99-caruca-userns.conf
    sudo sysctl -w kernel.apparmor_restrict_unprivileged_userns=0
fi
unshare --user --map-root-user true && echo OK     # must print OK
```

On macOS that Linux layer is a Lima VM:

```sh
brew install lima
limactl start --name=caruca --cpus=8 --memory=8 --disk=30 --mount-writable template:ubuntu-24.04
```

`--mount-writable` is not optional — it mounts your macOS home directory read-write inside
the guest **at the same path**, which is what lets outputs land back in the repository.

Full platform-by-platform detail, including the WSL2 and native-Linux variants and the
reasoning behind each step, is in
[caruca_v1 pipeline instructions](caruca_v1%20pipeline%20instructions.md).

---

## 2. Configuration and the two path rules

| Variable | Required | Meaning |
|---|---|---|
| `OPENROUTER_API_KEY` | yes | The single key. Every candidate model is reached through the OpenRouter gateway, so one code path serves them all. |
| `CARUCA_V1_ROOT` | yes | Path to the v1 checkout — the repository **root**, the directory containing `caruca/`. Per-machine: `~/dev/stevens/caruca` on the Mac, `~/stevens/caruca` on the WSL PC. |
| `CARUCA_V2_LOG_CONVERSATION` | no | Set to `1` to write `conversation.jsonl` into every run directory, same as `--log-conversation`. |

**Rule 1 — `CARUCA_V1_ROOT` must be absolute.** It is resolved with
`Path(...).expanduser()` and nothing more: no `resolve()`, no repo-relative anchor. A
relative value like `../caruca` anchors to whatever directory the CLI was invoked from, so
it appears to work from the repository root and fails everywhere else. This defect has
already invalidated one campaign in this repository — the evidence is still on disk as
`eval/campaigns/c0_syntax_spec/ledger.invalidated-relative-path-defect.jsonl`.

**Rule 2 — it must point at the root, not the package.** The root contains `caruca/`.
Pointing one level deeper is the most common misconfiguration, and the code raises a
specific error for it.

Two further constraints depending on where you are:

- **On macOS**, the checkout must live under `$HOME`. Lima mounts only the home directory,
  at the same path inside the guest, so a checkout outside it is invisible to every
  VM-side command — tracing and the v1 annotator silently have nothing to read.
- **On WSL2**, keep it under the Linux home directory, never `/mnt/c/...`. The Windows
  drive mount does not reliably support the FUSE, overlay, and permission semantics the
  sandbox relies on.

**One gotcha worth knowing:** the CLI calls `load_dotenv()` at startup, so values in `.env`
are loaded from disk. Unsetting `OPENROUTER_API_KEY` in your shell does **not** simulate a
missing key — the file still supplies it, and the call still goes out and still costs
money. To test key-absence behaviour, move `.env` aside.

---

## 3. The pipeline, stage by stage

Four model-driven stages and a free bookkeeping step. Each stage is a thin wrapper over one
typed function in `src/caruca_v2/stages/`, so anything the CLI does can also be called
directly from Python.

| # | Command | In | Out |
|---|---|---|---|
| 1 | `naive-llm` | a command's documentation | syntax specification (`<cmd>.py`) |
| 2 | `generate` | a syntax specification | `<cmd>.invocations.txt`, `<cmd>.configs.json` |
| 3 | `trace` | configurations | `<cmd>.observations.json`, `<cmd>.traces.json` |
| 4 | `annotate` | traces | `<cmd>.<format>.annotation` |
| 5 | `metrics rebuild` | run directories on disk | `eval/metrics.db` |

**`--model` and `--temperature` are required on every stage.** That is deliberate: no run
gets recorded without the configuration that produced it being stated. They stay explicit
until the one-time configuration selection freezes a choice.

**Inputs default to v1's own committed artifacts**, which makes every stage measurable
independently — a stage's score is its own, not a downstream consequence of an earlier
stage's mistake. Pass `--docs`, `--spec`, `--configs`, or `--traces` to chain stages
instead and see the compounding end-to-end behaviour.

### Stage 1 — `naive-llm`

One prompt, a few worked examples, a command's documentation in, a syntax specification
out in v1's own Python DSL.

This is a **deliberately weak control**. It exists to show how much better v1's engineered
pipeline is than an off-the-shelf prompt, so it is never tuned to perform better, and a bad
answer is recorded as a result rather than retried.

```sh
caruca-v2 naive-llm mkdir --model openai/gpt-4o --temperature 0.0
```

Closing lines of a real run:

```console
  cost: $0.016727
  time: 2.61s
  model: openai/gpt-4o (requested openai/gpt-4o)
  seed: 42
  metrics: row appended to eval/metrics.db
```

The specification it produced, verbatim:

```python
from caruca.ir.syntax import *

mkdir_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Permission(flag="-m", alias=["--mode"]),
            Flag("-p", alias=["--parents"]),
            Flag("-v", alias=["--verbose"]),
            Flag("-Z"),
            SecurityContext(flag="--context"),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],
    ]
]
```

v1 imported it successfully — `"validation": {"passed": true, "available": true, "error":
null, "elements": 8}` — and scoring it against v1's committed specification gives an exact
match. `mkdir` is an easy case; do not read one perfect score as a general result:

```console
$ caruca-v2 score mkdir --spec eval/runs/2026-09-08T194311Z_mkdir_e23fa290/mkdir.py --plain
scoring eval/runs/2026-09-08T194311Z_mkdir_e23fa290/mkdir.py against v1-specs...
score mkdir
  reference: /Users/tirandagan/dev/stevens/caruca/caruca/src/caruca/syntax_specs/mkdir.py
  matched: 7 of 7 reference flag(s)
  missing: 0
  spurious: 0
  exact: 1.000
  f1: 1.000
```

Useful flags: `--docs PATH` to supply documentation from outside v1's corpus.

### Stage 2 — `generate`

A syntax specification in; out come the concrete invocations it allows and the environment
each one needs. v1 does this with hand-written enumeration code; here a model does it, and
the two sets are diffed.

```sh
caruca-v2 generate mkdir --model openai/gpt-4o --temperature 0.0
```

The knobs mirror v1's own CLI exactly, so the comparison run is faithful: `--max-arity`,
`--max-count`, `--stdin`, `--content`, `--skip`. Leave them alone unless you are
deliberately varying one.

Two things to expect. v1's own enumeration runs alongside for the set-diff and is slow on
wide-interface commands — `--compare-timeout` (default 300s) bounds it and `--no-compare`
skips it, with the skip recorded in the manifest. And v1's `generate` is known to crash on
a subset of commands with an empty-flag-group `ValueError`; that is a v1 defect, not your
run failing. Record it and use `--no-compare`.

`trace` picks up the most recent `generate` output for a command automatically, so chaining
these two needs no flag.

### Stage 3 — `trace`

Each configuration gets a fresh workspace built from v1's own fixture files, the command
runs, and what it did is recorded as a v1-compatible traces file.

**This is the expensive stage: one model session per configuration.** `--limit` is the cost
brake and defaults to 5. `--max-turns` defaults to 15 per configuration.

```sh
caruca-v2 trace cat --limit 5 --model openai/gpt-4o --temperature 0.0
```

Destructive commands — `rm rmdir unlink shred truncate dd mkfs fdisk mv chmod chown chgrp
ln install tee` — are refused unless an isolation backend carries them:

```sh
caruca-v2 trace rm --isolation lima --limit 5 --model openai/gpt-4o --temperature 0.0
```

The refusal is the first statement in `run_trace`, before the API client is even
constructed, so a mistake here costs nothing. Quoted from
`src/caruca_v2/stages/trace.py`:

> `rm` is destructive and will not be traced directly on this machine. Re-run with
> `--isolation lima`, which runs it inside the caruca VM.

Lima is currently the **only** isolation backend implemented. That is a policy in the code
rather than an OS limitation, so even on a bare Linux box, tracing `rm` needs Lima
installed locally. Without it, stage 3 on that machine is limited to non-destructive
commands.

`manifest.json` carries the tool audit trail — every command the model actually ran — which
is the thing to read when a trace looks wrong.

### Stage 4 — `annotate`

Traces in, one consumer's annotation out, mirroring v1's `annotate FORMAT CMD`. Formats:
`pash`, `posh`, `sash`, `shellcheck`.

By default this reads **v1's own committed traces**, which makes the useful comparison the
default: both annotators working from byte-identical input, so any difference is
attributable to the annotator alone.

```sh
caruca-v2 annotate pash ls --model openai/gpt-4o --temperature 0.0
```

**On macOS you must add `--v1-runner lima`.** v1's annotator resolves paths against a
hardcoded `/tmp` prefix that macOS rewrites to `/private/tmp`, so it cannot run on the Mac
host at all. Without the flag, the v1 side of the diff is simply unavailable and the
comparison is half-empty.

```sh
caruca-v2 annotate pash ls --v1-runner lima --model openai/gpt-4o --temperature 0.0
```

`manifest.json` holds two diffs: one against v1's own annotator on the same traces, one
against the hand-curated ground truth in `benchmarks/annotations/`. That second artifact
cost two graduate students 80 person-hours — treat a disagreement with it as something to
investigate, not something to correct away.

### Stage 5 — `metrics rebuild`

No model call, no cost. Every completed run already appended a row to `eval/metrics.db`;
this regenerates the database from the telemetry files on disk.

```console
$ caruca-v2 metrics rebuild --plain
  rows: 40
warning: skipped 2026-09-08T160226Z_cat_956562b1: no telemetry sidecar
warning: skipped 2026-09-08T160535Z_cat_a914ac60: no telemetry sidecar
warning: skipped 2026-09-08T160535Z_mkdir_ab7b76eb: no telemetry sidecar
```

Those warnings are normal and are covered in §6.

---

## 4. What a run leaves behind

Every stage writes one run directory under `eval/runs/`, named
`<UTC timestamp>_<command>_<short hash>/`:

```console
$ ls -1 eval/runs/2026-09-08T194311Z_mkdir_e23fa290/
manifest.json
mkdir.py
mkdir.telemetry.json
```

| File | What it is |
|---|---|
| the stage artifact | the output, in v1's own format |
| `*.telemetry.json` | tokens, cost, wall-clock, model, seed, prompt hash |
| `manifest.json` | the full request, the raw response, and the `checks` that ran |
| `conversation.jsonl` | only with `--log-conversation` |

A real telemetry sidecar:

```json
{
  "run_id": "2026-09-08T160512Z_mkdir_03e3014b",
  "command": "mkdir",
  "component": "naive_llm",
  "condition": "plain",
  "stage": "syntax_spec",
  "model_id": "openai/gpt-4o",
  "prompt_tokens": 6291,
  "completion_tokens": 98,
  "cost_usd": 0.0090275,
  "wall_clock_seconds": 4.788535916013643,
  "seed": 42,
  "prompt_hash": "a573995ebabd68be973844425576b63cf5fe95be5360e607444cc02bfb528860",
  "timestamp": "2026-09-08T16:05:12.417074Z",
  "decoding_params": { "temperature": 0.0, "max_tokens": 4096 },
  "turn": 0,
  "config_index": null
}
```

Multi-turn stages write one sidecar per turn (`<cmd>.turn-00.telemetry.json`, …), all
sharing a run id. `manifest.json` additionally records `status`, `failure_reason`,
`model_requested` vs `model_reported`, `seed_honored`, `finish_reason`,
`output_truncated`, the exact `prompt_system` and `prompt_user` sent, the `raw_response`,
and the `validation` result from v1.

Whatever a stage produces is validated by **v1 itself**, in a subprocess against v1's own
interpreter and pydantic models. A failed validation is recorded and the run exits
non-zero; it never triggers a retry, because a weak control that quietly re-asks until it
succeeds is no longer a control.

`eval/runs/` and `eval/metrics.db` are gitignored. Run directories embed prompt text read
from the private v1 checkout, and a binary database does not merge across machines. What
gets committed is the write-up in `ai_docs/analysis/`, tied back to local runs by
`prompt_hash`.

---

## 5. The measurement layer

### `score` — argument-by-argument spec comparison, no model call

```sh
caruca-v2 score mkdir --spec <path-to-generated-spec>
caruca-v2 score mkdir --spec <path> --reference ground-truth
caruca-v2 score --self-test
```

`--reference v1-specs` (the default) scores against v1's committed specifications — the
primary population. `--reference ground-truth` scores against the hand-annotated set.
`--cmp-specs` additionally runs v1's own `eval/cmp_specs.py`, the paper's instrument, and
reports its number alongside with its denominator caveat attached.

`--self-test` scores each committed exemplar against itself; every cell must be perfect,
which is how you check the scorer before trusting it on real output:

```console
$ caruca-v2 score --self-test --plain
scoring each exemplar spec against itself...
score --self-test
  touch: perfect
  rm: perfect
  mv: perfect
  ls: perfect
```

### `sweep` — campaigns across commands, models, temperatures, samples

```sh
caruca-v2 sweep eval/campaigns/c0_syntax_spec.json --dry-run
caruca-v2 sweep eval/campaigns/c0_syntax_spec.json
```

Always `--dry-run` first: it enumerates and prints every cell without making a single model
call, which is how you find out what a campaign will cost before committing to it. Sweeps
resume from a ledger, apply budget brakes, and enforce the post-freeze configuration gate.

---

## 6. Exceptions and how to handle them

### Exit codes

| Code | Meaning | What to do |
|---|---|---|
| `0` | The artifact was produced **and** validated by v1 | Nothing. |
| `1` | The run completed but its output was unusable | **Nothing — this is a result.** It is recorded, deliberately not retried. Read `manifest.json` for `failure_reason` and `raw_response`. |
| `3` | A configuration problem — missing key, unreachable v1 checkout | Fix the environment and re-run. Nothing was spent. |

Exit `1` is the one people misread. Stage 1 is a control; a control that quietly re-asks
until it succeeds is no longer measuring anything.

### Missing `--model` / `--temperature`

```console
$ caruca-v2 naive-llm mkdir
caruca-v2 naive-llm: error: the following arguments are required: --model, --temperature
```

Working as designed — see §3. Supply both.

### No documentation for the command

```console
$ caruca-v2 naive-llm frobnicate --model openai/gpt-4o --temperature 0.0
asking openai/gpt-4o for a syntax specification for frobnicate...
error: No man page for 'frobnicate' in the v1 corpus (looked for
/Users/tirandagan/dev/stevens/caruca/caruca/src/caruca/doc_sources/man/frobnicate.txt).
Pass --docs PATH to supply documentation from elsewhere.
```

The corpus defines the population of runnable commands. List it with:

```sh
ls "$CARUCA_V1_ROOT/caruca/src/caruca/doc_sources/man/" | sed 's/\.txt$//'
```

Note the ordering: the "asking …" line prints before the documentation is read, so **this
error costs nothing** despite appearing after it. Either pick a command from the corpus or
supply `--docs`.

### v1 checkout unreachable, or pointing one level too deep

The errors name the path they looked at:

> caruca v1 checkout not found at `<path>`. Set `CARUCA_V1_ROOT` to the v1 repository root
> (the directory containing `caruca/`).

> caruca v1 package source not found at `<path>`. `CARUCA_V1_ROOT` should point at the
> repository root, not the package directory.

If the path exists on one machine but not another, do not assume the checkout is missing —
the two dev machines use different paths and a copied `.env` points at the wrong one.
Search before concluding:

```sh
find "$HOME" -maxdepth 6 -type d -path '*/caruca/src/caruca' \
     -not -path '*/node_modules/*' -not -path '*/.venv/*' 2>/dev/null
```

### v1's virtualenv missing

> v1's virtualenv interpreter not found at `<path>`.

Every artifact is validated through v1's own interpreter, so this blocks validation
entirely. Create it — §1, "The v1 checkout". On macOS the venv at `$CARUCA_V1_ROOT/caruca/.venv`
must be a **macOS** venv; the Linux one belongs at `~/caruca-venv` inside the guest. They
cannot be the same directory.

### `metrics rebuild` warns about missing telemetry sidecars

```console
warning: skipped 2026-09-08T160535Z_cat_a914ac60: no telemetry sidecar
```

Expected, not an error. A run directory is created before the model call completes, so any
run interrupted — cancelled, crashed, killed — leaves a directory with no telemetry.
Rebuild skips them and says so. Delete them if the clutter bothers you; nothing else reads
them.

### A traced invocation returns 1 with empty output and zero traces

The single most confusing failure in the whole system, and it is silent. Buried in the
trace JSON you will find:

```
unshare: write failed /proc/self/uid_map: Operation not permitted
```

This is Ubuntu 23.10+ restricting unprivileged user namespaces. Apply the sysctl from §1
and verify with `unshare --user --map-root-user true && echo OK`. Treat it as blocking:
until it prints `OK`, every trace is worthless.

### The v1 side of an annotation diff is empty on macOS

Not a bug. v1's annotator cannot run on macOS at all — it resolves paths against a
hardcoded `/tmp` prefix that macOS rewrites to `/private/tmp`. Re-run with
`--v1-runner lima` and a running VM.

### Lima is stopped

```console
$ limactl list
NAME      STATUS     SSH                VMTYPE    ARCH       CPUS    MEMORY    DISK
caruca    Stopped    127.0.0.1:52363    vz        aarch64    8       8GiB      30GiB
```

`limactl start caruca`, wait for `Running`, then re-run. Stopping the VM between sessions
is normal and costs nothing but the restart.

### v1's `generate` crashes with an empty-flag-group `ValueError`

A known v1 defect affecting a subset of commands, not a failure of your run. Re-run with
`--no-compare`; the skip is recorded in the manifest so nothing is lost silently.

### A campaign's results look wrong across the board

Check whether `CARUCA_V1_ROOT` was relative when it ran (§2, Rule 1). One campaign in this
repository was invalidated exactly this way, and the invalidated ledger was kept on disk
rather than deleted, as evidence.

---

## 7. Controlling cost

- **`trace` dominates.** It is per-configuration, not per-command. `--limit` defaults to 5;
  running a full configuration set is an explicit choice, never a default.
- **`--dry-run` every sweep first.** It enumerates the cells without a single model call.
- **Multi-turn stages do not run away.** `generate` and `annotate` continue across turns
  **only** when the token cap cut a response off. A model that stops on its own is never
  asked for more. Caps: 4 turns for `generate` and `annotate`, 15 per configuration for
  `trace`.
- **Nothing retries on failure.** A bad answer is recorded, not re-asked.
- **`score`, `metrics rebuild`, and `--dry-run` are free.** Use them freely.

For reference, the naive stage on a small command costs a bit under two cents at GPT-4o
prices: 6,291 prompt + 98 completion tokens, `$0.0090`.

---

## Related documents

- [README](../../README.md) — the short version
- [caruca_v1 pipeline instructions](caruca_v1%20pipeline%20instructions.md) — full
  platform setup for v1 itself, per operating system
- [`ai_docs/analysis/`](../analysis/) — findings produced by this project
- `CLAUDE.md` — orientation for the project as a whole
