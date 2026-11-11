---
name: feedback_never_modify_v1_source
description: 2026-10-13 — v1's source is never modified (one exception, 2026-11-10: local branch `pash-python-annotations` for task 020) (wrapper/console fixes only); v1 issues are captured as findings, improvements are made in v2 and noted as incremental differences
metadata:
  type: feedback
---

**What Tiran said (2026-10-13):** "We are not to touch V1 or change it. Whatever V1 does, unless
the wrapper needs to be fixed, the original Caruca is not to be touched. We are going to capture
issues with V1, but we have an opportunity to improve it with V2 and note what we're doing that is
incrementally different. We're not touching the source code for V1."

**Why:** v1 is the baseline being measured. A modified baseline is not the paper's system, and
co-authors (Greenberg) own it. The same rule already applies to PaSh ([[pash_work_scheduling]]:
"don't modify PaSh source").

**How to apply:**
- No edits under `~/stevens/caruca/` (Mac: `~/dev/stevens/caruca/`), including `llm.py`'s DSPy
  breakage, the `gpt-4o` hardcode, `tracer/data.py`'s macOS `/tmp` path, `cli/trace.py`'s
  `--output` help text, or `generate --number`. Redirect v1 from the *outside* only: environment
  variables (`OPENAI_BASE_URL`, `CARUCA_ISOLATION_METHOD`), a separate virtualenv (`.venv-llm`),
  running it inside the Lima VM, or the console wrapper.
- "Wrapper" = the console (`console/`) and v2's `v1.py` runner. Those may be fixed freely.
- Every v1 defect becomes a finding (`ai_docs/analysis/findings/`) and, where v2 does better, an
  entry in `v2_fidelity_to_v1.md`'s deviation ledger marked as a deliberate increment — never a
  patch to v1.
- This supersedes any earlier suggestion that task 005 would "instrument v1" by editing it; v1
  telemetry must come from the wrapper (the console's run records and the metering forwarder).
- Watch for accidental modification: on 2026-10-13 `caruca/save/ls.json` in v1's checkout showed
  as modified (mtime 2026-09-03, the Lima setup day) — report such things to Tiran, don't fix
  silently.

**Exception (Tiran, 2026-11-10, task 020):** "improve the original Caruca, not V2" so it writes PaSh's
current Python annotations. Tiran chose to put the new `caruca annotate pash-py` target inside v1's code
on a **local branch `pash-python-annotations`** of v1's repo, never on v1's `main`, never pushed without
asking. The exception covers that branch only; every other v1 edit is still off limits. Its commits
must leave out the pre-existing local `caruca/save/ls.json` change and untracked `eval/correct_specs.txt`.
The writer must be deterministic and contain no LLM (Tiran's explicit condition).

**2026-11-10, later:** at Tiran's request ("i need to push a new branch in caruca's original repo so authors
can review it") the branch `pash-python-annotations` was **pushed to `binpash/caruca`** (commits `5794d373b`
writer + tests, `7c967a983` save_pash_py/ outputs for cut/sort/rm + run_pash_py.sh + README). Still never v1's
`main`; `save/ls.json` and `eval/correct_specs.txt` stay out of every commit. Further pushes to this branch
are within that request; anything else in v1's repo still needs asking.

**Where task 020 work goes (Tiran, 2026-11-10, after twice not finding it):** "let's make all changes to caruca
pipeline to the caruca repo under our new branch. stop using caruca_v2 repo". So the writer, run scripts
(`caruca/run_pash_py.sh`, `caruca/count_runs.py`), every generated output (`caruca/save_pash_py/<cmd>/<grammar>_grammar/trace_<n>/`)
and the detailed README (`caruca/save_pash_py/README.md`) live in v1's branch and are pushed there; caruca_v2's
`naive_llm_caruca/v1_pash_py/` is only a pointer. **Why:** the authors review the branch, and Tiran looks for
the work there. Commits on the branch so far: `5794d373b`, `7c967a983`, `b7da7f8a0`, `5496c6672`.
