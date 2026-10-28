---
name: caruca-v1-cross-platform-assets
description: v1 already holds BSD and busybox material (87 BSD man pages; 240-command busybox reference grammars, v1.30.1; notes on commands dropped as inexpressible) from mid-2024 — never used in the paper, whose cross-platform motivation is untested
metadata:
  type: reference
---

Found 2026-10-06 while answering what v1 is for. Verified on the Mac at v1 `d80324073`. None of this
appears in the paper's evaluation, and `ai_docs/archive_2026-09_rebuild/analysis/evaluation_gaps.md` gap 3 ("cross-platform
motivation untested") did not know it existed until a note was added that day.

- `benchmarks/bsd/man/`: 87 BSD man pages for coreutils-style commands (`grep`, `cp`, `rm`, `sort`,
  `tail`, `wc` and others), plus `download.sh`. Commits "Add bsd benchmark set" (2024-06-27) and "Move
  bsd benchmark" (2024-07-01). Example difference: BSD `grep.txt` has no `-P`/`--perl-regexp`, which
  GNU grep has.
- `benchmarks/busybox/`: `man/` (240), `ground-truth/` (240 JSON reference grammars, each stamped
  `"version": "Busybox v1.30.1"`), `commands.json`, `commands.txt`, `scrape.py`, and `removed/` (12 man
  pages: ash, cttyhack, dc, dd, fatattr, fsfreeze, grep, ip, kill, killall, losetup, sh). Its `README.md`
  names six commands removed because the grammar format cannot express their syntax unambiguously:
  `find` (actions), `ps` (`-o COL1,COL2=HEADER`), `su` (`-`, `-l`), `umount` (`-t` with an unspecified
  number of arguments), `sysctl` (`-p`), `md5sum` (`-c`). Last commits are 2024-04-06/07.

**Why:** the paper motivates automation partly with platform differences (Linux, macOS, BSD) but never
tests them. This material is the cheapest route to that test, and the busybox removals are concrete
evidence of what the grammar format cannot express.

**How to apply:** before proposing new BSD or busybox collection work, start from these. When
discussing the grammar format's limits, cite the six README removals. Note that `removed/` is a
different list of 12, so check which one is meant. Related: [[caruca-grep-grammar-single-shape]],
[[project-greenberg-caruca-purpose]].
