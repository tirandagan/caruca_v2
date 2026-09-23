---
id: stage4-two-commands-exceed-the-context-window
claim: "v2 cannot annotate rm or tee at all: their traces make a prompt larger than the model's context window."
status: confirmed
created: 2026-09-22
updated: null
dimensions:
  - 1
  - 3
stages:
  - annotate
paper_sections:
  - Q1
  - §6
evidence:
  - label: cells that produced no annotation
    value: 6
    denominator: 27 stage-4 cells; all six failures are rm and tee, in every sample
    metric: status
    method: annotation_diff
    run_ids: []
    campaign_ids:
      - p1_annotate
    aggregation: count of cells with status error
    scorer_commit: null
    excluded: null
    recheck: null
  - label: prompt tokens requested for rm
    value: 224394
    denominator: tokens, against the endpoint's 128,000 limit
    metric: prompt_tokens
    method: measured_cost
    run_ids: []
    campaign_ids:
      - p1_annotate
    aggregation: as reported by the provider's rejection
    scorer_commit: null
    excluded: null
    recheck: null
corrections: []
needs_v1_authors: false
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

This is a ceiling intrinsic to the approach, not a quality result, and it should be
reported as one. v1 has no equivalent limit: it derives its specification procedurally from the
trace file, however large that file is.

Stating it as "v2 scored 0 on rm and tee" would be wrong twice over — it never produced an
annotation to score, and the failure is about input size rather than about reasoning.

The practical consequence for the experiment programme is that any stage-4 result is implicitly
conditioned on the trace fitting in a context window, and the commands that do not fit are
exactly the ones with the most filesystem activity.
