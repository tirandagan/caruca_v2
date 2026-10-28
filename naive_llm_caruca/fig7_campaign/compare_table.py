#!/usr/bin/env python3
"""Task 019: the agent's runs next to Caruca's figures, one row per finished command, in Fig. 7's order.

    python3 naive_llm_caruca/fig7_campaign/compare_table.py      # writes interim_comparison.md beside this file

Agent (main arm, first repeat): OpenRouter's bill, wall time, program runs and refused share from ledger.jsonl.
Caruca: its GPT-4o model step's bill (caruca_side/v1_llm_ledger.jsonl), the Fig. 7 time (measured up to 4
options for group A, the paper's projection for group B), test runs at up to 4 options per line
(caruca_side/counts.tsv) and the refused share of its test runs at 2 options per line, weighted as v1 runs them
(caruca_side/refused/<cmd>.json). Refused shares on both sides are provisional until the rule table for
unclassified messages is written.
"""
import csv, json, statistics
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIDE = HERE / "caruca_side"


def rows(path):
    return list(csv.DictReader((l for l in open(path) if not l.startswith("#")), delimiter="\t"))


def human(s):
    if s < 120:
        return f"{s:.0f} s"
    if s < 7200:
        return f"{s / 60:.0f} min"
    if s < 172800:
        return f"{s / 3600:.1f} h"
    return f"{s / 86400:.1f} days"


def pct(x):
    return "n/a" if x is None else f"{100 * x:.1f}%"


def main():
    fig7 = rows(SIDE / "fig7_values.tsv")
    runs4 = {r["command"]: int(r["traced_configurations"]) for r in rows(SIDE / "counts.tsv") if r["k"] == "4"}
    step = {}
    for l in open(SIDE / "v1_llm_ledger.jsonl"):
        d = json.loads(l)
        if d["exit"] == 0 and d["calls"] and all(x.get("status") == 200 for x in d["call_records"]):
            step[d["command"]] = d["billed_usd"]
    agent, late, note = {}, None, {}
    for l in open(HERE / "ledger.jsonl"):
        d = json.loads(l)
        if d.get("arm", "main") == "main" and d.get("repeat", 1) == 1 and d.get("status") == "ok":
            agent[d["command"]] = d
            # OpenRouter's counter can lag past the runner's wait: a run then reads $0 and the next run's
            # figure holds both (uname and id, 2026-10-28); the pair's total is right, the split is not known
            if late:
                note[late], note[d["command"]] = f"in `{d['command']}`'s", f"incl. `{late}`"
                late = None
            if d["billed_usd"] == 0:
                late = d["command"]
    out, tot = [], dict(a_usd=0.0, a_s=0.0, a_runs=0, c_usd=0.0, c_runs=0)
    ratios = []
    for f in fig7:
        c = f["command"]
        if c not in agent:
            continue
        a = agent[c]
        t = a.get("tries") or {}
        cl = t.get("classes") or {}
        a_ref = cl.get("refused", 0) / t["tries"] if t.get("tries") else None
        rp = SIDE / "refused" / f"{c}.json"
        c_ref = json.loads(rp.read_text()).get("k2", {}).get("refused_share_as_v1_runs") if rp.is_file() else None
        if f["group"] == "A":
            f7 = human(float(f["real4_s"]))
        else:
            f7 = human(float(f["proj4_s"])) + " (projected)"
        f7s = float(f["real4_s"] or f["proj4_s"])
        ratios.append(f7s / a["wall_s"])
        tot["a_usd"] += a["billed_usd"]; tot["a_s"] += a["wall_s"]; tot["a_runs"] += t.get("tries") or 0
        tot["c_usd"] += step.get(c, 0); tot["c_runs"] += runs4.get(c, 0)
        bill = f"${a['billed_usd']:.2f}" + (f" ({note[c]})" if c in note else "")
        out.append(f"| `{c}` | {bill} | {human(a['wall_s'])} | {t.get('tries', 0):,} | {pct(a_ref)} | "
                   f"{'$%.3f' % step[c] if c in step else 'no manual'} | {f7} | {runs4.get(c, 0):,} | {pct(c_ref)} |")
    head = [f"# Task 019: agent vs Caruca, commands finished so far ({len(out)} of 79)", "",
            f"Made {datetime.now():%Y-%m-%d %H:%M} by `compare_table.py`. Agent = Claude Code, Fable 5.1 at medium "
            "effort, one run per command. Refused shares on both sides are provisional (messages not yet classed "
            "are left out).", "",
            "| Command | Agent: billed | Agent: wall time | Agent: program runs | Agent: refused share | "
            "Caruca: GPT-4o step billed | Caruca: Fig. 7 time | Caruca: test runs (up to 4 options) | "
            "Caruca: refused share (2 options) |",
            "|---|---|---|---|---|---|---|---|---|"]
    foot = ["", f"**Totals:** agent ${tot['a_usd']:.2f}, {human(tot['a_s'])} of wall time, {tot['a_runs']:,} program "
            f"runs; Caruca's model step ${tot['c_usd']:.2f}, {tot['c_runs']:,} test runs. Fig. 7 time divided by the "
            f"agent's wall time: median {statistics.median(ratios):.0f}x (range {min(ratios):.1f}x to "
            f"{max(ratios):,.0f}x).", "",
            "`cp` and `diff`: Caruca's current syntax files would make 308 million and 2.4 billion test runs at up "
            "to 4 options, which cannot fit the paper's measured 2.7 h and 3.3 h (crosscheck.txt); the paper must "
            "have run other syntax files or settings for these two.", ""]
    text = "\n".join(head + out + foot)
    (HERE / "interim_comparison.md").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
