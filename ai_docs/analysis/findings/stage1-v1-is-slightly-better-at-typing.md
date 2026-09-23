---
id: stage1-v1-is-slightly-better-at-typing
claim: Where the two stage-1 specifications differ, the difference is argument typing rather than missing flags, and v1 is slightly ahead.
status: confirmed
created: 2026-09-22
updated: null
dimensions:
  - 1
stages:
  - syntax_spec
paper_sections:
  - Q2
evidence:
  - label: exact-argument rate, v2
    value: 0.967
    denominator: arguments in the reference specification, over 27 scored cells
    metric: exact_argument_rate
    method: q2_syntax_diff
    run_ids: []
    campaign_ids:
      - p1_syntax_spec
    aggregation: mean over the arm's scored cells
    scorer_commit: null
    excluded: null
    recheck:
      kind: campaign_metric
      campaign: p1_syntax_spec
      metric: exact_argument_rate
      method: q2_syntax_diff
  - label: exact-argument rate, v1's own LLM output
    value: 0.983
    denominator: arguments in the reference specification, same nine commands
    metric: exact_argument_rate
    method: q2_syntax_diff
    run_ids: []
    campaign_ids: []
    aggregation: measured once; v1's LLM output is a fixed archived artifact
    scorer_commit: null
    excluded: nothing
    recheck: null
corrections: []
needs_v1_authors: false
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

The two systems are identical on seven of the nine commands. They differ on `tail`
(0.769 against 0.846) and `tac` (0.933 against 1.000), and both differences are typing.

Worth stating plainly because most of this study's surprises run the other way. v1's side is a
fixed archived artifact rather than a campaign, so it has no runs to re-check against.
