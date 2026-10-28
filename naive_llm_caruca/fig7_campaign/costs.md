# Task 019: cost of every run, and of the campaign

Rewritten after every run by `run_campaign.py` (2026-10-27 22:58). Budget: target $120, ceiling $150. **Billed** is OpenRouter's own usage counter for the key, read before and after each session; *Claude Code's figure* is the session's own estimate, kept for comparison with runs 3 to 10. Times are the session's wall clock.

| # | Command | Group | Run | Status | Estimate | **Billed** | Claude Code's figure | Input / output / cache read / cache write tokens | Wall time | Turns |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `dd` | B | 1 | ok | $1.42 | **$2.11** | $2.80 | 40 / 1,146 / 920,525 / 63,626 | 296 s | 20 |

| Total | Money |
|---|---|
| Agent sessions (1 runs) | **$2.11** |
| Caruca's model step (77 commands) | $1.65 |
| Smoke test | $0.30 |
| Charges billed but not recorded by a run (Caruca's model step, convert: the GPT-4o call was billed but) | $0.18 |
| **All billed** (sum of the rows above) | **$4.24** |
| OpenRouter's counter since the campaign began | $4.29 |
| Left before the $150 ceiling | $145.71 |
| Projected total for the 79 commands (actual/estimate so far: 1.48; 78 not yet run) | $186.72 |
