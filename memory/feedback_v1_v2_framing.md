---
name: feedback-v1-v2-framing
description: "Frame v2 as extending v1's capabilities, not fixing v1's shortcomings, in stakeholder-facing writing"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e55744e3-d1dd-487a-99ca-6aa32eb049d4
  modified: 2026-08-29T13:17:50.938Z
---

When writing prose that compares caruca_v2 to v1 (planning docs, stakeholder-facing summaries, paper
drafts, README-style text), favor framing v2 as extending v1's capabilities and application scope, not
as correcting v1's deficiencies. Prefer "v2 adds the ability to handle X" over "v1 fails to handle X" or
"v1 is broken/limited."

**Why:** Tiran asked for this explicitly while drafting the Master Idea Document's stakeholder section
(2026-08-29), specifically because this document and similar framing will be shared with mentors and
advisors — including Prof. Greenberg, who is both Tiran's PhD advisor and the PI/author of Caruca v1
itself (see [[project_key_people]]). Casting v1 as flawed reads poorly when a co-author of v1 is a
primary reader.

**How to apply:** This is about tone/framing in prose meant for people, not about hiding real technical
facts. Plainly-stated engineering limitations that already live in CLAUDE.md (e.g., v1's LLM step broken
against modern DSPy, WSL missing strace/overlayfs) are fine to state when needed for accuracy or planning
- don't suppress them. But when writing narrative/evaluative sections (End Goal, Core Problem, summaries
for advisors), lead with what v2 newly enables rather than dwelling on what v1 lacks. Applies to
`ai_docs/prep/master_idea.md` and any future planning docs, not just the current step.
