---
name: project-experiment-program
description: The experiment program is planned end-to-end (2026-09-06 doc + task 006); ONE approval (the run matrix) unblocks all result phases; E0 started
metadata:
  type: project
---

As of 2026-09-06 the science program for the white-paper resubmission is fully planned and
grounded in the implemented v2:

- `ai_docs/analysis/experiment_implementation_plan.md` re-grounds every designed experiment
  (E0–E6, plus the disagreement study S5) in the implemented four-stage pipeline, adds the
  adversarially-reviewed second cycle (observation-limited tracing promoted; per-stage
  fidelity study promoted-reframed; two new arms; demotions recorded), and carries the
  **run matrix + cost estimate in its Part 6** — the single approval that unblocks the
  blocked result phases of tasks 001 (Ph7), 002 (Ph4), 003 (Ph5), 004 (Ph4).
  Program LLM cost ≈ $400–800 total; scarce resources are person-time and Lima hours.
- `ai_docs/tasks/006_evaluation_harness.md` specifies the missing instrument (stage-1 scorer,
  sweep runner, doc-mutation harness, aggregation, two Lima-track drivers) as an in-package
  build (`src/caruca_v2/harness/`). Task numbering: **005 stays reserved** for v1
  instrumentation per 001's sequencing decision; the harness is 006.
- Tiran's decisions this session: recommendations as a new analysis doc; harness gap treated
  as a first-class finding WITH a created task; start E0 (artifact pinning) immediately after
  the doc. E0 groundwork done same day: the caruca-experiments-branch worry is retired
  (≈ main), the paper's grep/ps/cp claims refer to the UPSTREAM annotations
  (github.com/binpash/annotations — public, history intact), not v1's local copies.

**Why it matters:** any future session picking up experiments should start from that doc's
Part 6 gate status and task 006's phase checkboxes — not re-derive the program. If the run
matrix has been approved since, the next action is task 006 Phase 6 (C0 pilot).

Related: [[caruca-v2-build-tiering]], [[caruca-v1-eval-tooling-notes]], [[mac-lima-tracing-env]].

**E0 update (2026-09-06, same session):** E0 is DONE — findings in
`ai_docs/analysis/e0_artifact_pinning.md`. Headlines: grep claim reproduces only against
pre-2021-04-06 PaSh (fixed by binpash/pash#192, 3.5 years before Caruca); ps annotation
still wrong upstream today but ps is entirely outside v1's population (no man page/spec
anywhere — ask Greenberg where the paper's ps run came from); cp never had a hand-written
annotation (the claim describes PaSh's conservative default) and fresh v1-on-main derives
side-effectful, contradicting the paper's "pure" (ask Greenberg which revision produced it).
Population pinned: Q2 denominator = ~120 committed specs, NOT the 108 ground-truth JSONs.
Redundancy sweep: 82.7% duplicate invocations overall; tracer executes the duplicated
stream; --number wrong for 90/90; 14 commands crash generate (empty-flag-group ValueError).
Artifacts: eval/e0/ (committed-side), v1's caruca/outputs/ (13 fresh small-command traces +
bounded grep/cp traces + annotations, untracked). Lima VM returned to stopped state.

**Approval (2026-09-08):** Tiran approved the FULL run matrix (C0-C6, implementation plan
Part 6) in-session and asked for execution with milestone stops. The single gate is open;
task 006 build started same day. Requested working style: show the work, stop at milestones.

**Model pair (Tiran, 2026-09-08):** the harness compares models as a first-class feature;
the directed pair is `openai/gpt-4o` (paper baseline, runs first, pinned to OpenAI routing)
vs `anthropic/claude-haiku-4.5` (comparison arm). Campaign files carry both; summaries roll
up per model. Cross-model campaigns after the config freeze must set
`frozen_model_only: false` (the C4 pattern) — the freeze gate enforces this in code.

**C0 pilot complete (2026-09-08):** first live model calls ever. Total spend ≈ $1.15.
Pilot caught 4 defects (all fixed + regression-tested, suite now 174): relative-path
validation, frozen-dataclass exception, contextmanager enter outside try, scorer not
deduplicating across v1's alternative syntax forms. Post-fix: stage 1 perfect (F1 1.0)
for BOTH gpt-4o and claude-haiku-4.5 on mkdir/cat/wc; stage 2 = perfect precision/tiny
recall (models incomplete, not wrong — gpt-4o stops voluntarily, haiku hits the cap);
stage 4 all valid. TWO structural findings: v1's CommandConfig JSON schema renders stdin
as bare {"title": "Stdin"} (custom serializer defeats pydantic) → both models emit null
→ 0/6 stage-2 validity + stage-3 workspace_failed propagation at the seam. Haiku
10-50% cheaper per cell everywhere. PENDING DECISION before C1: complete the stage-2
prompt with valid stdin enum names (pre-freeze output-format completion, new
prompt_hash); stage-3 token calibration waits on it.

**Agentic-SDK arm directed into scope (Tiran, 2026-09-08):** task 007 adds a per-stage
`--approach {one-shot,agentic}` toggle using the Claude Agent SDK (Claude Code as a
library), to MEASURE what the engineered agentic harness buys over the single prompt.
Why this does not conflict with the Eiers deferral: the deferred thing was an agentic
*replacement pipeline*; 007 adds agentic cells as measured treatment arms while the naive
one-shot control stays frozen and untouched. Key design controls (in the task doc): same
information budget (Read/Write only, no execution/web tools), jailed workspace so the
agent never sees this repo or v1 beyond its placed files, a plumbing-control arm
(SDK single-turn/no-tools) separating harness effects from access-layer effects,
pre-registered per-stage predictions (stage-1 null expected, stage-2 recall gain
expected), and API-key-billing required so SDK cost is real. Stage 3 deferred
(harness-vs-harness). Needs its own cost-line approval before any live agentic cell.
