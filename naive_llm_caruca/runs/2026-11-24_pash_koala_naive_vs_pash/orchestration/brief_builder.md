# Brief: naive LLM's PaSh files vs PaSh's own, on Koala (pilot: one script)

You are a worker. An orchestrating Claude session gave you this brief and will review your results.
Work only on what is described here.

## Goal

Find out how PaSh behaves when it uses the **naive LLM's PaSh annotation files** instead of **PaSh's own
original annotation files**, on real benchmark scripts. For each script, the questions are:

1. Does PaSh's output still match plain `bash` byte for byte?
2. Which commands did PaSh actually split into parallel copies, with each set of files?
3. How long did it take with each set?

**This pilot runs one script only:** Koala's `oneliners/scripts/spell.sh` at Koala's "small" input size.
It uses `cat sed col tr sort uniq comm`; the naive LLM has files for all of these except `tr`.
Build the runner so it can later take any Koala script, but run only `spell.sh` now.

## The three runs per script

| Run | What |
|---|---|
| `bash` | the script under plain bash: the reference output |
| `pash-own` | PaSh with a private copy of its own installed annotation package, unchanged |
| `naive` | PaSh with a private copy of that package in which, for **every command the naive LLM has files for**, the naive LLM's three files replace PaSh's (or are added, when PaSh has none), and the command is added to PaSh's name table. Commands without naive files keep PaSh's own files |

Choose a set for a run with PaSh's `--local-annotations-dir <folder>` option. Never edit the installed
package, PaSh's source, or the Koala checkout.

**Which naive files:** the Fig. 7 campaign's first run of each command, which is the row with
`"repeat": 1` for that command in `naive_llm_caruca/fig7_campaign/ledger.jsonl`. Its files are in
`<run_folder>/output/annotation/` (`<cmd>.json`, `InputOutputInfoGenerator<Cmd>.py`,
`ParallelizabilityInfoGenerator<Cmd>.py`). Record the run folder used for each command.

## Reuse what exists (copy it, don't edit it)

Task 022 already solved most of this for single command lines and for PaSh's old benchmark scripts:
`naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/pash_runs/`. Read its `README.md`
and `observations.md`, then reuse from `run_pash.py`: `three_files`, `build_set`, `add_to_name_table`,
the stand-in shim on `PATH` that logs each time a command starts (`counts`, `standin_count`),
`read_log`/`classify`, and the `controls` and `answers` ideas. Copy what you need into your own runner in
this folder.

## Environment (verified 2026-11-24)

- Everything runs in the Lima VM `pash` (`limactl shell pash -- bash -lc '...'`): 8 CPUs, aarch64,
  Ubuntu 24.04. The Mac's home folder is visible inside the VM **read-only**, so the naive files can be
  read from their Mac paths. Write your work inside the VM, e.g. under `~/t024/`, and copy results out.
- PaSh: `~/pash`, commit `42a8b87c`, unmodified. `export PATH="$HOME/pash/python_pkgs/bin:$PATH"`, then
  `pash`. Stock annotation package (version 0.2.4, all 107 files verified unmodified):
  `~/pash/python_pkgs/lib/python3.12/site-packages/pash_annotations`.
- Koala: `~/koala`, commit `ccf25a57`, small inputs already downloaded (do not fetch again). `spell.sh`
  takes the input file as its first argument (`~/koala/oneliners/inputs/30M.txt`) and reads
  `$SUITE_DIR/inputs/dict.txt`, so set `SUITE_DIR=~/koala/oneliners` and `LC_ALL=C` (Koala's
  `oneliners/execute.sh` does both). Koala's expected hash: `~/koala/oneliners/hashes/small/spell.hash`.
- PaSh settings: `pash -w 8 -d 2 --log_file <file> --local-annotations-dir <set> spell.sh <input>`.

## Known PaSh behaviour you must handle

- PaSh **falls back to plain bash quietly** when it can't handle something, and the output is then
  right. A correct output alone proves nothing about splitting. In `-d 2` logs, count
  `Received data: Compile` (regions sent) and `Optimized script saved in` (regions run in parallel). The
  reasons appear as `WARNING: Exception caught ...`. Don't rely on `Got response from compilation-server: ERROR`;
  it is missing for many fallbacks. Also use the stand-in shim to count how many copies of each command started.
- PaSh **swallows exceptions inside an annotation class and treats the command as having no
  annotation**. So for each command invocation in the script, call each set's annotation generator
  directly and record its answer (input/output info and parallelizability), including any exception.
  A naive file that crashes must show up as a crash, not as "no split".
- Prove the folder decides: run at least one control, e.g. the `naive` set with the naive files for
  `sort` removed, and show the change in what splits.
- **Timing is only valid while the Mac is awake.** Before reporting any time, check the Mac's power log
  for the run window (`pmset -g log | grep -E 'Entering Sleep|Wake from|FullWake'`, from the Mac side).
  Run timed passes one at a time, with nothing else heavy in the VM. Repeat each timed run 5 times and
  report the median and the spread.

## Output

Put everything in this folder: `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/`.

- the runner script(s) you wrote;
- `manifest.json`: commits, package hashes, the naive run folder and the three files' hashes per command, machine;
- `answers.jsonl`: each set's annotation answer for each command invocation in the script;
- `results.jsonl`: one row per script, set and repeat (state, regions sent/parallel, copies started per
  command, output hash, same as bash, matches Koala's hash, seconds, fallback reasons);
- PaSh logs, compressed if large (keep the folder under ~5 MB, nothing over 1 MB uncompressed);
- `README.md` for Tiran: what was run and what was found for `spell.sh`, in plain words. Say which set
  split which commands, whether outputs matched, and the times. Explain every term; use no unexplained
  flags or field names; give every rate with its denominator; plain tables. Short.

Do not commit or push. Do not change anything outside this folder and your VM work folder.

## When done

Reply with three lines: the path of `README.md`; one sentence on the result; anything that blocked
you or that you could not verify.

## Amendment 1 (2026-11-24, from the orchestrator): five runs per script, not three

Tiran's goal is to compare **the naive LLM's files, Caruca's files, and PaSh's own**, over PaSh's whole
published benchmark suite (Koala's versions). So add two sets. Per script:

| Run | What |
|---|---|
| `bash` | as before |
| `pash-own` | as before |
| `naive` | as before |
| `caruca-pash` | Caruca's (v1's) PaSh files for the 8 commands it has (`cat cp cut grep rm sort split wc`); PaSh's own files for every other command. Use the `v1-pash` rows of `naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/sides.jsonl` (paths under `~/dev/stevens/caruca/caruca/save_pash_py/<cmd>/pash_grammar/...`) |
| `caruca-main` | the same with the `v1-main` rows (Caruca's main grammar) where a command has one, else its `v1-pash` files |

Rule for every set: a command the set has no files for keeps PaSh's own files ("organic" annotations).
Record, per set and command, which source was used. The checker will verify this.

Scope of the runner: it must take any script from the six Koala groups that stand in for PaSh's
published suite (`oneliners`, `unixfun`, `covid`, `nlp`, `weather`, `web-search`; all inputs are already
downloaded in the VM, small size, web-search at min). The pilot is still `spell.sh` only. Result rows
carry group and script name. `spell.sh`'s commands with Caruca files: `cat`, `sort`.

## Amendment 2 (2026-11-24, after the pilot): records the report needs, then the full suite

The pilot is accepted (checker running separately). A report-design pass produced
`orchestration/report_plan.md`; its **section 5** lists the record changes the report needs. Apply
these now, in this order, then re-run the pilot (`spell`) to validate the new records. **Do not start
the full suite until the orchestrator says so**: the naive LLM is being run on `tr`, `xargs` and `awk`
right now (Tiran's decision; `tr` is in 54 of 92 scripts), and the `naive` set must include those
files before the batch starts. Read section 5 in full; in short:

1. **5.1 `occurrences.jsonl`**: one row per command *use* (each place a script calls a command), with
   the part it sits in, its position, the command line as PaSh saw it, the matching `answers.jsonl` row,
   the source of its files, the file's answer, copies in PaSh's parallel script (counted by full command
   line, not by name), whether it was split, and why not (including "allowed by the file, not split by
   PaSh", the naive `sed` case). Plus rows for uses that ran outside every part sent to PaSh.
2. **5.2 a timing control `pash-own-copy`**: a second byte-identical copy of PaSh's own package, timed
   like the others (3 repeats); rotate the order of sources from repeat to repeat.
3. **5.3** record one `uptime` (VM load) at the start and end of each script's timed runs.
4. **5.5** the smaller changes: `source` on every `answers.jsonl` row; input size in bytes in
   `invocations.jsonl`; stand-ins for every command in `coverage.jsonl`; fixed labels for "other"
   outcomes; the folder-decides controls on `spell` at the start and end of the batch; one display-name
   map for the sets (`sets.json`).
5. Fix whatever stopped the weather launcher during discovery.
6. **Scope decided by Tiran:** the six downloaded groups plus `analytics` (without `port-scan`) and
   `file-mod`, `bio.sh` at min, the two `pkg` scripts once at min if they run. Another worker is
   downloading and installing those now and will write `orchestration/inputs_setup.md`; make the runner
   accept them once that exists.

Keep `README.md` for `spell` as it is until the full suite runs; the report itself will be built from
the records by a separate counting script (plan section 5.4), not by you.
