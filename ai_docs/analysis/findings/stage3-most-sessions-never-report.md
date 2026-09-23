---
id: stage3-most-sessions-never-report
claim: "At stage 3 the dominant failure is protocol rather than accuracy: most tracing sessions end without ever calling the reporting tool."
status: confirmed
created: 2026-09-22
updated: null
dimensions:
  - 1
stages:
  - trace
paper_sections:
  - §5
evidence:
  - label: core interaction recall
    value: 0.606
    denominator: 33 core filesystem interaction units v1 recorded, after projection
    metric: core.micro.recall
    method: trace_recovery_diff
    run_ids: []
    campaign_ids:
      - p1_trace
    aggregation: pooled over the 33 interaction units across all 12 scored cells
    scorer_commit: null
    excluded: null
    recheck: null
  - label: core interaction recall, averaged over cells instead of units
    value: 0.623
    denominator: the 12 scored cells, each contributing its own recall equally
    metric: core.micro.recall
    method: trace_recovery_diff
    run_ids: []
    campaign_ids:
      - p1_trace
    aggregation: mean of the per-cell rates, which is what `report` publishes
    scorer_commit: null
    excluded: null
    recheck:
      kind: campaign_metric
      campaign: p1_trace
      metric: core.micro.recall
      method: trace_recovery_diff
      referenceTraces: "{CARUCA_V1_ROOT}/caruca/outputs/{command}.parity.json"
  - label: core interaction precision
    value: 0.8
    denominator: the core interaction units v2 reported
    metric: core.micro.precision
    method: trace_recovery_diff
    run_ids: []
    campaign_ids:
      - p1_trace
    aggregation: pooled over all 12 scored cells
    scorer_commit: null
    excluded: null
    recheck: null
corrections:
  - date: 2026-09-20
    old_value: 0.769 precision / 0.588 recall
    new_value: 0.800 precision / 0.606 recall
    why: The first figures were computed by hand from one cell per command rather than all three samples, because the campaign ledger carried no stage-3 scores at all.
needs_v1_authors: false
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

Where a session did report, recovery is partial. Where it did not — most of them —
there is nothing to score at all.

**Recovery and reporting are different failures and must not be blended.** A session that ran
and observed nothing is a different outcome from one that ended without calling the reporting
tool, and a count of zero interactions cannot tell them apart. The console distinguishes them
from the session's recorded status.

These figures were corrected once already, and the re-check found a third thing worth
recording.

**"Core recall" is two different numbers, and they differ by more than rounding.** The study's
0.606 is pooled over the 33 interaction units — every unit counts once. `caruca-v2 report`
publishes 0.623, the mean of the twelve per-cell rates — every *cell* counts once, so a cell
with one interaction weighs as much as a cell with eight. Both are defensible; they are not
interchangeable, and neither may be quoted without saying which it is.

**The pooled figure cannot be recomputed from the campaign ledger.** The ledger records each
cell's rate but not its unit counts (`counts` is null on every stage-3 row), and a pooled rate
cannot be rebuilt from rates alone. So the 0.606 in this document is checkable only against
whatever produced it originally. That is the same weakness §4.3 of the study describes — the
ledger carried no stage-3 scores at all until after publication — in a smaller form.

Recording the unit counts per cell would fix it, and is worth doing before any stage-3 number
goes into the resubmission.
