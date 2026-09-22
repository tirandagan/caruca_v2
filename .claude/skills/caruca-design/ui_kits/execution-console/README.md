# Execution Console mockup (downloaded source)

The source of the mockup deployed at `https://caruca.tirandagan.com/` (Vercel project
`caruca-v2-execution-console-84b2252e-e850-4b88-ba2e-cddd66ec4f70`). It was downloaded on
2026-09-22 from the public page, because the Vercel connector could not read the project (it
returned 404 and showed no deployments). The server reported
`last-modified: Sat, 12 Sep 2026 15:29:56 GMT` and `etag "c53e7393b4210860f8bf77f12db422d7"`.

**Every file here is a verbatim copy. None was written or edited by hand.** The page is a
Claude Design "bundled page": one HTML file that carries a manifest of embedded files (base64,
gzip-compressed where marked), a JSON page template, and the external scripts it vendored in.

| file | what it is | bytes | sha256 |
|---|---|---|---|
| `bundled-snapshot.html` | the page exactly as served | 463,784 | `de5afd0e53d76d4063bef47e5dd0fc0557c8e5c760e3be1a8d73d4caec2ceb74` |
| `template.html` | the page template, decoded from the `__bundler/template` script | 34,797 | `b244182312d98efe8c6641732c5eb4ef137d306b0d20d3095105d1683d0d20e5` |
| `page.dc.js` | the page definition: the `text/x-dc` script inside the template | 10,383 | `2df7ec7586170d9ade59192a5afda38def1bb71525e07d095f2c80e55321a5c7` |
| `props.json` | that script's declared settings (its `data-props` attribute, with HTML entities decoded) | 266 | `667b233ca5734317627e6c4492ffd3fae91cbe34bcd8edbd358f73b6cabee2a7` |

## What was not saved again, and why

These files are embedded in the page but byte-identical to copies the skill already has, so
they are not duplicated:

| embedded file (manifest id) | bytes | identical to |
|---|---|---|
| `a4b15187-da5e-460a-9a6b-a5dcf4466025` | 45,885 | `../../_ds_bundle.js` (the design-system bundle) |
| `e05412f0-ec94-4847-9f75-1f4893cf74b6` | 27,018 | `../../assets/logo.png` |
| `41f220f5-14a3-427b-a47b-9cb1aa7587f2` | 70,736 | `../../assets/fonts/LexendDeca-Regular.ttf` |
| `34255961-e0b2-4ae9-870b-8c1e0c8869f2` | 71,116 | `../../assets/fonts/LexendDeca-SemiBold.ttf` |
| `2d4044c5-3dbc-461f-804e-ef9773da8c87` | 70,988 | `../../assets/fonts/LexendDeca-Bold.ttf` |
| `bf6bd7ce-061f-4bd0-b398-38fa4ec2a5fc` | 92,164 | `../../assets/fonts/JetBrainsMono-Regular.woff2` |

Three embedded files have no copy in the skill. They survive only inside
`bundled-snapshot.html`:

- React 18.3.1 and ReactDOM 18.3.1, vendored from unpkg.
- The bundle's generic `dc-runtime` renderer (`60398939-2005-4396-86bc-9e0bc6d7aac5`,
  69,150 bytes).

## What is new compared with `../eval-console/`

Only the page definition. It composes the design-system bundle's screens into an *execution
console*:

- v1 and v2 run at the same time or one after the other (`defaultMode`)
- a stream-speed control (`streamSpeed`, 80 to 700 ms)
- a command picker
- each side's stage, step, tokens, cost and wall-clock
- a Runs table and a Report view

**Every number in it is scripted**, and several scripted details contradict the real pipeline.
Task `ai_docs/tasks/010_execution_console.md` builds the console for real, and its §8 lists
the details that must not be carried over.

## How to re-check these files

1. Download the page again. The live deployment may change later; these files are the
   2026-09-22 snapshot.
2. In the page, the `__bundler/manifest` script maps each id to base64 data, gzip-compressed
   wherever `compressed` is true.
3. The `__bundler/template` script holds the page's HTML as one JSON string.
4. The page definition is the `<script type="text/x-dc">` element inside that HTML.
5. Compare each result's sha256 with the tables above.
