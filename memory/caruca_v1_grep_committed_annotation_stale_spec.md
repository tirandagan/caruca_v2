---
name: caruca-v1-grep-committed-annotation-stale-spec
description: v1's committed save/grep.json was generated from a PaSh grep spec with NO pattern positional (fixed a day later, never regenerated); current v1 cannot emit its invocation form at all
metadata:
  type: project
---

Verified 2026-10-05 on the Mac against v1 at `d80324073`, from git history plus a fresh
`caruca generate` (no tracing needed).

v1's committed reference annotation `caruca/save/grep.json` describes invocations written
`grep -v relpath_1` and `grep -c -v relpath_1` — a **file path as the only positional, no
pattern**. Real grep reads that path as the pattern and takes its input from stdin. Current
v1 cannot produce that form: under today's PaSh grep spec it enumerates 46 distinct
invocations, every one with the pattern `a` first (`grep -v a`, `grep a relpath_1`), and
zero with a path as the sole positional.

Timeline that explains it:

| date | commit | what happened |
|---|---|---|
| 2024-12-08 | `6ceda7586` | `save/grep.json` regenerated for the last time. The PaSh grep spec then had one positional: `Path(ZERO_OR_MORE, dash_as_stdin=True)` |
| 2024-12-09 | `3d1fde4eb` "Fix pash grep syntax spec" | adds `Regex(EXACTLY_ONE)` in front of the path. `save/grep.json` was not regenerated |
| 2025-12-21 | `c97306bb4` "fix parallelizability class classification" | `stateless` now also requires that output preserve input line order |

Consequences:

- `len_args_eq 1` means different things in the two artifacts: **one path** in the committed
  file, **one pattern** in any fresh run. The numbers agree with PaSh's hand-written
  `len_args_eq 1` case only by coincidence in the committed file.
- The committed file has **no two-argument case**; fresh output does
  (`grep a relpath_1`, input `args[1]`).
- The committed cases list 121 and 151 inputs each (stdin plus `pipe:[…]` descriptors);
  fresh cases list one.
- **Do not attribute the class difference to one cause.** Committed says `-v` is
  `stateless`; the only fresh grep annotation (E0, `caruca/outputs/e0_grep_pash.json`,
  2026-09-06) says all 44 cases are `non-pure`. Three things differ between them: the spec
  fix above, the classifier fix, and the trace mode (E0 used the full spec at
  `--max-count 1` with the `simple` default, not `run.sh`'s `--pash --stdin split --content
  split`). No like-for-like fresh grep annotation exists; producing one is 5,504 traced
  executions in the Lima VM.

This is a grep-specific cause **in addition to** the classifier fix that
[[caruca-v1-macos-annotate-limitation]] and [[mac-lima-tracing-env]] already name as the
reason committed `save/*.json` disagree with fresh output. `ls` shows the classifier-side
effect cleanly (6 cases → 4, four `stateless` → two `non-pure`); grep has the spec-side
effect on top.

**How to apply:** never use `save/grep.json` as a v1 reference for grep — not for the
invocation form, the argument count, or the class. Regenerate under `run.sh` settings in the
Lima VM first, and record the v1 commit. Before trusting any other `save/<cmd>.json`, check
whether `pash_syntax_specs/<cmd>.py` changed after the file's last commit.
