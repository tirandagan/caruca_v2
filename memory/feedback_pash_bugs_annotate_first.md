---
name: feedback-pash-bugs-annotate-first
description: When a PaSh bug that looks fixable in a pull request turns up, write it up for Tiran's review first; no fix, no PR, no issue upstream until it has been discussed
metadata:
  type: feedback
---

**Rule (Tiran, 2026-11-19, said while task 022's PaSh runs were under way):** he has already seen PaSh
crash in our environment. When a run turns up a bug in PaSh (or in its annotation library) that could be
fixed with a pull request, **annotate it first so he can review it, then discuss.** Do not patch PaSh, do
not open a PR or an issue, and do not contact PaSh's authors before that discussion.

**Why:** his words were "annotate them first so that we can review them, and then we can discuss". My
reading of the reason (not stated by him): PaSh's authors overlap with Caruca's co-authors, so what goes
upstream and how it is worded is his call. It also fits the standing rule not to modify PaSh's source
([[pash-work-scheduling]]).

**How to apply:**
- Keep one review list: `naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/pash_runs/pash_bugs_for_review.md`
  (started 2026-11-19). Add new bugs there instead of scattering them across reports.
- Each entry: which repository (`binpash/pash` or `binpash/annotations`), file and line, a script that
  reproduces it, what happens, what should happen, a sketch of the fix, and how it was established (run,
  or read in source). Mark anything not reproduced as not confirmed.
- Separate a crash or wrong output from a missing feature that PaSh declines cleanly.
- Runs keep using private copies of the annotation package; PaSh's install stays untouched.

**What happened next (2026-11-20).** After the list was written and summarised to him, Tiran asked, in
two messages: "create a pr with the pash repo and be very clear when describing the reason and context
for the code fixes: what broke, why and how we are fixing it", and "also file an issues with the repo and
point to the PR". Done the same day: issue `binpash/pash#794` and pull request `binpash/pash#795` (one
line, the missing `Arg` import; fork `tirandagan/pash`, branch `fix-ir-arg-import`, clone on the Mac at
`~/dev/stevens/pash`). Only the one fault that was fixed and verified went up. The other entries stayed
in the review list.

- **What he wants in a PaSh pull request or issue (his words above):** what broke, why, and how it is
  fixed, stated very clearly.
- **My reading, not stated by him:** that go-ahead covered that one request. A new PaSh finding still
  goes into the review list first, and nothing more is sent upstream until he asks.
- **Practice that worked:** test on private copies in the VM (`~/pash-base` pristine, `~/pash-pr` with
  the fix), never on the install at `~/pash`; run PaSh's own test suite before and after; check whether
  a "one-line" fix un-hides a wrong answer before proposing it (the `OptionWithIOVar` one did).
- No AI-credit lines in the commit, the pull request or the issue ([[feedback-no-ai-credit]]). PaSh's
  guide asks for a signed-off commit (`git commit -s`).

Related: [[reference-pash-annotations-runtime]], [[feedback-never-modify-v1-source]].

**2026-11-24:** Tiran asked directly to file the operand-quoting issue (PaSh formats a quoted operand as `"…"` before annotation generators see it): filed as binpash/pash#796 with a repro, the code path and two suggested fixes. Listed in `orchestration/judgment_errors.md` of the 2026-11-24 run.
