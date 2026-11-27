---
name: feedback_single_results
description: Results that come from several runs/sessions are presented as one set (one number per source); how the runs were split belongs only in the method appendix and records
metadata:
  type: feedback
---

2026-11-27, PaSh suite report Draft 2.0: Table 1 showed PaSh's own time for two sessions ("second session: 2.3 x bash")
and labelled each cell by session. Tiran: "distinguishing between these two makes no sense. It just gave you more
data. It should have a single set of results across the board."

**Why:** for the reader the extra run is more data for the same experiment, not a second experiment; session labels
in tables and figures read as two results and invite the wrong question (he took it for the 8-command run).

**How to apply:** when sources are measured in different runs, normalise each to its own run's reference (bash,
PaSh's own) and show one figure per source; pool the reference across runs (geometric mean) and pool noise controls.
Describe the runs once in the method appendix and list both record folders in the records table; nowhere else.
Related: [[feedback_greenberg_report_style]], [[project_pash_suite_comparison]].
