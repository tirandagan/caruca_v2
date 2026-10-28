---
name: caruca-v1-enumeration-redundancy
description: "v1 re-emits any invocation that doesn't spend the full flag budget — C(n-k, max_count-k) copies, 89% waste at the shipped default, never deduplicated before tracing; a cost finding in v1's favour, and it shrank stage 3's real sample to 12 distinct command lines"
metadata:
  type: project
---

**The rule.** v1's enumerator (`ir/syntax.py::__filtered_args`) selects *exactly*
`min(n, max_count)` of the `n` optional argument positions, once per combination, and each
selected position's `syntax_variation()` includes its own absent case. So every combination
independently re-emits the invocation that uses none of the positions it selected. An invocation
using **k** optional positions is emitted **C(n − k, max_count − k)** times; only invocations
spending the full budget appear once.

Verified exactly on `cat` (n = 13: twelve flags plus the optional operand) at the shipped
`--max-count 4` — emitted 715 / 220 / 55 / 10 for k = 0 / 1 / 2 / 3, predicted 715 / 220 / 55 / 10.

**Two things that follow, and are easy to get wrong:**
- A command's duplicate rate depends on `(n, max_count)` **only** — not on what the command does.
- It **rises with the bound**, so it is worst where cost already hurts: `cat` 44% → 69% → 82% →
  **89%** at `--max-count` 1 → 2 → 3 → 4. At the default `cat` emits 13,200 lines for 1,392
  distinct invocations.

**Nothing deduplicates before execution.** `cli/trace.py` passes `string_invocations(...)`
straight into `Tracer(...).run(...)`. Visible in v1's own committed output:
`caruca/outputs/tail.parity.json` has 41 entries, 28 distinct, bare `tail` traced 14 times —
14 of 49 recorded executions.

**This is a redundancy defect, not a correctness one, and it favours v1.** Every invocation
emitted is valid; repeats yield identical observations that the annotator aggregates, so no
specification is wrong because of it. The paper's Q4 timings were measured with the repeats
included, so **the method is cheaper than published**. Say it that way, not "the generator is
broken" — [[feedback-v1-v2-framing]] (Greenberg co-authored v1).

**Where it bit v2's own measurement.** `v1.reference_configs()` groups configurations under their
invocation string when writing `eval/v1_configs/<cmd>.configs.json`, so all the copies land
together at the head of the file, and stage 3's `--limit 5` takes the first five. Across the nine
parity commands the 45 executions cover **12 distinct command lines**, and for six of them
(`cat`, `sha256sum`, `tac`, `tail`, `uniq`, `wc`) all five were the *same* no-argument
invocation — **no flag exercised**. Stage 3's protocol finding is unaffected (sessions failed to
call `report_observations` regardless of input), but its recovery figures are bounded to the
forms actually run. Any re-run should deduplicate by invocation string before applying the limit;
that raises distinct coverage roughly fivefold at identical cost.

**Do not re-derive this from scratch.** The 120-command empirical sweep already existed before
the mechanism was worked out (`eval/e0/redundancy_sweep.py`, results in
`ai_docs/analysis/e0_artifact_pinning.md` — 82.7% duplicates across 90 fully-enumerating
commands, `--number` wrong for 90 of 90, 14 commands crashing in `max_group_arity`). On
2026-10-06 the same redundancy was rediscovered from `tail` and presented as novel; it was not.
Check that document first.

**Write-ups:** mechanism and closed form in `ai_docs/analysis/e0_artifact_pinning.md`
(enumeration-redundancy section); the stage-3 sampling consequence as confound 8 in
`ai_docs/archive_2026-09_rebuild/analysis/v1_v2_parity_study.md` §8, flagged at the head of its §4.

**Reproduce:** `caruca generate CMD --max-arity 1 --max-count N | sort | uniq -c | sort -rn`.

Related: [[caruca-v1-pipeline-reference]] for the surrounding pipeline,
[[harness-report-metric-naming]] for other instrument quirks.
