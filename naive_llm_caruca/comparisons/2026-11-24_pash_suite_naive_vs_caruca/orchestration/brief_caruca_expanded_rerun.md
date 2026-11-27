# Brief: rerun PaSh's suite with Caruca's expanded annotation files (2026-11-26)

You are the builder for this rerun. Read first: `full_run/README.md`, `orchestration/brief_builder.md` (with its
amendments), `orchestration/metrics_spec.md`, `run_koala.py --help` and `caruca_conversion/` in this folder.
Do not commit. Do not modify v1 (`~/dev/stevens/caruca`) except reading its `caruca/save_pash_py/`.

## Why

The first run gave Caruca files for only 8 commands (`cat cp cut grep rm sort split wc`), the ones converted to
PaSh's current Python format at the time. Caruca has 54 small (PaSh) grammars and ~120 full grammars. On
2026-11-26 the orchestrator converted the rest (`caruca_conversion/logs/status.tsv` lists every command, grammar,
result and seconds): all small grammars at max-count 4 (as the first 8), and the full grammars of the suite's
commands at max-count 2 where tractable (as cut, rm and sort were). Tiran wants the suite rerun so Caruca is
compared at full reach, with the same metrics as before.

## Sets to run (all of a source's files swapped in at once, as before)

- `bash`, `pash-own`, `pash-own-copy` (the noise control): rerun in this session so every ratio has a same-session
  reference.
- `caruca-pash-all`: Caruca's small-grammar files for every command with a successful conversion
  (`save_pash_py/<cmd>/pash_grammar/trace_1/`), PaSh's own elsewhere.
- `caruca-main-all`: Caruca's full-grammar files where they exist (`main_grammar/trace_1/`), otherwise its
  small-grammar files, otherwise PaSh's own. Record per command which grammar was used (the report must label
  this set "Caruca, full grammar where traced").
- Do not rerun `naive` / `naive-sed2`: their times are compared as ratios to `pash-own` of their own session.
  State this in the README.

Build the set folders the same way the first run did (`run_koala.py` set-building step; copy files byte for
byte, record hashes in `manifest.json`). Check every new file imports and its classes load in the pash VM before
the batch (as the first run's checks did); a file that fails to load is recorded, not fixed.

## Run

The pash VM was stopped during tracing; start it (`limactl start pash`) only after tracing has finished (the
orchestrator tells you). Same 86 scripts, small inputs, same phases: answers (direct calls with PaSh's words),
instrumented pass, three timed repeats with bash first in every repeat (the runner fix from the first run).
Watch for Mac sleeps (`pmset -g log`) and the battery (`pmset -g batt`); redo any timed run that overlaps a
sleep or ran on battery. Write records to `full_run_caruca_all/` in this folder (same file names as `full_run/`),
copied out every 10 scripts.

## Then

Run `full_run/summarise.py` on the new records (or a copy pointed at them) to make
`full_run_caruca_all/numbers.md`; then run `per_command.py`-style counts for Caruca against PaSh's own on every
command Caruca now covers (copy `per_command.py` to `per_command_caruca.py`, change the set names). Write
`full_run_caruca_all/README.md`: what ran, which Caruca files were used per set, every fault and redo.
Report to the orchestrator at each step's end in at most 6 lines.

## Conversion outcome (orchestrator, 2026-11-26 13:05)

See `caruca_conversion/README.md`. Small grammars: 53 of 54 commands now have files (all but `gzip`, broken grammar).
Full grammars: 21 commands (`cut rm sort` from 2026-11-10 plus 18 new); `grep` full is being retraced with 16 GB
(OOM at 8 GB); `ls` full is not traced (only used outside parts); `comm join cp diff` too large. The pash VM stays
stopped until the orchestrator says the grep retry is done.

## Go (orchestrator, 2026-11-26 14:15)

`grep` full grammar converted (22 full grammars in all). Tracing is finished and the caruca VMs are stopped; start the
pash VM and begin. The Mac is on mains with caffeinate; still check `pmset -g log` and `pmset -g batt` per script.
