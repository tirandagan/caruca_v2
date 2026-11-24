---
name: caruca-paper-review-2026-11
description: "BASELINE LIST OF CHANGES TO THE ORIGINAL CARUCA PAPER: the 2026-11-19 AI referee review (ai_docs/refs/caruca white paper-review.md, W1-W7 + Q1-Q6 + nits), what project evidence already bears on each item, the paper-internal number mismatches, the 4 uncited closest works; later naive-LLM findings add to or revise this list (change log at the bottom)"
metadata:
  type: project
---

**What this is.** On 2026-11-24 Tiran named the 2026-11-19 referee review of the original Caruca paper
as **the reference list of changes to the paper**. Later naive-LLM findings will add items or change
these. Refer back here, and log each addition or revision with its date in the change log below.

- Review: `ai_docs/refs/caruca white paper-review.md`; scores: `caruca white paper-review.scores.json`
  (same folder). Written with the agentic-paper-reviewer skill, grounded in arXiv only.
  Overall 6.7 (ICLR-calibrated estimate, raw 5.2). The two low scores: soundness 4 and prior-work
  positioning 4.
- It is AI-generated. Re-check any item against the paper before it goes into a draft.
- **Item IDs are the review's own labels** (W1-W7 weaknesses, Q1-Q6 author questions). Never renumber them.
  New items from later work get new IDs (suggested: `N1`, `N2`… for naive-LLM-derived changes).
- Prose for the co-authors goes in `naive_llm_caruca/white_paper_addendum_naive_llm.md`
  ([[feedback-naive-llm-standalone]]), framed as extending v1 ([[feedback-v1-v2-framing]]).
  Purpose: the resubmission ([[project-dual-objectives]]); venue: [[project-venue-research-2026-11]].

**The change list (from the review) and evidence the project already holds**

| ID | Change the review asks for | Evidence already in hand |
|---|---|---|
| W1 | State the flag limit and time limit behind every headline number. Report accuracy and coverage at the same limit as the cost result (2 flags; the default is 4) | v1 re-runs duplicate command lines, so the paper's cost figure is overstated, in v1's favour ([[caruca-v1-enumeration-redundancy]]) |
| W2 | Check specifications outside the hand-written references, i.e. the invocations no reference covers | Real PaSh runs, 2,377 of them ([[reference-pash-comparison-scorer]]) |
| W3 | Describe how "stateless" test inputs and split points are chosen, and measure how often the label is wrong | v1 labels `sort -n -u` stateless. That is wrong when run, and was confirmed under real PaSh on 2026-11-19 ([[caruca-v1-class-combining-rule]]) |
| W4 | Add baselines and ablations: a model writing the final specification directly, a second model, repeated runs, token cost | The naive-LLM experiment *is* the direct-model baseline. The paper measures no LLM cost and never tests repeatability ([[caruca-paper-unmeasured-contributions]]). Cost varies between identical runs ([[cost-not-reproducible]]). Repeated runs: [[project-fig7-campaign]] |
| W5 | Scope the over-claims: "completely eliminating manual effort", "immediately usable" (POSH was never run), ShellCheck 6/6 out of 47 checks, PaSh correctness with no speedup | PaSh suite comparison, under way. Small inputs only, so no full-size timing yet ([[project-pash-suite-comparison]]) |
| W6 | State how the coverage corpus was filtered. Give per-command coverage and a conservative figure (Fig. 6 gives 23.7% without string and argument-count normalization) | 40% of corpus lines count as read only because a word is taken as an option it is not ([[caruca-v1-matcher-behaviour]]) |
| W7 | Cite KumQuat, KernelGPT and ProphetFuzz (and GUIde as concurrent work), and narrow the "first" claim | none (literature only) |
| Q2 | Did Tab. 1 use the model's grammars or the curated ones? | **Answered from v1's code:** `trace` loads only the curated grammars, so the paper's downstream results never started from the model's output ([[caruca-v1-class-combining-rule]], fact 5) |
| Q6 | Results on commands the model hasn't seen, across repeated runs and across models | binwalk and other non-coreutils runs ([[project-fig7-campaign]]) |

The other review items, all in the review's "Detailed Comments":

- **Method:**
  - `sed`'s class depends on its script.
  - The side-effect rule contradicts the `rm`/`cp` examples.
  - `rm` is marked both O({}) and ↓, which is vacuous.
  - `getcwd` vs. `ls` (marked unverified in the review).
  - The grammar is never checked against the binary.
  - Commands whose state isn't in the filesystem (kill, date, timeout, who, df, chroot).
- **Experiments:**
  - About 30 Fig. 7 commands are projected, not measured.
  - The manual comparisons aren't independent (author overlap).
  - No held-out commands: rm/mv/touch are both prompt examples and evaluated commands.
  - No PaSh speedup reported.
  - Missing ablations: flag limit, typed vs. untyped arguments, pruning.
- **Clarity:**
  - C1-C4 labels are reused.
  - Tab. 1 mixes units.
  - The 120 commands are never listed.
  - Nits: "Ubuntu 22.07"; "LLM Parser (Q3)" should be Q2.

Not in the review, but also a paper change: the 116/120 syntax-accuracy figure doesn't reproduce.
v1's own shipped specs score 78/116 ([[caruca-v1-stage1-baseline]], [[caruca-v1-eval-tooling-notes]]).

**Paper-internal mismatches, from arithmetic on the paper's own numbers (2026-11-19):**
- **Coverage text vs. Fig. 6.** The text says flag normalization gives 64,542, which is below the 66,882
  exact matches. It then gives 122,816 (18%) and 632,780 (94%). Fig. 6's own values add up to 158,101
  (23.7%) and 500,007 (75.0%). Argument-count normalization is worth 18,953 by the text and 151,726 by
  the figure. 59.1% if strings are allowed only for printing and filtering commands.
- **Ground-truth count.** "88 specification ground truths" = 52+17+6+12 = 87, or 93 with Tab. 1's
  Shseer 18.
- **Invocation total.** §4.1's per-flag-count invocations sum to 665,614, vs. the 666,468 used in §7.3.
- **Corpus filtering.** Fig. 4's top-40 commands include `rmdir`/`realpath` (under 1,000 uses) but not
  `grep`, `sed` or `git`. The corpus looks filtered, and the paper never says how.
- **Fig. 7.** About 31 commands didn't finish in 5 h at 4 flags (incl. `test`, `grep`, `sort`, `sed`,
  `ls`). Its labels: 8.3 d for grep, 16.5 d for sort, 123.7 d for test.
- **Side-effect rule.** §6.3 defines it as "writes to a path not named in its arguments", which wouldn't
  make `rm` side-effectful, yet §6.1 and Fig. 3 do. Fig. 3 also gives `rm` both O({}) and ↓.
- **Prompt examples.** The worked examples `rm`, `mv` and `touch` are themselves evaluated commands
  (Fig. 7). See [[caruca-v1-llm-retry-mechanics]].

**Closest related work the paper doesn't cite (checked on arXiv, 2026-11-19):**
- **KumQuat**, arXiv:2012.15443. Black-box combiner synthesis for Unix commands. It shares an author
  (Vasilakis) and fills the aggregator gap Caruca calls out of scope.
- **KernelGPT**, arXiv:2401.00563. An LLM writes syscall specs, repaired from validator feedback. It
  reports a model ablation and a $34 cost.
- **ProphetFuzz**, arXiv:2409.00922. An LLM reads man pages to pick option combinations.
- **GUIde**, arXiv:2510.01453. Concurrent work: an LLM turns man pages into grammars, with an 89.8% parse
  rate on real invocations.

PaSh's own paper (arXiv:2007.09436, §3.2) says its 47 annotations took "about 3–4 hours" and calls
automating the task "infeasible".

Location: the review lives in caruca_v2. As of 2026-11-24 the repo split hasn't been executed
([[project_naive_llm_repo_split]]); this note concerns both repos if it happens.

**Change log** (newest first; one dated line per item added, revised or dropped)
- 2026-11-24: Tiran named this the baseline for paper changes. Linked the evidence already in memory to
  each item. Q2 is answered from v1's code.
- 2026-11-19: Review written; baseline list = W1-W7, Q1-Q6, method/experiment/clarity items.
