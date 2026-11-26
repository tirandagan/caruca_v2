---
name: feedback_herdr_worker_model_choice
description: Herdr rules from Tiran (2026-11-26) - worker panes default to Antigravity "Gemini 4 Neon" (other models only when complexity needs them, effort matched to task); related work = panes in the current tab, a different class of work = a new tab; close panes whose agents are no longer needed
metadata:
  type: feedback
---

Tiran, 2026-11-26 ("remember"): whenever work is being orchestrated from inside Herdr by Claude Code running
on Fable, use **Antigravity (Gemini 4 Neon)** for the worker tasks by default (`herdr agent start <name> --kind agy`).
Other models (Claude Code Opus/Sonnet panes, Fable itself) remain allowed, but only when the task's complexity
needs them; pick the model and the effort level that fit the task so tokens are not wasted.

**Why:** cost. Opus panes at medium or high effort were being used for every worker task (report rewrites,
counting, indexing); most of those tasks do not need that.

**How to apply:** before `herdr agent start`, decide: mechanical or well-specified work (file gathering,
counting scripts, HTML edits from a precise brief, README fixes) goes to `--kind agy`; judgment-heavy work
(vetting causes, design review, writing for Michael) may use a Claude pane, stating why; pass the lowest
effort that fits. Antigravity gotchas seen 2026-11-24: a "trust folder" prompt needs `enter`; prompts sent while
an overlay is open do not submit (send `esc`, resend). Related: [[project_pash_suite_comparison]],
[[project_requesty_llm_billing]].

## Layout rules (Tiran, 2026-11-26, same day)

- **Related work goes in panes of the current tab**, split from the orchestrator (`herdr pane split`), launched
  first before anything else; **a different class of work gets a new tab** (`herdr tab create`), e.g. the
  venue research or a repo split would not share the PaSh-suite tab.
- **Close panes whose agents are no longer needed** as soon as their report is read (`herdr pane close <id>`);
  do not leave idle agents open "in case". Name every pane and tab after its job (`herdr pane rename`).

**Why:** he watches the Herdr window; stray idle panes and unrelated work mixed into one tab make it hard
to see what is running, and idle agents cost context when re-prompted.
