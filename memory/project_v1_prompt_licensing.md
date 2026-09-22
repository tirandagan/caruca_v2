---
name: project-v1-prompt-licensing
description: "2026-09-22: Tiran cleared copying v1's prompts verbatim into caruca_v2 (he owns the licensing rights); supersedes the 'paraphrase, never copy' rule for prompts"
metadata:
  type: project
---

On 2026-09-22 Tiran stated there are **no licensing issues with reusing v1's prompts**:
"we own the licensing rights", so v2 may copy them word for word where exact replication
needs it.

**Why it matters:** the earlier rule (v1 is private and unlicensed, so committed prompts
contain only text written for this project and v1 text is injected at runtime) made the
stage-1 instructions a paraphrase. The parity study (confound 2) and
`ai_docs/analysis/v2_fidelity_to_v1.md` (section 2.2, section 3.3, and deviations 1 and 5 in
section 8.1) name that paraphrase as the largest uncontrolled difference at stage 1.
Task 009 removes it.

**How to apply:**
- v1 prompt text (the DSPy `Signature` docstring, field descriptions, DSPy's rendered layout,
  retry wording) may now be committed verbatim. Cite the v1 commit it came from.
- The clearance was given for **prompts**. Tiran didn't say whether it extends to v1's code
  and data in general (man pages, specs, fixtures). Keep reading those at runtime from
  `CARUCA_V1_ROOT` unless he extends it. Never put any v1 material in a public location
  either way, per [[caruca-v2-project-overview]].
- The fidelity doc and the parity study still carry the old reasoning. Task 009 updates them.
  Until then, don't repeat the "cannot be copied" claim as current.

Related: [[feedback-instrument-defect-vs-tuning]] (adopting v1's prompt is a recorded scope
decision by Tiran, not tuning).
