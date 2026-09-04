---
name: llm-pipeline-replication
description: "2026-09-03: Tiran greenlit replicating ALL of v1's hard-coded stages with minimally-instructed LLMs (tasks 002-004), alongside — not replacing — the naive one-prompt control; core principles and decisions"
metadata:
  type: project
---

On 2026-09-03, after reviewing task 001, Tiran directed that v2 should replicate **every**
stage of v1's pipeline with LLMs — not only the syntax-spec stage the naive control
covers. Authoritative design: `ai_docs/prep/llm_pipeline_replication.md`; tasks
`002_llm_config_generation`, `003_llm_execution_tracing`, `004_llm_annotation` (v1's
DSPy repair/instrumentation moved to task 005).

**Why:** the interesting research question is how much of v1's ~3,300 hand-written lines a
simply-instructed LLM replaces (evaluation criterion 6). The Eiers-scoped one-prompt
control (task 001) **stays** as the first deliverable — the series *extends* the agreed
comparison, and every stage is measured against its v1 counterpart via v1's own file
formats as seams. Frame it to advisors as extending, not superseding.

**Decisions made by Tiran that day (all interactive Q&A):**
- **Structure:** keep 001 as the control; stages as separate tasks 002-004, each
  standalone-runnable by consuming v1-produced input files.
- **Engine:** our own hand-written tool loop over OpenRouter (works with every model
  behind the one key; every message loggable) — NOT the Claude Agent SDK, NOT litellm.
- **Prompts are markdown files** in a repo-root `prompts/` folder (`<stage>/system.md` +
  `user.md`, `{{placeholder}}` substitution only) — never assembled in code. Committed
  files contain only our text; v1-derived content injected at runtime (v1 is private and
  unlicensed).
- **Minimal instruction:** prompts state input / expected behavior / output / format,
  nothing more — no algorithms, no coaching past failures; failures are results.
- **Hard enforcement over prompt politeness:** e.g. "you may only use `cat`" appears in
  the prompt AND the executor rejects any other binary; observation happens via jailed
  Python tools (list/read/stat), not shell commands.
- **v1-faithful environments, "no improvements":** stage-3 workspaces must match v1's
  environment setup exactly (same files/dirs/fixture payloads from v1's `data/`, read at
  runtime) — Tiran explicitly rejected enriched/extra fixtures; comparability requires
  identical inputs.
- **Execution safety staging:** harmless commands in throwaway temp dirs on the Mac
  first; `rm`-class/destructive commands deferred until Docker or a Linux host (no Docker
  on the Mac as of this date).
- **Observability:** telemetry record per LLM call (multi-turn stages emit one per turn,
  shared `run_id`, `stage` field) + `eval/metrics.db` row; conversation-trace logging via
  one switch (`--log-conversation` / `CARUCA_V2_LOG_CONVERSATION=1`) writing
  `conversation.jsonl` per run, off by default.

**How to apply:** when scoping any v2 pipeline work, check the design doc first; don't
re-propose agent frameworks, prompt engineering, or "better" fixtures — those calls are
made. See also [[caruca-v2-baseline-scope]] (the control's guardrail still binds task 001).
