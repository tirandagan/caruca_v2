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

**Update 2026-09-22 — the second finding is out of date.** Since 2026-09-03 every v1 stage has an LLM
replication (tasks 002-004, [[llm-pipeline-replication]]), so dimension 6 can now be measured
stage by stage. Task 010's code map does that. Two cautions carry over: the ~3,456 figure's counting
method was never recorded, so both sides get recounted with one counter; and prompt lines count as
hand-written, because moving logic into a prompt does not remove it.

**Update 2026-09-22 — the lost counting method is recovered, and the counter is now fixed.**
Task 010's Phase 0 settled this. The counter is **cloc 2.10** (installed via Homebrew on the Mac at
Tiran's direction), and the rule is **code lines only: blank lines and comment lines excluded, applied
identically to both sides, with the cloc version recorded beside every result.**

Running it against v1 reproduced the old figure exactly and revealed what the unrecorded method had
been — **physical lines**, meaning every line in the file including blanks and comments:

| v1 area | physical lines | code lines |
|---|---|---|
| `ir` | 1,249 | 973 |
| `tracer` | 946 | 781 |
| `annotator` | 586 | 428 |
| `cli` | 354 | 302 |
| package-level (`llm.py`, `oracle.py`, `querier.py`, `error.py`, `__init__.py`) | 321 | 214 |
| **total** | **3,456** | **2,698** |

The four directory figures match the 2026-08-29 memo above digit for digit (1,249 / 946 / 586 / 354),
and the total lands on 3,456 — so the old number was physical lines, not code lines.

**So the v1 baseline for dimension 6 is 2,698 code lines, not 3,456.** Quoting 3,456 against a
cloc-counted v2 figure would overstate the reduction by about 28%, in the same direction as the
original 6,520-vs-3,456 error. State the counter and rule with every dimension-6 number.

Two rules carry over from task 010: **pipeline code is counted apart from harness code** (the harness
measures the systems and belongs to neither pipeline), and **prompt lines count as hand-written**,
because moving logic out of code and into a prompt does not remove it.

**How to apply:** when writing any dimension-6 result, state the narrow scope explicitly and never present
it as the broad "we eliminated N% of Caruca's code" claim. Full reasoning and the phase assignment live in
`ai_docs/prep/roadmap.md` (Dimension 6 section + coverage audit).
