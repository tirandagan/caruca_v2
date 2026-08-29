repo: tirandagan/caruca_v2
branch: main

## Last sync
date: 2026-08-29T21:00:36Z
### Updated in this project
- Extracted brand tokens (colors, type scale) from scripts/md-to-pdf/styles.ts + cover.ts
- Copied Lexend Deca + JetBrains Mono webfonts into assets/fonts/
- Decoded the Caruca logo from scripts/md-to-pdf/assets/logo-base64.ts → assets/logo.png
- Read prep/memory docs for product context (master_idea, component_functionality)

## Screen map
| Project file | Repo source |
| --- | --- |
| tokens/*.css, assets/fonts.css | scripts/md-to-pdf/styles.ts, scripts/md-to-pdf/cover.ts |
| assets/logo.png | scripts/md-to-pdf/assets/logo-base64.ts |
| assets/fonts/* | scripts/md-to-pdf/fonts/* |
| ui_kits/eval-console/* | ai_docs/prep/component_functionality.md (Web GUI spec), memory/component_functionality_spec.md |
| readme.md | ai_docs/prep/master_idea.md, memory/*.md |
