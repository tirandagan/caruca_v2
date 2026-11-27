# Brief: one folder with the naive LLM's latest PaSh annotation files, by command

You are a worker. An orchestrating Claude session gave you this brief on behalf of Tiran Dagan. Work
only on it. Do not touch anything under `~/dev/stevens/caruca` (v1) and do not modify any run folder.
Do not commit.

## Why

Tiran keeps having to search the 100-odd run folders under `naive_llm_caruca/runs/` to find the PaSh
annotation files the naive LLM wrote for a command. He wants them in one place, organised by command,
latest run per command, with a README that says what each entry is and links back to the run that made it.

## What to build

Folder: `naive_llm_caruca/pash_annotations_latest/` (new).

```
pash_annotations_latest/
  README.md
  <cmd>/
    <cmd>.json
    InputOutputInfoGenerator<Cmd>.py
    ParallelizabilityInfoGenerator<Cmd>.py
    (any other file the run's PaSh output folder holds, e.g. a syntax .py, copied as is)
```

One `<cmd>/` folder per command the naive LLM has ever produced PaSh annotation files for. Copy the files
byte for byte (plain `cp`, keep mtimes with `cp -p`). Never edit a copied file. Do not copy `__pycache__`.

## Where the sources are

- Run folders: `naive_llm_caruca/runs/<timestamp>_naive-run-<clone>_<cmd>_PROMPT_v1/`. The command is
  the second-to-last underscore field; confirm it against `run.env` / `paths.tsv` inside the folder.
- Two layouts for the PaSh files: older runs have `output/pash/`, newer runs have `output/annotation/`
  (e.g. `runs/2026-11-24_125757_naive-run-sed-r2_sed_PROMPT_v1/output/annotation/`). Check for both and
  for any third layout you find; report any run that has a PaSh-format file somewhere else.
- The campaign ledger `naive_llm_caruca/fig7_campaign/ledger.jsonl` has one line per run (`command`,
  `repeat`, `run_folder`, `started_driver`, `model`, `billed_usd`, notes). Not every run is in it
  (the October pilot runs predate it); use the folder timestamps as the authority for "latest".
- `naive_llm_caruca/README.md` is the prompt-variant and run log; read its run table to catch anything
  the folders alone would hide (a run marked invalid, a rerun, a renamed command).

## Rules for "latest"

- Latest = the run folder with the newest timestamp prefix among runs for that command that actually
  produced PaSh files. A run with no PaSh output does not count, but list it in the README's
  "runs without PaSh files" section.
- `sed` has a repeat 2 from 2026-11-24 (after the format-document repair); that is the latest. Note in
  the README that the earlier sed run exists and why it was superseded (see
  `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/orchestration/judgment_errors.md`).
- Where two runs of the same command have the same date, the later time wins.

## README.md content (plain language, short)

1. One paragraph: what this folder is, that the files are byte copies of the latest run per command,
   and that the run folders stay the record.
2. A table, one row per command, sorted by command: command · files present (count and names) · run
   folder (as a relative Markdown link to the folder, e.g. `[2026-11-24_125757…](../runs/2026-11-24_125757_naive-run-sed-r2_sed_PROMPT_v1/)`)
   · run date · prompt version · cost if the ledger has it · note (e.g. "repeat 2, after format repair").
3. "Runs without PaSh files": commands/runs that produced none, with links.
4. "Superseded runs": for commands with more than one run, the older run folders, linked, one line each.
5. How to refresh: a short description of the steps (a script is fine, see below).

## Make it repeatable

Write `naive_llm_caruca/pash_annotations_latest/refresh.py` (Python 3, stdlib only) that rebuilds the
folder and the README from the run folders and the ledger, so the next run just re-runs it. Run it to
produce the deliverable; check the result by hand (count of commands, spot-check 3 commands against
their run folders with `diff -r`). Give the script a `--dry-run` that prints what it would copy.

## Report back

Reply in your pane with: the number of commands indexed, the number of run folders scanned, any run
with PaSh files in an unexpected place, any command whose latest run lacks a file of the three, and the
folder path. Keep it to ten lines.
