---
name: reference-naive-run-playbook
description: Step-by-step playbook to run one command through the naive-LLM arm end to end (VM clone, run, collect, record, analyse with Excalidraw diagrams, compare with v1, PDF, addendum), with every gotcha hit on 2026-10-20
metadata:
  type: reference
---

How a run was done on 2026-10-20 (runs 4 `grep` and 5 `rm`), written so a future agent can repeat it
exactly. Operator docs: `naive_llm_caruca/README.md` (authoritative for the VM steps); design record:
`ai_docs/tasks/016_naive_claude_code_arm.md`. Related: [[project-naive-claude-code-arm]],
[[feedback-naive-llm-standalone]], [[reference-md-to-pdf-wide-diagrams]], [[feedback-readme-is-prompt-variant-log]].

## 1. Before the run (Mac, repo root)

- Prompt and launcher are in `naive_llm_caruca/` (`PROMPT_v1.md`, `PROMPT_v2.md`, `vm/naive-run`). Since
  2026-10-20 both prompts carry a "What you may not use" (no web) section and `naive-run` passes
  `--disallowedTools WebSearch WebFetch RemoteTrigger --strict-mcp-config`, then picks the model with a
  ~$0.02 trial call: `claude-fable-5-1` medium effort if allowed, else `claude-opus-5-5` high. It aborts
  (exit 4) if the VM is signed out. No `--fallback-model` (effort is per session).
- Choose the command and prompt with Tiran; default so far was `PROMPT_v1.md`, watch mode. Samples
  (`tee uniq grep rm`) show the agent a finished answer; prefer non-samples for evidence.
- `./new_run_vm.sh <name>` (e.g. `naive-run-rm`) clones `naive-golden` (stopping it if running), copies
  prompts/formats/samples and the helper in fresh. "signed in: yes" there is NOT proof: on 2026-10-20 a
  clone printed it and still failed with "OAuth session expired" seconds later. If that happens, Tiran must
  `limactl start naive-golden && limactl shell naive-golden`, run `claude`, `/login`, exit, stop the image
  (only he can: needs a browser). After his re-login, the next two clones (runs 4 and 5) worked.
- **It recurs (2026-10-26):** run 10's clone (`dirname`) ran fine; the next clone (`dd`), made a minute later
  from the same golden image, failed at the model trial call with "OAuth session expired and could not be
  refreshed" (`naive-run` exit 4). Cause not established. Batch scripts must stop on exit 4, not move on.
  `claude setup-token` ("Set up a long-lived authentication token (requires Claude subscription)", in
  `claude --help`, 2.1.293 on the Mac) is a candidate fix for long batches; untried, and Tiran's call
  because it creates a credential.

## 2. The run

```sh
limactl shell <name> -- bash -lc 'cd ~/naive-arm && naive-run <cmd> PROMPT_v1.md' > <scratch>/console.log 2>&1
```
Run it in the background (Bash `run_in_background`); the harness notifies on exit. Then read the first
lines to confirm `== model claude-fable-5-1, effort medium (fable-ok)` and the session line. A command
outside the core nine (`cat grep pwd rm tac tail tee uniq wc`) asks y/N on a terminal and errors with no
terminal, so non-core commands need an interactive shell. If you add a Monitor on the log, start it
before the run can finish (run 5 ended in 60 s, before the monitor attached). macOS has no `timeout`.

### Non-coreutils commands (first done 2026-10-20: run 6, binwalk)

- `naive-run` requires `command -v <cmd>` AND `man -w <cmd>` to succeed in the clone, else exit 2. A tool
  built from a source repo usually has no installed man page, so it is refused as the script stands.
- Run 6's binwalk was apt-installed **in the golden image** by Tiran (not per clone). `run.env` records the
  OS but not the package version: record `dpkg -s <pkg>` from the clone by hand.
- Unattended launch without editing `naive-run`: `limactl shell <clone> -- bash -lc 'cd ~/naive-arm && echo
  y | script -qec "naive-run <cmd> PROMPT_v1.md" /dev/null' > log 2>&1` in the background (worked).
- **Never run the command in the golden image to check it** (run 6: a `binwalk --help` check there created
  `~/.config/binwalk/` in the image). Check in the clone instead. Use `collect_run.sh <clone> --keep` to keep
  the clone for post-run probes of the agent's claims, then `limactl delete -f <clone>`.
- Check packaging first: binwalk's binary is a Python script, so its source is on the machine and the agent
  used it (PROMPT_v1 bans only online repositories).
- The prompts forbid online code repositories but allow "a package installer" to use the network, so a
  session could `apt-get source` the command and read its code. Not observed; nothing audits for it.
- v1 has reference grammars (`syntax_specs/`) for some non-coreutils: awk, bc, sed, unzip, iconv, pandoc,
  convert, mogrify, uglifyjs. Anything outside v1's list has no reference to score against.

- **Probing a non-GNU command: binwalk's error conventions** (observed 2026-10-27, binwalk 2.3.4 /
  "v2.3.3", Python argparse). An unknown option is taken as a *file name*: "General Error: Cannot open file
  --bogus", exit 3. A missing value is "expected one argument", exit 2. A value given to a flag is "ignored
  explicit argument". It has no `--version`; its version is the first line of `--help`. A negative number
  after an option is read as an option (`-1` is `--preserve-symlinks`), so v1's default integer samples
  (−1, 0, 1) fail. `naive_llm_caruca/scoring/probe_binary.py` understands all of these; GNU-only regexes do not.

### Long runs: keep the Mac awake, and guard the cost (run 8, convert, 2026-10-20)

- **A sleeping Mac freezes the VM.** Run 8 ran with the lid closed on battery: the Mac slept three times and
  the session lost ~1 h 50 min (resumed correctly each time). `caffeinate -ims` does NOT hold system sleep on
  battery (`-s` is AC-only); check `pmset -g batt` and the lid (`ioreg -r -k AppleClamshellState -d 1`) before
  a long run and ask Tiran to plug in. Claude Code's `duration_ms` excludes suspended time (1,291 s vs 2 h 14
  min on the clock); report both. A Claude Code Bash call that runs past 300 s is moved to the background.
- **Cost guard:** `naive-run` has no spend cap. Run 8 used a Mac-side Monitor polling `stream.jsonl` via
  `limactl shell <clone> -- cat` every 2 min, summing each assistant message's usage (dedupe by message id)
  at Fable 5.1 rates that slightly overestimate list cost (~4% on runs 4 and 5): $11/M input, $55/M output,
  $1.10/M cache read, $13.75/M cache write. It printed a line every 10 min and on thresholds.
- **In a clone after sleeps, time-based searches fail:** `find -newer <run's prompt.md>` returned untouched
  system files (cause not established); list the agent's folders directly instead.
- `collect_run.sh <clone> --keep` then probe claims in the clone (no ImageMagick on the Mac or in the pash
  VM); a throwaway `limactl clone naive-golden <name>` + `limactl delete -f` works for later checks.

## 3. Collect and record (same turn)

- `./collect_run.sh <name>` copies `~/runs/<stamp>_<vm>_<cmd>_<ver>/` into `naive_llm_caruca/runs/` and
  deletes the clone. The folder holds prompt.md, run.env (model, effort, model_choice, bash_urls),
  stream.jsonl, stream.actions.log, transcript_*.jsonl, output/, bash_urls.txt, environment.txt.
- Write an "Observed, run N" entry under the prompt version in `naive_llm_caruca/README.md`, a ledger line
  in task 016 section 8, and update the memory note. Per the README rule, same turn as the run.

## 4. Analyse (the README's "Analysing a collected run" prompt)

1. Extract every call with timestamps and full results from the transcript (Python over
   `transcript_*.jsonl`: `tool_use` input, `tool_result` content, record `timestamp`), or
   `./tool_log.py -r`. Read ALL calls in full: summaries from the action log misled twice on 2026-10-20
   (run 4 actually read tee/uniq samples and hit the ugrep shell function in call 2; a first read said not).
2. Timeline (phase = calls, duration to next phase's first call), sources, copied-vs-derived (diff
   against `samples/<cmd>/`, which are v1's `syntax_specs/<cmd>.py` byte for byte plus PaSh 0.2.4 files),
   isolation, testing, versions, mechanics, cost, behaviour.
3. Check every claim in the agent's closing report against the log, in a table. Each analysed run had
   at least one overstated claim (run 4 "Everything passed" over `TOTAL FAILURES: 1`; run 5 "tested" with
   no post-write test).
4. Mechanical checks: `ast.parse` all files; import `output/<cmd>.py` under v1's real DSL with
   `~/dev/stevens/caruca/caruca/.venv/bin/python -I` and `sys.path.insert(0, '<v1>/caruca/src')`, run
   from a scratch dir; compare option spellings with the manual's option lines the agent printed.
5. To count binary runs inside an agent's own test harness, replay it on the Mac with paths rewritten and
   a counting stand-in binary (run 4: 154). Delete any `__pycache__` the replay leaves in the run folder.
6. v1 comparison (Tiran asked for it on every analysis): paper sections 2-6 vs the agent, job by job
   (syntax / choose what to run / run and observe / decide behaviour / write for consumers). Useful v1
   facts: model reads only `doc_sources/man/<cmd>.txt`, never `--help` or the binary; prompt forbids
   choices not in the man page; few-shot examples `touch rm mv ls` are their own references; paper's rm
   figure 8,749,056 configurations; `caruca generate <cmd> --max-count 1` runs on the Mac (grep: 122 lines);
   v1's committed PaSh annotation is `caruca/save/<cmd>.json`. Frame neutrally (v2 extends v1).
7. Tiran also wants a short plain-language "What this run teaches" section near the top (not verbose,
   not technical).
8. **Load the agent's PaSh files into PaSh's real code** (first done for runs 7 and 9, 2026-10-20; it
   found run 9's class silently broken): copy of `pash_annotations` 0.2.4 in the pash VM with the agent's
   files laid over it; recipe and PaSh's run-time rules in [[reference-pash-annotations-runtime]]. Compare
   against the same invocations with PaSh's own files.
9. **Feed the agent's syntax file to v1's generator and run every distinct line on the binary** (runs 7, 9):
   `PYTHONPATH=<scratch> caruca generate <cmd> --path <pkg> --max-count N | sort -u`, then run each line in
   the pash VM (GNU coreutils 9.4) on a small stdin, classify exit codes by error message, exclude lines a
   shell cannot re-read and v1's `relpath_1`/`abspath_1` placeholders, and count "real work" = accepted
   and no `--help`/`--version`. Do the same for v1's reference and v1's model output
   (`outputs/llm-dsl-generation/<cmd>.py`) for comparison. See [[caruca-v1-value-generation]].
10. **Several sessions may run and analyse naive runs at once.** Run numbers follow start time across all
   sessions; check `naive_llm_caruca/runs/`, task 016's ledger and `ListAgents` before numbering, and
   re-read the README and task 016 right before editing them.

## 5. Diagrams (Excalidraw skill, `.claude/skills/excalidraw-diagram/`)

Read its SKILL.md and color-palette.md. Write a compact hand-placed spec, build with
`naive_llm_caruca/excalidraw_fill.py spec.json out.excalidraw`, render with
`cd .claude/skills/excalidraw-diagram/references && uv run python render_excalidraw.py <file>`, Read the
PNG, fix, repeat (1-3 rounds each). Start from an existing `runs/*/analysis/*.spec.json` (session_workflow,
information_flow, v1_design_vs_agent, run3_vs_run4). Gotchas: a long title widens the canvas and shrinks
everything; text placed over the first-write dashed line collides; arrows must end left of the target box
(x 1324 boxes, arrows 600→1322); dashed ellipses render badly. Keep `<name>.spec.json` beside each
`<name>.excalidraw`/`.png` in the run's `analysis/`.

## 6. PDF

`npm run convert -- <analysis.md> --title ... --subtitle ...` from the repo root. It downscales relative
images to 1,600 px, so: back up the .md, rewrite `](x.png)` to absolute paths, convert, restore, `cmp`.
The rewrite pattern must allow digits (`[a-z0-9_]*\.png`): `v1_design_vs_agent.png` slipped through a
letters-only pattern on 2026-10-20 and was downscaled.
Check `pdfimages -list` shows full-size images (~1,100 ppi). zsh: never start a word with `=` (`echo =====`
fails).

## 7. Addendum material

Anything for the paper goes in `naive_llm_caruca/white_paper_addendum_naive_llm.md` under the "Naive LLM"
heading, re-verified at primary sources, never citing the earlier rebuild's findings, then converted to PDF
the same way. Then add a dated bullet to `naive_llm_caruca/latest_findings.md` and, for a new document
or diagram, a row in the start page at the top of `naive_llm_caruca/README.md` (moved there 2026-10-27;
`ai_docs/analysis/README.md` no longer indexes naive-LLM work).

## Task 018 scoring VMs (2026-10-27)

`t018-probe` is a long-lived clone of `naive-golden` used only to run the scoring probes (the same binaries
the agent saw; no Claude session runs in it). Scoring also needs the `caruca` VM. Both are stopped between
sessions; `score_t018.py` needs both running (`limactl start t018-probe caruca`).

**Before building any analysis tool, check what exists (lesson of 2026-10-26/27).** Two sessions built
overlapping instruments in parallel:
- `naive_llm_caruca/scoring/` (task 018): `probe_binary.py`, `facts*.py`, `reach.py`,
  `trace_usefulness.py`, `score_t018.py`;
- `naive_llm_caruca/comparisons/2026-10-26_syntax_files_vs_v1/scripts/` (session caruca-v2-dd):
  `render.py`, `probe_vm.py`, `gnuread.py`/`readcheck_lib.py` (GNU getopt emulation, coreutils 9.4
  tables for cut/sort/rm), `corpus_split.py`.

Reuse them, by copying them into a temp folder, never by editing the other folder in place. Coordinate
with a live peer session through `SendMessage` to its `uds:` address. Never edit a file a peer has
announced it is moving until it confirms; after a move, re-read any file the harness flags as changed on
disk.
