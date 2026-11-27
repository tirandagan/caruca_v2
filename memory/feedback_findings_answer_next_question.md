---
name: feedback_findings_answer_next_question
description: In reports, every finding must answer its obvious next question on the spot (which ones? same as the others? why?) or point to exactly where the detail is; show overlaps in a small table, give one number per cell, explain counter-intuitive numbers next to them
metadata:
  type: feedback
---

2026-11-27, PaSh suite report Draft 2.1. Tiran: "I have to hunt for information all over the place. This should be
easier to read." Examples he gave: Table 1's compiler-stop row (4 / 4 / 11 / 3 of 177) immediately raises "are the
naive LLM's 4 the same as PaSh's own 4? which scripts, why? how do they overlap with Caruca's 11?"; the time row
still had two numbers per cell; and nothing explained why PaSh (and the naive LLM) are slower than bash, which
contradicts the expectation that parallelism speeds things up. He also asked: whenever the appendix has more detail,
the body must reference it; and examples (e.g. concise diffs of wrong outputs) belong in the appendix.

**Why:** the reader is checking how the naive LLM fared; each number he cannot interpret on the spot costs a search.
**How to apply:** for every table row and body claim ask "what will he ask next?"; answer it in a sentence or a small
overlap table right there, or cite the section/appendix part that does; one number per cell; explain anything
counter-intuitive (e.g. slower than bash at small inputs: per-part start-up/compile overhead) where it first appears.
Related: [[feedback_single_results]], [[feedback_greenberg_report_style]], [[feedback_report_metrics_in_pdf]].

2026-11-27 addition: the callout under the title said "With Caruca's it was wrong in 9 and 10". Tiran: confusing, "I
don't know what that means". A headline number must carry its unit, its denominator and what each of a pair belongs
to ("wrong in 11 scripts: 9 of 86 with Caruca's small grammar, 10 of 86 with its full grammar"), never a bare pair.
Same day, follow-up: the subtitle under the title stays very short, the striking stats only ("never changed the
output; Caruca's changed it in 11 of 86 scripts"); the breakdown (per grammar, overlap, splits, time) belongs in the
page-1 summary and section 1, not in the subtitle.
