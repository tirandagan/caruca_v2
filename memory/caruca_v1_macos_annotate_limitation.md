---
name: caruca-v1-macos-annotate-limitation
description: v1's `caruca annotate` cannot run on macOS at all (hardcoded /tmp vs /private/tmp); every v1-side annotation comparison must run in the Lima VM
metadata:
  type: project
---

Verified 2026-09-03 on the Mac, against v1's own committed `caruca/outputs/ls.json` at
commit `d8032407346aadc135b14c043618c8c1d4f4e0cf`:

```
caruca annotate pash ls --input outputs/ls.json
ValueError: '/private/tmp/sandbox_outer/sandbox_inner' is not in the subpath of
            '/tmp/sandbox_outer/sandbox_inner'
```

`tracer/data.py::__readwrite` calls `Path.resolve()` on each traced path and then
`relative_to(Path("/tmp/sandbox_outer/sandbox_inner"))`. On macOS `/tmp` is a symlink to
`/private/tmp`, so `resolve()` moves the path out from under the hardcoded prefix and
`relative_to` raises. This is not data-dependent: **v1's annotate stage cannot run on a
Mac at any input.**

Consequences:

- The `annotate` phase joins the `trace` phase in needing the Lima VM `caruca` (see
  [[mac-lima-tracing-env]]). Previously only tracing was believed to be Linux-only, and
  `CLAUDE.md` still says annotation "works fine here" — that is true on the WSL PC, not
  on the Mac.
- caruca_v2's `annotate` subcommand therefore takes `--v1-runner {host,lima}`; on the Mac
  the v1 side of every annotation diff must use `lima`, which runs
  `~/caruca-venv/bin/caruca` inside the VM.
- Anything comparing against v1's annotator must record the v1 commit alongside the
  result: v1's committed `save/*.json` predate its parallelizability-classification fix
  and disagree with freshly generated output.
