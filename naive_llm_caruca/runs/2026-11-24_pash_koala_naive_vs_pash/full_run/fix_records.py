#!/usr/bin/env python3
"""One-off repair of occurrences.jsonl written before two runner faults were fixed (2026-11-24, evening).
Runs in the VM on ~/t024/out (or a folder given as the first argument). Writes occurrences.fixed.jsonl and
fix_records_report.json; the original file is left in place.

1. Copies of a command use that shares its command and options with another use in the same part were
   split evenly by name ("by name only"). PaSh's parallel script, kept per part in regions.jsonl as
   worker_lines, tells them apart by their words. Where a use's words match worker lines exactly, its
   copies are set from them ("by command line (exact words)"), and split / why_not_split are recomputed
   with the runner's own rule. The old values are kept in copies_before_fix / split_before_fix.
2. Uses "outside every part" were matched to bash's starts by full command line. In loop parts the
   rebuilt line does not always carry the loop variables' values, so most did not match and were counted
   as outside (over a million rows). They are replaced by one row per command: starts under bash minus
   that command's uses in every execution of every part, as the fixed runner now does.
"""
import json
import shlex
import sys
from collections import Counter, defaultdict
from pathlib import Path

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "t024/out"
ALLOWED = "allowed by the files, not split by PaSh"
WHY = {"says no split": "file says no split", "no answer": "no answer", "raised": "raised", "no files": "no files",
       "allows only a split PaSh has not implemented": "file allows only a split PaSh has not implemented"}


def jl(p):
    with open(p) as f:
        for x in f:
            if x.strip():
                yield json.loads(x)


def run_key(r):
    return (r["id"], r["set"], r["mode"], r["repeat"], r.get("phase"))


def dequote(w):
    return w[1:-1] if len(w) >= 2 and w[0] == w[-1] == '"' else w


def file_answer_of(a):
    if a is None:
        return "no files"
    if a.get("exception"):
        return "raised"
    if a["parallelizability_outcome"] in ("no class", "not in name table") and \
            a["io_outcome"] in ("no class", "not in name table"):
        return "no files"
    if a["parallelizability_outcome"] != "answered":
        return "no answer"
    if not a["allows_split"]:
        return "says no split"
    if not any(x.get("implemented", True) for x in a["split_recipes"]):
        return "allows only a split PaSh has not implemented"
    return "allows a split"


results = list(jl(OUT / "results.jsonl"))
more = {run_key(r): r.get("more_starts_than_bash") for r in results}
bash_starts = {(r["id"], r.get("phase")): r["starts_per_command"] or {} for r in results
               if r["set"] == "bash" and r["mode"] == "instrumented"}
workers = {}
for r in jl(OUT / "regions.jsonl"):
    if r.get("worker_lines") is not None:
        workers[run_key(r) + (r["region"],)] = [(shlex.split(line), n) for line, n in r["worker_lines"]]

report = Counter()


def scripts():
    """The rows of one script at a time (the runner writes each script's rows together)."""
    cur, rows = None, []
    for u in jl(OUT / "occurrences.jsonl"):
        if u["id"] != cur and rows:
            yield cur, rows
            rows = []
        cur = u["id"]
        rows.append(u)
    if rows:
        yield cur, rows


seen_ids = set()
with open(OUT / "occurrences.fixed.jsonl", "w") as f:
    for sid, rows in scripts():
        ans, ans_src = defaultdict(Counter), {}
        ap = OUT / "answers" / (sid.replace("/", "_") + ".jsonl")
        if ap.exists():
            for a in jl(ap):
                if a.get("method") == "direct, quotes removed":
                    ans[(a["set"], a["command"])][file_answer_of(a)] += 1
                    ans_src[(a["set"], a["command"])] = (a.get("source"), a.get("files_from"))
        inside = defaultdict(Counter)
        kept = []
        for u in rows:
            if u["outside_pash"]:
                report["outside rows dropped"] += 1
                continue
            inside[run_key(u)][u["command"]] += u.get("executions", 1)
            if u.get("copies_attributed") == "by name only" and u.get("invocation"):
                wl = workers.get(run_key(u) + (u["region"],))
                if wl is not None:
                    argv = [dequote(w) for w in shlex.split(u["invocation"].replace("~", str(Path.home())))]
                    argv_h = [w.replace(str(Path.home()), "~") for w in argv]
                    exact = sum(n for w, n in wl if w == argv_h or w == argv)
                    if exact:
                        m = more.get(run_key(u))
                        split = exact >= 2 and (m is None or u["command"] in m)
                        u["copies_before_fix"], u["split_before_fix"] = u["copies"], u["split"]
                        u["copies"], u["copies_attributed"], u["split"] = exact, "by command line (exact words)", split
                        u["why_not_split"] = None if split else (
                            ALLOWED if u["file_answer"] == "allows a split" else WHY.get(u["file_answer"], u["why_not_split"]))
                        report["copies re-attributed by exact words"] += 1
                        if u["split_before_fix"] != split:
                            report["split changed by the re-attribution"] += 1
                    else:
                        report["by name only, no exact match (left)"] += 1
            kept.append(u)
        for u in kept:
            f.write(json.dumps(u, sort_keys=True) + "\n")
        for k, cmds in sorted(inside.items(), key=lambda x: str(x[0])):
            sid_, sname, mode, rep, phase = k
            starts = bash_starts.get((sid_, phase)) or bash_starts.get((sid_, "main")) or {}
            src_of = {u["command"]: (u["source"], u["source_detail"]) for u in kept if run_key(u) == k}
            for c, n in sorted(starts.items()):
                left = n - cmds.get(c, 0)
                if left <= 0:
                    continue
                src, detail = src_of.get(c) or ans_src.get((sname, c), (None, None))
                fa = ans.get((sname, c), Counter())
                f.write(json.dumps({"group": sid_.split("/")[0], "script": sid_.split("/", 1)[1].split("#")[0],
                                    "id": sid_, "set": sname, "mode": mode, "repeat": rep, "phase": phase,
                                    "region": None, "region_text_sha": None, "position": None, "command": c,
                                    "invocation": None, "exact_words": None, "answer_ref": None,
                                    "source": src, "source_detail": detail,
                                    "file_answer": fa.most_common(1)[0][0] if fa else None,
                                    "file_answers": dict(fa), "exception": None, "recipes": None, "copies": None,
                                    "copies_attributed": None, "split": None,
                                    "why_not_split": "started, but not a command use in any part sent to PaSh "
                                                     "(outside every part, or started by another program)",
                                    "outside_pash": True, "executions": left, "fixed": True}, sort_keys=True) + "\n")
                report["outside rows written (one per command)"] += 1
        print(sid, dict(report), flush=True)

(OUT / "fix_records_report.json").write_text(json.dumps(dict(report), indent=1))
print(json.dumps(dict(report), indent=1))
