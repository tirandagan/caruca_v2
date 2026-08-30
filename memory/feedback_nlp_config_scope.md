---
name: feedback-nlp-config-scope
description: Model/decoding-parameter/output-format selection is core v2 scope, not scope creep - frame it as inherent to moving from hardcoded to NLP-based
metadata:
  type: feedback
---

When describing any v2 component that's NLP-based (the naive-LLM baseline, and any future LLM-driven
piece), frame selecting its model, decoding parameters (e.g. temperature), and output-format constraint
(e.g. structured/JSON output) as **core, in-scope work** — not an optional add-on, not scope creep, and
not the kind of "tuning" [[caruca_v2_baseline_scope]] says to avoid.

**Why:** Tiran pushed back (2026-08-29) on an earlier framing where I'd flagged a proposed
model/configuration comparison step in the roadmap as a scope-creep risk to keep bounded. His point: v1's
behavior is fixed by hand-written code, so it has no configuration surface at all outside its one LLM
call. The moment v2 replaces hardcoded logic with an NLP-based component, these choices stop being
incidental setup and become part of the method itself — they directly drive accuracy, consistency, and
cost. Treating that as risky scope creep misrepresents what v2 fundamentally is.

**How to apply:** Draw a clean distinction, and state it explicitly wherever this comes up (roadmap,
slides, paper write-ups): choosing a model/parameter/output-format configuration **once, up front, through
a small fixed comparison, then freezing it** is in scope and inherent to the NLP-based approach. Iteratively
refining a component's output to produce a better answer and win the comparison is the actual thing
[[caruca_v2_baseline_scope]]'s "don't over-engineer the baseline" guidance excludes. Don't conflate the two
when explaining this to advisors — conflating them is what triggered this correction in the first place.
Reflected in `ai_docs/prep/roadmap.md` (Phase 2), `ai_docs/prep/master_idea.md` (Specific Problem), and
`CLAUDE.md`'s Conventions section.
