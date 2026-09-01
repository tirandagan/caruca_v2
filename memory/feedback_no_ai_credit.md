---
name: feedback-no-ai-credit
description: Never credit Claude/Claude Code in commits, PRs, or other outward-facing artifacts
metadata:
  type: feedback
---

Never add AI-attribution lines to anything outward-facing — commit messages, PR titles/descriptions,
code comments, issue text, etc. No "Co-Authored-By: Claude...", no "🤖 Generated with Claude Code", no
similar credit line.

**Why:** Tiran asked for this explicitly (2026-09-01), right after a PR (`binpash/caruca#54`) was opened
with both a `Co-Authored-By: Claude Opus 5` trailer and a "Generated with Claude Code" line in the body.
No further reasoning given — treat it as a firm preference, not just for that one PR.

**How to apply:** This applies project-wide, to any repo Tiran works in through this project (`caruca_v2`
itself, and `~/stevens/caruca` / `binpash/caruca` when opening PRs or making commits there), not just the
one that triggered it. When drafting a commit message or PR body, don't include the co-author trailer or
generated-with line even if a tool default or template would normally add one.
