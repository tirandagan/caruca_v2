---
name: feedback-addendum-style
description: Tiran's required shape for the naive-LLM addendum (2026-10-28) - very simple, four questions per insight, no file names or command-line examples in the body, sources/runs table at the end
metadata:
  type: feedback
---

Tiran, 2026-10-28, on `naive_llm_caruca/white_paper_addendum_naive_llm.md`: "very simply stated, clear, with
links to other documents. reduce any unhelpful details such as file names, command line argument examples,
or long descriptions: for every insight focus on: what did we find? what does this teach us about the naive
llm decision making? how is it different than caruca's approach? how is it better?" The last part holds
citations, references, links to the runs' source data, and a summary table of runs.

**How it was applied (version 0.6):** one-paragraph summary; a findings-at-a-glance table with a "stronger
here" column (agent / Caruca / level, so findings where Caruca's design wins are stated honestly, with the
fourth heading becoming "Where Caruca's way is stronger"); each finding as What we found / What this shows
about the agent's choices / How Caruca does it / What the agent's way adds; proposals pairing "agent finds,
Caruca checks"; a short not-yet-checked list; runs table, per-finding sources table and documents at the end.
File-and-line evidence was left in version 0.5, linked as a GitHub permalink (commit 5ea191c).

**Why:** the addendum goes to the Caruca co-authors; they need the insight, not the forensic trail.
Related: [[feedback-plain-language]], [[feedback-v1-v2-framing]], [[feedback-naive-llm-standalone]].
