---
name: project_naive_llm_repo_split
description: 2026-11-24 Tiran decided to move the naive-LLM experiment (naive_llm_caruca/, tasks 016-022, its memory, the video project, the PaSh executions) out of caruca_v2 into a sibling folder ~/dev/stevens/naive_llm on a new private repo tirandagan/caruca-naive-llm; caruca_v2 keeps the LLM-as-pipeline-substitute work; plan = task 023, not yet executed
metadata:
  type: project
---

**Decision (Tiran, 2026-11-24).** Separate the naive-LLM experiment from `caruca_v2`:

- Everything about the naive Claude Code arm moves: code, runs, reports, scoring/comparison code and
  metrics, the PaSh executions (tasks 020-022 material), the Fig. 7 campaign, the addendum, diagrams,
  task documents 016-022, the naive memory notes, `videos/caruca-naive-run-1`, and a copy of all six
  `.claude/skills/`.
- Destination: a new folder at the same level as `caruca_v2` ("Naive LLM" → planned spelling
  `~/dev/stevens/naive_llm`, WSL `~/stevens/naive_llm`), connected to a new **private** GitHub repo
  "Caruca Naive LLM" (planned `tirandagan/caruca-naive-llm`).
- `caruca_v2` keeps: the execution, approach and methodology for using an LLM as a substitute for
  Caruca's pipeline (`src/caruca_v2`, harness, console, prep docs, paper refs, rebuild archive), so it
  can keep developing independently.

**Plan:** `ai_docs/tasks/023_separate_naive_llm_repo.md` (written 2026-11-24, revised the same day with
dependencies, risks and 12 decisions). Defaults: keep `naive_llm_caruca/` as a subfolder of the new repo
(zero path rewrites), extract history with `git filter-repo`, vendor the two v2 modules the task-018
scorer imports, new repo continues task numbering at 025 and caruca_v2 restarts at 101 (024 = the
converter's page-break marker, created 2026-11-24 while the plan was written; it is copied like 023),
leave a stub README in caruca_v2, invite nobody to the private repo yet, tag caruca_v2
`pre-naive-split` first.
**Status: plan only; nothing moved as of 2026-11-24.** Must wait for the Koala PaSh run and its Herdr
panes to finish (their cwd is caruca_v2).

**Facts established while planning (read from source, 2026-11-24):**
- `naive_llm_caruca/scoring/score_t018.py` imports `caruca_v2.v1` and `caruca_v2.harness.score.score_spec`
  from `caruca_v2/src` (the only naive script that depends on the v2 package); `quality.py`,
  `score_t018.py`, `score_pash.py` and `run_campaign.py` compute the repo root by walking up from their
  own file, and `run_campaign.py` reads `.env` from that root.
- The Lima VMs `pash` (read-only) and `caruca` (writable) mount the whole Mac home at `/Users/tirandagan`;
  `naive-golden` mounts nothing. The `pash` VM's `~/t024-check/check1.py` and `~/t024/out/manifest.json`
  carry the Mac path of caruca_v2 and go stale on a move.
- Nothing in `src/`, `tests/`, `console/src/`, `scripts/`, `prompts/` references `naive_llm_caruca`.
- The hand-built report's `build.ts` (runs/2026-11-24_pash_koala_naive_vs_pash/report/) imports fonts,
  colour tokens and the logo from `../../../../scripts/md-to-pdf/` (four levels up) and uses `puppeteer`
  and `pdf-lib` from the root `package.json`; the converter folder must be copied to the same place.
- `DESIGN.md` and `.impeccable/design.json` are read by the `impeccable` skill from the repo root
  (copied to both repos); `.impeccable/critique/` and `review/` are about the 2026-11-24 report (move).
- The Koala run's `full_run/occurrences.jsonl` (233 MB) is git-ignored since 2026-11-24 and tracked only
  as `.gz`; branch `backup-before-rewrite` holds the pre-rewrite history with the large blob and must be
  deleted before any clone that `git filter-repo` will process.

**Why:** the naive folder is 182 MB of the repo's tracked content and its concerns (runs, PaSh,
reports for the co-authors) have diverged from the pipeline rebuild; Tiran wants each to develop alone.

**How to apply:** until the move happens, keep working in `caruca_v2` as before. Once executed, this
note must be updated in both repos with the final paths, repo URL and commit hashes, and
[[dev_machine_paths]] and [[caruca_v2_project_overview]] updated too. Two different things are called
"naive": the Claude Code arm (moves) and the v2 pipeline's `naive-llm` syntax-spec stage option
(stays). Don't conflate them when moving files. See [[feedback_single_entry_point]] for why the naive
README is the start page.
