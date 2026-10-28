---
name: feedback-naive-llm-standalone
description: Addendum material from the naive-LLM arm goes under its own "Naive LLM" heading and must stand alone, citing only primary sources, never the earlier rebuild's findings
metadata:
  type: feedback
---

Tiran, 2026-10-20: "all our addendums should be under a new heading: naive llm. it differs from prior runs
so shouldn't rely on earlier findings."

**Rule.** Every resubmission proposal drawn from the naive-LLM arm (`naive_llm_caruca/`, task 016) lives in
`naive_llm_caruca/white_paper_addendum_naive_llm.md` (title "Naive LLM: addendum to *Caruca*"), as numbered
sections under that one heading; the analysis index has a "Naive LLM" heading for it. These documents do not
slot into `white_paper_addendum.md` and do not cite the earlier stage-by-stage rebuild (parity study, E0,
`caruca_purpose_grep_case`, campaign figures) or memory notes as evidence. Each claim is re-established from
a primary source: the paper, v1's code, files or git history, or the naive runs' own logs.

**Why:** the naive arm is a different experiment (one undirected agent, no pipeline), so carrying over the
earlier findings would mix evidence from two designs.

**How to apply:** when a fact first came from an earlier note, re-verify it at the source and cite the source
(as done 2026-10-20 for grep's single-form grammars, by loading them through v1's DSL and running
`caruca generate grep --max-count 1`, and for the references' provenance, via `git log`). Related:
[[project-naive-claude-code-arm]], [[feedback-v1-v2-framing]].
