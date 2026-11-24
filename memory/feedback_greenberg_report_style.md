---
name: feedback-greenberg-report-style
description: Michael Greenberg dislikes long, AI-sounding, detail-heavy reports; he wants very simple, human-like reporting of what was observed, with clean, clear tables and charts
metadata:
  type: feedback
---
Reports for Michael Greenberg must be **very simple and human-like: what did we observe, with clean,
clear tables and charts.** He does not like long, AI-sounding reports; he finds them confusing and
over-detailed.

**Why:** Tiran, 2026-11-24, when setting up the reporting of the PaSh suite comparison; it matches his
own earlier reactions (addendum v0.6 rewritten as simple insights, "be brief", plain language).

**How to apply:** for any report Michael will read, plan the tables and charts first, lead with the
observation, keep the body short, and move method detail and records to an appendix or linked files.
A report-design pass by a separate high-effort agent (`orchestration/brief_report_ideation.md` in the
2026-11-24 run folder) is the pattern Tiran asked for.
Related: [[feedback-plain-language]], [[feedback-be-brief]], [[feedback-addendum-style]],
[[feedback-v1-v2-framing]], [[project-key-people]].

**Addition (Tiran, 2026-11-24):** he wants the path to every test script in the report, but in an
addendum, so the body stays simple. General rule: detail he wants on record (paths, command lines,
records) goes in an addendum; the body keeps only the observations, tables and charts.

**Addition (Tiran, 2026-11-24):** the report carries an appendix explaining, in simple terms for someone
new to PaSh, how the experiment was set up: what PaSh does with annotation files, what was compared (nothing
regenerated), which scripts and why Koala, how each ran, how splitting was detected, why it takes hours
(the scripts' own run time × sources × repeats), timing conditions, the independent check. Written as A5
in `report_draft.md`; keep it in every later version.

**Format (Tiran, 2026-11-24, on the interim PDF):** no "To/From/Date" email fields and no "where this
stands / done" section; the opening page carries the title, one line with the draft version, and the
short summary in large text (`<p style="font-size:1.3em">` works in the repo's PDF converter).

**Numbering (Tiran, 2026-11-24):** every table and figure is numbered ("Table 1.", "Figure 3.") with a
caption (bold label above tables; italic paragraph under figures, since the converter drops alt text) and
is referred to by number in the text, so he can ask questions by number.
