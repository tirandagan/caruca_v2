---
name: caruca-v1-stage1-baseline
description: "v1's own committed LLM specs score 78/116 by v1's own cmp_specs instrument, not the paper's 116/120 — measured 2026-09-14; the stage-1 baseline for any v1-vs-v2 comparison"
metadata:
  type: project
---

**v1's shipped LLM output does not reproduce the paper's Q2 number against v1's shipped
ground truth.** Measured 2026-09-14 during task 008, at v1 commit `d8032407`.

| Instrument | Result |
|---|---|
| v1's own `eval/cmp_specs.py` (the paper's Q2 tool), `diff_count == 0` | **78 / 116** |
| caruca_v2's independent structural scorer, no option *or* type errors | **83 / 116** |
| The paper (§7.2), "116/120 exact — 1 type misclassification, 3 missing/spurious options" | **116 / 120** |

Inputs: `outputs/llm-dsl-generation/*.py` (117 specs, repo root — **not** `caruca/outputs/`,
which holds traces) scored against `caruca/src/caruca/syntax_specs/*.py`. One command
(`mogrify`) does not interpret at all.

**The instrument is sound.** Ground truth scored against itself is **117/117** exact, and two
independently built instruments land within 5 of each other (78 and 83). The gap is not a
scoring artifact.

Breakdown from the structural scorer: 105/116 have no missing/spurious options (11 commands
do), but only 86/116 have no **type** misclassification (30 commands do). The paper reports 3
and 1 respectively. Worst offenders: `stty` (34 spurious), `iconv` (14 diffs), `pandoc` (9),
`od` (6).

**Candidate explanations, none yet confirmed — a question for Greenberg, like E0's `ps`/`cp`
claims** (see [[caruca-v2-project-overview]] and `ai_docs/analysis/e0_artifact_pinning.md`):
1. The committed `llm-dsl-generation/` set is *a* run, not necessarily the run the paper
   reported. Most likely.
2. Ground truth was revised afterwards — but only 2 `syntax_specs/` commits postdate it
   (2025-09-21, 2025-10-25), and the LLM set and ground truth were committed a day apart
   (2024-11-10/11), so this explains less than it first appears.
3. A different model or decoding configuration produced the paper's run.

**How to apply.** Any v1-vs-v2 stage-1 comparison must use **78/116 (or 83/116 by the v2
scorer) as v1's baseline**, not 116/120 — comparing v2 against a number the shipped artifacts
do not reproduce would be comparing against something unverifiable. State the paper's figure
alongside, with this discrepancy named. Per [[feedback-v1-v2-framing]] this is a reproducibility
gap in the artifact set, not a claim that the paper is wrong.

Also settled here: `syntax_specs/*.py` is genuinely human-curated ground truth, so scoring v1's
LLM output against it is not circular — see [[caruca-v1-eval-tooling-notes]] for the provenance
audit (92 commits, 4 authors including a paper co-author).
