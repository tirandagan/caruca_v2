---
name: caruca-v1-pipeline-reference
description: "Verified map of v1's five pipeline phases (modules, CLI commands, LLM boundary), llm.py internals, the Traces seam, latent bugs, and macOS-vs-WSL path corrections"
metadata:
  type: reference
---

Verified 2026-09-03 by reading v1 source directly (two exploration passes over the actual code, not
inferred from the paper or CLAUDE.md). Saves re-deriving the pipeline map in future sessions.

## Locations — per-machine paths (see [[dev-machine-paths]])

- On the Mac, v1's repo root is **`/Users/tirandagan/dev/stevens/caruca`** (package root
  `caruca/`, source `caruca/src/caruca/`). `caruca_v2`'s CLAUDE.md says `~/stevens/caruca` — that is
  the WSL PC's path, equally current on that machine (Tiran uses both). Resolve by platform;
  full mapping in [[dev-machine-paths]].
- The v1 **`CLAUDE.md` and `CODE_INSIGHTS.md` that v2's CLAUDE.md says to read do not exist in this
  clone** — they were local, uncommitted files on the WSL box. On the Mac, v1's only docs are its two
  READMEs and the architecture docstring in `ir/__init__.py`. Facts previously cited from
  CODE_INSIGHTS.md survive in [[caruca-v1-eval-tooling-notes]].

## The five phases

Entry point: `caruca = "caruca:main"` (pyproject) → **argparse** subparsers in `cli/__init__.py`.
~3,470 lines of hand-written Python + ~3,130 lines of committed specs (see
[[caruca-v1-loc-baseline]]). **Only phase 1 uses an LLM** — everything downstream is hand-coded.

| # | Phase | What it does | Modules (`src/caruca/`) | CLI |
|---|-------|--------------|--------------------------|-----|
| 1 | Syntax inference — **the only LLM step** | man page → GPT-4o via DSPy → syntax spec in the Python-embedded DSL (flags, options, arg types). 120 committed specs in `syntax_specs/` | `llm.py`, `ir/syntax.py` | `caruca syntax-spec CMD` (`--fetch` prints the committed spec, no LLM) |
| 2 | Configuration generation (hand-coded) | Spec → all concrete invocation strings (nested `itertools`) → environment configs (files/dirs/stdin each invocation needs) | `ir/string.py`, `ir/environment.py`, `ir/contents.py` | `caruca generate CMD` (`--number`, `--full`) |
| 3 | Isolated tracing (hand-coded) | Runs every invocation under `strace` in an overlayfs sandbox; records FS interactions + stdout/stderr/exit code → `outputs/CMD.json` | `tracer/tracer.py`, `tracer/strace_parser.py`, `tracer/data.py`; vendored `scripts/try` | `caruca trace CMD` |
| 4 | Specification derivation (hand-coded) | Traces JSON → inferred properties: inputs/outputs, parallelizability, stdin/args splittability (checked by rerunning on split inputs and comparing output) | `tracer/data.py` (`to_annotation`), `annotator/annotator.py` | `caruca annotate FORMAT CMD` |
| 5 | Adapters + oracle (hand-coded) | Renders the derived spec for PaSh / POSH / SaSh / ShellCheck (the ShellCheck adapter renders Haskell source); `oracle` checks how many real-world invocations the specs can parse | `annotator/{pash,posh,sash,shellcheck}.py`, `oracle.py` | `caruca annotate {pash\|posh\|sash\|shellcheck} CMD`, `caruca oracle` |

## Key mechanics (with line refs)

- **`llm.py`** (163 lines): model hardcoded `dspy.OpenAI(model="gpt-4o", seed=42, max_tokens=4096)`
  at `llm.py:109-114`, installed process-wide via `dspy.settings.configure`. Few-shot exemplars
  hardcoded `["touch", "rm", "mv", "ls"]` at `llm.py:116` — each pairs `doc_sources/man/<c>.txt`
  with the raw text of `syntax_specs/<c>.py`, compiled with `LabeledFewShot(k=4)` +
  `dspy.ChainOfThought`. Output code is regex-stripped from ``` fences (`extract_code`), validated
  by writing a temp file **in the CWD** and importing it; failures retried via
  `dspy.Suggest`/`Retry`/`assert_transform_module` — exactly the DSPy 2.x APIs removed in 3.x.
  The full retry mechanics (prompt layout, what the retry sends, and its dependence on the DSPy
  version) are in [[caruca-v1-llm-retry-mechanics]].
- **Spec discovery**: `syntax_specs/__init__.py::get_syntax_spec` imports
  `caruca.syntax_specs.<cmd>` reflectively and reads attribute `<cmd>_syntax_spec`; spaces become
  underscores (`git commit` → `git_commit.py`). Its `path` param is a **dotted module path** (e.g.
  `"caruca.pash_syntax_specs"`), not a filesystem path — the CLI's `--path` flag (`type=Path`)
  cannot work as written.
- **Trace ↔ annotate seam**: `tracer/data.py` last line —
  `Traces = RootModel[list[CommandInvocationTraceSet]]`; written by `cli/trace.py:45`, read by
  `cli/annotate.py:9`. The seam is leaky: `tracer/data.py` imports
  `RunSpecification`/`Parallelizability` from `annotator/annotator.py`.
- **Simplified spec dirs** for eval only: `pash_syntax_specs/` (54 specs), `posh_syntax_specs/`
  (16), selected by `trace --pash/--posh`. Bulk driver `caruca/run.sh` → `save/<cmd>.json`.
- The DSL "types" named in the prompt (`Signal`, `Glob`, `Duration`, … ~27 of them) are `MetaString`
  factories at `ir/syntax.py:363-425` — each is a small enumerated set of concrete probe values used
  during generation, not a real type system.
- Module sizes: `ir/` 1,249 lines, `tracer/` 946, `annotator/` 586, `cli/` 354; loose `llm.py` 163,
  `oracle.py` 120.
- **The syntax spec's standalone uses (added 2026-10-06).** Outside generation, the grammar feeds two
  things. (1) `oracle.py::oracle(invocation)`: `shlex`-splits a real command line, strips a leading
  `sudo`, loads the grammar, removes every recognised flag, option and argument, and returns the
  unrecognised remainder (empty means fully recognised). The paper's coverage study runs it over
  `eval/user-scripts/invocations.txt`. (2) The ShellCheck adapter emits a Haskell module named
  `Caruca.DangerousDelete`, with two checks. **Missing destination** (`annotator/__init__.py` around
  lines 80–105): derived when a usage has at least 2 positional `Path`s and the required-path count is
  at least 2. Every `Path`-typed *option* (for example `cp -t/--target-directory`) is collected as an
  exemption flag. The rendered check fires when an invocation has fewer arguments than required, no
  flags, and only static arguments. **Dangerous delete**: `DeletePattern`s pairing a predicate (flags
  plus argument count) with the arguments that tracing showed get deleted, so it depends on behaviour
  as well as syntax. Context: [[project-greenberg-caruca-purpose]].

## Latent v1 bugs / gotchas spotted (don't trip over these)

- `cli/generate.py:60`: `--full` calls `to_exec_env("split", "varied")` but the signature is
  `(prefix, stdin_variation, content_variation)` — `"split"` lands in `prefix`. Almost certainly a bug.
- Dead flags (parsed, never read): `syntax-spec --json`, `generate --output`,
  `annotate --hide-trivial`, `annotate --include-all-traces`. Dead files: `cli/oracle.py` (the real
  oracle subparser lives in `oracle.py`), `querier.py`.
- Sandbox path `/tmp/sandbox_outer/sandbox_inner` is hardcoded in **both** `tracer/tracer.py:59` and
  `tracer/data.py:266` and must stay in sync.
- Tracing hardcodes `timeout 2` and `strace -yfo … --trace=%file,%desc,getcwd`, a fixed `PATH`, and
  `SHELL=/bin/sh`.
- Isolation env var is `CARUCA_ISOLATION_METHOD` (`try` | `docker` | `none`) — the commit message
  that introduced it says `..._MODE`; the code reads `..._METHOD`.

**How to apply:** cite this instead of re-exploring v1 when mapping v2 components to v1 phases; the
naive-LLM baseline (v2 task 001) occupies phase 1's slot and should mirror `llm.py`'s choices
(exemplars, man-page inputs, DSL output) wherever a design choice exists.

**PaSh grammars vs main grammars, measured 2026-11-10 (Mac checkout, commit d80324073).** Folder
listings show 123 / 56 entries, but `__init__.py` + `__pycache__` are among them: **120 main, 54 PaSh**
grammars. Counting option entries (main spelling, `flag="…"` / `Flag("…")` text match, ±1 per file):
the 42 commands with both have **64** options in their PaSh grammars vs **923** in their main ones;
23 of 54 PaSh grammars have **no options** (rm, cp, mv, seq, tee, sha256sum …); 24 have **no file
operand** (cut: `-b -c -d -f`, stdin only); sort's has only `-m`; 12 have no main grammar (ffmpeg,
find, groff, gunzip, gzip, history, jq, nc, ps, read, readelf, xargs). So v1's committed PaSh files
(`save/*.json`) describe tiny grammars, not the paper's main ones.

## What v1's PaSh cases hold (read from source + `save/*.json`, 2026-11-10)

- `Specification.to_pash` (`annotator/annotator.py:77-155`) uses only each run's `inputs` and `outputs`.
  A deleted file is put in **both** `deleted` and `wrote_to` (`tracer/data.py:176-178`), so in a PaSh case a
  removed file is just "written"; the delete/write distinction survives only in the traces' `deletions`
  (used by the ShellCheck target). v1 records direction only (read / written), never PaSh's
  stream-vs-other distinction.
- An operand can be both read and written in one case (committed `save/rm.json`: `args[0]` in inputs and outputs).
- Entries across all committed `save/*.json` (counted 2026-11-10): `pipe:[…]` 4,972; `args[i]` 250; `stdout` 240;
  `stdin` 212; the rest are names that are **not** operands: files the command created (`split`'s `xaa`…,
  `csplit`'s `xx00`…), paths inside an operand directory (`relpath_2/relpath_1`, from cp/mv into a dir), placeholder
  names not mapped to an operand (`relpath_1.jpg`, `abspath_1.jpg`, 69 each), iconv charset words (`ASCII/TRANSLIT`).
  PaSh's current IO record has slots only for operands, option values, stdin and stdout, so these have no place there.
- `save/gzip.json` is an empty (0-byte) file.
- **`pipe:[…]` entries are a 2024 artefact, not current behaviour (checked 2026-11-10).** Committed
  `save/cut.json` (commit `6ceda7586`, 2024-12-08) has 350 `pipe:[…]` entries. Tracing cut's PaSh grammar
  with today's v1 (d80324073 + branch `pash-python-annotations`, Lima Ubuntu 24.04) and running `annotate pash`
  gives none: every case's input is just `stdin`. So the committed `save/*.json` cannot stand in for current
  v1 output; compare with a fresh `annotate pash` on the same traces (`save_pash_py/.../v1_pash.json`).
