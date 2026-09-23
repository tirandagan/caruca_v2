# caruca_v2

A research project, not a product. It asks how much of **Caruca**'s specification-mining
pipeline an LLM can carry out, and measures the answer against the original implementation
("v1") and against human ground truth.

> **To run the pipeline:** [Pipeline Usage Guide](ai_docs/docs/caruca_v2_pipeline_usage_guide.md)
> — installation, every command, real terminal output, and how to handle failures.
>
> **To look at what it produced:** [the execution console](console/README.md) — a local web page
> that replays any run in a real terminal, compares v1 against v2 stage by stage, and shows
> where every number came from. `cd console && npm install && npm run dev`.

---

## Provenance: what v1 established, and what v2 asks

Caruca is a system for mining partial specifications for opaque shell commands. It was
built by Lamprou, Jung, Keoliya, Lazarek, Kallas, Greenberg, and Vasilakis
([arXiv:2510.14279](https://arxiv.org/abs/2510.14279), October 2025), and it works: 59 of
60 commands annotated correctly across four downstream consumers, and 116 of 120 syntax
specifications matching hand-built ground truth exactly.

v1 reaches those numbers with a deliberately narrow use of an LLM. A model reads a man page
and emits a syntax specification; **every stage after that is hand-written code** —
configuration generation, sandboxed execution under `strace`, specification derivation, and
the four output adapters. The paper is explicit: "the LLM solely generates the syntax
specification — it is not involved in any remaining components."

That boundary is the opening this project works in. v2 replicates each of v1's stages with
an LLM standing where the procedural code stands, plus a deliberately naive single-prompt
control, and measures all three against each other on six dimensions: correctness, cost,
coverage, reproducibility, the v1→v2 delta per dimension, and how much hand-encoded logic
is replaced for equal-or-better output.

Two properties of the design follow from that goal:

- **v1 is read at runtime, never imported and never copied.** It is a separate, private
  repository; caruca_v2 shells out to it and reads its corpus from `CARUCA_V1_ROOT`. None of
  its text lives in this repository.
- **v1 validates v2's output, not the other way round.** Every artifact a stage produces is
  checked by running it through v1's own interpreter and pydantic models. A failed
  validation is recorded and the run exits non-zero — it never triggers a retry, because a
  control that quietly re-asks until it succeeds has stopped being a control.

`CLAUDE.md` is the orientation document for the project as a whole; planning documents live
in `ai_docs/prep/`, findings in `ai_docs/analysis/`.

---

## The pipeline at a glance

| # | Command | In | Out |
|---|---|---|---|
| 1 | `naive-llm` | a command's documentation | syntax specification (`<cmd>.py`) |
| 2 | `generate` | a syntax specification | invocations + configurations |
| 3 | `trace` | configurations | v1-compatible traces |
| 4 | `annotate` | traces | one consumer's annotation |
| 5 | `metrics rebuild` | run directories | `eval/metrics.db` |

Plus three measurement tools that make no model call and cost nothing: `score`
(argument-by-argument spec comparison), `sweep --dry-run` (enumerate a campaign before paying
for it), and `report` (aggregate a finished campaign, with a percent change only where one is
valid). The console calls `report` rather than recomputing anything, so the two cannot
disagree.

Each stage defaults its input to v1's own committed artifact, so every stage is measurable
independently; pass `--docs`, `--spec`, `--configs`, or `--traces` to chain them instead.

---

## Install

Three independent parts. Install only what you need.

| part | what it is | install | needs |
|---|---|---|---|
| **The pipeline** (`caruca-v2`) | the four stages and the measurement harness | `uv sync` | Python 3.12+, [`uv`](https://docs.astral.sh/uv/), a v1 checkout, an OpenRouter key |
| **The execution console** (`console/`) | a local web page for replaying, comparing and explaining runs | `cd console && npm install` | Node 22.5+, and the pipeline installed |
| **The document pipeline** (`scripts/md-to-pdf/`) | turns Markdown into the project's branded PDFs | `npm install` at the root | Node |

### The pipeline

**With Claude Code** — the repository ships two slash commands:

```
/setup_pipeline      detect this machine, validate every prerequisite, install what is missing
/run_pipeline        walk the pipeline stage by stage, with a cost gate before each model call
```

`/setup_pipeline` detects which of four machine shapes you are on — macOS host, WSL2, native
Linux, or inside a Linux guest — because every install recipe differs between them. It will
also clone and configure the v1 checkout if this machine does not have one. They are plain
Markdown in `.claude/commands/`, readable and followable by hand.

**By hand:**

```sh
uv sync
cp .env.example .env      # then fill in OPENROUTER_API_KEY and CARUCA_V1_ROOT
uv run pytest             # check it works; nothing in the suite spends money
```

The CLI is then at `.venv/bin/caruca-v2`. A v1 checkout with its own virtualenv is required
for anything beyond `--help`; see the
[guide](ai_docs/docs/caruca_v2_pipeline_usage_guide.md#the-v1-checkout).

**Tracing needs a Linux kernel.** On macOS that means the Lima VM named `caruca`, and v1's
`annotate` cannot run on macOS at all. `/setup_pipeline` sets this up; the operating
instructions are in `ai_docs/docs/`.

### The execution console

```sh
cd console
npm install          # also fixes a file permission npm leaves broken
npm run dev          # then open http://127.0.0.1:4317
```

It reads the evidence already in `eval/` and needs no API key. It binds to `127.0.0.1` only
and makes no outside requests. Full details, including what to do when something goes wrong,
in [`console/README.md`](console/README.md).

### The document pipeline

```sh
npm install                              # at the repository root
npm run convert -- <input.md> [output.pdf] [--title "…"] [--subtitle "…"]
```

Produces the branded PDFs that go to advisors alongside presentations. It shares its visual
identity with the console: both are built from the `caruca-design` skill.

## Quick start

```sh
caruca-v2 naive-llm mkdir --model openai/gpt-4o --temperature 0.0   # stage 1
caruca-v2 score mkdir --spec eval/runs/<run-id>/mkdir.py            # free: how good was it?
caruca-v2 metrics rebuild                                           # free: refresh the database
```

`--model` and `--temperature` are required on every stage on purpose: no run is recorded
without the configuration that produced it being stated.

Costs, isolation requirements, and every failure mode are in the
[Pipeline Usage Guide](ai_docs/docs/caruca_v2_pipeline_usage_guide.md).

Then look at what happened:

```sh
cd console && npm run dev     # http://127.0.0.1:4317
```

The run appears in the list. Opening it shows what it cost, what it sent, what came back, and
— for a run the console started itself — a replay of the terminal.

---

## Repository layout

Every folder, and which README covers it in depth.

| Path | Contents | Its own README |
|---|---|---|
| `src/caruca_v2/` | the CLI, the four stages, the v1 boundary, telemetry, the measurement harness (`src/caruca_v2/harness/`) | — |
| `console/` | the execution console: a local Next.js page that replays runs, compares v1 with v2, and explains every number | [`console/README.md`](console/README.md) |
| `prompts/` | every instruction given to a model, as Markdown, one directory per stage; loaded verbatim at runtime | [`prompts/README.md`](prompts/README.md) |
| `tests/` | the Python suite. No test reaches the network; none needs a v1 checkout | — |
| `eval/` | the evidence: run directories, the metrics database, campaign ledgers, generated drill-downs | — |
| `campaigns/` | campaign definitions — the grids `sweep` runs (`c0_*` pilot, `p1_*` parity study) | — |
| `scripts/` | `parity_diff.py` (the per-command v1-vs-v2 drill-down) and `md-to-pdf/` (the branded PDF pipeline) | — |
| `ai_docs/` | everything this project has written down | [`ai_docs/README.md`](ai_docs/README.md) |
| `ai_docs/analysis/` | findings produced by this project | [`ai_docs/analysis/README.md`](ai_docs/analysis/README.md) |
| `ai_docs/refs/` | source material we did not write, including the paper. Third-party, excluded from this licence | — |
| `ai_docs/tasks/` | numbered task documents for multi-session work | — |
| `ai_docs/prep/` | planning: master idea, architecture, telemetry schema, roadmap | — |
| `memory/` | cross-session project memory | `memory/MEMORY.md` is the index |
| `.claude/commands/` | slash commands, including `/setup_pipeline` and `/run_pipeline` | — |
| `.claude/skills/` | `caruca-design` (the binding visual system), `task-creator`, `diagram` | — |

### What is committed, and what is not

Worth knowing before you go looking for something that is not there:

- **`eval/runs/` and `eval/metrics.db` are committed** (since `eedd91a`, 15 September 2026).
  The evidence travels with the repository.
- **`eval/campaigns/` is not.** The scored campaign ledgers are local to whichever machine ran
  them. The console works without them; its comparison screens say so rather than showing
  empty tables.
- **v1's corpus is never copied here.** Man pages, syntax specifications, fixtures and
  ground-truth annotations are read from the v1 checkout at runtime and stay there.

### Where to read next

| If you want to… | Read |
|---|---|
| run the pipeline | [Pipeline Usage Guide](ai_docs/docs/caruca_v2_pipeline_usage_guide.md) |
| look at results, replay a run, compare v1 and v2 | [`console/README.md`](console/README.md) |
| find out what this project has concluded so far | [`ai_docs/analysis/README.md`](ai_docs/analysis/README.md) |
| find any document at all | [`ai_docs/README.md`](ai_docs/README.md) |
| see exactly what a model is asked | [`prompts/README.md`](prompts/README.md) |
| understand the original system | `ai_docs/refs/caruca_white_paper.md`, and v1's own checkout |
| pick up a piece of work in progress | `ai_docs/tasks/` |

## Development

```sh
uv run pytest                      # the Python suite
uv run ruff check .

cd console && npm test             # the console's suite
cd console && npm run typecheck
```

Two rules the Python suite enforces rather than documents: no test can reach OpenRouter, and
no test needs a v1 checkout — it builds a fake one from text written for the purpose. The
console's suite runs against the committed run directories, so it checks the readers against
real evidence rather than fixtures; the tests that need campaign ledgers skip themselves with
a message when those are not on the machine.

## License

This repository — the code, the prompts, the templates, the skills, and the documentation —
is licensed under the **[PolyForm Noncommercial License 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0)**.
Full terms and scope in [`LICENSE-TEMPLATES.md`](LICENSE-TEMPLATES.md).

**Copyright © 2026 Tiran Dagan.**
Required notice: `Copyright 2026 Tiran Dagan (https://github.com/tirandagan/caruca_v2)`

In plain terms:

- **Permitted.** Any noncommercial purpose — expressly including academic research,
  teaching, personal study, and use by educational institutions, public research
  organizations, and government institutions, regardless of how that work is funded. You may
  modify it, build on it, and redistribute it.
- **Prohibited.** Any commercial use, by anyone, in any form.
- **Required.** Anyone who receives any part of this from you must also receive a copy of the
  terms (or the URL above) **and** the required-notice line. It must survive redistribution.

This is a **source-available**, not an open-source, license: not OSI-approved, not Creative
Commons. For commercial use, contact the copyright holder for a separate written license.

Two exclusions:

| Path | Status |
|---|---|
| `ai_docs/refs/` — the Caruca white paper and other reference material | Third-party work under its own terms; included for reference, redistributed under no license granted here |
| `.claude/skills/impeccable/` | Third-party software under its own terms |

**Caruca v1 is not covered and is not relicensed by anything here.** It is a separate,
private, unlicensed repository that this project reads at runtime and copies none of. Its
corpus — man pages, syntax specifications, fixtures, ground-truth annotations — cannot be
redistributed with results, so plan any public release around that.
