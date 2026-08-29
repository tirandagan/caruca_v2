---
name: component-functionality-spec
description: "Key design decisions behind ai_docs/prep/component_functionality.md — shared pipeline seam, dual-profile evaluation, deferred Web GUI shape"
metadata:
  type: project
---

`ai_docs/prep/component_functionality.md` was produced via the `05_generate_app_pages_and_functionality`
planning pass, covering the 5 priority MVP components (Baseline Instrumentation, Naive-LLM Baseline,
Secure Sandbox Environment, LLM Tool-Augmentation Layer, Evaluation Harness) plus a deferred Web GUI. Three
decisions from that session aren't obvious from re-reading the spec file alone:

**Naive-LLM baseline shares v1's downstream pipeline, not just its output format.** Because the naive-LLM
emits the same Python-DSL syntax-spec shape v1 uses, it slots into the exact same position v1's own
LLM-generated spec occupies — so it can flow through v1's existing config-gen → trace → annotate stages to
get BOTH a Q2-style (syntax-spec, via `cmp_specs.py`) AND an **annotation-diff** comparison (diffing the
resulting annotation against `benchmarks/annotations/`), from one design choice. Secure Sandbox and the
annotate step are therefore shared infrastructure across both approaches, not v1-only tooling being reused
ad hoc.

**Correction (2026-08-29 review):** this was originally labeled a "Q1-style" comparison here, which
overstates it — see [[caruca-v1-eval-tooling-notes]]. The paper's actual Q1 methodology is mostly
execution-based (real PaSh/ShellCheck/Shseer suite reruns), not diff-based. Annotation-diff is a real,
useful, but genuinely lighter and different check, now correctly labeled as such in
`component_functionality.md`. True execution-based Q1 is deferred to [[caruca-v2-build-tiering]]'s Tier 1.

**Why:** avoids building two separate evaluation paths, and keeps the naive-LLM baseline genuinely
"naive" (per Eiers, [[caruca-v2-baseline-scope]]) since it never has to synthesize a full annotation
itself.

**Dual-profile evaluation design (v1-faithful vs. v2-extended).** Initially proposed gating the extended
fixture model (symlinks, permissions, pipes, deeper directories, correlated content — see
`ai_docs/analysis/evaluation_gaps.md` gaps 1/5/6/7/8/10/11/12) behind a "coverage probe" that avoided
running it through v1's annotator. Tiran corrected this: both a `v1-faithful` profile (exact replication,
the control) and a `v2-extended` profile should run through the FULL annotate pipeline, tagged separately
in results, not blended. Where v1's unmodified annotator mishandles a v2-extended trace shape, that's
itself a reportable coverage-gap finding (evaluation dimension 3), not something to avoid surfacing.

**Why:** the whole point of the project is measuring how far v2 extends past v1's sweet spot — refusing to
run the extended profile through annotation would throw away that exact measurement to avoid an
implementation risk. The implementation risk (v1's annotator needs targeted extensions to correctly
interpret new trace shapes) is instead captured as an explicit open dependency in the spec's Open
Questions, not worked around.

**Web GUI concrete shape (deferred, not building yet).** Tiran proposed a live side-by-side terminal
comparison app: backend spawns v1's CLI and `caruca-v2`'s CLI each inside a PTY, streams both over
websocket to xterm.js panes in the browser (left = v1, right = v2), with a metrics panel reading the same
telemetry JSON files the CLIs already write. Captured as the Web GUI component's design in
`component_functionality.md`, explicitly deferred behind the 5 priority components per CLAUDE.md's stated
build order (baseline + eval harness first, then naive-LLM baseline, before sandbox/web work). Costs the
other components nothing later since it's a pure presentation layer over their existing CLI/telemetry
surfaces, not a new data format.

**How to apply:** when implementation on any of these 5 components starts, or when the data/telemetry
schema pass (`08_generate_initial_data_models.md`) or system architecture pass (`09_generate_system_design.md`)
runs, reference `component_functionality.md` as the settled I/O/CLI contract — but verify the file still
exists and these specific decisions (shared pipeline seam, profile tagging, PTY web design) still stand,
since the spec is provisional per the Master Idea's own "flexible" framing on MVP components.
