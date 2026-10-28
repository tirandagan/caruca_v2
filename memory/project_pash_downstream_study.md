---
name: project-pash-downstream-study
description: Task 012 — PaSh as downstream consumer for v1-vs-v2; Tiran's four design decisions; the trace-mode finding (v1 at --stdin simple can never emit stateless); Phase 0 run 2026-10-05 (PaSh installed, annotation format resolved as Python classes, decision probe still unsolved)
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

**That open unknown is now RESOLVED** — see the Phase 0 entry at the end of this file. Current PaSh
does not read JSON at all, and neither did the paper's revision.

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
as `_v1.1` beside the originals; see `ai_docs/archive_2026-09_rebuild/docs/presentations/ASSEMBLY.md`. Still unreconciled
by deliberate choice: `CLAUDE.md` and `PRODUCT.md` (same Q1 wording, WSL-only machine description),
and the live Dropbox deck, which the repo cannot edit.

**Phase 0 run 2026-10-05 — PaSh installed. Full record in `ai_docs/docs/pash_vm_setup.md`;** only
the decision-changing facts are repeated here.

- **No PaSh since 2022-09-08 reads JSON annotations, including the revision the paper ran.** JSON
  was deleted in `binpash/pash` commit `92364f6a`; the paper's-run revision `0d0a563b` (2024-11-18)
  already required `pash-annotations==0.2.2`, a Python-class format. Established by reading
  `pyproject.toml`, `requirements.txt` at that revision, and the dispatch in
  `pash_annotations/annotation_generation/AnnotationGeneration.py`. **This resolves task 012's
  pinning rule with no judgement call: pin modern, adapter emits Python classes.** It also sharpens
  the Greenberg question — Caruca's committed JSON annotations could not have been consumed by the
  paper's own PaSh.
- **Installed and verified on aarch64**: `binpash/pash` at `42a8b87` (2026-09-29),
  `pash-annotations` 0.2.4, in a new Lima VM `pash` (Ubuntu 24.04.4, coreutils **9.4 — matches the
  `caruca` VM**, Mac home mounted **read-only**, verified). `libdash`/`libbash` C extensions build
  natively, so the x86-fallback plans are not needed. Output byte-identical to `bash` on a
  `sort | uniq -c | sort -rn` pipeline at width 8.
- **PaSh's own installer is broken on Ubuntu 24.04**: `scripts/distro-deps.sh` omits
  `python3-venv`, which `setup-pash.sh` needs immediately. Install `python3.12-venv` first.
- **Of task 012's nine commands, only `uniq` has a stock parallelizability annotation.** `cat`,
  `tail`, `tee`, `rm` have input/output generators but no parallelizability one; `pwd`,
  `sha256sum`, `tac`, `wc` are absent from the dispatch table entirely (`wc`'s generator file
  exists but is unreachable). The hand-written comparison arm is far thinner than planned.
- **Fixed overhead is 0.15 s per run**, not the ~1 s task 012 assumed — so Tier A's ~15,000 runs is
  ~40 minutes of overhead, not 5-10 VM-hours.
- **Per-command decision probe — SOLVED 2026-10-13, correcting the entry below.** Each PaSh worker
runs `bash -c ' CMD … '`, so the command is resolved through `PATH`. A wrapper of the same name
placed earlier on `PATH` logs one line per invocation; **a count above one is positive, per-command
proof that this command was parallelized**. Demonstrated at width 8 with per-worker start/end/busy
times. Three cautions: it also intercepts PaSh's own calls to that command (filter on argument
shape and report both counts), it costs a fork plus two `date` calls per worker, and it cannot work
for a shell builtin such as `pwd`. Recipe in `ai_docs/docs/pash_vm_setup.md` §3.3; task 012's
Phase 0 box is ticked and its exit gate can now be attempted. Also corrected in 012 §4 the same
day: the Tier A script shape it specified ended in `> "$OUT"`, and a trailing redirect makes PaSh
fall back to plain `bash` — every such script would have measured nothing while still returning the
right answer.

**`--assert_all_regions_parallelizable` passes vacuously** when PaSh never attempts a region, so
  it cannot be used alone as a decision probe. **Reading the per-command parallelization decision is
  unsolved and is now Phase 4's blocker**; the exit gate is therefore NOT met. Untried candidates:
  `--graphviz dot`, higher debug levels, `-p` captured from stdout (it writes to stdout, not stderr).

**Framing changed 2026-10-06.** Greenberg's position, as Tiran relayed it, is that v1's objective is
the overall syntax definition of a command and parallelization is a side topic
([[project-greenberg-caruca-purpose]]). Task 012 therefore tests one consumer, not v1's purpose. Its
findings stand. When presenting them, don't frame PaSh speedup as the measure of whether v1 works.
Facts about PaSh's grep annotation, old and current: [[pash-grep-annotation-current-vs-json]].
