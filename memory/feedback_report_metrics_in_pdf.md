---
name: feedback_report_metrics_in_pdf
description: Every metric Tiran specified for an experiment must appear in the delivered PDF (addendum tables), not only in the counting output; brevity applies to the body, not to coverage
metadata:
  type: feedback
---

2026-11-26, after the PaSh suite report Draft 1.0: Tiran asked "I thought we would report based on the test
scripts, including all the metrics we discussed such as crashes, the reason for the PaSh crashes, etc. Are you
using the right instructions?" The counting had every metric from his spec (`orchestration/metrics_spec.md`),
but the PDF's addendum had lost the detail tables when the pilot report was cut down for a deadline.

**Why:** his metrics spec is the contract for the write-up; Michael's brevity rule shapes the body, not what the
document contains. A metric that exists only in a numbers file is, to Tiran, not reported.

**How to apply:** before calling a report ready, check every item of the metrics spec against the PDF (body or
addendum) and list where each appears; per-script tables, crash counts with exception text and causes per part
go in addendum tables. Related: [[feedback_greenberg_report_style]], [[project_pash_suite_comparison]].
