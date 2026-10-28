---
name: caruca-v1-matcher-behaviour
description: How v1's real-world matcher (`caruca oracle`, the paper's real-world reach figure) treats a grammar — value options without `=` claim any word, `=` options need attached values, positions read once, `-` never a file, required files unchecked; replay reproduces v1's committed counts; 40% of corpus lines are "read" only via a word taken as an option it is not; which v1 programs read a grammar
metadata:
  type: project
---

Established 2026-10-26 by reading v1 `d80324073` (`oracle.py`, `ir/syntax.py` `could_match`) and by
replaying the matcher on `eval/user-scripts/invocations.txt`. Scripts/results:
`naive_llm_caruca/comparisons/2026-10-26_syntax_files_vs_v1/`; write-up
`naive_llm_caruca/syntax_files_vs_v1.md`. Related: [[caruca-v1-eval-tooling-notes]],
[[caruca-v1-value-generation]], [[project-naive-claude-code-arm]].

**Behaviours (code-read, then seen in runs):**
1. A value-taking node **without** `flag_followed_by_equals` matches *any* word as its spelling
   (`ValueArgument.__flag_match` final `else` → `StringAgnosticism(arg, self.flag)`, returns True). With
   v1's reference, `sort -u` is read as `--random-source`; `cut -d ' ' -f 2` as `-b`,`-c`,`-d`,`-f`.
2. A node **with** `=` takes its value only attached; `-d ,` → `-d` with no value (`DefaultArg('')`), `,`
   left behind and read as a file.
3. After `=`, the value must be one of the kind's sample values (`MetaString` match is strict), so
   `cut --fields=2` is not read.
4. Positions are walked once, in order (options, then files); syntaxes are chained, not tried as
   alternatives (`chain.from_iterable(usages)`).
5. `Path._value_match` rejects any word starting with `-`, so a lone `-` is never a file (`dash_as_stdin`
   ignored). Required operands are never checked: once words run out it returns success.

**Two kinds of `StringAgnosticism`, separable mechanically:** `matched_with` is an option spelling
(behaviour 1, a word taken as an option it is not) or a value-list repr (unknown value, the case the
paper's §7.3 "string normalization" describes). v1's `completeness_accumulate.sh` greps class names only,
and misspells `ShortFlatSplat`, so its "no assumption" level never excludes `ShortFlagSplat`.

**Measured.** Replay with v1's own grammars reproduces `oracle_results.txt` and `command_counts/`
exactly (rm 24,094 / sort 5,011 / cut 5,890). Whole corpus (665,631 lines as Python reads it; `wc -l`
665,628; 3 carriage returns): full 650,890; without ArityStrategy 631,937; without Arity+String 123,174
(paper: 651,733 / 632,780 / 122,816 on 666,468). **267,070 full matches (40% of all lines, 42% of the
631,937) use at least one behaviour-1 guess** — top: test 193,623, mkdir 15,008, cp 12,861, cut 5,812,
mv 4,953, ls 3,939. For cut and sort, every such line was checked against an emulated GNU `getopt_long`
reading and all were wrong (cut: 78 of 5,856 valid lines read correctly by the reference; sort 2,360 of
5,010). Not checked line by line for other commands.

**Every v1 program that loads a grammar:** generator (`cli/generate.py`), matcher (`oracle.py`),
ShellCheck adapter (`annotator/__init__.py` lines 60–106, "missing destination" check, added
2025-12-21: fires when a layout has ≥2 positional `Path` entries requiring ≥2 files), scorer
(`eval/cmp_specs.py`), `cli/syntax_spec.py`, and `llm.py`'s import-based validation. PaSh does not.

**Running the matcher with another grammar without touching v1:** import `caruca.oracle as O`, wrap
`O.get_syntax_spec` to call the real one with your package name, call `O.oracle(line)`.

**Also measured (task 018, 2026-10-26/27).** With v1's shipped GPT-4o `sort` file, which has no `-k`/`--key`,
the matcher still reads 5,011 of 5,011 real `sort` lines, 2,343 of them via a behaviour-1 substitution;
read with GNU's rules that file reads 4,179 of 5,010. So the paper-style count cannot see a missing option.
Task 018 reports the GNU-rules reading (this note's `gnuread.py`) beside v1's count, never instead of it.
(Merged here 2026-10-27 from a duplicate note, `caruca_v1_oracle_flag_substitution.md`, now deleted.)
