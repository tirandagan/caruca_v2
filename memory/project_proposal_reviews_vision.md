---
name: project-proposal-reviews-vision
description: "The \"Caruca v1 submission reviews\" file is NSF's 2023 panel review of Greenberg's grant proposal, not the paper's reviews; shared for vision only — don't address the feedback; keep it simple; goal = working LLM v2 consumed by downstream tools, PaSh first"
metadata:
  type: project
---

**What the file is (read 2026-10-08, confirmed against the paper 2026-10-10).**
`ai_docs/docs/Caruca v1 submission reviews.md` is the NSF panel review of a **grant proposal**:
FMitF Track I, agency tracking number 2319293, "Collaborative Research: FMitF: Track I: Modeling,
Learning, and Checking Specifications for Black-Box Shell Components". Greenberg was PI and Vasilakis
co-PI. Four reviews were rated Good, Fair, Good and Fair. The proposal had three thrusts: (A) a formal
model of command specs plus a library and tooling; (B) testing, plus black-box and white-box synthesis
of specs; (C) tools built on the specs. Caruca is the black-box part of (B) made real. The file itself
does not state a year; dating it to 2023 is an inference from the 23xxxxx number. The paper
(arXiv 2510.14279) credits NSF CNS-2247687 and CNS-2312346, not 2319293. **No record of the paper's
own venue or reviews exists in either repository**, and Tiran (2026-10-10) is "not sure" he can get
them.

**Tiran's direction, 2026-10-10, verbatim:** "Michael shared this with me only so I can understand the
vision behind writing the article. We don't need to address the feedback, and we need to keep things
simple. The goal here is to implement a working v2 caruca that uses an LLM and that can be run against
a bunch of downstream tools. We are starting the testing with Pash first."

**Why:** before this, Claude had planned to map every reviewer criticism (formal semantics, synthesis
cost, isolation, broadening participation and so on) to paper and v2 changes. That was the wrong
target. The reviews are context for the vision, not a to-do list.

**How to apply:**
- Never frame work as answering these reviewers.
- When the resubmission comes up, don't cite this file as "the paper's reviews".
- **Corrected 2026-10-13 by Tiran ([[feedback_pash_is_consumer_not_objective]]):** the immediate
  goal is the v2 pipeline running end to end with every execution problem diagnosed, producing a
  strong, repeatable, reproducible syntax description. Downstream tools are *tests that the output
  is consumable*, not the goal: PaSh first only because it is already set up, then ShellCheck,
  Shseer and POSH. Task 013 and `ai_docs/archive_2026-09_rebuild/analysis/reflections_on_caruca_v1_submission_reviews.md`
  (both written 2026-10-13) still put the PaSh study ahead of the full chain, and need revising to
  match. That revision is on hold until Tiran confirms.
- The vision in one line: one model per command in two halves, *how it is called* and *what it does*,
  kept in an open library, checked by running the commands, conditioned on file state, and used by
  many tools.

Related: [[project-dual-objectives]], [[project-greenberg-caruca-purpose]],
[[caruca-v1-class-combining-rule]].
