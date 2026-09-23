---
id: stage3-pwd-moves-between-identical-runs
claim: At temperature 0, pwd's stage-3 core recall moves by 0.400 across three otherwise identical runs.
status: confirmed
created: 2026-09-22
updated: null
dimensions:
  - 4
stages:
  - trace
paper_sections:
  - §5
evidence:
  - label: core recall spread, pwd
    value: 0.4
    denominator: three samples of one cell at temperature 0 (1.000, 1.000, 0.600)
    metric: core.micro.recall
    method: trace_recovery_diff
    run_ids: []
    campaign_ids:
      - p1_trace
    aggregation: max minus min across the cell's samples
    scorer_commit: null
    excluded: null
    recheck: null
corrections: []
needs_v1_authors: false
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

The second reproducibility result, and the second one the existing report
understates: it shows 0.250, which is the spread in F1 rather than in recall.

Taken with [[stage1-tac-moves-between-identical-runs]], two of the four stages show run-to-run
variation at temperature 0 on at least one command. That is itself a result — the paper reports
no variance measurement of any kind.
