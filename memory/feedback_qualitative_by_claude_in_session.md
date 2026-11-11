---
name: feedback-qualitative-by-claude-in-session
description: Qualitative comparisons (diff views + assessment) are done by Claude in the working session against a versioned rubric, not coded; scorers do only the counting; Greenberg's standing question is whether/how the IO sets differ
metadata:
  type: feedback
---
2026-11-11, Tiran, reviewing task 021 (v1 vs naive PaSh annotations): add a first step that is a
qualitative comparison (diff view + an LLM assessment). "This is where you can use an LLM. You can do
that yourself, no need to write code for it... so that we can tweak how we do the qualitative
assessment." A scorer is still built for the quantitative side. Greenberg wants to know whether the
IO sets differ and what the difference is.

**Why:** the judgement method has to stay easy to change while it's being worked out; code would freeze
it too early. Counting must still be reproducible, so it stays in code.

**How to apply:**
- Qualitative assessment = Claude in session, following a versioned `rubric.md`; record rubric
  version + model ID + date per assessment; blind A/B labels (the naive agent is also Claude); check
  verdicts by running the command; pilot on a few commands and stop for Tiran's review before scaling.
- Scorer code counts and builds the views (decision tables, IO-set diffs), and reads assessment
  front matter, but never judges.
- Any v1-vs-naive annotation report leads with the IO-set difference answer for Greenberg.
- Where it was applied: `ai_docs/tasks/021_pash_annotations_v1_vs_naive_comparison.md` sections 4, 6, 8.
  Related: [[project-naive-claude-code-arm]], [[feedback-be-brief]].
