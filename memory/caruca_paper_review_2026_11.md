---
name: caruca-paper-review-2026-11
description: "2026-11-19 AI referee review of the Caruca paper (ai_docs/refs/caruca white paper-review.md): internal number mismatches found by arithmetic, and four uncited closest related works (KumQuat, KernelGPT, ProphetFuzz, GUIde)"
metadata:
  type: reference
---

Review written 2026-11-19 with the agentic-paper-reviewer skill: `ai_docs/refs/caruca white paper-review.md`
(+ `.scores.json`; overall 6.7 ICLR-calibrated, raw 5.2; soundness 4 and prior-work positioning 4 were the low dimensions).

**Paper-internal mismatches, established by arithmetic on the paper's own numbers (2026-11-19):**
- Coverage text vs Fig. 6 disagree: text says flag normalization gives 64,542 (below the 66,882 exact matches),
  then 122,816 (18%) and 632,780 (94%); Fig. 6's own values add up to 158,101 (23.7%) and 500,007 (75.0%).
  Argument-count normalization = 18,953 by the text, 151,726 by the figure. Without string and argument-count
  normalization, Fig. 6 gives 23.7% coverage, not 97.78%.
- Evaluation suite "88 specification ground truths" = 52+17+6+12 = 87; with Tab. 1's Shseer 18 it is 93.
- §4.1 per-flag-count invocations sum to 665,614, vs 666,468 used in §7.3.
- Fig. 4's top-40 commands include `rmdir`/`realpath` (<1,000 uses) but no `grep`, `sed`, `git`: the corpus looks filtered; the paper never says how.
- Fig. 7: about 31 commands did not finish in 5 h at 4 flags (incl. `test`, `grep`, `sort`, `sed`, `ls`); labels 8.3 d grep, 16.5 d sort, 123.7 d test.
- Side-effect rule (§6.3 "writes to a path not named in its arguments") would not make `rm` side-effectful, yet §6.1/Fig. 3 do; Fig. 3 gives `rm` both O({}) and ↓ (vacuous).
- The prompt's worked examples `rm`, `mv`, `touch` are themselves evaluated commands (Fig. 7). Compare [[caruca-v1-llm-retry-mechanics]].

**Closest related work the paper does not cite (verified on arXiv 2026-11-19):** KumQuat arXiv:2012.15443
(black-box combiner synthesis for Unix commands, shares author Vasilakis; fills the aggregator gap Caruca calls out of
scope), KernelGPT arXiv:2401.00563 (LLM writes syscall specs + validator repair; reports model ablation and $34 cost),
ProphetFuzz arXiv:2409.00922 (LLM over man pages picks option combinations), GUIde arXiv:2510.01453 (concurrent;
LLM man page → grammar, 89.8% parse rate on real invocations). PaSh (arXiv:2007.09436 §3.2) says its 47 annotations
took "about 3–4 hours" and calls automation "infeasible".

Related: [[caruca-paper-unmeasured-contributions]], [[caruca-v1-stage1-baseline]], [[project-dual-objectives]].
