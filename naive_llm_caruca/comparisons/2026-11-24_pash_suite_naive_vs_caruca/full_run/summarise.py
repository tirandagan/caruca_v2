#!/usr/bin/env python3
"""Counts only. Reads results.jsonl, regions.jsonl, occurrences.jsonl in this folder; writes numbers.md.

Timed rows are the `plain` pass (no stand-in programs). Splitting and command-use rows are the
`instrumented` pass. A script counts once per source.
"""
import json
import math
import statistics as S
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SETS = ["pash-own", "naive", "naive-sed2", "caruca-pash", "caruca-main"]
NAMES = {"bash": "Plain bash", "pash-own": "PaSh's own files", "naive": "Naive LLM's files",
         "caruca-pash": "Caruca's files, PaSh grammar", "caruca-main": "Caruca's files, main grammar",
         "pash-own-copy": "PaSh's own files, second copy", "naive-sed2": "Naive LLM, sed file v2"}


def jl(name):
    import gzip
    p = HERE / name
    if not p.exists() and (HERE / (name + ".gz")).exists():
        with gzip.open(HERE / (name + ".gz"), "rt") as f:
            return [json.loads(x) for x in f if x.strip()]
    return [json.loads(x) for x in open(p) if x.strip()] if p.exists() else []


# step4_results.jsonl is the newest copy of the whole results file (it includes every earlier row)
res = jl("step4_results.jsonl") or jl("results.jsonl")
reg, occ = jl("regions.jsonl"), jl("occurrences.jsonl")

# Fix-up 1 (recorder fault found 2026-11-24 23:40): in the repeats phase the runner rotated bash out of
# first place, so a source that ran before bash in its repeat had no reference and was recorded as "not
# same as bash". The records are not edited; the comparison is redone here from the stored hashes, against
# bash's run of the same script, phase, pass and repeat.
bash_ref = {(r["id"], r.get("phase"), r["mode"], r["repeat"]): r for r in res if r["set"] == "bash"}
FIX1 = Counter()
for r in res:
    if r["set"] == "bash":
        continue
    b = bash_ref.get((r["id"], r.get("phase"), r["mode"], r["repeat"]))
    if b is None:
        continue
    before = (r["same_as_bash"], r.get("output_files_same_as_bash"))
    r["same_as_bash"] = r["out_sha256"] == b["out_sha256"]
    if r.get("output_files_sha") and b.get("output_files_sha"):
        r["output_files_same_as_bash"] = r["output_files_sha"] == b["output_files_sha"]
    elif r.get("output_files") == 0 and b.get("output_files") == 0:
        r["output_files_same_as_bash"] = True
    elif r.get("order") and "bash" in r["order"] and r["order"].index("bash") > r["order"].index(r["set"]):
        r["output_files_same_as_bash"] = None  # no reference was recorded and the files' hashes were not kept
    FIX1["rows compared again"] += 1
    if before[0] != r["same_as_bash"]:
        FIX1["same as bash: changed"] += 1
    if before[1] != r["output_files_same_as_bash"]:
        FIX1["output files same as bash: changed"] += 1

# Fix-up 2 (found 2026-11-24 23:40): web-search's launcher puts node at $TOP/.tools, which the shadow copy
# did not have, so its timed runs (no stand-in programs, which had supplied node) stopped early with
# "node: No such file or directory". Those rows are left out of times and output counts.
BROKEN = [r for r in res if r["mode"] == "plain" and r["id"] == "web-search/engine"
          and "node" in (r.get("stderr") or "") and "No such file" in (r.get("stderr") or "")]
res = [r for r in res if r not in BROKEN]

# Redos (phases redo-r1, redo-r3): web-search's timed runs of repeat 1 (no node) and repeat 3 (Mac on
# battery and asleep) were run again on mains power. Where a redo exists for a script, pass and repeat, the
# earlier rows of that script, pass and repeat are left out.
REDONE = {(r["id"], r["mode"], r["repeat"]) for r in res if str(r.get("phase", "")).startswith("redo")}
SUPERSEDED = [r for r in res if not str(r.get("phase", "")).startswith("redo")
              and (r["id"], r["mode"], r["repeat"]) in REDONE]
res = [r for r in res if r not in SUPERSEDED]
errs = jl("batch_errors.jsonl")
ids = sorted({r["id"] for r in res})
# Timed runs: every repeat of a source and script; bash's reference time is the median of its repeats too.
# `T` holds one row per script and source, its seconds replaced by the median over repeats, its output
# "same as bash" only if every repeat was. `I` holds the first run with the stand-in programs.
Tl = defaultdict(list)
for r in res:
    if r["mode"] == "plain" and not (r["set"] == "bash" and r.get("phase") not in (None, "main", "repeats", "redo-r1", "redo-r3")):
        Tl[(r["id"], r["set"])].append(r)
T = {}
for k, rows in Tl.items():
    row = dict(rows[0])
    row["seconds"] = S.median(x["seconds"] for x in rows)
    row["seconds_all"] = [x["seconds"] for x in rows]
    row["same_as_bash"] = all(x["same_as_bash"] for x in rows)
    row["matches_koala_hash"] = None if rows[0]["matches_koala_hash"] is None else all(x["matches_koala_hash"] for x in rows)
    T[k] = row
I = {}
for r in res:
    if r["mode"] == "instrumented":
        I.setdefault((r["id"], r["set"]), r)
reps = Counter(len(v) for (i, s), v in Tl.items() if s != "bash")
out = []
w = out.append

w(f"# Numbers for the run ({len(ids)} scripts)\n")
w("Fix-ups applied when counting (records unchanged): output compared again against the same repeat's bash: "
  + ", ".join(f"{k} {v}" for k, v in FIX1.items()) + f". Timed runs left out because node was missing: {len(BROKEN)}. "
  f"Rows replaced by redone runs: {len(SUPERSEDED)}.\n")
w("Built by `summarise.py` from the records in this folder. It only counts.\n")
w("Timed repeats per script and source: " + ", ".join(f"{k} repeat(s): {v}" for k, v in sorted(reps.items())) +
  ". Times are medians over the repeats. The naive LLM's second sed file was run on the 12 oneliners and unixfun scripts that use sed and on all 40 scripts of the other groups (52; in 27 of them bash starts no sed), so its time ratios cover a different set of scripts from the other sources' 86.\n")
if errs:
    w(f"Scripts the runner itself failed on: {len(errs)} ({', '.join(e['id'] for e in errs)}).\n")

# 1. outputs and what PaSh did, per source
w("## 1. Output and what PaSh did, per source (timed runs)\n")
w("| Source | Scripts | Output same as bash | Same as Koala's stored answer (of scripts with one) | "
  "PaSh ran at least one part in parallel | Fell back to plain bash | Other state |")
w("|---|---|---|---|---|---|---|")
for s in SETS + ["pash-own-copy"]:
    rows = [T[(i, s)] for i in ids if (i, s) in T]
    same = sum(r["same_as_bash"] for r in rows)
    kh = [r for r in rows if r["matches_koala_hash"] is not None]
    st = Counter(r["state"] for r in rows)
    other = {k: v for k, v in st.items() if k not in ("split", "fell back to bash")}
    w(f"| {NAMES[s]} | {len(rows)} | {same} of {len(rows)} | {sum(r['matches_koala_hash'] for r in kh)} of {len(kh)} | "
      f"{st.get('split', 0)} of {len(rows)} | {st.get('fell back to bash', 0)} of {len(rows)} | "
      f"{', '.join(f'{k}: {v}' for k, v in sorted(other.items())) or '-'} |")
b = [T[(i, "bash")] for i in ids if (i, "bash") in T]
kb = [r for r in b if r["matches_koala_hash"] is not None]
w(f"\nPlain bash itself matched Koala's stored answer in {sum(r['matches_koala_hash'] for r in kb)} of {len(kb)} "
  f"scripts that have one.\n")
diff = [(i, s) for i in ids for s in SETS + ["pash-own-copy"] if (i, s) in T and not T[(i, s)]["same_as_bash"]]
w("Timed runs whose output differs from bash: " + (", ".join(f"{i} ({s})" for i, s in diff) or "none") + ".\n")
idiff = [(i, s) for i in ids for s in SETS if (i, s) in I and not I[(i, s)]["same_as_bash"]]
w("Runs with the stand-in programs whose output differs from bash: " +
  (", ".join(f"{i} ({s})" for i, s in idiff) or "none") + ".\n")

# 2. parts
w("## 2. Parts of the scripts (what PaSh compiles), per source (runs with the stand-in programs)\n")
w("A part is one piece of a script that PaSh asks its compiler to handle. Every part not run in parallel "
  "counts against the source, whatever the cause (Tiran, 2026-11-24); the causes are listed.\n")
w("| Source | Scripts | Parts sent (each time) | Run in parallel | Distinct parts | Distinct run in parallel | Causes, parts not run in parallel (each time) |")
w("|---|---|---|---|---|---|---|")
for s in SETS:
    tot = Counter(); dist = Counter(); n = nd = 0
    ns = sum(1 for i in ids if (i, s) in I)
    for i in ids:
        r = I.get((i, s))
        ro = (r or {}).get("region_outcomes") or {}
        n += ro.get("regions", 0); nd += ro.get("distinct_regions", 0)
        tot.update(ro.get("per_execution", {})); dist.update(ro.get("per_distinct", {}))
    causes = ", ".join(f"{k} {v}" for k, v in sorted(tot.items()) if k != "parallelized" and v)
    w(f"| {NAMES[s]} | {ns} | {n} | {tot['parallelized']} of {n} | {nd} | {dist['parallelized']} of {nd} | {causes or '-'} |")

# 3. parts against PaSh's own files
w("\n## 3. Distinct parts compared with PaSh's own files\n")
w("Paired by script and part text. 'Gained': run in parallel with this source but not with PaSh's own; "
  "'lost': the reverse.\n")
par = defaultdict(dict)
for r in reg:
    if r["mode"] != "instrumented":
        continue
    k = (r["id"], r["text_sha"])
    par[k][r["set"]] = par[k].get(r["set"], False) or r["outcome"] == "parallelized"
w("| Source | Distinct parts with both | Both in parallel | Gained | Lost | Neither |")
w("|---|---|---|---|---|---|")
for s in [x for x in SETS[1:]]:
    c = Counter()
    for k, v in par.items():
        if s in v and "pash-own" in v:
            c[(v[s], v["pash-own"])] += 1
    n = sum(c.values())
    w(f"| {NAMES[s]} | {n} | {c[(True, True)]} | {c[(True, False)]} | {c[(False, True)]} | {c[(False, False)]} |")

# 4. command uses
w("\n## 4. Command uses, by who supplied the files (runs with the stand-in programs)\n")
w("A command use is one place a script calls a command, in one distinct part. 'Ours' means the source's "
  "own files (naive LLM's or Caruca's); 'PaSh's own' means the source has none for that command, so PaSh's "
  "own files were used.\n")
w("| Source | Whose files | Uses in parts PaSh ran in parallel | Split | Not split: file says no | Not split: only a split PaSh has not implemented | Not split: no answer / no files / raised | Not split: allowed but not split | Uses in parts not run in parallel | Uses outside every part |")
w("|---|---|---|---|---|---|---|---|---|---|")
for s in SETS:
    for who in ("ours", "pash-own", "none"):
        rows = [u for u in occ if u["set"] == s and u["source"] == who]
        if not rows:
            continue
        inpar = [u for u in rows if u["copies"] is not None]
        why = Counter(u["why_not_split"] for u in inpar if not u["split"])
        w(f"| {NAMES[s]} | {who} | {len(inpar)} | {sum(1 for u in inpar if u['split'])} | {why['file says no split']} | "
          f"{why['file allows only a split PaSh has not implemented']} | "
          f"{why['no answer'] + why['no files'] + why['raised']} | {why['allowed by the files, not split by PaSh']} | "
          f"{sum(1 for u in rows if u['copies'] is None and not u['outside_pash'])} | "
          f"{sum(1 for u in rows if u['outside_pash'])} |")
raised = sorted({(u["command"], u["set"], (u.get("exception") or "")[:120]) for u in occ if u["file_answer"] == "raised"})
w("\nFiles that raised an error when PaSh's words were passed to them: " +
  ("; ".join(f"{c} ({s}): {e}" for c, s, e in raised) or "none") + ".\n")
agree = [u for u in occ if u["copies"] is not None]
mism = [u for u in agree if (u["file_answer"] == "allows a split") != bool(u["split"])]
w(f"Check of the method: in {len(agree) - len(mism)} of {len(agree)} uses in parts PaSh ran in parallel, PaSh split "
  f"the use exactly when the files (asked with PaSh's words) allowed a split PaSh can carry out.\n")

# 5. commands each source brought and what changed
w("## 5. Commands where the source's own files changed what PaSh split\n")
w("Per command: in how many scripts the command was split with this source and not with PaSh's own "
  "(gained), and the reverse (lost). Counted per script.\n")
spl = defaultdict(set)
for r in res:
    if r["mode"] == "instrumented" and r["set"] != "bash":
        spl[(r["id"], r["set"])] = set(r["split_commands"] or [])
w("| Source | Command | Gained (scripts) | Lost (scripts) |")
w("|---|---|---|---|")
for s in SETS[1:]:
    g, l = Counter(), Counter()
    for i in ids:
        if (i, s) not in spl or (i, "pash-own") not in spl:
            continue
        a, o = spl[(i, s)], spl[(i, "pash-own")]
        g.update(a - o); l.update(o - a)
    for c in sorted(set(g) | set(l)):
        w(f"| {NAMES[s]} | {c} | {g[c]} | {l[c]} |")

# 6. time
w("\n## 6. Time (median of three timed runs per source and script)\n")
w("Ratios are bash time divided by the source's time (above 1 = faster than bash). Summaries are geometric "
  "means over the scripts. All of a source's commands are swapped in at once, so a time difference belongs "
  "to the source as a whole, not to any one command.\n")


def gm(xs):
    xs = [x for x in xs if x and x > 0]
    return math.exp(sum(map(math.log, xs)) / len(xs)) if xs else float("nan")


w("| Source | Scripts | Speed-up over bash (geometric mean) | Time vs PaSh's own (geometric mean; below 1 = faster) | Faster than PaSh's own by more than 10% | Slower by more than 10% |")
w("|---|---|---|---|---|---|")
for s in SETS + ["pash-own-copy"]:
    rr = [(T[(i, "bash")]["seconds"], T[(i, s)]["seconds"], T[(i, "pash-own")]["seconds"])
          for i in ids if (i, s) in T and (i, "bash") in T and (i, "pash-own") in T]
    vs = [x / p for _, x, p in rr]
    w(f"| {NAMES[s]} | {len(rr)} | {gm([b_ / x for b_, x, _ in rr]):.2f}x | {gm(vs):.2f} | "
      f"{sum(v < 0.9 for v in vs)} of {len(rr)} | {sum(v > 1.1 for v in vs)} of {len(rr)} |")
cp = [T[(i, "pash-own-copy")]["seconds"] / T[(i, "pash-own")]["seconds"] for i in ids
      if (i, "pash-own-copy") in T and (i, "pash-own") in T]
if cp:
    w(f"\nNoise check: the second, identical copy of PaSh's own files took between {min(cp):.2f} and {max(cp):.2f} "
      f"times as long as the first (median {S.median(cp):.2f}; {sum(abs(x - 1) > 0.1 for x in cp)} of {len(cp)} "
      f"scripts differ by more than 10%). A difference smaller than that spread is not evidence of anything.\n")
w("\n### Per script (seconds)\n")
w("| Script | bash | " + " | ".join(NAMES[s] for s in SETS + ["pash-own-copy"]) + " |")
w("|---|---" + "|---" * (len(SETS) + 1) + "|")
for i in ids:
    w(f"| {i} | " + " | ".join(f"{T[(i, s)]['seconds']:.2f}" if (i, s) in T else "-"
                               for s in ["bash"] + SETS + ["pash-own-copy"]) + " |")

(HERE / "numbers.md").write_text("\n".join(out) + "\n")
print("\n".join(out[:60]))
