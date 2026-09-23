---
id: v1-generate-number-cannot-be-used-as-a-denominator
claim: v1's `generate --number` disagrees with what v1 actually prints on every command checked, and crashes outright on fourteen.
status: confirmed
created: 2026-09-22
updated: null
dimensions:
  - 2
  - 3
stages:
  - generate
paper_sections:
  - Q4
  - §7.4
evidence:
  - label: commands where --number disagrees with actual emission
    value: 90
    denominator: 90 commands that enumerate fully under a 500,000-line cap
    metric: hint_vs_emitted
    method: q2_syntax_diff
    run_ids: []
    campaign_ids: []
    aggregation: count of disagreeing commands
    scorer_commit: null
    excluded: null
    recheck: null
  - label: commands where --number crashes
    value: 14
    denominator: 120 man-page commands
    metric: hint_error
    method: q2_syntax_diff
    run_ids: []
    campaign_ids: []
    aggregation: count, including pwd, which is in the parity set
    scorer_commit: null
    excluded: null
    recheck: null
corrections: []
needs_v1_authors: false
source_document: ai_docs/analysis/e0_artifact_pinning.md
---

`--number` uses a different code path from the enumeration it claims to count. It
must never be used as a denominator or as a cost estimate.

The console's pre-flight counts by running `generate` at the chosen limits and counting the
lines it prints, which is what `mkdir` at v1's defaults shows as 4,240 printed and 1,094
distinct.

Twelve of the fourteen crashes are `ValueError: max() iterable argument is empty` on
mostly-zero-flag commands — a latent v1 defect worth an upstream issue.
