---
name: caruca-paper-unmeasured-contributions
description: "The Caruca paper measures zero LLM cost/tokens and never tests reproducibility of its own LLM step — two things caruca_v2 measures that the original never did"
metadata:
  type: project
---

Verified by a full-text read of `ai_docs/refs/caruca_white_paper.md` during the 2026-08-29 plan-mode
review (`~/.claude/plans/review-our-progress-so-delightful-token.md`), useful whenever framing
`caruca_v2`'s contribution to Greenberg or the resubmission co-authors — this isn't just "redo the paper
with an LLM," it extends the original paper's own evaluation on two axes it never touched.

**No cost/token accounting for the LLM step, anywhere.** §7.4 "Computational Cost" is wall-clock only
(hours/command, one named machine: Xeon E5-2667 v2). Zero hits anywhere in the paper for "token" or
"$"/"dollar." "Eliminating manual effort" is a real stated selling point (Abstract, Introduction, §2) but
it's never quantified against Caruca's *own* LLM cost — only against the 80 person-hours the ground-truth
annotation itself cost (§7.2). `caruca_v2`'s Baseline Instrumentation component (retrofitting
tokens/cost/wall-clock telemetry onto v1's own `syntax-spec` step) produces a number the paper's own
authors have never reported.

**No reproducibility/nondeterminism testing of the LLM step.** Zero hits anywhere for "reproduc-,"
"determinis-," "temperature," "seed," or repeated/multiple LLM sampling. There's a retry loop (§3.2, ≤3
attempts on validation failure, previous output + error fed back) but that's error-correction on a single
generation, not variance measurement across independent runs. The reported 99.7% argument-level accuracy
(§2.2) and 116/120 command-level exact-match (§7.2) are both single-run numbers. `caruca_v2`'s planned
repeated-sampling variance check (evaluation dimension 4, also `evaluation_gaps.md` gap #9) is genuinely
novel, not just good practice.

**How to apply:** when writing evaluation results or advisor-facing summaries, lead with these two as
"what v2 adds that the original paper never measured," per [[caruca-v2-build-tiering]] — this is a
stronger case for the resubmission's value than framing v2 as just reproducing existing numbers, and it's
true regardless of how the naive-LLM baseline's own correctness compares to v1's.
