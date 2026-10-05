---
name: project-v1-content-public-ok
description: "2026-09-23: v1-derived content in caruca_v2 may stay in the public repo; Tiran's call, supersedes CLAUDE.md's 'don't copy v1 source to a public location' for this repo"
metadata:
  type: project
---

`tirandagan/caruca_v2` is a **public** GitHub repository, and its committed evaluation record
contains v1-derived material verbatim:

- **135 run manifests** (`eval/runs/*/manifest.json`). The `prompt_user` field records the exact
  text sent to the model, which for stage 2 includes v1's syntax specification file in full
  (`cat_syntax_spec: list[SyntaxSpecification] = [Flag("-A", ...)]`) and for stage 1 includes the
  command's complete manual page.
- **9 comparison files** (`eval/parity_diffs/*.md`), which quote v1's source and output side by
  side. These carry their own header line saying "read locally, do not commit or share" — the
  header is now out of date, not a live instruction.
- Present since commit `eedd91a` ("added eval folder"), **2026-09-15**, and already pushed.

**Tiran's decision, 2026-09-23, asked directly and answered directly:** *"dont worry about
binpash/caruca - everything in our repo is for research purposes and should remain public."*

So: **do not** propose making the repo private, rewriting published history, scrubbing manifests,
or withholding a commit over this. Raising it again as a problem wastes his time.

**Why this needs writing down:** `CLAUDE.md` still says of upstream `binpash/caruca` — *"private,
unlicensed, and fork-restricted at the org level... Don't copy its source into a public location or
a personal fork"* — and `console/README.md` says run data "embeds v1's man pages and
specifications, which must not reach a public location." A session reading either will conclude
there is an active leak and stop work to escalate, which is what happened on 2026-09-23. Those
documents were written before the call; this memory is the later word.

**What still holds.** This is about *caruca_v2's own research record*, not a general licence to
redistribute v1:
- Don't push to `binpash/caruca` or open a fork of it. That repo is not ours.
- Don't lift v1's source into some *other* public place — a gist, a package, a blog post — just
  because it appears in this repo's evaluation artifacts.
- Keep the provenance visible. v1 material in this repo is evidence for a comparison, labelled as
  v1's, not presented as v2's own work.
- Prompts specifically were already cleared separately: see [[project-v1-prompt-licensing]]
  (Tiran owns those rights). This memory is broader and covers specs, man pages and traced output.

Related: [[caruca-v2-project-overview]] for what v1 and v2 are and where each lives.
