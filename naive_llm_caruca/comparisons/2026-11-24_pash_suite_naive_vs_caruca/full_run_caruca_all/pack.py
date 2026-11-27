#!/usr/bin/env python3
"""Runs in the pash VM after the batch. Packs the records for the repo the way ../full_run/ was packed:
answers per script with the direct answers grouped (lines with the same answer, count + one example; rows
"as PaSh passes them" kept whole, as the first run's collapse_answers.py did), and PaSh's logs cut to their
first 2,000 and last 500 lines. Full files stay in the VM under ~/t024/out_caruca_all/."""
import collections, gzip, json, os
from pathlib import Path
OUT = Path(os.environ.get("T024_OUT", Path.home() / "t024/out_caruca_all"))
P = OUT / "pack"
(P / "answers").mkdir(parents=True, exist_ok=True); (P / "logs").mkdir(exist_ok=True)
for f in sorted((OUT / "answers").glob("*.jsonl")):
    groups, out = collections.OrderedDict(), []
    for l in open(f):
        if not l.strip():
            continue
        r = json.loads(l)
        if r.get("method") != "direct, quotes removed":
            out.append(r); continue
        key = (r["set"], r["command"], r["source"], r["io_outcome"], r["parallelizability_outcome"], r["allows_split"],
               json.dumps(r["split_recipes"], sort_keys=True), r["exception"])
        g = groups.get(key)
        if g is None:
            g = dict(r); g["lines"] = 0; g["example_invocation"] = r["invocation"]
            for x in ("invocation", "line", "position"):
                g.pop(x, None)
            g["method"] = "direct, quotes removed (grouped: lines with the same answer)"
            groups[key] = g
        g["lines"] += 1
    with gzip.open(P / "answers" / (f.name + ".gz"), "wt") as o:
        for r in list(groups.values()) + out:
            o.write(json.dumps(r, sort_keys=True) + "\n")
for f in sorted((OUT / "logs").glob("*.log.gz")):
    with gzip.open(f, "rt", errors="replace") as i:
        lines = i.readlines()
    if len(lines) > 2500:
        lines = lines[:2000] + [f"... [{len(lines) - 2500} lines cut] ...\n"] + lines[-500:]
    with gzip.open(P / "logs" / f.name, "wt") as o:
        o.writelines(lines)
for name in ("results.jsonl", "regions.jsonl", "occurrences.jsonl", "commands.jsonl"):
    with open(OUT / name, "rb") as i, gzip.open(P / (name + ".gz"), "wb") as o:
        o.write(i.read())
print("packed")
