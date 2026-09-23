---
id: stage1-neither-system-misses-a-flag
claim: At stage 1 neither v2 nor v1's own LLM output misses or invents a single flag on any of the nine parity commands.
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
  - label: flag F1, v2
    value: 1
    denominator: flags in v1's committed reference specification, over 27 scored cells
    metric: f1
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
      metric: f1
      method: q2_syntax_diff
corrections: []
needs_v1_authors: false
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

Both systems recover every flag v1's committed specification declares, on all nine
commands. Nothing is missing and nothing is invented on either side.

This is the one stage where v1 also uses a model, so it is the only like-for-like comparison in
the study. It is also one of the few results that runs in v1's favour on the finer measure — see
[[stage1-v1-is-slightly-better-at-typing]].
