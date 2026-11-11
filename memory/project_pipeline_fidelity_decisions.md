---
name: project_pipeline_fidelity_decisions
description: 2026-10-13 — Tiran's decisions creating tasks 014 (v2 reproduces v1's four steps, with telemetry) and 015 (iterate the tracing-step prompt until the model always returns its report); done = per-step on v1's input AND a chained run; six confirmation commands; $40 ceiling; open check 2 answered from v1 code
metadata:
  type: project
---

**Decisions Tiran made on 2026-10-13, when tasks 014 and 015 were created** (`ai_docs/tasks/`):

1. **"Faithfully reproduces v1" means both**: each v2 step, fed v1's own input to that step,
   agrees with v1 within stated thresholds, *and* v2's own output flows through all four steps
   (a chained run, never done as of this date) for every test command.
2. **Six confirmation commands outside the nine, chosen by the coordinating session before any
   run**: `rmdir nl du dirname split bc` (reasons and frozen predictions in task 014 §4). They
   avoid task 001's held-out set and the four few-shot exemplars.
3. **$40 ceiling for task 014**, each paid batch's estimate written into the document first.
   Task 015 has its own $10 estimate awaiting his line.
4. **The tracing step's prose problem is attacked by iterating the prompt in a separate test
   task (015)** — forced JSON output, precise examples, a two-step prompt if needed — until the
   output is controlled. He chose this over the "force the tool call as one new arm" option.
   This is a recorded scope decision: output control, not tuning
   ([[feedback_instrument_defect_vs_tuning]]). Still banned: command-specific hints, telling
   the model how many answers to expect.
5. **Full telemetry on both sides, easy to reach in the console**, is a deliverable (task 014
   §7 and phase 3: forwarder for v1's model call, cached tokens, versions, a Performance screen).

**Decided later the same day (task 014 §8):** five setup variants per path at step 2 — yes, as a second arm; v1's prompt is the starting point and may be improved when the change resolves a named v1 issue ([[feedback_improve_v1_prompt_when_tied_to_issue]]); task 015's limit is $20; free phases started 2026-10-13 with the session assignment and file ownership written in task 014 §8.

**Facts established the same day:**
- **Task 011's open check 2 is answered from v1's code**: v1's annotator reads the
  relevance-*filtered* traces — `tracer/data.py:198`, `to_annotation` calls
  `self.__readwrite(sandbox)` and derives everything from it. So feeding v2 the filtered view
  (which makes `rm` and `tee` fit the context window) is a fidelity alignment (kind C), not a
  method change. Open check 1 (does the empty `no_env` placeholder render as an empty
  argument?) is still open; task 014 phase 0.
- v1's enumeration for the six at `--max-count 1`, printed / distinct lines: rmdir 20/12,
  nl 52/38, du 160/106, dirname 12/8, split 60/42, bc 17/10 (counted by printing
  `caruca generate CMD --max-count 1`, Mac `.venv`).
- Tasks 009 and 011 are superseded for execution by 014; their diagnosis stands.
- Task numbering: 014 and 015 taken 2026-10-13; the pash-downstream-study session's planned
  VM-provisioning/benchmark task was to take 016, but 016 went to the naive Claude Code arm on
  2026-10-13 (`project_naive_claude_code_arm.md`); that VM task should take 018 (017 went to the naive arm's build documentation, 2026-10-13).

**Task numbering (2026-11-10):** 020 = v1 writes PaSh's current Python annotations
(`ai_docs/tasks/020_v1_pash_python_annotations.md`). Next free task number is **022** (021 = v1-vs-naive PaSh annotation comparison plan, 2026-11-11).
**Task 020 comparison decisions (Tiran accepted the proposed defaults, 2026-11-10):** test lines = the
real-world corpus (`eval/user-scripts/invocations.txt`) as the main set + every side's own test lines as
the second; reference = PaSh 0.2.4's own hand-written classes where they exist + every disagreement checked
by running the command; a second v1 column with the main grammar for commands that have both grammars
(2 flags per line if 4 exceeds 5 hours); v1 cases match on *exactly* their flags; lines v1 never traced
count as "v1 has no answer"; inputs/outputs compared mainly on read/written, since v1 knows nothing finer;
entries PaSh's format can't hold go to `v1_unplaced_io.json`, never silently dropped.
