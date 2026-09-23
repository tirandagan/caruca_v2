---
id: stage4-class-agreement-pooled-over-three-runs
claim: On the strict instrument, v2 agrees with the hand-curated ground truth on parallelizability class in 25 of 77 aligned cases.
status: corrected
created: 2026-09-22
updated: null
dimensions:
  - 1
stages:
  - annotate
paper_sections:
  - Q1
  - §6
evidence:
  - label: parallelizability-class agreement, v2, strict
    value: 0.325
    denominator: 77 cases aligned across all three runs (25 agreeing)
    metric: agreement.pclass
    method: annotation_diff
    run_ids: []
    campaign_ids:
      - p1_annotate
    aggregation: "pooled: agreeing cases summed over aligned cases summed, across samples and commands"
    scorer_commit: null
    excluded: null
    recheck:
      kind: campaign_pooled
      campaign: p1_annotate
      stage: annotate
  - label: parallelizability-class agreement, v1, same seven commands, strict
    value: 0.172
    denominator: 64 aligned cases (11 agreeing)
    metric: agreement.pclass
    method: annotation_diff
    run_ids: []
    campaign_ids: []
    aggregation: measured once against the same ground truth
    scorer_commit: null
    excluded: null
    recheck: null
corrections:
  - date: 2026-09-22
    old_value: 10 of 33
    new_value: 25 of 77
    why: The first edition reported v2's first run only. Pooling all three samples gives 25 of 77.
needs_v1_authors: true
source_document: ai_docs/analysis/v1_v2_parity_study.md
---

**Two figures exist and neither may be quoted without saying which it is.** On the
strict instrument — this project's own — v2 agrees in 25 of 77 aligned cases. Under the
relaxation the paper's own evaluation applies, where telling parallelizable-pure from
non-parallelizable-pure is not required, both systems score roughly three times higher: 88.3%
for v2 and 65.6% for v1.

**A note for anyone quoting the task document.** `ai_docs/tasks/010_execution_console.md`
states this as "v2 10 of 33, v1 11 of 64" in two places. 10 of 33 is v2's *first run only* —
the figure first published and since superseded. The parity study itself carries the correct
pooled figure. See [[stage4-the-denominator-is-not-fixed]].

Needs the v1 authors' input: which of the two instruments the resubmission should lead with is
a question about the paper's own evaluation, not about this measurement.
