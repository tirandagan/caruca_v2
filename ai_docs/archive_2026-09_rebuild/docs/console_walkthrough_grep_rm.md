# Walking one command through both pipelines from the console — `grep`, then `rm`

Written 2026-10-13 for Tiran, against the console as it stands that day (task 014, phase 3).
Every button named here exists; every limit stated was read from the code the same day.

## Before you start (two minutes)

1. The Lima VM must be running: `limactl list` shows `caruca  Running`. Both v1's tracing and
   anything destructive run inside it. If it is stopped: `limactl start caruca`.
2. `.env` at the repo root holds `OPENROUTER_API_KEY`. Every v2 step needs it. (It does today.)
3. Start the console: `cd console && npm run dev`, then open `http://127.0.0.1:4317`. It listens
   on this Mac only.
4. You start from a clean slate: the runs, scores and findings from before today are in
   `eval/_archive/2026-10-13_parity/`, so the Runs page is empty and no step shows a verdict.

## How the page is laid out

The home page is **one command's pipeline**: four steps, top to bottom, each with **v1 on the
left, the comparison in the middle, v2 on the right**. Every button names the command it will
run (`trace grep in the VM`, `Run step 1 on v2 · grep`). The step v2 has not done yet carries the
one blue button. Each step has **Side by side**, which opens a popup with v1's file on the left
and v2's on the right, read from disk.

Picking a command: the three link rows (the study's nine, the six confirmation commands, anything
with runs), or the dropdown **every command v1 supports**, which lists all 118 commands v1 has a
grammar for, read from v1's own checkout.

## `grep`

Choose `grep` from the dropdown. v1's left-hand side is already partly filled: its committed
grammar and its archived LLM output (what the parity study used) exist for every v1 command.

### Step 1 — syntax description (the grammar)

- **v1:** nothing to run. v1's grammar was produced once by its LLM step and archived; the popup
  shows that file. (A *live* v1 step 1 is possible but not metered yet: it needs
  `OPENAI_API_KEY` and `OPENAI_BASE_URL=https://openrouter.ai/api/v1` exported in the shell that
  starts the console. Skip it for this walkthrough.)
- **v2:** click **Run step 1 on v2 · grep**. The run starts at once (no confirmation — your
  decision of 13 October; the estimate on the button is the only cost notice) and the Run page
  opens on that step alone, with the right-hand terminal showing v2 asking the model and
  validating the result. Measured on 13 October: 58 elements, validated, **$0.03, 12,347
  prompt + 597 completion tokens, 6.3 s**. When it says finished, click **← grep's pipeline**.
- Step 1 now shows v2's result: date, model, cost, tokens. **View v2's output** opens the run
  (terminal replay beside its events); **Inside the run** shows the prompt as sent and the raw
  response. **Side by side** shows the two grammars.

### Step 2 — command lines and file setups

- **v1:** its expansion for `grep` at the study's bound is already on disk
  (`eval/v1_configs/grep.configs.json`: 74 distinct command lines, 145 configurations). This
  is the one v1 artifact the page cannot make — it is a Python call, listed at the end.
  **Run v1 generate grep** only *prints* v1's command lines in the terminal (free, instant);
  it is a preview, not an input to anything.
- **v2:** **Run step 2 on v2 · grep** (the estimate is a mean over past runs; `grep` has 74
  distinct lines, so expect the upper end). Then **Side by side**: v1's expansion against v2's.

### Step 3 — run and trace

- **v1:** **Run v1 trace grep** → on the Run page, **trace grep in the VM** (free). v1 works out
  its own command lines from its grammar, runs each under strace inside the VM and writes the
  traces into this run's own folder (`eval/v1_runs/<run id>/grep.json`), never into v1's tree.
  `cat` took 2.4 seconds; `grep` has more lines, so allow a minute. The progress bar redraws in
  place; that is v1's real output.
- **v2:** **Run step 3 on v2 · grep** (about $0.035). v2 traces **v2's own newest step-2
  output** for `grep` — so run step 2 first — and runs in the VM, because v1's row does. It
  traces the **first 5 configurations only**: that is the cost brake (`--limit 5` by default,
  one model session per configuration). The command line's `--limit` lifts it.
- **Side by side** now shows your fresh v1 trace run on the left (the newest one wins) and v2's
  traces on the right. Both files are in v1's traces format.

### Step 4 — consumer description (the PaSh annotation)

- **v1:** **Run v1 annotate grep** → **annotate pash grep, in the VM** (free). It reads the newest
  trace run of `grep` on disk — your v1 trace from step 3 — and prints the PaSh description.
  The popup shows what it printed.
- **v2:** **Run step 4 on v2 · grep** (about $0.05). It reads v2's newest trace run of `grep`
  (falling back to a v1 one if v2 has none) and asks the model for the same description.
- **Side by side**: the two descriptions. This is the end of the pipeline.

Rough total for v2's four steps on one command: about $0.17 at today's estimates (`grep`'s
step 1 came in at $0.03, above the mean, because its man page is long). The figure on each
button is the estimate; there is no confirmation step.

## Starting a command over

At the foot of the pipeline page, **Delete every run of `grep`…** shows what would go — v2's run
folders, any that recorded nothing, the v1 runs started from here, and their database rows,
with a warning for anything a campaign result or finding cites — then asks you to type
`delete`. v1's own files and its checkout are never touched. The deletion is logged in
`eval/deleted_runs.jsonl`.

## `rm`

Same four steps. Two differences:

- `rm` is destructive, so **both sides run in the VM automatically**; the page decides that, and
  the Run page's command line shows `--isolation lima` for v2.
- v1's side is already complete from the September study (`eval/v1_configs/rm.configs.json`,
  and v1's traces and annotation in its own `outputs/`). Running v1's trace and annotate again
  from the page is still worth doing: the popup prefers your fresh runs, and a second v1 trace
  lets you check that v1 reproduces itself.

## What the page cannot do yet (and the command line for each)

| want | today |
|---|---|
| a **verdict** in the middle column (replicates / diverges) | a campaign: `caruca-v2 sweep campaigns/<file>.json` scores both sides by one instrument; Compare and the home page read its ledger. Starting one from the page is task 014 phase 3 |
| v1's step-2 **expansion file** for a new command | `.venv/bin/python -c "import json; from caruca_v2 import v1; r=v1.reference_configs('CMD', max_arity=1, max_count=1); json.dump([c for cs in r.by_invocation.values() for c in cs], open('eval/v1_configs/CMD.configs.json','w'), indent=1)"` |
| trace **more than 5** configurations on v2 | `caruca-v2 trace --isolation lima --limit N CMD --model openai/gpt-4o --temperature 0.0` |
| a **metered** live v1 step 1 | export the two variables above before `npm run dev`; the tokens and cost are not recorded until the forwarder is built |
| choose an **older** trace run as step 4's input | the page uses the newest; name one with `caruca-v2 annotate --traces <path> …` |

## Where everything lands

- v2 runs: `eval/runs/<run id>/` (manifest, telemetry, the step's file, and the terminal
  recording when started from the page). The Runs page lists them; the home page shows the
  newest per step.
- v1 runs: `eval/v1_runs/<run id>/` (the record of exactly what was run and where, the terminal
  recording, and for `trace` the traces file). v1 itself writes nothing about its own runs.
- Nothing is written into v1's checkout by any button.
