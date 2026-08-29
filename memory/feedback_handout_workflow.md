---
name: feedback-handout-workflow
description: "Tiran distributes supporting docs as PDFs alongside presentations — reference documents by name without file extensions, and ship an assembly list"
metadata:
  type: feedback
---

When producing a presentation or similar deliverable for Tiran:

1. **Reference source documents by name without the file extension.** Write `system_architecture`, not
   `system_architecture.md`. He converts the Markdown documents to PDF before distributing them, so an
   `.md` extension on a slide points at something the reader is not holding.
2. **Include a footnote on every slide that makes a claim**, naming which document it came from. Keep it
   small and unobtrusive.
3. **Ship an assembly document alongside the deck**, listing every document that needs converting to PDF
   and including in the handout package. For each: the file path, a one-line summary, which slides cite
   it, and whether a PDF already exists so it does not get converted twice.

**Why:** Tiran asked for this explicitly on 2026-08-29 while planning the advisor status deck. His
distribution pattern is a package: slides plus a set of PDF supporting documents. Footnotes only work as
navigation if the name on the slide matches the file the reader has in hand, and he needs a checklist so
assembling the package does not depend on remembering what was cited.

**How to apply:** applies to presentations and any other deliverable that cites project documents for an
outside audience. The first example is `ai_docs/docs/presentations/` — see `ASSEMBLY.md` there for the
established shape. Related: [[feedback-plain-language]] governs how the content itself is worded.
