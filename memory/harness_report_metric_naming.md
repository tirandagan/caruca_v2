---
name: harness-report-metric-naming
description: "`caruca-v2 report --json` labels every stage's metrics with stage-1 names, produces nothing for stage 4, and cannot reproduce stage 3's pooled figures"
metadata:
  type: project
---

Found on 2026-09-22 while building the execution console's finding re-check (task 010, Phase 3).
Three defects in `src/caruca_v2/harness/report.py` and the ledger it reads. **None is in the
console; all three affect anything that reads `report --json`, including any figure copied into
the paper.**

**1. Every campaign's metrics are published under stage-1 names.** `Arm.as_dict` emits its two
metric slots as `"f1"` and `"exact_argument_rate"` regardless of stage, filling them from the
method's own metric list (`methods.py`). So:

| campaign | key `f1` actually holds | key `exact_argument_rate` actually holds |
|---|---|---|
| `p1_syntax_spec` | flag F1 | exact-argument rate (correct) |
| `p1_generate` | invocation F1 | **invocation recall** (0.878) |
| `p1_trace` | core.micro.f1 | **core.micro.recall** |

Reading those keys at face value attaches a stage-1 name to a stage-2 number. The console
resolves the slot through each method's declared metric list
(`console/src/data/recheck.ts::reportKeyFor`). The fix in `report.py` is to emit the real names.

**2. `report p1_annotate` produces no numbers at all** — `Mean F1 | n/a | n/a | n/a`.
`annotation_diff` declares `rates.fully_agreeing` and `rates.pclass` as its leading metrics, but
the ledger's flattened score carries only the `agreement.*` counts; the `rates` the scorer
computes in `annotation.py` are dropped on the way into the ledger. **Stage 4 has never been
aggregatable by the harness**, which is why the parity study's stage-4 figures were derived
another way.

**3. Stage 3's pooled figures cannot be recomputed from a campaign.** `counts` is null on every
`p1_trace` ledger row, so only per-cell rates survive, and a pooled rate cannot be rebuilt from
rates. The study's **0.606** is pooled over 33 interaction units; `report` gives **0.623**, the
mean of the 12 per-cell rates, which weights a cell with one interaction the same as a cell
with eight. Both are defensible and they are **not interchangeable** — never quote either
without saying which. Recording per-cell unit counts would fix it.

**How to apply:** before quoting any figure from `report --json` for a stage other than 1, check
which metric the slot actually holds. Before quoting a stage-3 pooled figure, state the
aggregation. Do not expect `report` to give you anything for stage 4. Related:
[[feedback-plain-language]] rule 6 (define every rate with its denominator) and
[[feedback-instrument-defect-vs-tuning]] — fixing these is repair, not tuning.
