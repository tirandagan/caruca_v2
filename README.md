# caruca_v2

A research project, not a product. It asks how much of **Caruca**'s hand-written
specification-mining pipeline an LLM can replace, and measures the answer against the
original implementation ("v1") and against human ground truth.

Planning documents live in `ai_docs/prep/`; `CLAUDE.md` is the orientation document for
the project as a whole. What follows covers the Python CLI only.

## Install

Requires Python 3.12 or newer and [`uv`](https://docs.astral.sh/uv/).

```sh
uv sync
cp .env.example .env      # then fill in the two required values
```

The CLI is then available as `.venv/bin/caruca-v2` (or `caruca-v2` with the venv active).

## Environment

| Variable | Required | Meaning |
|---|---|---|
| `OPENROUTER_API_KEY` | yes | The single key. Every candidate model is reached through the OpenRouter gateway, so one code path serves them all. |
| `CARUCA_V1_ROOT` | yes | Path to the caruca v1 checkout — the repository root, the directory containing `caruca/`. Per-machine: `~/dev/stevens/caruca` on the Mac, `~/stevens/caruca` on the WSL PC. |
| `CARUCA_V2_LOG_CONVERSATION` | no | Set to `1` to write `conversation.jsonl` into every run directory, same as `--log-conversation`. |

v1 is read at runtime and never imported: it is a separate, private repository, and none
of its text is copied into this one.

## Usage

Every subcommand is a thin wrapper over one typed function in `src/caruca_v2/stages/`,
so anything the CLI can do can also be called directly.

```sh
# Stage 1 (the naive control): documentation in, a v1-DSL syntax specification out.
caruca-v2 naive-llm mkdir --model openai/gpt-4o --temperature 0.0

# Stage 2: a syntax specification in, the invocations it allows and their environments out.
caruca-v2 generate mkdir --model openai/gpt-4o --temperature 0.0

# Stage 3: run each configuration in a prepared workspace, record what the command did.
caruca-v2 trace cat --limit 5 --model openai/gpt-4o --temperature 0.0

# Stage 4: traces in, one consumer's annotation out (pash | posh | sash | shellcheck).
caruca-v2 annotate pash ls --model openai/gpt-4o --temperature 0.0

# Regenerate the metrics database from the run directories on disk.
caruca-v2 metrics rebuild
```

Each stage defaults its input to the deterministic v1-sourced artifact, so comparisons
are reproducible; point `--docs`, `--spec`, `--configs`, or `--traces` at an earlier
stage's output to chain the pipeline instead.

### Two things that spend money, and two that are refused

`trace` opens one model session per configuration, so `--limit` (default 5) is the cost
brake; running a full configuration set is an explicit choice. `generate` and `annotate`
continue across turns **only** when the token cap cut a response off — a model that stops
on its own is never asked for more.

Destructive commands (`rm`, `mv`, `chmod`, and similar) are refused outright by `trace`
unless `--isolation lima` runs them inside the Lima VM. On macOS, v1's own annotator
cannot run at all — it resolves paths against a hardcoded `/tmp` prefix that macOS
rewrites to `/private/tmp` — so the v1 side of an annotation diff needs
`--v1-runner lima`.

`--model` and `--temperature` are required on purpose. They stay explicit until the
one-time configuration selection freezes a choice, so no run can be recorded without the
configuration that produced it being stated.

Exit codes: `0` when a specification was produced *and* validated by v1, `1` when the run
completed but its output was unusable (recorded, not retried), `3` on a configuration
problem such as a missing key or an unreachable v1 checkout.

## What a run leaves behind

```
eval/runs/2026-09-04T101530Z_mkdir_a1b2/
├── mkdir.py                  # the stage's output, in v1's own format
├── mkdir.telemetry.json      # tokens, cost, wall-clock, model, seed, prompt hash
├── manifest.json             # the full request, the raw response, the checks that ran
└── conversation.jsonl        # only with --log-conversation
```

The multi-turn stages write one telemetry sidecar per model turn
(`mkdir.turn-00.telemetry.json`, …), all sharing the run id. `manifest.json` carries the
stage's `checks`: the invocation set-diff for `generate`, the tool audit trail and
per-session record for `trace`, the two annotation diffs for `annotate`.

Whatever a stage produces is validated by **v1 itself**, in a subprocess against v1's own
interpreter and pydantic models — never by our imitation of its formats. A failed
validation is recorded and the run exits non-zero; it never triggers a retry, because a
weak control that quietly re-asks until it succeeds is no longer a control.

Each completed run also appends a row to `eval/metrics.db`, a SQLite view over those
files for cross-run queries. The JSON files are the source of truth; the database is a
cache, and `caruca-v2 metrics rebuild` regenerates it from them.

`eval/runs/` and `eval/metrics.db` are gitignored. Run directories embed prompt text read
from the private v1 checkout, and a binary database does not merge across machines. What
gets committed is the write-up in `ai_docs/analysis/`, which ties back to local runs by
`prompt_hash`.

## Development

```sh
uv run pytest          # the whole suite; every test mocks the model, none spends money
uv run ruff check .
```

Two rules the test suite enforces rather than documents: no test can reach OpenRouter,
and no test needs a v1 checkout (it builds a fake one from text written for the purpose).
