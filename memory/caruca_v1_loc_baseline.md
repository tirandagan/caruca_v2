---
name: caruca-v1-loc-baseline
description: "The paper's 6,520 LOC figure is ~half generated spec data, not hand-encoded logic — dimension 6 must be measured against ~3,456 LOC"
metadata:
  type: project
---

Measured directly against v1 (`~/stevens/caruca/caruca/src/caruca/`) on 2026-08-29 during the
`10_generate_build_order_worker` pass:

- Hand-written pipeline logic: **~3,456 LOC** — `ir` 1,249 · `tracer` 946 · `annotator` 586 · `cli` 354,
  plus package-level modules.
- Generated syntax-spec data: **~3,130 LOC** across `syntax_specs/` (121 files).

These sum to ~6,586, closely matching the paper's published **6,520 LOC** figure — meaning the headline
number **includes the LLM-generated spec data**, not just hand-written code.

**Why this matters:** evaluation dimension 6 is "reduction in hand-encoded logic." Measuring a v2 claim
against 6,520 would overstate the reduction by roughly 2x, since about half that total is generated data
that no one hand-encoded. Any dimension-6 claim should be stated against the ~3,456 LOC of pipeline logic,
with the split disclosed.

**Second, related finding:** dimension 6 is largely *unmeasurable* within Tier 0/Tier 1 (see
[[caruca-v2-build-tiering]]). The naive-LLM baseline substitutes only for v1's syntax-spec step; every
downstream stage is v1's code being *reused*, and the sandbox/tool-augmentation phases *add* hand-written
logic rather than removing it. The honest in-scope measurement is narrow: how much of `llm.py`'s DSPy
scaffolding, retry logic, and prompt engineering a single prompt replaces. The broad claim needs the
deferred agentic rebuild.

**How to apply:** when writing any dimension-6 result, state the narrow scope explicitly and never present
it as the broad "we eliminated N% of Caruca's code" claim. Full reasoning and the phase assignment live in
`ai_docs/prep/roadmap.md` (Dimension 6 section + coverage audit).
