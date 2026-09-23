---
name: project-pash-downstream-study
description: Task 012 (2026-09-22) — PaSh as downstream consumer for v1-vs-v2; Tiran's four design decisions; the trace-mode finding (v1 at --stdin simple can never emit stateless); annotation-format unknown
metadata:
  type: project
---

Tiran asked (2026-09-22) to judge v2 vs v1 by having a real consumer, PaSh, use the outputs.
Specified as `ai_docs/tasks/012_pash_downstream_study.md` (drafted as 011, renumbered after a
parallel session took 011 for the v2 improvement program). Specification only; nothing built.

**Tiran's decisions (AskUserQuestion, same session):** both v2 arms, isolation first (v2 annotator
on v1 traces, then the full v2 chain); full depth (acceptance → parallelization decision →
output-hash correctness → timing, timing secondary); both script tiers, synthesized micro-scripts
first, then PaSh's own benchmark scripts; a second dedicated Lima VM `pash` (keeps `caruca` clean).

**Finding made while writing it, verified in v1 code and against v1's own paper-run artifacts.**
State it precisely — a first draft of it overstated the point and Tiran caught that:

- All 64 cases across the nine parity annotations are `non-pure` or `side-effectful`; none is
  `stateless` or `pure` (even `cat`). `tracer/data.py:217-225` never assigns `pure` in any mode.
- **`non-pure` is a correct answer, not a blank.** It means non-parallelizable pure. The paper
  (§6.1) says Caruca cannot tell the two kinds of pure apart because that needs aggregator
  synthesis, and its own check (§7.1) counts `non-pure` as correct where a human wrote `pure`.
  So "v1 says nothing is parallelizable" is **wrong**; the accurate claim is that such an
  annotation set is *safe but inert* downstream, because PaSh cannot parallelize `non-pure`.
- What the trace mode changes is `stateless` specifically: it needs split-input traces (stdin
  names ending `_1`/`_2`), which only `caruca trace --stdin split --content split` produces
  (`ir/contents.py`). Parity used the `simple` default. v1's own PaSh pipeline `caruca/run.sh`
  uses split mode, and its artifacts (`eval/pash-annotations/`) do contain `stateless`: `cat` 1,
  `uniq` 2, `tail` 1 — versus 0 in the default-mode run of the same tool.
- Two document corrections for Tiran (decision D5 in task 012): parity study §5 and white-paper
  addendum §5 attribute v1's conservatism to the `--max-count 1` bound, and task 011's stage-4
  diagnosis says nothing about trace mode; and those tallies count `pure → non-pure` (33 of 58)
  as disagreement where the paper's own criterion would not, making our instrument stricter than
  the paper's.
- **The word "speedup" never appears in the paper** (verified over the full transcription), and
  its PaSh check was output-hash equality, which an inert annotation set passes trivially. How
  much parallelism mined specifications actually unlock has never been reported for v1 or v2.
  That is task 012's main product. v2's `generate` has the same `--stdin/--content split` knobs.

**Biggest open unknown:** whether current PaSh still reads JSON annotations (moved to
`binpash/annotations` 2022-09-08; JSON now under `old_annotations/`, live format is Python generator
classes). Task 012 Phase 0 settles it with a pinning rule fixed in advance.

**Why:** a future session picking this up should start at task 012's Phase 0 and not re-derive the
design, and should not repeat the "conservatism is caused by the bound" claim without the
trace-mode caveat.

Related: [[caruca-v1-eval-tooling-notes]] (the corrected reading of the paper's PaSh 52/52),
[[mac-lima-tracing-env]], [[project-experiment-program]], [[caruca-v1-macos-annotate-limitation]].

**Cross-chunk ordering hazard (Tiran, 2026-09-22).** Tiran asked whether splitting a recursive
delete could have one worker try to remove a directory another worker has not emptied yet. It
cannot reach PaSh through a *correct* Caruca annotation: v1 classes anything writing/deleting
files as side-effectful (`no_effect`, `tracer/data.py:196`), its splittability evidence is stdout
concatenation only (`__is_similar`, `data.py:88`, cannot fire for a command that prints nothing),
and PaSh never parallelizes side-effectful commands. But the underlying point stands and is now in
task 012: **a parallelizability class describes one invocation and cannot express a precondition on
the relationship between the items being split** (`rm -r a b` is safe unless one contains the
other; `find dir -depth | xargs rmdir` is correct only because of the ordering). Exposure is to a
*wrong* class — v2's risk, since it labels from world knowledge. Added to task 012: order-dependent
input shapes (nested trees, ancestor/descendant argument lists) and a third canary (Canary-O) that
must be caught by exit code and file manifest rather than stdout. v1's fixtures cannot produce these
shapes at all (`NonEmptyDirectory.prepare_env` = one directory, one child; no recursive tree-building
in v1 — gap 5 in `evaluation_gaps.md`). This is the concrete instance of that document's gap 2, and
**POSH, not PaSh, is where it is the native failure mode** (POSH splits by argument list; Caruca
emits `args_split`) — a reason to make POSH the next consumer studied.

**Repo-wide accuracy audit, 2026-09-22.** Tiran asked for every past analysis and presentation to
be re-checked and corrected. Two errors were systemic and are now fixed at source in ten documents
(each carries a dated "Version 1.1 / corrected 22 September 2026" note): (1) the paper's PaSh 52/52
described as execution-based; (2) v1's conservative parallelizability classes blamed on the
`--max-count 1` bound rather than the `--stdin simple` trace mode. Numbers re-derived from the
stored campaign that day and now authoritative: stage-4 class agreement against the hand-curated
ground truth is **v2 25/77 (32.5%) strict, 68/77 (88.3%) under the paper's pure≡non-pure rule**;
**v1 20/83 (24.1%) strict, 53/83 (63.9%) relaxed**; the published 10/33 was run 1 only and 11/64
was the seven-command subset. v1's disagreements: **63 total, 58 conservative, of which 33 are
`pure → non-pure` that the paper counts as correct.** v2's one unsafe-direction error: **`pwd`
classed `stateless` where truth is `side-effectful`, in all three runs.** Nine PDFs were reissued
as `_v1.1` beside the originals; see `ai_docs/docs/presentations/ASSEMBLY.md`. Still unreconciled
by deliberate choice: `CLAUDE.md` and `PRODUCT.md` (same Q1 wording, WSL-only machine description),
and the live Dropbox deck, which the repo cannot edit.
