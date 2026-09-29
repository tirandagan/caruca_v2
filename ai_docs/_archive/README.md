# Archive

Nothing in this folder is part of caruca_v2's development, documentation or presentation. It is
kept, rather than deleted, for two reasons: the licence terms in
[`LICENSE-TEMPLATES.md`](../../LICENSE-TEMPLATES.md) cover this material and require its
attribution notices to stay intact, and the provenance matters if anyone asks where the
repository's scaffolding came from.

**Do not read anything here for guidance on this project.** If a document here contradicts one
outside the archive, the one outside is right.

## `shipkit/` — the starter-kit residue (archived 22 September 2026)

caruca_v2 began from **ShipKit**, a Next.js / Drizzle / Trigger.dev web-application starter kit.
Five of its planning templates were adapted and used; everything else described a product this
project is not building, and was cluttering the folders and the slash-command list.

| Folder | Files | What it was |
|---|---|---|
| `dev_templates/` | 17 | Drizzle migrations and rollbacks, Next.js refactors, Trigger.dev orchestration, Stripe/auth setup, landing pages, UI work, git and PR workflows. Only `task_template.md` was kept, in place, because the `task-creator` skill builds task documents from it |
| `prep_templates/` | 6 | The planning passes that never applied: app naming (no product needing a market name), UI theme and wireframe (no interface at the time), logo generation, Trigger.dev workflows, and the theme HTML. Passes 01, 05, 08, 09 and 10 were adapted, used, and stay in place as the provenance for the five design documents in `ai_docs/prep/` |
| `claude_commands/` | 22 | The slash commands wrapping the above. Removing them leaves seven commands that are all about this project |
| `claude_agents/` | 3 | Subagents for Drizzle, TypeScript/React and Trigger.dev |

**If you need one back**, move the file to its original folder — `ai_docs/dev_templates/`,
`ai_docs/prep_templates/`, `.claude/commands/` or `.claude/agents/` — and it works again. Nothing
was edited on the way in.

## What was *not* archived, and why

- **`ai_docs/prep_templates/` 01, 05, 08, 09, 10** — adapted by Tiran and already run; they are how
  the five design documents in `ai_docs/prep/` were produced.
- **`ai_docs/dev_templates/task_template.md`** — live, used by the `task-creator` skill.
- **`.claude/skills/`** — `caruca-design`, `diagram` and `task-creator` are Tiran's own;
  `impeccable` is third-party and excluded from the repository licence.
- **Superseded handout PDFs** — those live in
  [`../docs/presentations/archive/`](../docs/presentations/archive/), not here, because they are
  this project's own output rather than starter-kit material.
