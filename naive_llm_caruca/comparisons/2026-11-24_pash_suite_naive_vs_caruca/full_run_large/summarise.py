#!/usr/bin/env python3
"""Adapted from ../full_run_caruca_all/summarise.py for the larger-input run (2026-11-27,
../orchestration/brief_large_inputs.md): one session, five or six sets, groups A and B counted separately,
time against PaSh's own and against Caruca per script and per group (geometric means), and the same times
with PaSh's start-up removed (the model of ../overhead_adjusted.py: 0.11 s + 6 ms per part compiled).

Counts only. Reads results.jsonl, regions.jsonl, occurrences.jsonl, scale.jsonl, ids_group_a.txt and
ids_group_b.txt in this folder; writes numbers.md. Stdlib only: python3 -I summarise.py

Timed rows are the `plain` pass (no stand-in programs); splitting and command-use rows are the
`instrumented` pass. A script counts once per source. Where a redo exists (phase "redo-..."), the earlier
rows of that script, pass and repeat are left out.
"""
import gzip
import json
import math
import statistics as S
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIX, PER = 0.11, 0.006  # ../overhead_adjusted.py
NAMES = {"bash": "Plain bash", "pash-own": "PaSh's own files", "naive-sed2": "Naive LLM (sed file v2)",
         "caruca-pash-all": "Caruca (PaSh grammars, as in its paper)",
         "caruca-main-all": "Caruca, full grammar where traced", "pash-own-copy": "PaSh's own files, second copy"}
NAIVE, CARUCA, REF = "naive-sed2", "caruca-pash-all", "pash-own"


def jl(name):
    p = HERE / name
    if not p.exists() and (HERE / (name + ".gz")).exists():
        with gzip.open(HERE / (name + ".gz"), "rt") as f:
            return [json.loads(x) for x in f if x.strip()]
    return [json.loads(x) for x in open(p) if x.strip()] if p.exists() else []


res, reg, occ = jl("results.jsonl"), jl("regions.jsonl"), jl("occurrences.jsonl")  # .gz read too
scale = {r["id"]: r for r in jl("scale.jsonl")}
GROUPS = {"A": (HERE / "ids_group_a.txt").read_text().split(), "B": (HERE / "ids_group_b.txt").read_text().split()}
REDONE = {(r["id"], r["mode"], r["repeat"]) for r in res if str(r.get("phase", "")).startswith("redo")}
SUPERSEDED = [r for r in res if not str(r.get("phase", "")).startswith("redo")
              and (r["id"], r["mode"], r["repeat"]) in REDONE]
res = [r for r in res if r not in SUPERSEDED]
sup_keys = {(r["id"], r["set"], r["mode"], r["repeat"]) for r in SUPERSEDED}
reg = [r for r in reg if not (str(r.get("phase", "")).startswith("redo") is False
                              and (r["id"], r["mode"], r["repeat"]) in REDONE)] if REDONE else reg
occ = [r for r in occ if not (str(r.get("phase", "")).startswith("redo") is False
                              and (r["id"], r["mode"], r["repeat"]) in REDONE)] if REDONE else occ
present = {r["set"] for r in res}
SETS = [s for s in [REF, NAIVE, CARUCA, "caruca-main-all"] if s in present]
ALL = SETS + (["pash-own-copy"] if "pash-own-copy" in present else [])

# output compared against bash's run of the same script, pass and repeat (hashes stored in each row)
bash_ref = {(r["id"], r["mode"], r["repeat"]): r for r in res if r["set"] == "bash"}
for r in res:
    b = bash_ref.get((r["id"], r["mode"], r["repeat"]))
    if r["set"] != "bash" and b is not None:
        r["same_as_bash"] = r["out_sha256"] == b["out_sha256"]
        r["output_files_same_as_bash"] = r["output_files_sha"] == b["output_files_sha"]

Tl = defaultdict(list)
for r in res:
    if r["mode"] == "plain":
        Tl[(r["id"], r["set"])].append(r)
T = {}
for k, rows in Tl.items():
    row = dict(rows[0])
    row["seconds"] = S.median(x["seconds"] for x in rows)
    row["seconds_all"] = [x["seconds"] for x in rows]
    row["same_as_bash"] = all(x["same_as_bash"] for x in rows)
    row["files_same"] = all(x.get("output_files_same_as_bash") for x in rows)
    row["n_same"] = sum(x["same_as_bash"] for x in rows)
    T[k] = row
I = {}
for r in res:
    if r["mode"] == "instrumented":
        I.setdefault((r["id"], r["set"]), r)
reps = Counter(len(v) for (i, s), v in Tl.items() if s != "bash")
errs = jl("batch_errors.jsonl")


def gm(xs):
    xs = [x for x in xs if x and x > 0]
    return math.exp(sum(map(math.log, xs)) / len(xs)) if xs else float("nan")


def adj(i, s):
    """seconds with PaSh's start-up removed (bash unchanged)."""
    t = T[(i, s)]["seconds"]
    if s == "bash":
        return t
    n = (I.get((i, s)) or {}).get("regions_sent") or T[(i, s)].get("regions_sent") or 0
    return max(t - (FIX + PER * n), 0.01)


def stops(i, s):
    """distinct parts where PaSh's compiler stopped (outcome "pash crash"), first execution of each."""
    first = {}
    for r in reg:
        if r["id"] == i and r["set"] == s and r["mode"] == "instrumented":
            first.setdefault(r["text_sha"], r["outcome"])
    return sum(1 for o in first.values() if o == "pash crash")


out = []
w = out.append
w("# Numbers for the larger-input run\n")
w("Built by `summarise.py` from the records in this folder. It only counts. Timed repeats per script and source: "
  + ", ".join(f"{k} repeat(s): {v}" for k, v in sorted(reps.items())) + ". Times are medians over the repeats. "
  f"Rows replaced by redone runs: {len(SUPERSEDED)}.\n")
if errs:
    w(f"Scripts the runner itself failed on: {len(errs)} ({', '.join(e['id'] for e in errs)}).\n")

w("## 0. Input size per script (bash-only pilot, `scale.jsonl`)\n")
w("| Group | Script | k | Input (MB) | Bash at k=10 (s) | Bash at k=30 (s) | Note |")
w("|---|---|---:|---:|---:|---:|---|")
for g, ids in GROUPS.items():
    for i in ids:
        r = scale.get(i, {})
        bs = r.get("bash_seconds", {})
        w(f"| {g} | {i} | {r.get('k', '-')} | {r.get('input_bytes', {}).get(str(r.get('k')), 0) / 1e6:.0f} | "
          f"{bs.get('10', '-')} | {bs.get('30', '-')} | {r.get('note', '') or ('bash at k=1: ' + str(bs.get('1')) + ' s' if '1' in bs else '')} |")

for g, ids0 in GROUPS.items():
    ids = [i for i in ids0 if (i, "bash") in T]
    w(f"\n# Group {g} ({len(ids)} of {len(ids0)} scripts with records)\n")

    w("## 1. Output, splits, compiler stops, files that raised\n")
    w("| Source | Output same as bash (timed, every repeat) | Same with stand-ins | Written files same as bash | "
      "Scripts with a part run in parallel | Parts run in parallel / sent (distinct) | Compiler stops (distinct parts) | "
      "Command uses whose files raised |")
    w("|---|---|---|---|---|---|---|---|")
    for s in ALL:
        rows = [T[(i, s)] for i in ids if (i, s) in T]
        ir = [I[(i, s)] for i in ids if (i, s) in I]
        dist_par = dist_all = 0
        for i in ids:
            first = {}
            for r in reg:
                if r["id"] == i and r["set"] == s and r["mode"] == "instrumented":
                    first.setdefault(r["text_sha"], r["outcome"])
            dist_all += len(first)
            dist_par += sum(1 for o in first.values() if o == "parallelized")
        raised = sum(1 for u in occ if u["set"] == s and u["id"] in ids and u["file_answer"] == "raised")
        st = sum(stops(i, s) for i in ids)
        if s == "pash-own-copy":
            w(f"| {NAMES[s]} | {sum(r['same_as_bash'] for r in rows)} of {len(rows)} | (timed only) | "
              f"{sum(r['files_same'] for r in rows)} of {len(rows)} | - | - | - | - |")
            continue
        w(f"| {NAMES[s]} | {sum(r['same_as_bash'] for r in rows)} of {len(rows)} | "
          f"{sum(r['same_as_bash'] for r in ir)} of {len(ir)} | {sum(r['files_same'] for r in rows)} of {len(rows)} | "
          f"{sum(1 for r in ir if r['state'] == 'split')} of {len(ir)} | {dist_par} / {dist_all} | {st} | {raised} |")
    wrong = [(i, s, T[(i, s)]["n_same"], len(T[(i, s)]["seconds_all"])) for i in ids for s in ALL
             if (i, s) in T and not T[(i, s)]["same_as_bash"]]
    w("\nWrong output (timed runs; repeats same as bash / repeats): " +
      (", ".join(f"{i} ({NAMES[s]}, {a}/{b})" for i, s, a, b in wrong) or "none") + ".\n")
    iw = [(i, s) for i in ids for s in SETS if (i, s) in I and not I[(i, s)]["same_as_bash"]]
    w("Wrong output with the stand-in programs: " + (", ".join(f"{i} ({NAMES[s]})" for i, s in iw) or "none") + ".\n")
    stl = [(i, s, stops(i, s)) for i in ids for s in SETS if stops(i, s)]
    w("Compiler stops per script: " + (", ".join(f"{i} ({NAMES[s]}: {n})" for i, s, n in stl) or "none") + ".\n")
    rz = sorted({(u["command"], u["set"], (u.get("exception") or "")[:100]) for u in occ
                 if u["id"] in ids and u["file_answer"] == "raised"})
    w("Files that raised: " + ("; ".join(f"{c} ({NAMES.get(s, s)}): {e}" for c, s, e in rz) or "none") + ".\n")

    w("## 2. Commands split, per script (runs with the stand-in programs)\n")
    w("| Script | " + " | ".join(NAMES[s] for s in SETS) + " |")
    w("|---" * (len(SETS) + 1) + "|")
    for i in ids:
        w(f"| {i} | " + " | ".join(", ".join((I.get((i, s)) or {}).get("split_commands") or []) or "-" for s in SETS) + " |")
    for s in [x for x in SETS if x != REF]:
        gn, ls = Counter(), Counter()
        for i in ids:
            if (i, s) in I and (i, REF) in I:
                a, o = set(I[(i, s)]["split_commands"] or []), set(I[(i, REF)]["split_commands"] or [])
                gn.update(a - o); ls.update(o - a)
        w(f"\n{NAMES[s]} against PaSh's own, per command (scripts gained / lost): " +
          (", ".join(f"`{c}` {gn[c]}/{ls[c]}" for c in sorted(set(gn) | set(ls))) or "no difference") + ".")
    if CARUCA in SETS:
        gn, ls = Counter(), Counter()
        for i in ids:
            if (i, NAIVE) in I and (i, CARUCA) in I:
                a, o = set(I[(i, NAIVE)]["split_commands"] or []), set(I[(i, CARUCA)]["split_commands"] or [])
                gn.update(a - o); ls.update(o - a)
        w(f"\nNaive LLM against Caruca, per command (scripts split by the naive LLM only / by Caruca only): " +
          (", ".join(f"`{c}` {gn[c]}/{ls[c]}" for c in sorted(set(gn) | set(ls))) or "no difference") + ".\n")

    w("## 3. Time\n")
    w("Speed-up = bash time / source time (above 1 = faster than bash). 'Against X' = source time / X's time "
      "(below 1 = faster than X). Geometric means over the group's scripts. 'Start-up removed': each PaSh time "
      f"minus {FIX} s and {PER * 1000:.0f} ms per part compiled; the cost of the split copies is kept.\n")
    w("| Source | Scripts | Speed-up over bash | Against PaSh's own | Against Caruca | Faster / slower than PaSh's own by >10% | "
      "Speed-up, start-up removed | Against PaSh's own, start-up removed |")
    w("|---|---|---|---|---|---|---|---|")
    for s in ALL:
        ii = [i for i in ids if all((i, x) in T for x in (s, "bash", REF))]
        vs = [T[(i, s)]["seconds"] / T[(i, REF)]["seconds"] for i in ii]
        vc = [T[(i, s)]["seconds"] / T[(i, CARUCA)]["seconds"] for i in ii if (i, CARUCA) in T]
        w(f"| {NAMES[s]} | {len(ii)} | {gm([T[(i, 'bash')]['seconds'] / T[(i, s)]['seconds'] for i in ii]):.2f}x | "
          f"{gm(vs):.2f} | {gm(vc):.2f} | {sum(v < 0.9 for v in vs)} / {sum(v > 1.1 for v in vs)} | "
          f"{gm([adj(i, 'bash') / adj(i, s) for i in ii]):.2f}x | {gm([adj(i, s) / adj(i, REF) for i in ii]):.2f} |")
    cp = [T[(i, "pash-own-copy")]["seconds"] / T[(i, REF)]["seconds"] for i in ids if (i, "pash-own-copy") in T]
    if cp:
        w(f"\nNoise: the second copy of PaSh's own files took {min(cp):.2f} to {max(cp):.2f} times as long as the first "
          f"(median {S.median(cp):.2f}; {sum(abs(x - 1) > 0.1 for x in cp)} of {len(cp)} scripts beyond 10%).\n")
    w("\n### Per script (median seconds; ratios: naive LLM / PaSh's own, naive LLM / Caruca)\n")
    w("| Script | k | bash | " + " | ".join(NAMES[s] for s in ALL) + " | Naive / PaSh's own | Naive / Caruca | "
      "Same, start-up removed: naive / PaSh's own | naive / Caruca |")
    w("|---|---:|---:" + "|---:" * (len(ALL) + 4) + "|")
    for i in ids:
        f = lambda s: f"{T[(i, s)]['seconds']:.2f}" + ("" if T[(i, s)]["same_as_bash"] else " ✗") if (i, s) in T else "-"
        rt = lambda a, b, fn: f"{fn(i, a) / fn(i, b):.2f}" if (i, a) in T and (i, b) in T else "-"
        sec = lambda i_, s: T[(i_, s)]["seconds"]
        w(f"| {i} | {scale.get(i, {}).get('k', '-')} | {f('bash')} | " + " | ".join(f(s) for s in ALL) +
          f" | {rt(NAIVE, REF, sec)} | {rt(NAIVE, CARUCA, sec)} | {rt(NAIVE, REF, adj)} | {rt(NAIVE, CARUCA, adj)} |")
    w("\n✗ = output differs from bash in at least one timed repeat.\n")

(HERE / "numbers.md").write_text("\n".join(out) + "\n")
print("\n".join(out))
