<!-- ATTRIBUTION-NOTICE:START -- required by LICENSE-TEMPLATES.md, do not remove -->
<!--
 caruca_v2 agent skill: Retrieve caruca run.
 Created by Tiran Dagan. Copyright (c) 2026 Tiran Dagan.
 Licensed under the PolyForm Noncommercial License 1.0.0
 https://polyformproject.org/licenses/noncommercial/1.0.0
 Noncommercial use only. Commercial use is prohibited.
-->
<!-- ATTRIBUTION-NOTICE:END -->

# The data model

What lives in each artifact, so you can reach a figure the CLI does not already print.
Everything here was read off the files rather than inferred from documentation.

## Contents

- [The four stages](#the-four-stages)
- [Headline metrics](#headline-metrics)
- [`manifest.json` — one run](#manifestjson--one-run)
- [Per-stage `checks`](#per-stage-checks)
- [`ledger.jsonl` — one scored cell](#ledgerjsonl--one-scored-cell)
- [Per-stage `score`](#per-stage-score)
- [`metrics.db`](#metricsdb)
- [Campaign families](#campaign-families)
- [Counting traps](#counting-traps)

## The four stages

| # | slug | in → out | replaces in v1 |
|---|---|---|---|
| 1 | `syntax_spec` | man page → syntax specification (v1's Python DSL) | `llm.py` |
| 2 | `generate` | syntax spec → invocations + the environment each needs | `ir/string.py`, `ir/environment.py`, `ir/contents.py`, `ir/mixin.py` |
| 3 | `trace` | configurations → a v1-compatible traces file | `tracer/tracer.py`, `tracer/strace_parser.py` |
| 4 | `annotate` | traces → one consumer's annotation (pash/posh/sash/shellcheck) | `tracer/data.py::to_annotation`, `annotator/` |

`caruca_run.py` accepts a stage as `1`-`4`, the slug, or the common words (`syntax`,
`gen`, `tracing`, `annotation`).

## Headline metrics

Mirrored from `console/src/data/compare.ts::HEADLINE`. If you change one, change it there
too, or the console and this skill will disagree about the same run.

| stage | metric key | label | counted over | method |
|---|---|---|---|---|
| 1 | `f1` | flag F1 | flags in the reference specification | `q2_syntax_diff` |
| 2 | `f1` | invocation F1 | v1's distinct invocations at the same limits | `invocation_set_diff` |
| 3 | `core.micro.f1` | core interaction F1 | v1's projected filesystem interactions | `trace_recovery_diff` |
| 4 | `agreement.pclass` / `agreement.comparable` | parallelizability-class agreement | aligned cases where both sides state a class | `annotation_diff` |

**Stage 4 is a count, not a rate.** `agreement.pclass` counts agreeing cases and
`agreement.comparable` is how many were aligned at all. Pool them — summed numerator over
summed denominator — and report as "0 of 3". Averaging the raw counts across cells gives
a number that is not a rate and not anything.

A figure at or above **0.9** is called `replicates`, below it `diverges`. `improves` is
reserved for a figure that beats v1's *and* is measured against a reference that is not v1
itself; no stage-2 or stage-3 cell can earn it, because there "better than v1" is a
contradiction in terms. Apply it by hand only for a ground-truth comparison.

## `manifest.json` — one run

`eval/runs/<timestamp>_<command>_<hash>/manifest.json`.

| field | notes |
|---|---|
| `run_id`, `timestamp`, `command`, `stage` | identity |
| `status` | `ok` or `failed`; `failure_reason` when failed |
| `model_requested` / `model_reported` / `provider` | record both; they can differ |
| `seed`, `seed_honored`, `decoding_params` | `{temperature, max_tokens}` |
| `prompt_system`, `prompt_user` | **the rendered prompt as actually sent** |
| `prompt_files`, `prompt_hash`, `prompt_variant` | `prompt_files` are templates, not what was sent |
| `raw_response`, `finish_reason`, `turns`, `output_truncated` | the model's side |
| `validation` | `{passed, available, error, traceback, elements}` |
| `checks` | per-stage; see below |
| `inputs` | what the stage was given, including `replaces_v1_modules` |
| `output_paths` | repo-relative; the artifact the run produced |
| `prompt_tokens`, `completion_tokens`, `cost_usd`, `wall_clock_seconds` | totals for the run |

**A prompt template cannot be compared to a recorded prompt, and `prompt_hash` cannot
detect prompt drift.** The files in `prompts/` are templates; the manifest records the
rendered text; the hash covers the rendering. To know what a model was told, read
`prompt_user` — this is the field that distinguishes "the model failed" from "the model
was asked the wrong thing".

## Per-stage `checks`

**Stage 1** — empty. Scoring lives entirely in the ledger cell.

**Stage 2** — `parse` and `invocation_comparison`:

- `parse`: `lines_returned`, `objects_parsed`, `unparseable_lines`, `malformed_objects`,
  `turns_used`, `model_declared_complete`, `hit_turn_cap_while_incomplete`. A truncated
  final line is left unparseable rather than repaired, because a repaired line would be
  partly ours and partly the model's.
- `invocation_comparison`: `bounds` (**`max_arity`, `max_count`, `skip`,
  `stdin_variation`, `content_variation`** — the bounds the run was actually given),
  `counts`, `recall`, `precision`, `f1`, `missing_sample`, `spurious_sample`,
  `equivalence` (how two invocations are judged the same), `form_notes` (matches that
  agreed on content but differed in spelling — reported, never scored), `parse_health`
  (including an injectivity note: whether the equivalence relation merges two distinct v1
  invocations, which would change the denominator), `caruca_v1_commit`.

**Stage 3** — `configs` (`available`, `attempted`, `reported`, `limit`), `sessions` (one
per configuration: `invocation`, `status`, `turns`, `stop_reason`, `executions`, tokens,
cost, `interactions`, `rejected_interactions`, `error`), `tool_audit` (every tool call with
`allowed` and a reason), `refused_calls`.

**Stage 4** — `format` (which consumer), `output_was_fenced`, `comparisons`.

## `ledger.jsonl` — one scored cell

`eval/campaigns/<campaign_id>/ledger.jsonl`, one JSON object per line.

`cell_key` (`command|model|temperature|sample`), `campaign_id`, `stage`, `command`,
`model`, `temperature`, `sample`, `prompt_variant`, `attempts`, `run_id`, `run_dir`,
`status`, `validation_passed`, `cost_usd`, `prompt_tokens`, `completion_tokens`, `score`.

`summary.json` beside it has campaign totals and `by_model` rollups including `mean_f1`
and `scored_cells`.

## Per-stage `score`

Every score carries `scoreable`, `method`, `instrument`, `reference`, `error`.
`reference` is what the stage was compared against, and it is not the same at every stage:

| stage | `reference` | meaning |
|---|---|---|
| 1 | `v1-specs` | v1's own committed syntax specifications |
| 2 | `v1-enumeration` | v1's `caruca generate` output at the same bounds |
| 3 | `v1-strace` | v1's recorded filesystem interactions |
| 4 | `ground-truth` | the hand-curated annotation, **not** v1 |

That last row matters: at stage 4 both systems are measured against a third thing, so v2
scoring above v1 there is a real improvement claim, while at stages 2 and 3 it cannot be.

Metric keys by stage:

- **1**: `f1`, `precision`, `recall`, `exact_argument_rate`; `counts` = `generated_flags`,
  `reference_flags`, `matched`, `missing`, `spurious`.
- **2**: `f1`, `precision`, `recall`; `counts` = `v1_lines`, `v1_unique`, `produced_lines`,
  `produced_unique`, `matched`, `missing`, `spurious`; plus `config_comparison` with
  `env_agreement_rate` and `rates.{value, arg_type, relative, content, parent_exists,
  stdin, node_grouping, fully_agreeing}`.
- **3**: `core.micro.{f1, recall, precision}`, `inference.micro.f1`, `ceiling_fraction`.
  `counts` is null.
- **4**: `agreement.{fully_agreeing, pclass, inputs, outputs, comparable}`. `counts` is null.

`caruca_run.py -v numbers` flattens all of these to dotted keys and prints mean, min, max
and spread across samples, marking the headline.

## `metrics.db`

One table, `runs`, keyed `(run_id, turn)`: `config_index`, `timestamp`, `command`,
`component`, `condition`, `stage`, `model_id`, `prompt_tokens`, `completion_tokens`,
`cost_usd`, `wall_clock_seconds`, `seed`, `decoding_params`, `prompt_hash`,
`validation_passed`, `run_dir`. Read-only; `carucadata.metrics_rows()` opens it that way.

It knows runs whose directories are gone, so a count here and a count from `eval/runs/`
legitimately differ. **No per-turn clock time was ever recorded** — every sidecar carries
the run's start time, so any per-turn timing is derived by accumulating durations and must
not be presented as measured.

## Campaign families

- **`p1_*`** — the nine-command parity study (task 008): `cat`, `pwd`, `rm`, `sha256sum`,
  `tac`, `tail`, `tee`, `uniq`, `wc`; 3 samples each, `gpt-4o` at temperature 0,
  `--max-arity 1 --max-count 1`.
- **`c0_*`** — the earlier, smaller pilot. Stages 1-3 cover `cat`, `mkdir`, `wc`; stage 4
  covers `arch`, `dirname`, `printenv` — a *different command set from its own stages 1-3*.

`cat` and `wc` appear in both. They are different experiment designs, so a mean over both
is a mean over two experiments; `caruca_run.py` picks one family, names it, and says when
another exists. `--campaign all` pools them only if you ask.

## Counting traps

Each of these has produced a wrong number in this project before.

- **Three different run counts are all correct.** Run directories, directories holding a
  manifest, and rows in `metrics.db` differ: a directory is created when a run starts and
  the manifest written only when it ends, so a run that dies in between leaves a shell.
  Say which denominator you mean.
- **Runs on disk are not the same as scored samples.** `cat` has nine stage-4 runs but
  three scored cells. `caruca_run.py` reports uncited runs separately and excludes them
  from the figure.
- **`--max-count` counts optional *elements*, not optional flags** — the operand included.
  See `v1_probe.py --explain-bounds`; this is the largest single cause of stage-2 surplus.
- **v1's annotator never emits `pure`**, and reaches `stateless` only from split-input
  traces, which exist only under `caruca trace --stdin split --content split`. At the
  `simple` default no command can be classified `stateless` at any `--max-count`, so a
  parallelizability comparison made at the default measures the trace configuration as
  much as the annotator.
- **v1's `annotate` cannot run on macOS at all**, on any input, so v2's `annotate` takes
  `--v1-runner lima`.
