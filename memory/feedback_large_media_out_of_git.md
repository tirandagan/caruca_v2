---
name: feedback-large-media-out-of-git
description: Large media (recordings, renders) never go into the repo; they live in ~/Documents and the project links to them
metadata:
  type: feedback
---

Keep very large files (screen recordings, rendered videos, anything near GitHub's 100 MB limit) out of git.
Source recordings and rendered videos live in `~/Documents` (where Tiran puts the source video and SRT);
a HyperFrames project under `videos/` references the recording through a symlink that `.gitignore` excludes
(`videos/*/assets/walkthrough.mp4`, `videos/**/*.mp4`, `videos/*/.hyperframes/`, `videos/*/renders/`).

**Why:** on 2026-10-13 `git push origin main` was rejected because `videos/caruca-naive-run-1/assets/walkthrough.mp4`
(169 MB) was in an unpushed commit. Fixed by replacing it with a symlink and amending that one unpushed commit.

**How to apply:** when staging media into a repo project, symlink or copy it to `~/Documents` instead, render with
`-o ~/Documents/...`, and check `git ls-tree -r -l HEAD` for files over ~50 MB before telling Tiran a commit is pushable.
Related: [[project-caruca-youtube-video]].

**Addition 2026-11-24:** the PaSh-suite run's `full_run/occurrences.jsonl` (one row per command use per
run) reached 120 MB and blocked a push (GitHub's 100 MB hard limit). It is now git-ignored
(`naive_llm_caruca/runs/*/full_run/occurrences.jsonl`) and tracked only as `occurrences.jsonl.gz`
(1.5 MB); regenerate the .gz before each commit of the records. Two unpushed commits were rewritten to
carry the .gz (backup of the old history: branch `backup-before-rewrite`, delete after the push).
Check `git ls-tree -r -l HEAD | awk '$4 > 50000000'` before telling Tiran a commit is pushable.
