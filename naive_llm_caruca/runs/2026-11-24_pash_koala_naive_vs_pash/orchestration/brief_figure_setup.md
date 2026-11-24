# Brief: one diagram of how the experiment was set up

You are a worker. An orchestrating Claude session gave you this brief. Work only on it. Run nothing in
the Lima VM `pash`.

## Goal

Appendix A5 of `report_draft.md` (this folder's parent) explains the experiment in plain words for a
reader new to PaSh. Draw **one** diagram that shows it at a glance, for that appendix. Read A5 first, and
`orchestration/report_plan.md` section 2 for the colours (PaSh's own files dark grey, naive LLM blue,
Caruca orange).

What it must show, left to right: one benchmark script → run under plain bash (reference output and
time) and under PaSh four times, each time with a different folder of annotation files handed to PaSh →
each folder is PaSh's own package with one source's files swapped in for the commands that source has
(PaSh's own files kept for the rest) → the three things recorded per run (output compared with bash;
which commands PaSh split; seconds). Keep it to about a dozen boxes; plain labels, no file names or
option names; readable at portrait page width.

Use the `excalidraw-diagram` skill (the renderer needs the esm.sh import pinned to
`@excalidraw/excalidraw@0.18.0`; see `memory/reference_excalidraw_diagram_skill.md`) and export
`figures_interim/setup_diagram.png` at 300 dpi; if the renderer fails, draw it with matplotlib instead.
Also write `figures_interim/setup_caption.md`: a two-sentence caption.

Do not edit the report. Do not commit. Reply with the file path and what you used to draw it.
