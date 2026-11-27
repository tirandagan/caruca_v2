# Brief: inventory of PaSh's benchmark suite as it exists in Koala, and who covers its commands

You are a worker. An orchestrating Claude session gave you this brief. Read-only task: you run nothing
heavy and download nothing. Another worker is running timed PaSh jobs in the Lima VM `pash`; keep your
VM use to reading files (`limactl shell pash -- bash -lc 'cat ...'`).

## Why

Tiran wants PaSh run over its **whole published benchmark suite** (the OSDI 2022 PaSh paper, Table 1,
rows 2–13: 12 benchmark sets) with three annotation sources: the naive LLM's files, Caruca's files, and
PaSh's own. The published suite's inputs are no longer downloadable (its MIT server is down), so the
same group's newer **Koala** suite stands in. Koala is checked out in the VM at `~/koala` (commit
`ccf25a57`); six groups already have inputs (`oneliners unixfun covid nlp weather web-search`). Before
anyone runs the rest, we need to know what the rest is and what it would cost.

## Produce

`orchestration/coverage.md` (for Tiran, plain words, short) and `orchestration/coverage.jsonl` (one row
per script) in `naive_llm_caruca/runs/2026-11-24_pash_koala_naive_vs_pash/`, answering:

1. **Mapping.** For each of the 12 published benchmark sets (the OSDI'22 Table 1 rows: Classics,
   Unix50, COVID-mts, NLP, AvgTemp, WebIndex, MediaConv, ProgInf, LogAnalysis, Genomics, AurPkg,
   FileEnc), which Koala group holds its successor, how many scripts, and how close the scripts are to the
   published ones (same / renamed / rewritten / no successor). Sources: `~/koala/README.md`,
   `~/koala/INSTRUCTIONS.md`, each group's `README.md`, and the OSDI'22 artifact README at
   `~/pash/evaluation/osdi22-eval/README.md` in the VM (the published groups' scripts are under
   `~/pash/evaluation/benchmarks/`; `dependency_untangling/` holds rows 8–13).
2. **Commands per script.** For every script in the Koala groups found in step 1, the list of commands it
   calls (read the scripts; include commands called inside helper scripts the script sources or runs,
   and note them as such). Then, per command, who has annotation files for it:
   - naive LLM: the 79 commands with a `runs/*/output/annotation/` folder under
     `naive_llm_caruca/runs/` (use the first run per command);
   - Caruca: `cat cp cut grep rm sort split wc` only;
   - PaSh's own: the names in `DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES` in
     `~/pash/python_pkgs/lib/python3.12/site-packages/pash_annotations/annotation_generation/AnnotationGeneration.py`
     in the VM.
   Per script give: commands, how many each source covers, and the commands nobody covers.
3. **Runnability.** For each Koala group not yet downloaded: its input source and size at `--small` and
   `--min` (read `fetch.sh`; probe URLs with `curl -sI` only, never download), its dependencies
   (`install.sh`; flag anything that needs large models, GPUs, Docker, root, or network services), and
   whether the VM (8 CPUs, 8 GiB, 17 GB free disk) can run it.
4. **Recommendation.** A proposed order to run the groups in, with the reason for each, and the groups
   you'd leave out and why.

## Rules

- Read-only. Don't change the Koala or PaSh checkouts, the installed package, or any worker folder.
- No downloads. No PaSh runs.
- Plain words in `coverage.md`: explain every term, give every rate with its denominator, no bare
  option names or field names. Tables are fine.
- Do not commit or push.

## When done

Reply with three lines: the path of `coverage.md`; the number of scripts found across the groups; the
biggest obstacle to running the whole suite.
