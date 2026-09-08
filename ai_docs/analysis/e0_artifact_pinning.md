# E0 Findings — Artifact Pinning and the Paper's Three Divergence Claims

**Run 2026-09-06** on this Mac. E0 is the blocking reproducibility check defined in
[`experiment_designs.md`](experiment_designs.md) and re-scoped in
[`experiment_implementation_plan.md`](experiment_implementation_plan.md) Part 4: before any
experiment builds on the paper's three specification-divergence claims (`grep`/`ps`/`cp`), pin
exactly which artifact revisions they refer to and confirm what reproduces. This note reports
the findings; each of the three claims ends in a definite state.

**Pinned artifact set for everything below:**

| Artifact | Revision |
|---|---|
| v1 (`binpash/caruca`) | `d8032407346aadc135b14c043618c8c1d4f4e0cf` (`main`), local clone `~/dev/stevens/caruca` |
| Upstream hand-written annotations (`binpash/annotations`) | clone of `main` at `2b57533` (repo public; last updated 2026-01-26) |
| PaSh repo history (`binpash/pash`) | queried via GitHub API 2026-09-06 (commits `f4c5bca7`, `6c147188`, `92364f6a`) |
| The paper | arXiv:2510.14279 (Oct 2025), §7.1 wording |
| Execution environment | Lima VM `caruca` (Ubuntu 24.04) for trace/annotate; macOS host for generate-only |

**One prior worry retired first.** The concern that the paper's numbers came from a diverged
branch is closed: `origin/caruca-experiments` is `main` plus exactly two commits (a CLI crash
fix, documentation) with no differences under `benchmarks/annotations/` or
`eval/pash-annotations/`, and `origin/paper` is fully contained in `main`
(`git log main..origin/caruca-experiments`; `git diff --stat main origin/caruca-experiments --
benchmarks/annotations/ eval/pash-annotations/` → empty).

---

## Claim 1 — grep: **REPRODUCED, against a 2021 revision** (and the fix predates the paper by 3.5 years)

The paper: *"`grep` is marked as always stateless in the original specifications, but in
reality it is not if invoked with the `-c` flag."*

**Provenance found.** The hand-written grep annotation's history (in `binpash/pash`, path
`annotations/grep.json`, before the 2022-09-08 move to `binpash/annotations`):

- At `f4c5bca7` (2020-12-27 → 2021-04-05): **no `-c` case exists.** Cases: single-arg →
  `stateless`; `-r/-R` → `side-effects`; default → `stateless`. For the `-c` dimension this
  is exactly "marked as always stateless."
- PR **binpash/pash#192, "Fix an issue with grep's annotation," merged 2021-04-06** (author
  `angelhof`), adds the first case: `exists -c` → `pure`.
- Every artifact from then on — the 2022 move into `binpash/annotations`
  (`old_annotations/grep.json`, unchanged since), v1's local copy
  (`benchmarks/annotations/pash/grep.json`, added 2024-07-01, unchanged), and the new-format
  generator (`ParallelizabilityInfoGeneratorGrep.py`, which routes `-c` to a sum-aggregator
  and, because that aggregator is `is_implemented=False`, conservatively produces no
  parallelizer for `grep -c`) — **handles `-c`**.

**So the claim is true of the pre-2021-04-06 revision and of no artifact since.** The
correction was *not* prompted by Caruca (it predates it by ~3.5 years). For the resubmission
this means the grep example must cite the historical revision explicitly — as shipped today,
a reviewer checking any live artifact will find `-c` handled and conclude the paper
misdescribes it. (Note the fix's author is a PaSh maintainer and Caruca co-author; the
resubmission can cite PR #192 as evidence the maintainers themselves treat these annotations
as living, correctable approximations — which is the paper's own argument.)

**Behavioral half, fresh reproduction.** v1 on `main`, Lima VM, bounded to single-flag
invocations (`caruca trace grep --max-count 1` — 122 invocations; the unbounded space is
1,426,920): the derived PaSh annotation (44 cases) classifies `grep -c a` as **`non-pure`** —
not stateless, consistent with the paper's behavioral observation. One nuance worth carrying
into the spec-holding study (E1): at this bound fresh v1 classifies **every** grep case
non-pure, including plain `grep a` — i.e. it diverges from the hand-written "stateless"
default in the *conservative* direction. Whether that reflects v1's post-paper
classification fix (the same one that makes committed `save/*.json` stale — see
[`../..//memory/mac_lima_tracing_env.md`](../../memory/mac_lima_tracing_env.md)) or the
reduced evidence of a bounded run is a one-experiment follow-up: rerun at the paper's
two-flag bound and diff. Commands: `caruca trace grep --max-count 1 --output
outputs/grep.maxcount1.json && caruca annotate pash grep --input outputs/grep.maxcount1.json`
(artifacts kept at v1's `caruca/outputs/{grep.maxcount1.json,e0_grep_pash.json}`, untracked).

## Claim 2 — ps: **annotation half REPRODUCED verbatim (and still wrong upstream today); behavioral half NOT REPRODUCIBLE from shipped artifacts — explained**

The paper: *"`ps` (marked as stateless, but in reality being side-effectful)."*

- **Reproduced:** `binpash/annotations` `old_annotations/ps.json` is a single default case →
  `stateless`. Created 2020-10-02 in the pash repo, moved 2022-09-08, **never modified —
  still `stateless` at upstream `main` today (2026)**. No new-format ps generator exists
  either. So unlike grep, the paper's ps observation has **not** been adopted upstream: the
  only ps annotation in existence still says stateless. That is a live, citable divergence —
  the strongest of the three for the resubmission's motivating section.
- **Explained (not reproducible as shipped):** ps is **outside v1's own command population
  entirely**. No `doc_sources/man/ps.txt`, no `syntax_specs/ps.py` on any branch
  (`git log --all -- caruca/src/caruca/syntax_specs/ps.py` → empty), and no
  `outputs/llm-dsl-generation/ps.py`. `caruca generate ps` dies with
  `ModuleNotFoundError: No module named 'caruca.syntax_specs.ps'`. The paper's ps behavior
  observation therefore came from outside the shipped artifact set (an unshipped spec or an
  ad-hoc run). For the resubmission: either add ps to the population (write/generate its
  spec — it then becomes a first-class E1 witness candidate) or cite the observation as
  external to the evaluated set. **Question for the team/Greenberg: where did the paper's ps
  run come from?**

## Claim 3 — cp: **no hand-written artifact has ever existed; the fresh run CONTRADICTS the paper's behavioral claim on `main`**

The paper: *"`cp` (marked as side-effectful, but in reality being pure)."*

- **Provenance: there is no cp annotation to pin.** `binpash/pash` history for
  `annotations/cp.json` is empty (the file never existed); `old_annotations/` has no cp; no
  new-format cp generator exists; v1's `benchmarks/annotations/pash/` has no cp. "Marked as
  side-effectful" can only describe **PaSh's conservative default for unannotated
  commands**, not a hand-written specification. The resubmission should say so — it is a
  different (and interesting) divergence class: *over-conservatism of a default policy*,
  a missed-optimization cost, not an unsoundness.
- **Behavioral half does not reproduce on `main`.** Fresh v1 (Lima, `--max-count 1`,
  368 invocations of the 736,560 unbounded): 26 of 29 derived cases **`side-effectful`**,
  3 `non-pure`, zero `pure` (artifacts at `caruca/outputs/{cp.maxcount1.json,e0_cp_pash.json}`;
  3 `--reflink never` invocation groups produced no successful runs and are excluded by v1
  itself). This **agrees** with v1's own committed `eval/pash-annotations/cp.json` (all cases
  side-effectful) and **disagrees** with the paper's "in reality being pure." Definite state:
  the cp claim reflects some other revision or derivation logic than `main`'s. **Question for
  the team/Greenberg: which run produced "cp is pure"?** (Candidate explanation: v1's
  parallelizability-classification logic changed post-paper — the same change that makes
  `save/ls.json` stale; if the paper's cp run predates it, the claim and `main` can both be
  faithful to their own revisions. That is precisely why E0 exists.)

---

## The population pin (every future denominator depends on this)

v1 ships three overlapping command sets (measured 2026-09-06):

| Set | Count | Notes |
|---|---|---|
| Man pages (`doc_sources/man/*.txt`) | **120** | The population the paper calls "120 commands" |
| Committed syntax specs (`syntax_specs/*.py`) | **120** real (121 files minus `__init__`) | `mogrify`, `uglifyjs` have specs but **no man page**; `jobs`, `xargs` have man pages but **no spec** |
| Hand-annotated ground-truth JSON (`doc_sources/ground-truth/*.json`) | **108** | Missing for 13 man-page commands incl. `grep`, `sed`, `awk`, `diff`, `convert`; plus a stray `coreutils.json` |

**Verdict:** the Q2-style accuracy denominator is the ~120-command man-page/spec population —
the 108 ground-truth JSON files *cannot* be it (they don't cover grep or sed). For the task
006 scorer: committed specs are the primary reference; the ground-truth JSON is a secondary,
107-command cross-check (`intersection of all three = 107`). Report the two references
separately, never blended.

## The enumeration-redundancy sweep (instrumentation, not a claim)

All 120 man-page commands, v1 defaults, macOS host (`generate` only — no execution), script
and CSV in the session scratchpad, key numbers reproduced here:

- **90 commands enumerate fully** (< 500k lines). Across them: **3,261,075 invocations
  emitted, 562,789 unique — 82.7% duplicates overall**; per-command median 75.7%, max 92.9%
  (`who`); 18 commands emit zero duplicates. `mkdir` reproduces task 002's exact numbers
  (hint 280 / emitted 4,240 / unique 1,094), validating the instrument.
- **The `--number` hint disagrees with actual emission for 90 of 90** fully-enumerated
  commands. It must never be used as a denominator (confirms task 002's finding at
  population scale).
- **16 commands truncate at the 500k-line cap** (in-window duplicate rates 52–87%); largest
  hints: `convert` **4,757,736,375**, `pandoc` 14.4M, `diff` 6.0M, `ls` 3.4M, `grep` 1.4M,
  `cp` 0.7M — the paper's flag-explosion cost story, quantified at the generator.
- **14 commands fail `generate --number` outright** on `main`: `jobs`/`xargs` (no committed
  spec — matches the population pin) and 12 more (`col dd false hostid logname nproc pwd
  true tty uname uptime whoami`) with `ValueError: max() iterable argument is empty` in
  `max_group_arity` — a latent v1 defect on (mostly) zero-flag commands, worth an upstream
  issue. Note these 14 cannot currently produce Q1-style annotations at defaults.
- **The tracer inherits the duplicated stream rather than deduplicating**: `caruca trace
  mkdir --length-only` = 10,368 executions ≈ 2.45 environment configs × the 4,240 *emitted*
  (duplicated) invocations, not the 1,094 unique. Duplicate enumeration therefore inflates
  *execution* counts, not just output lines — relevant to any cost accounting against the
  paper's Q4 hours, and the baseline-inefficiency figure for the adaptive-querying
  experiment (S4/E-series).

## What E0 changes downstream

1. **E1 gains a sharper motivating frame:** of the paper's three examples, one describes a
   2021-corrected artifact, one is still wrong upstream today, and one was never an artifact
   at all — the *taxonomy* (stale-citation / unadopted-finding / default-policy) is itself
   the argument that a systematic study (E1) is needed.
2. **Two questions go to Greenberg** (per the conversation the contributions document
   recommends): where did the paper's ps and cp runs come from? Their answers pin the last
   two artifacts E0 cannot reach from here.
3. **Task 006 scorer references are settled** (committed specs primary, ground-truth JSON
   secondary, 107-command overlap).
4. **Bounded-vs-paper-bounds check** added to E1's protocol: rerun grep at `--max-count 2`
   and diff classifications against this run before treating conservative-direction
   divergences as findings.
5. Fresh default-bounds traces for 13 small commands (`arch groups tsort unlink cksum
   nohup sleep users dirname expr factor link printenv`) were generated into v1's
   `caruca/outputs/` during the same VM session — these are the stage-3/stage-4
   isolation-cell inputs the per-stage fidelity study needs beyond `ls`. A 14th, `yes`,
   produced no trace file: it emits output forever, so every invocation hits v1's 2-second
   timeout and no successful run remains.
