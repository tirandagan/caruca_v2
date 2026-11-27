# Brief: verify every wrong output in the Caruca rerun (2026-11-27)

You are an independent checker. Work in `naive_llm_caruca/comparisons/2026-11-24_pash_suite_naive_vs_caruca/`.
Do not edit records, the report, or anything in `~/dev/stevens/caruca`. Do not commit. Write one file:
`full_run_caruca_all/wrong_outputs_verified.md`.

The rerun (`full_run_caruca_all/`, records `results.jsonl.gz`, `regions.jsonl.gz`, `occurrences.jsonl.gz`;
`README.md`; `numbers.md`) found printed output different from bash in 11 scripts under Caruca's expanded files
(9 with set `caruca-pash-all`, 10 with `caruca-main-all`). The builder's diagnosis: `sed` with a line address
(`sed 1d`, `sed 4d`, `sed 100q`) split per chunk (8 scripts); `uniq` split with plain concatenation (2 scripts);
`unixfun/23`: Caruca lets `tr -d '\n'` split, so each `cut -c 1-4` copy prints its own first 4 characters.

For each of the 11 (script, set) cases:
1. Confirm the output really differs: compare `out_sha256` and `out_bytes` with bash's row of the same repeat and
   pass, in every repeat. Show the first differing lines if the outputs are kept (look in the pash VM under
   `~/t024/` for the run folders; read only).
2. Name the command whose split causes it: from `occurrences.jsonl.gz` (rows for that script and set with
   `split` true) and from PaSh's log for the run (`~/t024/out_caruca_all/logs/` or as the README says).
3. Show the Caruca file's decision: open the generated class in
   `~/dev/stevens/caruca/caruca/save_pash_py/<cmd>/<grammar>_grammar/trace_1/ParallelizabilityInfoGenerator<Cmd>.py`
   and quote the branch that allowed the split for that command line (flags and operand count) and its
   `# v1: ...` comment (which labels Caruca's traces gave, e.g. `non-pure, stateless`).
4. Say whether the split is wrong in general for that command line (a reason a reader can check: e.g. `sed 1d`
   deletes the first line of the whole input, so applying it to every chunk deletes one line per chunk), and
   whether PaSh's own file allows the same split (it should not, since PaSh's own output was right).
5. Mark the builder's diagnosis confirmed, corrected, or not confirmed.

Then a short section: how many of the 11 come from Caruca keeping the most parallelizable label when its traces
disagree (memory: `memory/caruca_v1_class_combining_rule.md` describes this rule; check the `# v1:` comments for
mixed labels such as `non-pure, stateless`), and how many from something else.

Use the Lima VM `pash` (running) for the run folders. Reply in your pane in at most 8 lines: per cause, how many
cases, confirmed or not, and the path of your file.
