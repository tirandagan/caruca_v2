# Validation run of the amended records on `spell` (2026-11-24, 11:33–11:34)

This is a run of `run_koala.py` after Amendment 2 and section 5 of the report plan. It checks the new
records only. **Its times are not valid**: while it ran, another worker was running Koala's own
`analytics/pcaps.sh` in the same virtual machine (the VM load rose from 0.5 to 3.8, recorded in
`run_windows.jsonl`). The accepted pilot's records are in the folder above and are unchanged.

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
