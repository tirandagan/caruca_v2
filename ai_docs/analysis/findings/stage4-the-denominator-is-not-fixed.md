---
id: stage4-the-denominator-is-not-fixed
claim: "At stage 4 the denominator is itself a result: how many cases align at all depends on what v2 produced, so it moves between samples."
status: draft
created: 2026-09-22
updated: null
dimensions:
  - 1
  - 4
stages:
  - annotate
paper_sections:
  - Q1
evidence:
  - label: aligned cases, sample 0
    value: 33
    denominator: "a count, not a rate: cases aligned in that sample"
    metric: agreement.comparable
    method: annotation_diff
    run_ids: []
    campaign_ids:
      - p1_annotate
    aggregation: summed over the nine commands in one sample
    scorer_commit: null
    excluded: null
    recheck: null
  - label: aligned cases, sample 2
    value: 14
    denominator: "a count, not a rate: cases aligned in that sample"
    metric: agreement.comparable
    method: annotation_diff
    run_ids: []
    campaign_ids:
      - p1_annotate
    aggregation: summed over the nine commands in one sample
    scorer_commit: null
    excluded: null
    recheck: null
corrections: []
needs_v1_authors: false
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

The three samples align 33, 30 and 14 cases. That is not noise in a measurement — it
is the measurement changing shape, because alignment depends on the annotation v2 produced.

Two consequences:

- **A per-sample rate cannot simply be averaged.** A sample aligning 2 cases would carry the
  same weight as one aligning 14. The figures in [[stage4-class-agreement-pooled-over-three-runs]]
  are pooled for that reason.
- **"Movement between samples" is not a single number here.** Both parts of the ratio move, so
  a spread figure describes neither. The console shows each sample's own counts instead.
