---
name: reference-pash-annotations-runtime
description: How PaSh's annotation code (pash_annotations 0.2.4, pash VM) treats a command's three files at run time — exceptions swallowed to None, round robin only with conc/adj-lines aggregators, name allowlist, attached values left as operands; and how to test outside files without touching the install
metadata:
  type: reference
---

Established 2026-10-20 while analysing naive runs 7 (cut) and 9 (sort), by reading and running
`pash_annotations` 0.2.4 in the Lima VM `pash`. Related: [[project-naive-claude-code-arm]],
[[reference-naive-run-playbook]], [[pash-grep-annotation-current-vs-json]].

**Location.** `/home/tirandagan.guest/pash/python_pkgs/lib/python3.12/site-packages/pash_annotations`
(parser tables in `parser/command_flag_option_info/data/<cmd>.json`, classes in
`annotation_generation/annotation_generators/`). PaSh ships `cut` and `sort` annotations (and
`custom_sort`); its `cut.json` lists a `-M` flag that GNU cut 9.4 rejects.

**Run-time rules (read in the source, confirmed by running):**
- `annotation_generation/AnnotationGeneration.py`: `get_input_output_info_from_cmd_invocation` and
  `get_parallelizability_info_from_cmd_invocation` wrap the class in `try/except Exception` and return
  `None`. **A broken class fails silently**, as if no annotation existed. Call the class directly to see
  the traceback.
- Only commands named in `DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES` (30 names incl. cut, sort, grep,
  uniq, tee, rm; not convert) are looked up.
- `annotation_generation/datatypes/parallelizability/Parallelizer.py` `__init__` **asserts that a round-robin
  splitter is paired only with a concatenate, adj_lines_merge, adj_lines_seq or adj_lines_func aggregator.**
  Run 9's sort class paired round robin with a custom 2-ary `sort -m …` aggregator, so for every
  ordinary sort PaSh returned no parallelizability info (only `-s`/`-u`, where it skipped round robin,
  worked). PaSh's own grep class builds the same pairing, but only in a branch guarded by
  `is_implemented`, which its custom aggregators fail, so it never runs. The naive arm's
  `formats/pash_annotation.md` (renamed `formats/annotation.md` on 2026-10-27, task 019) does not state the rule (as of 2026-10-20).
- The parser does not split attached values: `cut -d: -f2` parses with no options and operands `-d:`,
  `-f2`; `--fields=2`, `--sort=numeric`, `-k2` likewise stay operands. Listing an optional-argument option
  (`--check`) as an option makes it take the next word (`sort --check a b` → value `a`, operand `b`).
- `Option.get_name()` / `get_arg()` and `Flag.get_name()` exist (`datatypes/BasicDatatypes.py`).

**Testing outside files without touching the install:** copy the package to `/tmp/<x>/pash_annotations`
(drop `__pycache__`), lay the agent's `<cmd>.json` and two classes into it, then
`python3 -I -c 'import sys; sys.path.insert(0,"/tmp/<x>"); from pash_annotations.parser.parser import parse; …'`.
Run the same invocations with `sys.path` pointing at the install for PaSh's own answers.
