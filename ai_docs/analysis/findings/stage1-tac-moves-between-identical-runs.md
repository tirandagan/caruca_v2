---
id: stage1-tac-moves-between-identical-runs
claim: At temperature 0, tac's exact-argument rate moves by 0.200 across three otherwise identical stage-1 runs.
status: confirmed
created: 2026-09-22
updated: null
dimensions:
  - 4
stages:
  - syntax_spec
paper_sections:
  - Q2
evidence:
  - label: exact-argument rate spread, tac
    value: 0.2
    denominator: three samples of one cell at temperature 0
    metric: exact_argument_rate
    method: q2_syntax_diff
    run_ids: []
    campaign_ids:
      - p1_syntax_spec
    aggregation: max minus min across the cell's samples
    scorer_commit: null
    excluded: null
    recheck: null
corrections: []
needs_v1_authors: false
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

One command in nine is enough to justify running more than one sample for the whole
experiment programme: with a single sample there is no way to tell "v2 differs from v1" from
"v2 differs from itself". Every other command is stable at 0.000.

**The existing report does not show this.** `report.py::consistency()` measures the stage's
headline metric, which at stage 1 is F1 — and F1 is 1.000 in every sample. The console computes
a spread for every metric instead, which is where this appears.

The paper runs its LLM step once per command and reports no variance measurement at all.
