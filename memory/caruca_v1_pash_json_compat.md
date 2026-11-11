---
name: caruca-v1-pash-json-compat
description: v1's PaSh JSON can't be read by modern PaSh (no JSON reader) or as-is by old pre-2022 PaSh (key, operator and "exists" meaning all differ); v1's own transform.py targets the OLD JSON format and crashes on v1's current output. Verified 2026-10-06; crash re-run 2026-11-10 on a copy of save/cut.json (TypeError at transform.py:45)
metadata:
  type: project
---

Tiran asked (2026-10-06) whether PaSh can read v1's `.json` annotations or whether they must become
Python. Verified in code, not taken from memory:

- **Modern PaSh: no.** It has no JSON annotation reader. The only JSON `pash_annotations` 0.2.4 loads
  is the flag table (`parser/util_parser.py`, `command_flag_option_info/data/<cmd>.json`).
  Parallelizability info and input/output info must each be a Python generator class, plus an entry
  in `DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES`. Converting means writing code that emits
  parallelizers, not reformatting the file. v1's `stateless` maps to round-robin/chunk splitting
  with concatenation. `pure` needs an aggregator v1 never produces. `non-pure` and `side-effectful`
  mean no parallelizer at all.
- **Old JSON PaSh (before `92364f6a`, 2022-09-08, read at `92364f6a^` in the `pash` VM clone): not
  as-is either.** (1) It reads `case['class']`, but v1 writes `pclass`. (2) Its predicate
  interpreter knows `len_args_eq/exists/value/all/or/not` and has no `and`. An unknown operator
  falls through to a lambda that returns `log(...)`, so it never matches. With no `default` case
  this hits `assert(False)` in `find_annotation_case`. (3) Its `exists` means *any* of the listed
  flags, and the first matching case wins. v1 means "this invocation's flag set", so in the
  paper-era `cut.json`, `cut -d , -f 1` matches `exists [-f]` (stateless) before the intended
  `[-d, -f]` case (non-pure).
- **v1 ships a converter, `caruca/save/transform.py`** (added 2024-11-23 as `890eac611`, moved
  2024-12-03 as `c3cefeea5`, unchanged since). It is JSON to *old-PaSh JSON*: it renames `pclass` to
  `class`, merges cases with the same operands (keeping the most **conservative** class: `min` under
  its own ordering stateless > pure > non-pure > side-effectful, `transform.py` lines 8–25 and 53;
  corrected 2026-10-27, this line had said "most permissive") and
  moves `default` last. It overwrites files in place. Its existence suggests the paper run targeted
  the pre-2022 JSON reader. That partly answers the open question in `pash_vm_setup.md` §1, which
  guessed at an "uncommitted conversion".
- **transform.py crashes on what v1 makes today** (`TypeError: unhashable type: 'dict'`). Commit
  `28a9946f9` ("Fix PaSh predicates", 2024-12-06) nested every predicate under `and`. All 358 cases
  in `caruca/save/*.json` use `and` and none is `default`. The committed paper-era set
  `eval/pash-annotations/` (1,781 cases) is the older shape: top-level `exists`, 40 `default`
  cases, and 1,778 still keyed `pclass`, so it was committed untransformed.

**Why:** task 012 already chose "pin modern PaSh, adapter emits Python"
([[project-pash-downstream-study]]). This note records why the alternatives fail, so no one tries
feeding v1 JSON straight to an old PaSh.

**How to apply:** for any v1 JSON to PaSh path, write a Python-emitting adapter. Old PaSh with
transform.py is not a shortcut: the script fails on v1's current output, and even when it worked,
`exists` was read as "any of these flags", so the class PaSh picked could differ from the one v1
meant. Related: [[pash-grep-annotation-current-vs-json]], [[caruca-v1-pipeline-reference]].
