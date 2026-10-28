---
name: caruca-v1-value-generation
description: How v1 picks argument values and file contents (verified in code 2026-10-20) — Integer emits every value in [min,max] (default -1..1); content pool is 8 files incl. ONE JPEG (paper says PNGs); binwalk finds nothing in 7 of them; v1 generate accepts an outside grammar via --path
metadata:
  type: project
---

Established 2026-10-20 while analysing naive run 6 (binwalk), by reading v1's code at commit d80324073 and
running it on the Mac (v1 `.venv`, Python 3.12.9). Related: [[project-naive-claude-code-arm]],
[[caruca-v1-enumeration-redundancy]].

- **`Integer` enumerates its whole range.** `ir/syntax.py:263-269`: `min: int = -1`, `max: int = 1`,
  `syntax()` returns `range(self.min, self.max + 1)`. So a grammar with `Integer(min=0, max=65535)` yields
  65,536 invocations for that one option. None of v1's own `syntax_specs/*.py` uses `min=` or `max=` (grep,
  2026-10-20). The paper's section 4.2 says only "for integer, it generates the numbers -1, 0, 1".
  The naive arm's `formats/syntax_description.md` mentions `min=`/`max=` with no warning about this.
- **File content pool.** `ir/contents.py` + `data/`: `human_1.txt`, `human_2.txt`, `math_1.txt`,
  `math_2.txt`, `time_1.txt`, `time_2.txt`, `json.json`, `usenix.jpg`. `simple` (the default `--content`)
  = human text only; `varied` = text, math, JSON, time, image; `split` adds the halves. The paper (section
  4.3) says images are "a set of PNG images ranging from 2kb to 4MB"; the code ships one JPEG.
- **binwalk on that pool** (binwalk 2.3.3 in the naive-run clone, 2026-10-20): 0 results in all 7 text /
  math / time / JSON files; 1 in `usenix.jpg` (its own JFIF header at offset 0).
- **`flag_followed_by_equals=True` puts `=` after whatever spelling is generated, short ones included**
  (observed 2026-10-20 in `caruca generate` output, naive runs 7 and 9): `Range(flag="-b", alias=["--bytes"],
  flag_followed_by_equals=True)` yields `cut -b=1`, which GNU cut 9.4 rejects (value read as `=1`). **Aliases
  are never generated**: 0 of the distinct `cut` lines at `--max-count 4` (v1's reference and run 7's
  grammar) and 0 of the `sort` lines at 2 use an `alias=` spelling, so a grammar whose `flag` is the short
  form never yields the `--long=value` form the `=` was meant for. v1's own curated grammars do this too:
  `syntax_specs/uniq.py` on `-f`/`-s`/`-w` (`uniq -f=1` → "invalid number of fields to skip", run in the
  pash VM) and `syntax_specs/sort.py` on `-S`. The naive arm's format document describes the flag as "the
  value is attached with `=`, as in `--interactive=always`", with no warning. Measured effect on `cut` at
  `--max-count 4`, every distinct line run on coreutils 9.4: v1's reference 360 lines doing real work (of
  9,856 judged), v1's model output 0, run 7's agent grammar 0. Also: v1's reference `cut` has a
  FreeBSD-only `-w` (992 rejected lines) and all three selectors optional (6,450 lines with two
  selectors, 141 with none); `sort` at 4 = 1,972,046 lines (307,023 distinct).
- **Operands share the option budget, and a repeatable operand gets at most one file** (`--max-arity`
  default 1, `cli/__init__.py`). Observed 2026-10-20 on `convert` at `--max-count 1`: with the naive run 8
  grammar (`Path(ZERO_OR_MORE)` inputs + `Path(EXACTLY_ONE)` output) every line that carries an option has
  one file (the output); only the 4 option-free lines (`convert X Y`) have two. v1's curated reference
  (`Path(ONE_OR_MORE)`) gives 0 lines with two files; v1's model output (two `EXACTLY_ONE` paths) gives
  2,272/2,272. Checked on ImageMagick 6.9.12-98 with `usenix.jpg`: an option plus one file fails ("no
  images defined"), one file alone prints the version. Distinct lines: agent 2,422 (63,048 total), reference
  1,052 (7,308), model output 2,272 (14,616). v1's PaSh tracing does not use any of these: `run.sh` runs
  `caruca trace --pash --stdin split --content split`; `--pash` selects `caruca.pash_syntax_specs`
  (`cli/trace.py` lines 11–12), whose `convert.py` is input, optional `-resize`, output (three positions,
  unchanged since `38aefafd0`, 2024-11-28); `--content split` includes `usenix.jpg`. The paper's section 7.4
  does not say which grammar or settings its `convert` projection (98.72 h at two flags) used.
- **The CLI accepts an outside grammar directly:** `PYTHONPATH=<scratch> caruca generate <cmd> --path <pkg>`
  where `<scratch>/<pkg>/__init__.py` and `<scratch>/<pkg>/<cmd>.py` exist (used for runs 7 and 9).
- **Running v1's generator on an outside grammar without touching v1:** put the file in a scratch package
  (`bwspec/__init__.py`, `bwspec/<cmd>.py`), then from that folder call
  `caruca.cli.generate.string_invocations("<cmd>", "bwspec", skip, 1, False, max_count)` with v1's
  `.venv/bin/python -I` and `sys.path.insert(0, '.')` (`get_syntax_spec` imports `f"{path}.{cmd}"`). On the
  binwalk agent grammar: 65,659 at max_count 1; skipping `-s`, 122 (72 distinct) at 1 and 7,282 (2,535
  distinct) at 2. Same method on v1's grep: 121 (74 distinct) at 1. `caruca generate --number`'s formula
  ignores value counts (gives 51 for binwalk at 1), so it undercounts. Wrap the loop with `python -u` or
  print per stage: output buffering hid progress for minutes.
- **`caruca oracle` cannot take an outside grammar** (read in v1 `cli/__init__.py`, 2026-10-26): only
  `trace` and `generate` get the `--path` option (`generate_mixin`); `oracle_subparser` is built with no
  parents. Scoring an agent's grammar on the real-world invocation corpus therefore needs a small wrapper
  that imports the grammar and calls the oracle's matching code. Not yet written.
- **`caruca trace` ignores `--path`, and `--length-only` ignores `--max-count`** (read in v1
  `cli/trace.py` lines 9–15 and 18–28, 2026-10-26; observed: three different `cut` grammars all gave
  3,483,648 with `--path p --max-count 1 --length-only`, the size of the default set). To trace an outside
  grammar, call v1 directly from a scratch folder in the `caruca` VM (the tracer writes `tracer.log` into
  the current folder): `string_invocations(cmd, "<pkg>", None, 1, False, max_count)` then
  `Tracer(10, "simple", "simple", "").run(invocations)`. It returns one `CommandInvocationTraceSet` per
  generated line: `.true_str` is the line, `.configs[i].return_code` / `.stderr` one per test environment.
  Done in `naive_llm_caruca/scoring/trace_usefulness.py` (task 018): the agent's `cut` grammar at
  max_count 1 gave 360 invocations, 240 distinct lines, 480 runs in ~9 s.

**Added 2026-10-26** (naive-LLM syntax-file comparison, `naive_llm_caruca/syntax_files_vs_v1.md`):
- `Integer(min=2)` with no `max` gives `range(2, 2)` = **no values**: v1's generator never writes the
  option (the agent's `sort --batch-size`). `min=1` alone gives only `1`.
- A `Selection` with choice `""` and `flag_followed_by_equals=True` is written `--opt=` (mixin.py drops the
  empty value but keeps `=`): `rm --preserve-root=` and `sort --check=` are both rejected by coreutils 9.4.
  All three `rm` grammars (reference, model output, agent) have it.
- An optional operand (`ZERO_OR_MORE`) competes with options for the `--max-count` budget. The agent's
  `rm` (operand made optional because `rm -f` needs none) yields lines with no file in 19 of 21 distinct
  lines at max-count 1 and 2,466 of 3,978 at 4; reference/model (`AT_LEAST_ONE`) never do. `--max-count`
  default is 4 (`cli/__init__.py` line 54).
- Sample values per kind decide generator validity: `Delimiter` = `,` and a two-character newline+tab
  (rejected by `cut -d`, `sort -t`); `String` = the word `string` (rejected by most `convert` numeric /
  geometry options); `Geometry` = `50%`, `100x100`.
- **v1's `Arity` enum has aliases** (read in v1 `ir/environment.py` lines 24–31, 2026-10-27):
  `ONE_OR_MORE` is an alias of `AT_LEAST_ONE` and `ZERO_OR_ONE` of `OPTIONAL` (same values), so a loaded
  node's `.arity.name` is always `AT_LEAST_ONE` / `OPTIONAL`; there is also `EXACTLY_TWO`. Code that
  checks for `ONE_OR_MORE` by name never matches (task 018's first pass made exactly that mistake).

**Added 2026-10-27 — how many test runs v1 needs (code-read + exact count, v1 `d80324073`):**
- Each generated command line becomes (product over its file arguments of the file situations) × (stdin
  variants) traced runs (`CommandInvocation.to_exec_env`, `ir/string.py`). With plain relations a file
  argument has 5 situations at `--content simple` (file with sample text, empty folder, non-empty
  folder, missing file, file in a missing folder; `Path.attach_env`), each as relpath and abspath.
  `Tracer.run` maps over every invocation with **no dedup** (`tracer/tracer.py`).
- Exact totals without listing: the generator picks exactly k optional entries (each may be "absent"),
  so lines = k-th elementary symmetric sum of per-entry variation counts. Script:
  `naive_llm_caruca/comparisons/2026-10-26_syntax_files_vs_v1/scripts/config_count.py`, matches v1's
  generator exactly (rm 54/664, cut 41/759, sort 3,640 lines / 7,640 runs at k=2, convert 1,566 / 8,710 at
  k=1). Reference grammars, traced runs at k=2 / k=4: rm 3,320 / 122,400; cut 1,063 / 114,004; sort 7,640 /
  7,814,222; convert 3,765,840 / 229,656,055,750. Agent's convert file at k=4: ~3.48 trillion.
- `wc -l` over `caruca generate` output overcounts when a value contains a newline (v1's `Delimiter`
  sample `"\n\t"`): cut k=1 shows 43 lines for 41 invocations.
- **Not established:** how the paper counted for Fig. 7. Its two `convert` figures (98.72 h at ≤2 flags,
  27,533.2 days at ≤4) imply ~6,700× growth from 2 to 4; v1's current code gives ~61,000×, so the paper's
  projections are not reproduced by these counts.
