# The Pipeline Chain — v2 Beside v1, Stage by Stage

This document follows one command, `cat`, all the way through both pipelines: what each stage
reads, what it writes, where that file lives, what it looks like inside, and how it is handed to
the next stage. It is the concrete counterpart to
[`../analysis/v1_v2_parity_study.md`](../analysis/v1_v2_parity_study.md), which reports the
scores but not the plumbing.

**Terminology:** **v1** is the original hand-written Caruca at `$CARUCA_V1_ROOT`; **v2** is the
LLM replication in this repository. Every artifact below is real output from the parity study
run of 2026-09-14 (`openai/gpt-4o`, temperature 0.0, seed 42, `--max-arity 1 --max-count 1`,
v1 commit `d8032407346aadc135b14c043618c8c1d4f4e0cf`).

`cat` is used because it is the one command that completed all four stages on both sides.

---

## The shape of the chain

```
   man page ──► [1] syntax spec ──► [2] invocations   ──► [3] traces ──► [4] annotation
                                       + configs
      │                 │                    │                  │              │
   SHARED           SHARED INPUT       SHARED INPUT       SHARED INPUT    SHARED INPUT
```

At every seam both systems are handed **the same input**. That is the *independent-inputs*
design: each stage is scored on its own merits rather than inheriting the previous stage's
mistakes. It is also why stage 2 reads v1's committed specification rather than stage 1's
output, and why stage 3 reads v1's own configuration expansion rather than stage 2's.

Chaining the stages instead — feeding each one the previous stage's output — is a different and
also legitimate experiment (it measures whether errors compound or wash out). It is not what
this run did.

---

## Stage 1 — documentation → syntax specification

### Input, shared

```
$CARUCA_V1_ROOT/caruca/src/caruca/doc_sources/man/cat.txt      1,827 bytes
```

Plain man-page text, one file per command, 120 of them.

### Output

| system | path |
|---|---|
| v1 | `$CARUCA_V1_ROOT/outputs/llm-dsl-generation/cat.py` *(committed; note the repo root, not `caruca/outputs/`)* |
| v2 | `eval/runs/2026-09-14T130803Z_cat_75b37300/cat.py` (629 bytes) |

Both open identically — this is a Python file in v1's embedded DSL:

```python
from caruca.ir.syntax import *

cat_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-A", alias=["--show-all"]),
            Flag("-b", alias=["--number-nonblank"]),
            Flag("-e"),
            Flag("-E", alias=["--show-ends"]),
            Flag("-n", alias=["--number"]),
```

The binding name is load-bearing: v1 registers a command by importing
`syntax_specs/<cmd>.py` and looking for `<cmd>_syntax_spec`. Nothing else registers a command.

### What else v2 writes beside the artifact

```
eval/runs/2026-09-14T130803Z_cat_75b37300/
  cat.py                    629 bytes   the artifact
  cat.telemetry.json        556 bytes   tokens, cost, wall clock, model, seed
  manifest.json          30,430 bytes   the complete prompt, the raw response, the checks
```

`manifest.json` is where to look when a result surprises you: it holds the exact text sent to
the model, the reply verbatim, `prompt_hash`, and the validation outcome. v1 has no equivalent —
its LLM step leaves no record of what it asked.

---

## Stage 2 — specification → invocations and configurations

### Input, shared

```
$CARUCA_V1_ROOT/caruca/src/caruca/syntax_specs/cat.py
```

v1's **committed ground-truth** specification, not stage 1's output.

### Output — and this is where the two systems differ in kind

**v1 writes no file at all.** `caruca generate cat` prints to stdout: 27 lines, 15 distinct.

```
cat
cat --help
cat --version
cat -A
cat -E
cat -T
cat -b
cat -e
…
```

The configurations themselves — the environment each invocation needs — never leave memory.
They are constructed by `CommandInvocation.to_exec_env()` and piped straight into tracing. Only
the invocation *strings* are ever externally visible.

**v2 must serialise them**, which is why it produces two files:

```
eval/runs/2026-09-14T130937Z_cat_268dc4d9/
  cat.invocations.txt         557 bytes   human-readable list
  cat.configs.json         12,818 bytes   ← the machine-readable one stage 3 consumes
  cat.turn-00.telemetry.json              two turns were needed
  cat.turn-01.telemetry.json
  manifest.json            32,150 bytes
```

One configuration:

```json
{ "name": "cat", "body": [], "string": {}, "stdin": "HUMAN_TEXT" }
```

**This asymmetry matters for the evaluation.** Because v1 never serialises a configuration, the
question "did it ask for the right filesystem?" had no artifact to check against — which is why
task 002's structural configuration comparison was deferred, and why the environment errors were
invisible until `harness/config_env.py` reconstructed v1's side explicitly
(`v1.reference_configs()` calls `to_exec_env` directly).

---

## Stage 3 — configurations → traces

### Input, shared

```
eval/v1_configs/cat.configs.json      17,735 bytes, 35 configurations
```

v1's **own** expansion, written out by `v1.reference_configs()` precisely so stage 3 does not
inherit stage 2's typing errors. One invocation expands to several configurations — one per
environment variant of its paths.

### v1 output

```
$CARUCA_V1_ROOT/caruca/outputs/cat.parity.json     27 groups, 35 configurations
```

Structure is `[ {command, true_str, configs: [ {command, return_code, stdout, stderr, traces} ]} ]`.
For `cat -b`:

```
return_code = 0
stdout      = "     1\tc\n     2\ta\n     3\tr…"
traces      = 10 raw (action, path) pairs:
  ["rf", "/usr/bin/cat"]
  ["rf", "/etc/ld.so.preload"]
  ["rf", "/etc/ld.so.cache"]
  ["rf", "/etc/ld.so.cache"]
  ["rf", "/usr/lib/aarch64-linux-gnu/libc.so.6"]     ← dynamic-loader noise
  …
```

### v2 output

```
eval/runs/2026-09-14T163935Z_cat_a3ea2a72/
  cat.observations.json     4,851 bytes   raw per-session record
  cat.traces.json           5,028 bytes   ← v1-compatible, assembled by v1's own models
  cat.turn-00..09.telemetry.json          ten turns
  manifest.json            18,733 bytes   includes the tool audit trail
```

```
return_code = 0
traces      = [["rf", "stdin"], ["wf", "stdout"]]
```

`cat.traces.json` is **not an imitation of v1's format** — it is built by v1's own
`Traces`/`CommandInvocationTraces`/`FSInteraction` pydantic models inside v1's interpreter
(`v1.assemble_traces`), so v1's annotator will accept it directly.

### Why 10 pairs and 2 pairs are the same answer

Run v1's own relevance filter (`tracer/data.py::__readwrite`) over its raw output:

```
10 raw pairs  →  3 kept  →  distinct: {("rf","stdin"), ("wf","stdout")}
7 system paths dropped
```

**v2 reported exactly those two.** The difference was entirely loader noise, which is why both
sides are projected before scoring. Unprojected, `dirname` would be capped near 12% recall
however perfectly a model observed; `ls` reduces from 17,512 raw pairs to 20 distinct ones.

---

## Stage 4 — traces → annotation

### Input, shared

```
$CARUCA_V1_ROOT/caruca/outputs/cat.parity.json
```

v2 receives it through the campaign's `stage_options.traces_pattern`, so both annotators read
**byte-identical** traces. (v1's default path, `caruca/outputs/<cmd>.json`, exists for only 18
commands — none of which overlap the 13 that have hand-curated annotations — so a parity
campaign can never use it.)

### The three artifacts, side by side

**v1** — `caruca/outputs/cat.parity.pash.json`, **14 cases**, one per observed flag combination:

```json
{
  "predicate": {"operator": "and", "operands": [
      {"operator": "exists", "operands": []},
      {"operator": "len_args_eq", "operands": [0]}]},
  "pclass": "non-pure",
  "inputs": ["stdin"], "outputs": ["stdout"],
  "true_str": "cat", "comments": "Automatically generated by caruca."
}
```

**v2** — `eval/runs/2026-09-14T155525Z_cat_8ed69ec8/cat.pash.annotation`, **2 cases**:

```json
{
  "predicate": "default",
  "pclass": "pure",
  "inputs": ["stdin"], "outputs": ["stdout"],
  "true_str": "cat",
  "comments": "The command reads from stdin and writes to stdout. It is pure as it does not modify any files or directories."
}
```

**Hand-curated ground truth** — `benchmarks/annotations/pash/cat.json`, **3 general cases**:

```json
{ "predicate": {"operator": "exists", "operands": ["-n"]},
  "class": "pure",
  "inputs": ["args[:]"], "outputs": ["stdout"] }
```

### Three disagreements visible in one screen

1. **Granularity.** v1 emits one conjunction per observed flag combination (14); the humans
   wrote 3 general atoms. Matching by predicate key aligns **zero** of them, which is why the
   scorer falls back to *subsumption* — the rule PaSh itself uses to select a case.
2. **The conservative bias, concretely.** On plain `cat`, v1 says **`non-pure`** and v2 says
   **`pure`**. The humans agree with v2. This is one of the 58-of-62 disagreements where bounded
   tracing leaves v1 with less evidence and it falls back cautiously — a property of
   `--max-count 1`, not a defect.
3. **Field names.** v1 serialises `pclass`/`comments`/`true_str`; the ground truth uses
   `class`/`comment`/`aggregate`. Compared raw, a *perfect* answer scores zero. The scorer
   projects across the gap and records what it translated.

v2's `manifest.json` for this stage is **109 KB** — the entire traces file was in the prompt.
That is also why `rm` (~211,000 tokens) and `tee` (~149,000) could not be annotated at all
against a 128,000-token window.

---

## Reproducing any of this

```sh
# the whole side-by-side, per command, into eval/parity_diffs/<cmd>.md
python scripts/parity_diff.py cat

# v1's side, by hand
$CARUCA_V1_ROOT/caruca/.venv/bin/caruca generate cat --max-arity 1 --max-count 1
limactl shell caruca -- ~/caruca-venv/bin/caruca trace cat --max-count 1 --output outputs/cat.parity.json
limactl shell caruca -- ~/caruca-venv/bin/caruca annotate pash cat --input outputs/cat.parity.json

# v2's side
.venv/bin/caruca-v2 naive-llm cat --model openai/gpt-4o --temperature 0.0
.venv/bin/caruca-v2 generate  cat --max-count 1 --model openai/gpt-4o --temperature 0.0
.venv/bin/caruca-v2 trace     cat --limit 5 --isolation lima --model openai/gpt-4o --temperature 0.0
.venv/bin/caruca-v2 annotate  pash cat --traces <path> --model openai/gpt-4o --temperature 0.0

# score a stage-1 spec against v1's (the only scoring verb on the CLI today)
.venv/bin/caruca-v2 score cat --spec <run_dir>/cat.py --reference v1-specs
```

Re-scoring a completed run of **any** stage from its artifacts, with no model calls, is
implemented but not yet exposed on the CLI — the planned `score run <dir>` sub-verb was not
built. Until it is:

```python
from pathlib import Path
from caruca_v2.harness import rescore
rescore.score_run(Path("eval/runs/2026-09-14T130937Z_cat_268dc4d9"))   # dispatches on stage
```

---

## Where things live, in one table

| what | v1 | v2 |
|---|---|---|
| man pages | `caruca/src/caruca/doc_sources/man/<cmd>.txt` | *(reads v1's)* |
| ground-truth spec | `caruca/src/caruca/syntax_specs/<cmd>.py` | *(reads v1's)* |
| LLM-generated spec | `outputs/llm-dsl-generation/<cmd>.py` **(repo root)** | `eval/runs/<ts>_<cmd>_<hash>/<cmd>.py` |
| invocations | *stdout only* | `<run>/<cmd>.invocations.txt` |
| configurations | *in memory only* | `<run>/<cmd>.configs.json` |
| v1 configs, extracted | `eval/v1_configs/<cmd>.configs.json` | *(shared input)* |
| traces | `caruca/outputs/<cmd>.parity.json` | `<run>/<cmd>.traces.json` |
| annotation | `caruca/outputs/<cmd>.parity.pash.json` | `<run>/<cmd>.pash.annotation` |
| hand-curated truth | `benchmarks/annotations/pash/<cmd>.json` | *(shared reference)* |
| prompts, responses, checks | — *(none kept)* | `<run>/manifest.json` |
| cost and timing | — *(none kept)* | `<run>/*.telemetry.json`, `eval/metrics.db` |

`eval/runs/`, `eval/campaigns/` and `eval/parity_diffs/` are gitignored: run directories embed
prompt text read from the private v1 checkout, so they are for local reading, not for committing
or sharing.
