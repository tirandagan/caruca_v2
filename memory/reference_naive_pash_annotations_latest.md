---
name: reference_naive_pash_annotations_latest
description: One folder with the naive LLM's latest PaSh annotation files per command (84 commands), rebuilt by refresh.py, README links each command to its run
metadata:
  type: reference
---

`naive_llm_caruca/pash_annotations_latest/` (built 2026-11-24 at Tiran's request) holds, per command, byte copies
of the PaSh annotation files (`<cmd>.json`, `InputOutputInfoGenerator<Cmd>.py`,
`ParallelizabilityInfoGenerator<Cmd>.py`) from that command's **latest** run folder under
`naive_llm_caruca/runs/`. 84 commands from 101 run folders on that date. `README.md` there has one row per
command linking back to the run, its date, prompt version, cost, and a "Superseded runs" list.

**How to apply:** when a file for a command is needed, look here first instead of searching the run folders.
After any new naive run, re-run `python3 naive_llm_caruca/pash_annotations_latest/refresh.py`
(`--dry-run` to preview); it rebuilds the folder and README from the run folders and the campaign ledger.
Notes on reruns live in `RUN_NOTES` / `SUPERSEDED_WHY` at the top of the script. Two run layouts exist:
`output/pash/` (October pilot runs) and `output/annotation/` (campaign runs). Related:
[[project_fig7_campaign]], [[project_naive_claude_code_arm]].
