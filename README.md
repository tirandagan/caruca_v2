# caruca_v2

A research project, not a product. It asks how much of **Caruca**'s specification-mining
pipeline an LLM can carry out, and measures the answer against the original implementation
("v1") and against human ground truth.

> **📖 [Pipeline Usage Guide](ai_docs/docs/pipeline_usage_guide.md)** — installation, every
> command, real terminal output, and how to handle failures. Start there to actually run
> anything.

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

Plus two measurement tools that make no model call and cost nothing: `score`
(argument-by-argument spec comparison) and `sweep --dry-run` (enumerate a campaign before
paying for it).

Each stage defaults its input to v1's own committed artifact, so every stage is measurable
independently; pass `--docs`, `--spec`, `--configs`, or `--traces` to chain them instead.

---

## Install

**With Claude Code** — the repository ships two slash commands:

```
/setup_pipeline      detect this machine, validate every prerequisite, install what is missing
/run_pipeline        walk the pipeline stage by stage, with a cost gate before each model call
```

`/setup_pipeline` detects which of four machine shapes you are on — macOS host, WSL2,
native Linux, or inside a Linux guest — because every install recipe differs between them.
It will also clone and configure the v1 checkout if this machine does not have one. They
are plain Markdown in `.claude/commands/`, readable and followable by hand.

**Manually** — requires Python 3.12+ and [`uv`](https://docs.astral.sh/uv/):

```sh
uv sync
cp .env.example .env      # then fill in OPENROUTER_API_KEY and CARUCA_V1_ROOT
```

The CLI is then at `.venv/bin/caruca-v2`. A v1 checkout with its own virtualenv is required
for anything beyond `--help`; see the
[guide](ai_docs/docs/pipeline_usage_guide.md#the-v1-checkout).

## Quick start

```sh
caruca-v2 naive-llm mkdir --model openai/gpt-4o --temperature 0.0   # stage 1
caruca-v2 score mkdir --spec eval/runs/<run-id>/mkdir.py            # free: how good was it?
caruca-v2 metrics rebuild                                           # free: refresh the database
```

`--model` and `--temperature` are required on every stage on purpose: no run is recorded
without the configuration that produced it being stated.

Costs, isolation requirements, and every failure mode are in the
[Pipeline Usage Guide](ai_docs/docs/pipeline_usage_guide.md).

---

## Repository layout

| Path | Contents |
|---|---|
| `src/caruca_v2/` | the CLI, the four stages, the v1 boundary, telemetry, the harness |
| `prompts/` | every prompt, as Markdown, one directory per stage |
| `ai_docs/docs/` | operating instructions for v2 and for v1 |
| `ai_docs/analysis/` | findings produced by this project |
| `ai_docs/prep/` | planning: master idea, architecture, telemetry schema, roadmap |
| `ai_docs/tasks/` | numbered task documents for multi-session work |
| `.claude/commands/` | slash commands, including setup and pipeline walkthrough |
| `eval/` | run directories, campaign ledgers, the metrics database (gitignored) |
| `memory/` | cross-session project memory; `MEMORY.md` is the index |

## Development

```sh
uv run pytest          # the whole suite; every test mocks the model, none spends money
uv run ruff check .
```

Two rules the test suite enforces rather than documents: no test can reach OpenRouter, and
no test needs a v1 checkout — it builds a fake one from text written for the purpose.

## License

The research code is released under **[THE CRAPL v0 BETA 1](https://matt.might.net/articles/crapl/)**
— Matthew Might's Community Research and Academic Programming License, written for exactly
this situation: academic code whose purpose is to make published claims reproducible, not to
be a polished artifact. Full text in [`CRAPL-LICENSE.txt`](CRAPL-LICENSE.txt).

Its preamble is the reason it was chosen:

> Science thrives on openness. In modern science, it is often infeasible to replicate claims
> without access to the software underlying those claims. […] So, let's release the ugly.
> And, let's be proud of that.

Three of its terms have real consequences, so read them rather than assuming:

- **It is not an open-source license.** Term III.5 reserves all rights not expressly granted.
  The permissions in section IV are about *validating scientific claims* — published ones,
  ones under peer review, and novel ones where you make a good-faith effort to notify the
  author first. It is not a general grant to use this code for whatever you like.
- **Publishing obliges you to release.** Under IV.4, if you publicly release claims or data
  generated by this program, you release your inputs and your modifications too, under the
  same license.
- **Support requests "will be discarded with extreme prejudice"** (III.4). That is the
  license's joke and also its literal meaning: this is a PhD research pipeline, not a
  maintained product.

| Scope | License |
|---|---|
| Research code and its documentation — `src/`, `tests/`, `prompts/`, `scripts/`, `eval/`, and `ai_docs/` outside the template directories | [CRAPL v0 Beta 1](CRAPL-LICENSE.txt) |
| Prompt templates and agent skills — `ai_docs/prep_templates/`, `ai_docs/dev_templates/`, `.claude/commands/`, and the `diagram` / `caruca-design` / `task-creator` skills | [PolyForm Noncommercial 1.0.0](https://polyformproject.org/licenses/noncommercial/1.0.0), see [`LICENSE-TEMPLATES.md`](LICENSE-TEMPLATES.md) |
| Third-party material — `ai_docs/refs/`, `.claude/skills/impeccable/` | Their own terms; redistributed under neither of the above |

**One thing the CRAPL cannot reach.** Caruca v1 is a separate, private, unlicensed
repository. This project reads it at runtime and copies none of it, so nothing here
relicenses it — and IV.4's obligation to release your inputs cannot be satisfied for inputs
drawn from v1's corpus until v1 itself is released. Plan any public release of results
around that.
