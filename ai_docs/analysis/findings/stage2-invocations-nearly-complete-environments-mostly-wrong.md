---
id: stage2-invocations-nearly-complete-environments-mostly-wrong
claim: At stage 2 v2 reproduces almost all of v1's distinct invocations but asks for the wrong filesystem environment in about four cases out of five.
status: confirmed
created: 2026-09-22
updated: null
dimensions:
  - 1
stages:
  - generate
paper_sections:
  - §4
evidence:
  - label: invocation recall
    value: 0.878
    denominator: v1's distinct invocations at the same bound
    metric: recall
    method: invocation_set_diff
    run_ids: []
    campaign_ids:
      - p1_generate
    aggregation: mean over the arm's scored cells
    scorer_commit: null
    excluded: null
    recheck:
      kind: campaign_metric
      campaign: p1_generate
      metric: recall
      method: invocation_set_diff
  - label: invocation precision
    value: 0.568
    denominator: v2's distinct invocations
    metric: precision
    method: invocation_set_diff
    run_ids: []
    campaign_ids:
      - p1_generate
    aggregation: mean over the arm's scored cells
    scorer_commit: null
    excluded: null
    recheck: null
  - label: environment agreement
    value: 0.208
    denominator: the 24 cells where the rate is defined
    metric: env_agreement_rate
    method: config_env_diff
    run_ids: []
    campaign_ids:
      - p1_generate
    aggregation: mean over cells where it is defined
    scorer_commit: null
    excluded: uniq's cells, where no invocation matched, so there is no environment to compare
    recheck: null
corrections:
  - date: 2026-09-20
    old_value: 0.185
    new_value: 0.208
    why: The first figure divided by 27 rather than 24, counting uniq's undefined cells as zeros. A rate is computed only over the cases where it is defined.
needs_v1_authors: false
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

The headline of the whole study sits here: v2 reproduces what v1 *writes* far better
than what v1 *means*. It recovers v1's invocation strings almost exactly and then asks for the
wrong filesystem.

**Environment agreement is a correctness rate, not a reach figure.** 0.208 means that of the
environments v2 asked for, roughly one in five is one v1 would also have built. It is not
"coverage" — that word is reserved for real-world reach.

The figure was published once as 0.185 and corrected; see the correction below and
[[stage2-the-0185-error]].
