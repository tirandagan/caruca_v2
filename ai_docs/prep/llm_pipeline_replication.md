# LLM Pipeline Replication — shared design for tasks 002-004

> **Created:** 2026-09-03, from Tiran's direction. Governs the task series that replicates
> caruca v1's hard-coded pipeline stages with minimally-instructed LLM calls (tasks
> `002_llm_config_generation`, `003_llm_execution_tracing`, `004_llm_annotation`).
> Task 001 (the naive one-prompt control) shares this document's prompt-storage, telemetry,
> and logging conventions but none of its tool machinery.

## What this series is, and how it relates to the control

Two experiments now run side by side, and they answer different questions:

1. **The control (task 001, per Prof. Eiers):** one simple prompt replacing v1's *only*
   LLM step. Question: *how much better is v1's engineered pipeline than an off-the-shelf
   prompt?*
2. **This series (tasks 002-004, Tiran's direction 2026-09-03):** every remaining
   hard-coded stage of v1 replaced by a minimally-instructed LLM, given real tools where
   the stage needs to act on the world. Question: *how much of v1's ~3,300 lines of
   hand-written pipeline logic can a simply-instructed LLM replace, at what fidelity and
   cost?* This directly serves the hand-encoded-logic-reduction evaluation criterion
   (criterion 6 in `master_idea.md`).

For advisor-facing narrative: the series *extends* the agreed comparison — the control
remains the first-run deliverable, and every stage here is measured against its v1
counterpart, so v1 stays the reference point throughout.

## Design principles

1. **Minimal instruction.** Each stage's prompt states only: what the **input** is, what
   the **expected behavior** is, what the **output** should be, and what **format** it must
   take. No algorithms, no step-by-step recipes, no "here's how v1 does it" hints. If the
   LLM can't do the stage from that, that *is* the result — we record it, we don't coach
   past it. (Same spirit as the Eiers guardrail on the control: don't min-max.)

2. **v1's file seams are the contracts.** Every stage reads and writes v1's exact file
   formats, so any single LLM stage can be dropped into an otherwise-v1 pipeline and
   measured in isolation — and v1's own outputs double as inputs for our stages
   (e.g. run our annotator on v1's committed trace files). Contract table below.

3. **Prompts are files, not code.** All prompt text lives in a repo-root `prompts/`
   folder as Markdown, loaded verbatim at runtime:

   ```
   prompts/
   ├── README.md                 # conventions (this layout, placeholder syntax)
   ├── syntax_spec/              # stage 1 — task 001
   │   ├── system.md
   │   └── user.md
   ├── generate/                 # stage 2 — task 002
   ├── trace/                    # stage 3 — task 003
   └── annotate/                 # stage 4+5 — task 004
   ```

   - Placeholders use `{{name}}` (e.g. `{{command}}`, `{{man_page}}`,
     `{{few_shot_examples}}`); assembly is a pure string substitution, so identical inputs
     always produce an identical prompt (`prompt_hash` = SHA-256 of the assembled text).
   - The committed files contain **only our own text**. Anything sourced from v1 (man
     pages, spec text, fixture contents) is injected at runtime from `CARUCA_V1_ROOT` —
     never committed (v1 is private and unlicensed).
   - The folder doubles as the paper appendix: the complete instruction set for the
     system, human-readable.

4. **Hard enforcement, not prompt politeness.** Constraints appear in the prompt ("You may
   only use the command `cat`. Do not use any other command.") **and** are enforced in
   code: the executor rejects any tool call that violates them. The prompt asks; the code
   guarantees.

5. **v1-faithful environments — no improvements.** When a stage needs a working directory
   with files (stage 3 especially), our code materializes it **exactly as v1's
   environment setup would**: the same directory layout, the same file names, the same
   fixture contents (v1's `data/` payloads — `human_1.txt`, `math_1.txt`, `json.json`,
   etc. — read from the v1 checkout at runtime), the same stdin variations. Explicit
   Tiran directive (2026-09-03): do not "improve" the setup with extra empty files,
   subfolders, or richer fixtures — comparability requires identical inputs.

6. **Measure everything.**
   - One telemetry record per LLM call (the task-001 sidecar shape, with `component` =
     `llm_pipeline` and a `stage` field); agentic stages emit **multiple** records per run
     (one per model turn) sharing a `run_id`, plus a roll-up in the run manifest.
   - Every record also lands as a row in `eval/metrics.db` (task 001's database).
   - **Conversation trace logging, off by default, one switch to turn on**
     (`--log-conversation` flag or `CARUCA_V2_LOG_CONVERSATION=1`): writes
     `conversation.jsonl` into the run directory — every message in order (system, user,
     assistant, tool call, tool result), verbatim. This is both a debugging aid and
     reproducibility evidence (consistency criterion 4).

7. **The engine is our own loop over OpenRouter.** No agent framework. One small,
   auditable loop: send messages → model replies (possibly with tool calls) → execute the
   allowlisted tool(s) → append results → repeat, up to a hard turn cap. Works identically
   for every model behind the one OpenRouter key, so cross-model comparison covers the
   tool-using stages too, and every message is ours to log and count.

## Stage contracts (the v1 seams)

| Task | Stage | CLI | Input (v1 format) | Output (v1 format) | Replaces (v1 modules, LOC) | Compared how |
|---|---|---|---|---|---|---|
| 001 | Syntax spec | `caruca-v2 naive-llm CMD` | man page text | `<cmd>.py` DSL spec | `llm.py` scaffolding (~163) | spec diff vs ground truth (`eval/cmp_specs.py`) |
| 002 | Config generation | `caruca-v2 generate CMD` | `<cmd>.py` DSL spec (ours or v1's committed one) | invocation list + environment configs, JSON-serialized in the `CommandConfig` shape used inside v1's Traces JSON | `ir/string.py` + `ir/environment.py` + `ir/contents.py` + `ir/mixin.py` (~715) | set-diff of invocation strings vs `caruca generate CMD`; structural diff of configs |
| 003 | Execution + tracing | `caruca-v2 trace CMD` | configs JSON (ours or derived from v1) | **Traces JSON that validates against v1's `Traces` pydantic model** (checked via v1's venv, subprocess) | `tracer/tracer.py` + `strace_parser.py` (~675) | field-by-field diff vs v1's strace-derived `outputs/CMD.json` on identical configs |
| 004 | Annotation + adapters | `caruca-v2 annotate FORMAT CMD` | Traces JSON (ours **or v1's own** `outputs/CMD.json`) | PaSh / POSH / SaSh / ShellCheck annotation in v1's output formats | `tracer/data.py::to_annotation` + `annotator/` (~850) | diff vs `caruca annotate` on identical traces; diff vs `benchmarks/annotations/` ground truth |

Build order 002 → 003 → 004, but each task also runs standalone by consuming v1-produced
input files — no stage blocks on another stage being good.

## The tool surface (stage 3, hard-enforced)

- **`run_command(argv)`** — the *only* way the model touches a shell. Enforced in code:
  `argv[0]` must be the command under test (else the call is rejected with an error the
  model sees); cwd is the throwaway workspace; `timeout 2` per execution (v1's value);
  stdout, stderr, and return code are captured and returned.
- **Observation tools implemented in Python, not shell** — `list_dir`, `read_file`,
  `stat_path`, all jailed to the workspace. This is how the model inspects state
  before/after execution without violating "only `cat`": observation never spawns a
  binary. (v1 observes via strace; our model observes via these tools — the fidelity gap
  between LLM-observed and strace-observed interactions is itself a measured result.)
- **Workspace lifecycle:** fresh temp directory per invocation, materialized per
  principle 5, deleted afterward (`--keep-workspace` preserves it for debugging). No
  network access is provided by any tool. `run_command` reproduces v1's execution
  environment: `timeout 2`, `PATH=/usr/bin:/bin:/usr/local/sbin:/usr/local/bin`,
  `SHELL=/bin/sh`.
- **The LLM observes; our code packages.** The model's output is the per-invocation trace
  entries (interactions + stdout/stderr/rc). Assembling v1's Traces envelope around them
  — and rewriting workspace paths into v1's sandbox namespace
  (`/tmp/sandbox_outer/sandbox_inner`, which v1's annotator expects and hardcodes) — is
  deterministic plumbing done in code. Format compliance where it's mechanical is not the
  experiment; observation and derivation are.
- **Safety staging (Tiran, 2026-09-03; updated same day):** harmless commands run in
  throwaway dirs directly on the Mac. `rm`-class/destructive commands run inside the Lima
  VM `caruca` (Ubuntu 24.04, working v1 tracing environment — see
  `memory/mac_lima_tracing_env.md`), which also produces the strace ground truth for the
  fidelity comparison locally. macOS `sandbox-exec` noted as possible extra hardening for
  the on-Mac tier.

## CLI conventions (all subcommands)

One entry point, `caruca-v2`, argparse subcommands, every subcommand a thin wrapper over
one typed function in `stages/`. Shared flags, identical everywhere they apply:

| Flag | Meaning | Default |
|---|---|---|
| `--model ID` | OpenRouter model ID, recorded verbatim | the frozen config (explicit until frozen) |
| `--seed N` | passed through; honesty flag recorded where unsupported | `42` (v1's value) |
| `--temperature T` | recorded in `decoding_params` | the frozen config |
| `--out DIR` | run-directory root | `eval/runs/` |
| `--log-conversation` | write `conversation.jsonl` (also `CARUCA_V2_LOG_CONVERSATION=1`) | off |
| `--plain` | no color/animation; line-oriented output (auto when not a TTY) | auto |
| `--limit N` | process only the first N items (configs, traces) — the cost brake | stage-specific, small |
| `--max-turns N` | hard cap on model turns (loop stages and continuations) | stage-specific |

Per-stage input overrides (each stage names its main input explicitly; defaults favor the
deterministic v1-sourced artifact so comparisons are reproducible):

| Stage | Input flag | Default |
|---|---|---|
| `naive-llm CMD` | `--docs PATH` | v1's `doc_sources/man/<cmd>.txt` |
| `generate CMD` | `--spec PATH` | v1's committed `syntax_specs/<cmd>.py` |
| `trace CMD` | `--configs PATH` | latest `generate` output for CMD under `--out` |
| `annotate FORMAT CMD` | `--traces PATH` | v1's `outputs/<cmd>.json` (the A/B-on-identical-traces default) |

Plus `caruca-v2 metrics rebuild`. Exit codes: `0` success-and-validated, non-zero
otherwise, always with the failure recorded in the run manifest.

## Source layout — keep it small

One package, one module per stage, one module per shared concern. Everything that touches
the v1 checkout goes through **one** boundary module (`v1.py`) so the
subprocess-only/no-committed-v1-text rules live in exactly one place:

```
src/caruca_v2/
├── cli.py            # argparse only; dispatches to stages/*.run()
├── stages/
│   ├── syntax_spec.py   # task 001   (each exposes one typed run(...) function)
│   ├── generate.py      # task 002
│   ├── trace.py         # task 003
│   └── annotate.py      # task 004
├── v1.py             # ALL v1-checkout access: man pages, exemplars, fixtures,
│                     #   venv-subprocess validation, reference outputs
├── prompting.py      # load prompts/<stage>/*.md, substitute {{placeholders}}, hash
├── llm.py            # OpenRouter client + the tool loop + per-turn telemetry capture
├── workspace.py      # stage-3 workspace materialization + path-namespace rewrite
├── tools.py          # stage-3 executor: run_command allowlist + jailed observers
├── telemetry.py      # record models, sidecar/manifest writers
├── metrics_db.py     # eval/metrics.db append + rebuild
└── ui.py             # all terminal presentation (see below)
```

Simplicity rules: no plugin systems, no config objects threaded everywhere, no
abstraction until the third caller exists; a stage module reads top to bottom as the
experiment it implements.

## Terminal UX (Tiran, 2026-09-03)

The CLI should be pleasant to read, not raw prints: color, progress bars, spinners,
box/character graphics for summaries. Implementation: the **`rich`** library (one pinned
dependency — hand-rolled ANSI/cursor control would be its own project), wrapped entirely
inside `ui.py`:

- live progress bar across configs/commands (stage 3 especially: `config 14/68 · $0.42 ·
  3 turns`), spinners during model calls, a summary table per run (tokens, cost,
  wall-clock, validation ✓/✗)
- color for state (green validated, red failed, yellow deferred), never for meaning that
  isn't also in the text
- `--plain` (and any non-TTY stdout) degrades to plain line output automatically
- **presentation only**: `ui.py` contains zero logic, and machine-readable outputs
  (sidecars, manifests, metrics.db, `conversation.jsonl`, stage output files) are never
  routed through it

## Open questions (settled inside each task, not here)

- The exact behavioral wording of each stage's prompt files (drafted at implementation,
  reviewed by Tiran before first real run).
- Stage 2 enumeration limits: v1 defaults to `--max-arity 2` — the prompt must state the
  same bound; how the LLM handles combinatorially huge commands (`convert`) is a result.
- The observed-vs-strace fidelity protocol for stage 3 (which Traces fields an LLM can
  realistically produce, and how partial credit is scored).
