---
name: design-authorities
description: "Where design truth lives for caruca_v2 — PRODUCT.md, the caruca-design skill, and the init decisions behind them"
metadata:
  type: reference
---

Two files govern any design or UI work in this repo. Read both before designing; don't re-derive either.

- **`PRODUCT.md`** (repo root) — durable product truth: users, purpose, positioning, operating context,
  capabilities/constraints, brand commitments, evidence on hand, and five product principles. Written by
  the `impeccable` skill's `init` flow on 2026-08-29. It deliberately contains **no** visual world,
  palette, typography, or surface strategy — those belong to the design system and to a future DESIGN.md.
- **`.claude/skills/caruca-design/`** — the binding visual authority (tokens, type, fonts, logo, UI kit,
  plus an `eval-console` kit). Tiran stated it "contains every aspect of our design guides." Its identity
  was extracted from this repo's own PDF pipeline (`scripts/md-to-pdf/`), so the shipped documents and any
  new UI are already one system.

**Three decisions settled during that init interview**, not derivable from the code:

1. **Stack for new UI: Next.js.** Chosen by Tiran over plain static HTML/CSS or React+Vite. The
   `scripts/md-to-pdf/` Node pipeline is unrelated and stays as it is. Left open: the Eval Console's PTY +
   websocket streaming needs a long-lived Node process that Next.js route handlers don't provide — custom
   server vs. sidecar service is undecided.
2. **All four surfaces are in scope**, not just one: the `caruca-v2` CLI, the Eval Console web app, a
   results/project site for advisors and co-authors, and the document/deck pipeline.
3. **Primary audience is Tiran operating the tooling**, not the reviewers. Design for dense telemetry,
   scanability, and repeated comparison runs first; advisors and co-authors are a secondary, read-only
   audience.

**Why:** future design sessions otherwise re-ask all three, or invent a visual direction that contradicts
the design system the PDFs and decks already ship.

**How to apply:** for new UI or a redesign, load `PRODUCT.md` and the `caruca-design` skill, then use
`impeccable`'s new-work flow to establish the surface. See [[component-functionality-spec]] for the Eval
Console's already-settled shape and [[feedback-handout-workflow]] for how documents ship to advisors.
