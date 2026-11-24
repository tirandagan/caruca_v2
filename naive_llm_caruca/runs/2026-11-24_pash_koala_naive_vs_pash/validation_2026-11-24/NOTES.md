# Validation run of the amended records on `spell` (2026-11-24; records here are from the re-run at 11:43–11:44)

**Re-run after the checker's review (11:43).** The files' answers are now taken by replaying PaSh's own
steps on the files PaSh keeps (its expansion of variables, its parsing of each command), so quoted words
keep their quotes as inside PaSh. In `occurrences.jsonl`, `file_answer` is that answer
(`answer_method`: "as PaSh passes them"); `direct_file_answer` is the old direct one, and
`direct_differs` marks where they disagree. `answers.jsonl` holds both, told apart by `method`.
Each recipe now records whether PaSh can carry it out (`implemented`: PaSh's own test), which adds the
answer "allows only a split PaSh has not implemented". Result: over all 180 command uses in the main and
control runs, PaSh split a use exactly when this answer allowed a split it can carry out. The VM was at
load 0.31 when the re-run started; the inputs worker was downloading into Koala at the time, so these
times are not used either.

The first validation run (11:33, after Amendment 2 and section 5 of the report plan; its records were
replaced by the re-run) also had invalid times: another worker was running Koala's own
`analytics/pcaps.sh` in the same virtual machine. The VM's load also rises during these runs from PaSh's
own 8 copies, so the load at the start of each script is the cleaner sign of a quiet VM. The accepted
pilot's records are in the folder above and are unchanged.

What is new in the records:

| Record | Change |
|---|---|
| `occurrences.jsonl` | one row per command use, per source and repeat: its part, its position, the command line as PaSh saw it (variables filled in from PaSh's log), the matching `answers.jsonl` row, the source of its files, the files' answer, its copies in PaSh's parallel script (matched by command name plus options), whether it was split, and why not. Rows marked `outside_pash` are uses started under bash that are in no part sent to PaSh |
| `results.jsonl` | the source `pash-own-copy` (a second, identical copy of PaSh's own files), timed runs only; the order of sources rotates from repeat to repeat (recorded in `order`) |
| `run_windows.jsonl` | one line per script: start and end times, the VM's load at each, and whether Koala's checkout changed |
| `answers.jsonl` | `source` (ours / pash-own / none) and the exact command line on every row |
| `invocations.jsonl` | input size in bytes. Entries named only in the environment can be left over from an earlier script of the same launcher (weather's `tuft-weather` carries `max-temp`'s file), so arguments and environment are counted separately (`input_bytes_from_arguments`); sizes are upper bounds |
| `standin_vs_inventory.jsonl` | for each script, the commands started under bash against the inventory's list; for `spell` they match |
| `regions.jsonl` | a part whose outcome is "other" starts its reason with a fixed label |
| `controls.jsonl`, `controls_*.jsonl` | the controls, run before (`phase` start) and after (`phase` end) the script |
| `sets.json` | one display name per source |

Weather's launcher: its two scripts are recorded correctly. Its exit code 1 comes from the launcher's
last step, which moves `weather/plots/*` into its outputs; when nothing really ran, that folder is empty.
The fix made is the one that mattered: `tuft-weather` writes into `weather/plots`, which in the shadow
copy was a link into the Koala checkout. The shadow copy now has its own `plots` folder, and the files
written there are hashed with the outputs. Koala's checkout status is recorded before and after each
script (unchanged in this run).
