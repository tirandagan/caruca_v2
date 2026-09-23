---
id: v1-published-stage1-accuracy-is-not-reproducible-from-the-artifacts
claim: v1's committed LLM specifications score 78 of 116 by v1's own instrument, against the paper's published 116 of 120.
status: confirmed
created: 2026-09-22
updated: null
dimensions:
  - 1
stages:
  - syntax_spec
paper_sections:
  - Q2
  - §7.2
evidence:
  - label: v1 specifications matching ground truth, by v1's own cmp_specs.py
    value: 78
    denominator: 116 commands with both a specification and a man page
    metric: exact
    method: q2_syntax_diff
    run_ids: []
    campaign_ids: []
    aggregation: count of exactly matching specifications
    scorer_commit: null
    excluded: null
    recheck: null
  - label: the same, by an independent scorer
    value: 83
    denominator: 116 commands with both a specification and a man page
    metric: exact
    method: q2_syntax_diff
    run_ids: []
    campaign_ids: []
    aggregation: count of exactly matching specifications
    scorer_commit: null
    excluded: null
    recheck: null
corrections: []
needs_v1_authors: true
source_document: memory/caruca_v1_stage1_baseline.md
---

The published 116 of 120 cannot be reproduced from the artifacts the repository
ships. Use 78 of 116 as the stage-1 baseline and cite 116 of 120 only as the published figure,
with both denominators stated.

This needs the v1 authors: the gap may be a different artifact set, a different instrument, or
a scoring rule that is not in the code. It is not a claim that the paper is wrong, and the
resubmission should not present it as one.
