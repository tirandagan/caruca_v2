# Prompts

Every instruction caruca_v2 gives a model lives here as Markdown, loaded verbatim at runtime. Nothing is assembled from string literals in Python. Two reasons: the folder is readable as the complete instruction set for the system (it doubles as the paper's
appendix), and prompt text can be reviewed and diffed without reading code.

## Layout

One directory per pipeline stage, matching the stage modules in `src/caruca_v2/stages/`:

```
prompts/
├── README.md
├── syntax_spec/     # stage 1 — man page -> syntax specification   (task 001)
├── generate/        # stage 2 — syntax specification -> configs     (task 002)
├── trace/           # stage 3 — configs -> execution traces         (task 003)
└── annotate/        # stage 4+5 — traces -> annotation              (task 004)
```

Each stage directory holds `system.md` and `user.md`. `system.md` becomes the system message, `user.md` the single user message.

## Placeholders

Placeholders are `{{name}}`. Substitution is a plain, ordered string replacement with no expressions, no conditionals, and no escaping rules, so identical inputs always produce a byte-identical prompt. That determinism is what makes `prompt_hash` (SHA-256 of the assembled text, recorded in every telemetry record) meaningful as a reproducibility key.

A placeholder left unsubstituted is an error, not an empty string: `prompting.py` raises rather than sending a prompt with a literal `{{man_page}}` in it.

## What may and may not be committed here

These files contain **only text written for this project**. Content drawn from the caruca v1 checkout — man pages, committed syntax specs, data fixtures — is injected at runtime through placeholders and is never written into a file in this repository. v1 is private and unlicensed; keeping its text out of the repo is a licensing constraint, not a style preference.

## Changing a prompt

Prompt wording is a frozen experimental parameter once a stage's configuration selection is complete. Editing a committed prompt after that point invalidates comparability with every run already recorded, because the `prompt_hash` changes. Treat an edit as a new experimental condition and say so in the write-up.
