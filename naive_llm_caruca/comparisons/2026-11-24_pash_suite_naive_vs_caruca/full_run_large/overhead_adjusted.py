"""Copy of ../overhead_adjusted.py for the larger-input run (2026-11-27): the model is fitted on the
first run as before (../full_run/), then applied to this folder's records, per group (A, B). Paths changed only.

Estimate PaSh's own overhead (start-up + per-part compile) and each source's time without it.

Model, fitted on the 44 first-run scripts where PaSh's own files split nothing (so PaSh time - bash time is pure
overhead): about 0.11 s per script (median over scripts with at most 2 parts compiled) plus about 6 ms per part
PaSh is asked to compile (loop scripts send it 3,000 to 9,000 parts). The cost of running split copies is NOT
removed: it is the price of a split decision. Writes overhead_adjusted.md. Stdlib only:  python3 -I overhead_adjusted.py
"""
import gzip, json, math, statistics as S, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
FIX, PER = 0.11, 0.006

def load(p):
    p = Path(p)
    op = gzip.open if p.suffix == ".gz" else open
    return [json.loads(l) for l in op(p, "rt") if l.strip()]

def fit(rows):
    plain = [x for x in rows if x.get("mode") == "plain" and x.get("phase") in PHASES]
    b = collections.defaultdict(list); o = collections.defaultdict(list); reg = {}
    for x in plain:
        k = x["group"] + "/" + x["script"]
        if x["set"] == "bash": b[k].append(x["seconds"])
        if x["set"] == "pash-own" and x.get("regions_sent") is not None:
            o[k].append(x["seconds"]); reg[k] = (x["regions_sent"], x["regions_parallel"])
    pts = [(reg[k][0], S.median(o[k]) - S.median(b[k])) for k in o if k in b and reg[k][1] == 0]
    small = [y for x, y in pts if x <= 2]
    loops = [(y / x) for x, y in pts if x >= 1000]
    return len(pts), S.median(small), S.median(loops)

def table(rows, sets, ids=None):
    plain = [x for x in rows if x.get("mode") == "plain" and x.get("phase") in PHASES]
    t = collections.defaultdict(list); rs = {}
    for x in plain:
        if ids is not None and x["id"] not in ids: continue
        k = (x["set"], x["group"] + "/" + x["script"]); t[k].append(x["seconds"])
        if x.get("regions_sent") is not None: rs[k] = x["regions_sent"]
    med = {k: S.median(v) for k, v in t.items()}
    g = lambda xs: math.exp(sum(map(math.log, xs)) / len(xs)) if xs else float("nan")
    out = {}
    for s in sets:
        raw, adj, one = [], [], []
        for (ss, sc), v in med.items():
            b = med.get(("bash", sc)); n = rs.get((ss, sc))
            if ss != s or not b or b <= 0.05 or n is None: continue
            a = max(v - (FIX + PER * n), 0.01)
            raw.append(v / b); adj.append(a / b)
            if n <= 3 and b >= 1.0: one.append(a / b)
        out[s] = (len(raw), g(raw), g(adj), len(one), g(one))
    return out

PHASES = {"main"}
r1 = load(PARENT / "full_run/results.jsonl.gz")
n, fixed, per = fit(r1)
PHASES = {"groupA", "groupB"} | {p for p in {x.get("phase") for x in load(HERE / "results.jsonl")} if str(p).startswith("redo")}
r = load(HERE / "results.jsonl")
redone = {(x["id"], x["mode"], x["repeat"]) for x in r if str(x.get("phase", "")).startswith("redo")}
r = [x for x in r if str(x.get("phase", "")).startswith("redo") or (x["id"], x["mode"], x["repeat"]) not in redone]
SETS = [s for s in ["pash-own", "naive-sed2", "caruca-pash-all", "caruca-main-all", "pash-own-copy"] if any(x["set"] == s for x in r)]
rows = {}
for g in ("a", "b"):
    ids = set((HERE / f"ids_group_{g}.txt").read_text().split())
    rows.update({(f"group {g.upper()}: " + k): v for k, v in table(r, SETS, ids).items()})
lines = ["# PaSh's overhead and time without it", "",
         f"Fitted on {n} first-run scripts where PaSh's own files split nothing: start-up about {fixed:.2f} s per script "
         f"(median, scripts with at most 2 parts compiled); about {per*1000:.1f} ms per part compiled (median over scripts "
         f"with 1,000 or more parts). Used: {FIX} s + {PER*1000:.0f} ms per part. Split copies' cost is not removed.", "",
         "Scripts: those with bash median over 0.05 s. One-pass: at most 3 parts compiled and bash at least 1 s.", "",
         "| Set (run) | Scripts | Time / bash, measured | Time / bash, overhead removed | One-pass scripts | Their time / bash, overhead removed |",
         "|---|---:|---:|---:|---:|---:|"]
for k, (a, b_, c, d, e) in rows.items():
    lines.append(f"| {k} | {a} | {b_:.2f} | {c:.2f} | {d} | {e:.2f} |")
(HERE / "overhead_adjusted.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
