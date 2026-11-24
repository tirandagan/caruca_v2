#!/usr/bin/env python3
"""Count every number the PaSh-suite report uses. Count only: no judgement, no prose beyond labels.

Reads the builder's records (results, regions, occurrences, answers, commands, invocations, sets,
controls, run windows) and the inventory (orchestration/coverage.jsonl), and writes numbers.md
(tables 1-4, the data behind charts A-C, appendix tables A1, A3, A4, A5, and the self-checks) and
numbers.json (the same, for make_charts.py). Definitions follow orchestration/report_plan.md,
sections 2 and 5.4; count_report.md explains each number.

Standard library only; runs with `python3 -I`:

    python3 -I count_report.py --records <folder with the records> --out <folder for numbers.*>

Fails loudly, naming the file, line and field, when a record lacks something it needs.
"""
import argparse
import json
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REF = "pash-own"                     # the reference source: PaSh's own files
ANSWER_METHOD = "as PaSh passes them"  # the answers that match what PaSh did (brief_builder, amendment 3)
SPLIT_OK = "allows a split"          # the only file answer under which PaSh can split (see count_report.md)


class RecordError(SystemExit):
    pass


def die(msg):
    raise RecordError(f"count_report.py: {msg}")


# ---------------------------------------------------------------- reading, strictly

class Row(dict):
    """A record row that knows where it came from, so a missing field names its file and line."""

    def __init__(self, data, where):
        super().__init__(data)
        self.where = where

    def need(self, *path):
        cur, walked = self, []
        for key in path:
            walked.append(str(key))
            if not isinstance(cur, dict) or key not in cur:
                die(f"{self.where}: field '{'.'.join(walked)}' is missing")
            cur = cur[key]
        return cur

    def need_not_none(self, *path):
        v = self.need(*path)
        if v is None:
            die(f"{self.where}: field '{'.'.join(map(str, path))}' is null, a value is needed")
        return v


def read_jsonl(path, required=True):
    if not path.exists():
        if required:
            die(f"record not found: {path}")
        return None
    out = []
    for n, line in enumerate(path.read_text().splitlines(), 1):
        if line.strip():
            try:
                out.append(Row(json.loads(line), f"{path.name}:{n}"))
            except json.JSONDecodeError as e:
                die(f"{path.name}:{n}: not valid JSON ({e})")
    return out


def read_json(path):
    if not path.exists():
        die(f"record not found: {path}")
    return Row(json.loads(path.read_text()), path.name)


def base_id(script_id):
    """A script Koala's launcher starts more than once has ids ending in '#n'; they count as one."""
    return script_id.split("#")[0]


def rate(a, b):
    return {"a": a, "b": b, "text": f"{a} of {b}"}


def median(xs):
    return statistics.median(xs) if xs else None


# ---------------------------------------------------------------- the counting

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--records", type=Path, default=HERE, help="folder holding the builder's records")
    ap.add_argument("--coverage", type=Path, default=HERE / "orchestration" / "coverage.jsonl")
    ap.add_argument("--out", type=Path, default=HERE, help="where numbers.md and numbers.json go")
    ap.add_argument("--tag", default="", help="suffix for the output names, e.g. 'pilot' -> numbers_pilot.md")
    ap.add_argument("--timing-check", type=Path, default=None,
                    help="the Mac power check written by timing_check.py (default: timing_check.jsonl in --records)")
    args = ap.parse_args()
    R = args.records

    sets_doc = read_json(R / "sets.json")
    names = sets_doc.need("display_names")
    main_sets = sets_doc.need("main")
    timing_only = sets_doc.need("timing_only")
    if REF not in main_sets:
        die(f"sets.json: 'main' does not list the reference source '{REF}'")
    sources = [s for s in main_sets if s not in ("bash", *timing_only)]   # REF first if listed first
    sources = [REF] + [s for s in sources if s != REF]
    others = [s for s in sources if s != REF]
    copy_sets = list(timing_only)
    for s in ["bash", *sources, *copy_sets]:
        if s not in names:
            die(f"sets.json: no display name for source '{s}'")

    results = [r for r in read_jsonl(R / "results.jsonl") if r.need("phase") == "main"]
    regions = [r for r in read_jsonl(R / "regions.jsonl") if r.need("phase") == "main"]
    occ_all = read_jsonl(R / "occurrences.jsonl")
    answers = read_jsonl(R / "answers.jsonl")
    commands = read_jsonl(R / "commands.jsonl")
    invocations = read_jsonl(R / "invocations.jsonl")
    controls = read_jsonl(R / "controls.jsonl", required=False) or []
    controls_occ = read_jsonl(R / "controls_occurrences.jsonl", required=False) or []
    windows = read_jsonl(R / "run_windows.jsonl", required=False) or []
    coverage = read_jsonl(args.coverage)
    occ = [o for o in occ_all if o.need("phase") == "main"]

    checks = []   # (name, passed, detail)

    def check(name, ok, detail=""):
        checks.append({"check": name, "passed": bool(ok), "detail": detail})

    # ---- scripts run, and bash's stability (N)
    script_ids = sorted({base_id(r.need("id")) for r in results})
    launches = defaultdict(set)
    for r in results:
        launches[base_id(r.need("id"))].add(r.need("id"))
    bash_hashes = defaultdict(set)
    for r in results + [c for c in controls if c.need("set") == "bash"]:
        if r.need("set") == "bash":
            bash_hashes[r.need("id")].add((r.need_not_none("out_sha256"), r.need("output_files")))
    unstable = sorted({base_id(i) for i, h in bash_hashes.items() if len(h) > 1})
    for sid in script_ids:
        for lid in launches[sid]:
            if lid not in bash_hashes:
                die(f"results.jsonl: no bash run for '{lid}'")
    N_ids = [s for s in script_ids if s not in unstable]
    N = len(N_ids)
    check("bash's own output is identical across all its runs", not unstable,
          f"{len(script_ids) - len(unstable)} of {len(script_ids)} scripts; varying: {', '.join(unstable) or 'none'}")

    # ---- table 1, column 1: output same as bash
    out_ok = defaultdict(dict)   # source -> script -> bool
    wrong_detail = defaultdict(list)
    for s in sources + copy_sets:
        for sid in N_ids:
            rows = [r for r in results if base_id(r.need("id")) == sid and r.need("set") == s]
            if not rows:
                if s in copy_sets:
                    continue
                die(f"results.jsonl: no run of '{sid}' with source '{s}'")
            ok = all(r.need("same_as_bash") is True and r.need("output_files_same_as_bash") is True
                     and r.need("state") != "timed out" for r in rows)
            out_ok[s][sid] = ok
            if not ok:
                wrong_detail[s].append(sid)

    # ---- parts (distinct by text, repeat 1, instrumented), pooled over launches
    def rep1_regions(s):
        rows = [r for r in regions if r.need("set") == s and r.need("mode") == "instrumented"
                and r.need("repeat") == 1]
        rows.sort(key=lambda r: (r.need("id"), r.need("region")))
        return rows

    parts = {}          # source -> {(sid, sha): outcome of first execution}
    parts_reason = {}   # source -> {(sid, sha): reason of first execution}
    execs = {}          # source -> {(launch id, region index): (sha, outcome)}
    for s in sources:
        first, why, ex = {}, {}, {}
        for r in rep1_regions(s):
            key = (base_id(r.need("id")), r.need_not_none("text_sha"))
            first.setdefault(key, r.need_not_none("outcome"))
            why.setdefault(key, r.need("reason"))
            ex[(r.need("id"), r.need("region"))] = (r.need("text_sha"), r.need("outcome"))
        parts[s], parts_reason[s], execs[s] = first, why, ex

    # self-check: distinct part count the same for every source, and the same part texts
    part_keys = {s: set(parts[s]) for s in sources}
    same_parts = all(part_keys[s] == part_keys[REF] for s in sources)
    check("the distinct parts are the same for every source (same texts, same count)", same_parts,
          "; ".join(f"{names[s]}: {len(part_keys[s])}" for s in sources))
    if not same_parts:
        die("distinct parts differ between sources; pairing by part text is not possible "
            "(report plan 5.5: fall back to order). Counts: "
            + ", ".join(f"{s}={len(part_keys[s])}" for s in sources))
    seq_same = all([v[0] for _, v in sorted(execs[s].items())] == [v[0] for _, v in sorted(execs[REF].items())]
                   for s in sources)
    check("each script sends the same sequence of part texts to PaSh under every source (repeat 1)", seq_same)

    # self-check: the regions record agrees with the results record's own part counts
    agree = True
    for s in sources:
        for r in results:
            if r.need("set") != s or r.need("mode") != "instrumented" or r.need("repeat") != 1:
                continue
            ro = r.need_not_none("region_outcomes")
            n_here = len({sha for (lid, _), (sha, _) in execs[s].items() if lid == r.need("id")})
            if ro["distinct_regions"] != n_here:
                agree = False
    check("the part count in results.jsonl equals the parts listed in regions.jsonl", agree)

    N_set = set(N_ids)
    P_keys = sorted(k for k in part_keys[REF] if k[0] in N_set)
    P = len(P_keys)
    par = {s: {k for k in P_keys if parts[s][k] == "parallelized"} for s in sources}

    scripts_any_par = {}
    for s in sources:
        scripts_any_par[s] = sorted({k[0] for k in par[s]})

    # ---- command uses (repeat 1, instrumented, inside parts sent to PaSh), pooled over launches
    def use_key(o):
        return (base_id(o.need("id")), o.need_not_none("region_text_sha"), o.need_not_none("position"))

    uses = {}       # source -> {key: row}
    outside = {}
    varying_uses = []
    for s in sources:
        d, out = {}, []
        for o in occ:
            if o.need("set") != s or o.need("mode") != "instrumented" or o.need("repeat") != 1:
                continue
            if o.need("outside_pash"):
                out.append(o)
                continue
            k = use_key(o)
            if k in d and d[k].need("split") != o.need("split"):
                varying_uses.append((s, k))
            d.setdefault(k, o)
            for f in ("command", "invocation", "source", "split", "file_answer", "why_not_split"):
                o.need(f)
        uses[s], outside[s] = d, out
    if not uses[REF]:
        die("occurrences.jsonl: no command uses for the reference source (repeat 1, instrumented)")
    use_keys = {s: set(uses[s]) for s in sources}
    same_uses = all(use_keys[s] == use_keys[REF] for s in sources)
    check("the command uses are the same for every source (same part, same position)", same_uses,
          "; ".join(f"{names[s]}: {len(use_keys[s])}" for s in sources))
    if not same_uses:
        die("command uses differ between sources; cannot pair uses by (script, part text, position)")
    check("a use that appears in more than one launch of a script has the same result in each",
          not varying_uses, f"{len(varying_uses)} differ")
    U_keys = sorted(k for k in use_keys[REF] if k[0] in N_set)
    U = len(U_keys)
    split_uses = {s: {k for k in U_keys if uses[s][k]["split"] is True} for s in sources}

    # self-check: a use split in occurrences <-> its command named among the split commands in results
    cons = True
    for s in sources:
        named = defaultdict(set)
        for r in results:
            if r.need("set") == s and r.need("mode") == "instrumented" and r.need("repeat") == 1:
                named[base_id(r.need("id"))] |= set(r.need("split_commands") or [])
        got = defaultdict(set)
        for k in use_keys[s]:
            if uses[s][k]["split"] is True:
                got[k[0]].add(uses[s][k]["command"])
        if any(got[i] != named[i] for i in set(got) | set(named)):
            cons = False
    check("the commands split per use match the commands split per script in results.jsonl", cons)

    # self-check: the files' answer predicts whether PaSh split the use
    mism = [(s, k) for s in sources for k in use_keys[s]
            if (uses[s][k]["file_answer"] == SPLIT_OK) != (uses[s][k]["split"] is True)]
    check("PaSh split a use exactly when its files allowed a split PaSh can carry out", not mism,
          f"{len(mism)} uses where the answer and PaSh differ"
          + (": " + "; ".join(f"{names[s]} {uses[s][k]['invocation']}" for s, k in mism[:10]) if mism else ""))

    # self-check: later instrumented repeats agree with repeat 1
    reps = defaultdict(dict)
    for o in occ:
        if o.need("mode") == "instrumented" and not o.need("outside_pash"):
            reps[(o.need("set"), use_key(o))][o.need("repeat")] = o.need("split")
    unstable_uses = [k for k, v in reps.items() if len(set(v.values())) > 1]
    n_rep = max((len(v) for v in reps.values()), default=0)
    check("every instrumented repeat split the same uses as repeat 1", not unstable_uses,
          f"{len(reps)} uses x sources, up to {n_rep} repeats each; {len(unstable_uses)} vary")

    # ---- times (plain mode, all repeats; pooled launches summed per repeat)
    times = defaultdict(dict)    # source -> script -> [seconds per repeat]
    for s in ["bash", *sources, *copy_sets]:
        for sid in script_ids:
            per_rep = defaultdict(float)
            rows = [r for r in results if base_id(r.need("id")) == sid and r.need("set") == s
                    and r.need("mode") == "plain"]
            for r in rows:
                if r.need("state") == "timed out":
                    per_rep[r.need("repeat")] = float("nan")
                else:
                    per_rep[r.need("repeat")] += r.need_not_none("seconds")
            if rows:
                times[s][sid] = [per_rep[k] for k in sorted(per_rep)]
    tstats = {s: {sid: {"median": median(v), "min": min(v), "max": max(v), "n": len(v)}
                  for sid, v in times[s].items()} for s in times}
    faster, speedups = {}, {}
    for s in sources + copy_sets:
        f, sp = 0, []
        for sid in N_ids:
            if sid not in tstats.get(s, {}) or sid not in tstats["bash"]:
                continue
            b, t = tstats["bash"][sid]["median"], tstats[s][sid]["median"]
            if t < b:
                f += 1
            sp.append(b / t)
        faster[s], speedups[s] = f, (median(sp) if sp else None)

    # ---- table 1
    table1 = []
    for s in sources:
        table1.append({
            "source": s, "label": names[s], "reference": s == REF,
            "output_same_as_bash": rate(sum(out_ok[s].values()), N),
            "wrong_scripts": wrong_detail[s],
            "scripts_any_part_parallel": rate(len([i for i in scripts_any_par[s] if i in N_set]), N),
            "parts_parallel": rate(len(par[s]), P),
            "uses_split": rate(len(split_uses[s]), U),
            "faster_than_bash": rate(faster[s], N),
            "median_speedup": speedups[s],
        })

    # ---- table 2 (case split) and chart A (parts paired with PaSh's own)
    table2, chartA = [], []
    for s in others:
        own = [k for k in U_keys if uses[s][k]["source"] == "ours"]
        filled = [k for k in U_keys if uses[s][k]["source"] == "pash-own"]
        nobody = [k for k in U_keys if uses[s][k]["source"] == "none"]
        bad = [k for k in U_keys if uses[s][k]["source"] not in ("ours", "pash-own", "none")]
        if bad:
            die(f"occurrences.jsonl: unknown 'source' value(s) {sorted({uses[s][k]['source'] for k in bad})}")
        table2.append({
            "source": s, "label": names[s],
            "uses_own_files": rate(len(own), U),
            "own_split_with_them": rate(sum(uses[s][k]["split"] is True for k in own), len(own)),
            "own_split_with_pash_own": rate(sum(uses[REF][k]["split"] is True for k in own), len(own)),
            "uses_pash_own_filled_in": rate(len(filled), U),
            "filled_same_as_pash_own": rate(sum(uses[s][k]["split"] == uses[REF][k]["split"] for k in filled),
                                            len(filled)),
            "filled_differs": [{"script": k[0], "invocation": uses[s][k]["invocation"]} for k in filled
                               if uses[s][k]["split"] != uses[REF][k]["split"]],
            "uses_no_files": rate(len(nobody), U),
        })
        both = sum(1 for k in P_keys if k in par[s] and k in par[REF])
        gained = sum(1 for k in P_keys if k in par[s] and k not in par[REF])
        lost = sum(1 for k in P_keys if k not in par[s] and k in par[REF])
        neither = P - both - gained - lost
        chartA.append({"source": s, "label": names[s], "P": P,
                       "both": both, "only_this": gained, "neither": neither, "only_pash_own": lost})
    chartA_ref = {"source": REF, "label": names[REF], "P": P,
                  "parallel": len(par[REF]), "not_parallel": P - len(par[REF])}

    # ---- table 3: every command where a source changed what PaSh did
    by_cmd = defaultdict(list)
    for k in U_keys:
        by_cmd[uses[REF][k]["command"]].append(k)
    table3, unchanged = [], []
    for cmd, ks in sorted(by_cmd.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        differs = {s: any(uses[s][k]["split"] != uses[REF][k]["split"] for k in ks) for s in others}
        if not any(differs.values()):
            unchanged.append(cmd)
            continue
        scripts_with = sorted({k[0] for k in ks})
        wrong = {s: [i for i in scripts_with if not out_ok[s].get(i, True)] for s in sources}
        table3.append({
            "command": cmd, "uses": len(ks),
            "cells": {s: {"split": sum(uses[s][k]["split"] is True for k in ks), "of": len(ks),
                          "differs": s != REF and differs[s]} for s in sources},
            "scripts_wrong": {s: v for s, v in wrong.items() if v},
        })

    # ---- table 4 row 1: agreement with PaSh's own files, per distinct command line
    ans = [a for a in answers if a.need("method") == ANSWER_METHOD]
    if not ans:
        die(f"answers.jsonl: no rows with method '{ANSWER_METHOD}'")
    ans_by = defaultdict(dict)  # source -> (id, position) -> row
    for a in ans:
        for f in ("source", "io", "io_outcome", "parallelizability_outcome", "file_answer", "split_recipes",
                  "invocation", "command", "position", "id"):
            a.need(f)
        ans_by[a["set"]][(a["id"], a["position"])] = a

    def decision(a):
        return a["file_answer"] == SPLIT_OK

    def special_merge_only(a):
        ok = [r for r in a["split_recipes"] if r.get("implemented")]
        return bool(ok) and all(r.get("aggregate") != "CONCATENATE" for r in ok)

    table4_agree, a4_answers = [], []
    for s in others:
        lines = defaultdict(list)   # (command, invocation) -> [(src row, ref row)]
        for key, a in ans_by[s].items():
            if a["source"] != "ours" or base_id(key[0]) not in N_set:
                continue
            ref = ans_by[REF].get(key)
            if ref is None:
                die(f"answers.jsonl: source '{s}' answered {key} but '{REF}' has no answer row for it")
            lines[(a["command"], a["invocation"])].append((a, ref))
        inconsistent = [k for k, v in lines.items()
                        if len({(json.dumps(x["io"], sort_keys=True), x["file_answer"]) for x, _ in v}) > 1]
        io_b = io_same = io_ref_none = 0
        sp_b = sp_same = sp_ref_none = merge_only = raised = 0
        per_cmd = defaultdict(lambda: [0, 0])  # command -> [lines comparable on both, lines agreeing on both]
        for (cmd, inv), pairs in sorted(lines.items()):
            a, ref = pairs[0]
            if a["exception"] or a["file_answer"].startswith("raised"):
                raised += 1
            io_cmp = ref["io_outcome"] == "answered"
            sp_cmp = ref["parallelizability_outcome"] == "answered"
            if io_cmp:
                io_b += 1
                io_same += a["io"] == ref["io"] and a["io_outcome"] == "answered"
            else:
                io_ref_none += 1
            if sp_cmp:
                sp_b += 1
                same = decision(a) == decision(ref)
                sp_same += same
                if not same and decision(ref) and not decision(a) and special_merge_only(ref):
                    merge_only += 1
            else:
                sp_ref_none += 1
            if io_cmp and sp_cmp:
                per_cmd[cmd][0] += 1
                per_cmd[cmd][1] += (a["io"] == ref["io"]) and decision(a) == decision(ref)
            a4_answers.append({"source": s, "command": cmd, "invocation": inv,
                               "same_io": (a["io"] == ref["io"]) if io_cmp else None,
                               "source_answer": a["file_answer"], "pash_own_answer": ref["file_answer"]})
        cmds_cmp = [c for c, v in per_cmd.items() if v[0]]
        table4_agree.append({
            "source": s, "label": names[s],
            "lines": len(lines),
            "same_inputs_outputs": rate(io_same, io_b),
            "same_split_decision": rate(sp_same, sp_b),
            "commands_all_lines_agree": rate(sum(per_cmd[c][0] == per_cmd[c][1] for c in cmds_cmp), len(cmds_cmp)),
            "pash_own_gives_no_io_answer": io_ref_none,
            "pash_own_gives_no_split_answer": sp_ref_none,
            "pash_own_splits_only_with_special_merge_source_says_no": merge_only,
            "source_files_raised": raised,
            "lines_answered_differently_in_different_scripts": len(inconsistent),
        })
        check(f"{names[s]}: a command line gets the same answer in every script that uses it", not inconsistent,
              f"{len(inconsistent)} lines differ")

    table4 = {"agreement": table4_agree,
              "output_identical": {s: table1[sources.index(s)]["output_same_as_bash"] for s in sources},
              "parts_parallel": {s: table1[sources.index(s)]["parts_parallel"] for s in sources},
              "median_speedup": {s: speedups[s] for s in sources}}

    # ---- chart B data and noise
    differs_script = {s: sorted({k[0] for k in U_keys if uses[s][k]["split"] != uses[REF][k]["split"]})
                      for s in others}
    chartB = {"panels": [], "noise": []}
    for c in copy_sets:
        for sid in N_ids:
            if sid in tstats.get(c, {}) and sid in tstats[REF]:
                x, y = tstats[REF][sid]["median"], tstats[c][sid]["median"]
                chartB["noise"].append({"script": sid, "x": x, "y": y})
    noise_pct = [abs(p["y"] / p["x"] - 1) * 100 for p in chartB["noise"]]
    chartB["noise_max_pct"] = max(noise_pct) if noise_pct else None
    chartB["noise_label"] = names[copy_sets[0]] if copy_sets else None
    for s in others:
        pts = []
        for sid in N_ids:
            if sid in tstats[s] and sid in tstats[REF]:
                pts.append({"script": sid, "x": tstats[REF][sid]["median"], "y": tstats[s][sid]["median"],
                            "output_ok": out_ok[s][sid], "split_differs": sid in differs_script[s]})
        chartB["panels"].append({"source": s, "label": names[s], "points": pts})
    if not copy_sets or not chartB["noise"]:
        check("the second copy of PaSh's own files was timed", False, "no timing runs found")

    # ---- chart C: which commands each source has files for
    run_set = set(script_ids)
    cov_rows = {f"{c.need('group')}/{c.need('script')}": c for c in coverage}
    missing_cov = [i for i in script_ids if i not in cov_rows]
    check("every script run is in the inventory", not missing_cov, ", ".join(missing_cov))
    scripts_per_cmd = Counter()
    for i in script_ids:
        if i in cov_rows:
            for c in cov_rows[i].need("commands"):
                scripts_per_cmd[c] += 1
    has_files = defaultdict(set)          # source -> commands with own files (from commands.jsonl)
    seen = defaultdict(set)               # script -> commands seen starting (commands.jsonl)
    for c in commands:
        if base_id(c.need("id")) not in run_set:
            continue
        seen[base_id(c["id"])].add(c.need("command"))
        st, src = c.need("set"), c.need("source")
        if st == REF and src == "pash-own":
            has_files[REF].add(c["command"])
        elif st in others and src == "ours":
            has_files[st].add(c["command"])
    only_cov, only_seen = set(), set()
    for i in script_ids:
        inv_cmds = set(cov_rows[i].need("commands")) if i in cov_rows else set()
        only_cov |= {(i, c) for c in inv_cmds - seen[i]}
        only_seen |= {(i, c) for c in seen[i] - inv_cmds}
    check("the commands the inventory lists equal the commands seen starting, per script",
          not only_cov and not only_seen,
          f"listed, not seen: {sorted(only_cov)[:20]}; seen, not listed: {sorted(only_seen)[:20]}")
    for i, c in only_seen:
        scripts_per_cmd[c] += 0 if c in scripts_per_cmd else 1
    all_cmds = sorted(set(scripts_per_cmd) | {c for _, c in only_seen}, key=lambda c: (-scripts_per_cmd[c], c))
    caruca_rows = [s for s in others if s.startswith("caruca")]
    rows_c = [REF] + [s for s in others if not s.startswith("caruca")]
    caruca_same = len({frozenset(has_files[s]) for s in caruca_rows}) <= 1
    if caruca_rows and caruca_same:
        rows_c.append(caruca_rows[0])
        caruca_label = "Caruca's files (both grammars)"
    else:
        rows_c += caruca_rows
        caruca_label = None
    nobody = [c for c in all_cmds if not any(c in has_files[s] for s in sources)]
    chartC = {"commands": [{"command": c, "scripts": scripts_per_cmd[c]} for c in all_cmds],
              "N": len(script_ids),
              "rows": [{"source": s, "label": (caruca_label if s in caruca_rows and caruca_label else names[s]),
                        "has": [c for c in all_cmds if c in has_files[s]]} for s in rows_c],
              "nobody": nobody}

    # ---- appendix A1: the scripts
    inv_by = {base_id(i.need("id")): i for i in invocations}
    a1 = []
    for c in coverage:
        i = f"{c.need('group')}/{c.need('script')}"
        a1.append({"published_set": c.need("published_set"), "group": c["group"], "script": c["script"],
                   "path": c.need("path"), "published_script": c.need("published_script"),
                   "closeness": c.need("closeness"), "run": i in run_set,
                   "launches": len(launches.get(i, ())),
                   "input_bytes": inv_by[i].get("input_bytes") if i in inv_by else None})

    # ---- appendix A3: why parts were not run in parallel
    def label_of(outcome, reason):
        if outcome == "other" and reason:
            return "other: " + reason.split(":")[0].split(" (")[0].strip()
        return outcome

    a3 = {"distinct": defaultdict(lambda: defaultdict(lambda: {"shared": 0, "only": 0})),
          "per_execution": defaultdict(lambda: defaultdict(lambda: {"shared": 0, "only": 0}))}
    for s in sources:
        for k in P_keys:
            o = parts[s][k]
            if o == "parallelized":
                continue
            lab = label_of(o, parts_reason[s][k])
            ro = parts[REF][k]
            shared = (s == REF) or label_of(ro, parts_reason[REF][k]) == lab
            a3["distinct"][lab][s]["shared" if shared else "only"] += 1
        for key, (sha, o) in execs[s].items():
            if base_id(key[0]) not in N_set or o == "parallelized":
                continue
            ref = execs[REF].get(key)
            if ref is None or ref[0] != sha:
                die(f"regions.jsonl: part {key} under '{s}' has no matching part under '{REF}'")
            lab = o if o != "other" else "other"
            shared = s == REF or ref[1] == o
            a3["per_execution"][lab][s]["shared" if shared else "only"] += 1
    a3 = {m: {lab: dict(v) for lab, v in d.items()} for m, d in a3.items()}
    per_exec_total = {s: sum(1 for key in execs[s] if base_id(key[0]) in N_set) for s in sources}

    # ---- appendix A4: every use whose result differs from PaSh's own
    a4 = []
    for k in U_keys:
        res = {s: uses[s][k]["split"] for s in sources}
        if all(res[s] == res[REF] for s in others):
            continue
        a4.append({"script": k[0], "position": k[2], "command": uses[REF][k]["command"],
                   "invocation": uses[REF][k]["invocation"],
                   "result": {s: ("split" if res[s] else "whole") for s in sources},
                   "why_not": {s: uses[s][k]["why_not_split"] for s in sources if not res[s]},
                   "file_source": {s: uses[s][k]["source"] for s in sources},
                   "output_same_as_bash": {s: out_ok[s][k[0]] for s in sources}})

    # ---- appendix A5: times
    a5 = []
    for sid in script_ids:
        row = {"script": sid}
        for s in ["bash", *sources, *copy_sets]:
            row[s] = tstats.get(s, {}).get(sid)
        a5.append(row)

    # ---- appendix A6 pieces the records hold: controls and run windows
    ctrl = []
    if controls:
        cset = sets_doc.get("controls", [])
        for c in controls:
            if c.need("mode") == "instrumented" and c.need("set") != "bash":
                ctrl.append({"phase": c.need("phase"), "set": c["set"], "label": names.get(c["set"], c["set"]),
                             "split_commands": c.need("split_commands") or [],
                             "output_same_as_bash": c.need("same_as_bash") is True})
        check("the folder-decides controls were run at the start and the end", {"start", "end"} <= {c["phase"] for c in ctrl},
              f"phases found: {sorted({c['phase'] for c in ctrl})}; sets: {len(cset)}")
    win = [{"what": w.need("what"), "phase": w.need("phase"), "id": w.need("id"), "start": w.need("start"),
            "end": w.need("end"), "load_start": w.need("uptime_start").split("load average:")[-1].strip(),
            "load_end": w.need("uptime_end").split("load average:")[-1].strip(),
            "koala_changed": w.need("koala_changed")} for w in windows]
    check("Koala's checkout did not change during any run window", not any(w["koala_changed"] for w in win))
    # the Mac power check (timing_check.py): a window with a sleep or wake in it, or not on mains power
    # at both ends, fails; so does a window with no power check at all
    timing_check = args.timing_check or R / "timing_check.jsonl"
    tc = read_jsonl(timing_check, required=False)
    invalid_windows = []
    if tc is None:
        invalid_windows = [f"{w['what']} {w['phase']} {w['id']} {w['start']}: no power check" for w in win]
        check("the Mac was awake and on mains power in every run window", False,
              f"{timing_check.name} not found; run timing_check.py on the Mac")
    else:
        by = {(t.need("what"), t.need("phase"), t.need("id"), t.need("start")): t for t in tc}
        for w in win:
            t = by.get((w["what"], w["phase"], w["id"], w["start"]))
            if t is None:
                problem = "no power check"
            elif t.need("valid") is not True:
                problem = "; ".join(t.need("problems")) or "not valid"
            else:
                problem = None
            w["power_check"] = "awake, on mains power" if problem is None else problem
            if problem:
                invalid_windows.append(f"{w['what']} {w['phase']} {w['id']} {w['start']}: {problem}")
        check("the Mac was awake and on mains power in every run window", not invalid_windows,
              f"{len(win) - len(invalid_windows)} of {len(win)} windows; "
              + ("; ".join(invalid_windows) if invalid_windows else f"from {timing_check.name}"))

    outside_counts = {s: len(outside[s]) for s in sources}

    numbers = {
        "records": str(R), "names": names, "sources": sources, "reference": REF,
        "N": N, "scripts_run": len(script_ids), "bash_output_varies": unstable, "P": P, "U": U,
        "uses_outside_pash": outside_counts,
        "table1": table1, "table2": table2, "table3": table3, "table3_unchanged_commands": unchanged,
        "table4": table4, "chartA": chartA, "chartA_reference": chartA_ref, "chartB": chartB, "chartC": chartC,
        "A1": a1, "A3": a3, "A3_parts_total": P, "A3_executions_total": per_exec_total,
        "A4": a4, "A4_answers": a4_answers, "A5": a5, "A6_controls": ctrl, "A6_windows": win,
        "checks": checks,
    }
    numbers["invalid_windows"] = invalid_windows
    stem = "numbers" + (f"_{args.tag}" if args.tag else "")
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / f"{stem}.json").write_text(json.dumps(numbers, indent=1, sort_keys=False) + "\n")
    (args.out / f"{stem}.md").write_text(render_md(numbers))
    failed = [c for c in checks if not c["passed"]]
    print(f"wrote {args.out / stem}.md and .json; {len(checks) - len(failed)} of {len(checks)} checks pass")
    for c in failed:
        print(f"  check not passed: {c['check']} ({c['detail']})")
    if invalid_windows:
        # times from these windows must not be used: re-run them (report plan 5.3)
        sys.exit(f"count_report.py: {len(invalid_windows)} run windows failed the Mac power check; "
                 "their times are not valid:\n  " + "\n  ".join(invalid_windows))


# ---------------------------------------------------------------- numbers.md

NUMERIC = re.compile(r"^(\*\*)?(split )?-?[\d.]+(x)?( of \d+)?( \(.*\))?(\*\*)?$|^[–-]$|^\d+ / \d+$")


def cell(c):
    return "–" if c is None else str(c)


def table(head, rows):
    rows = [[cell(c) for c in r] for r in rows]
    right = [i > 0 and bool(rows) and all(NUMERIC.match(r[i]) for r in rows) for i in range(len(head))]
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---:" if r else "---" for r in right) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


def sec(x):
    return "–" if x is None else f"{x:.2f}"


def render_md(n):
    L, nm, src, ref = [], n["names"], n["sources"], n["reference"]
    others = [s for s in src if s != ref]
    L.append("# Numbers for the PaSh-suite report\n")
    L.append(f"Written by `count_report.py` from `{n['records']}`. Every rate is \"a of b\". "
             "Do not edit by hand; re-run the script.\n")
    if n["invalid_windows"]:
        L.append("**Not valid: run windows that failed the Mac power check (sleep, wake, or not on mains power). "
                 "Their times must not be used:** " + "; ".join(n["invalid_windows"]) + "\n")
    L.append(f"- Scripts run: {n['scripts_run']}. Scripts whose plain-bash output is the same in every bash run "
             f"(**N**): {n['N']}" + (f"; left out because bash's own output varies: {', '.join(n['bash_output_varies'])}"
                                     if n["bash_output_varies"] else "") + ".")
    L.append(f"- Distinct parts sent to PaSh (**P**): {n['P']}. Command uses inside those parts (**U**): {n['U']}.")
    L.append("- Command uses that ran outside every part sent to PaSh (not in U): "
             + ", ".join(f"{nm[s]} {v}" for s, v in n["uses_outside_pash"].items()) + ".\n")

    L.append("## Table 1: What PaSh did with each source's files\n")
    rows = []
    for r in n["table1"]:
        lab = r["label"] + (" (reference)" if r["reference"] else "")
        outc = r["output_same_as_bash"]["text"] + (f" — **wrong: {', '.join(r['wrong_scripts'])}**" if r["wrong_scripts"] else "")
        sp = f" (median speed-up {r['median_speedup']:.2f}x)" if r["median_speedup"] else ""
        rows.append([lab, outc, r["scripts_any_part_parallel"]["text"], r["parts_parallel"]["text"],
                     r["uses_split"]["text"], r["faster_than_bash"]["text"] + sp])
    L.append(table(["Source", "Output same as bash", "Scripts with any part run in parallel",
                    "Parts run in parallel", "Command uses split", "Faster than bash"], rows) + "\n")

    L.append("## Table 2: Commands a source brings its own files for, and what PaSh did with them\n")
    rows = [[r["label"], r["uses_own_files"]["text"], r["own_split_with_them"]["text"],
             r["own_split_with_pash_own"]["text"], r["uses_pash_own_filled_in"]["text"],
             r["filled_same_as_pash_own"]["text"], r["uses_no_files"]["text"]] for r in n["table2"]]
    L.append(table(["Source", "Uses with the source's own files", "… split with them",
                    "… the same uses split with PaSh's own files", "Uses with PaSh's own files filled in",
                    "… result same as with PaSh's own", "Uses with no files from anyone"], rows) + "\n")
    for r in n["table2"]:
        for d in r["filled_differs"]:
            L.append(f"- {r['label']}: filled-in use with a different result: {d['script']}, `{d['invocation']}`")
    L.append("")

    L.append("## Chart A data: the scripts' parts, compared with PaSh's own files\n")
    a = n["chartA_reference"]
    L.append(f"Reference, {a['label']}: run in parallel {a['parallel']} of {a['P']}; not {a['not_parallel']} of {a['P']}.\n")
    L.append(table(["Source", "Run in parallel with both", "Only with this source", "With neither",
                    "Only with PaSh's own files"],
                   [[r["label"], f"{r['both']} of {r['P']}", f"{r['only_this']} of {r['P']}",
                     f"{r['neither']} of {r['P']}", f"{r['only_pash_own']} of {r['P']}"] for r in n["chartA"]]) + "\n")

    L.append("## Table 3: Every command where a source changed what PaSh did\n")
    rows = []
    for r in n["table3"]:
        cells = []
        for s in src:
            c = r["cells"][s]
            t = f"split {c['split']} of {c['of']}"
            cells.append(f"**{t}**" if c["differs"] else t)
        out = "all same as bash" if not r["scripts_wrong"] else "; ".join(
            f"{nm[s]}: wrong in {len(v)} scripts" for s, v in r["scripts_wrong"].items())
        rows.append([f"`{r['command']}`", r["uses"], *cells, out])
    L.append(table(["Command", "Uses in the suite", *[nm[s] for s in src], "Output"], rows) if rows
             else "No command: every source gave the same result as PaSh's own files on every use.")
    L.append(f"\nThe other {len(n['table3_unchanged_commands'])} commands: every source gave the same result as "
             f"PaSh's own files ({', '.join(n['table3_unchanged_commands'])}). Bold = differs from PaSh's own.\n")

    L.append("## Chart B data: time against PaSh's own files\n")
    b = n["chartB"]
    L.append(f"Noise ({b['noise_label']} against the first copy): largest difference "
             f"{'–' if b['noise_max_pct'] is None else f'{b['noise_max_pct']:.1f}%'} over {len(b['noise'])} scripts.\n")
    rows = []
    for p in b["panels"]:
        for q in p["points"]:
            rows.append([p["label"], q["script"], sec(q["x"]), sec(q["y"]), "yes" if q["output_ok"] else "**no**",
                         "yes" if q["split_differs"] else "no"])
    L.append(table(["Source", "Script", "Median s, PaSh's own files", "Median s, this source",
                    "Output same as bash", "Split choices differ"], rows) + "\n")

    L.append("## Chart C data: which of the suite's commands each source has files for\n")
    c = n["chartC"]
    for r in c["rows"]:
        L.append(f"- {r['label']}: {len(r['has'])} of {len(c['commands'])} commands ({', '.join(r['has'])})")
    L.append(f"- Files from nobody: {len(c['nobody'])} of {len(c['commands'])} ({', '.join(c['nobody'])})")
    L.append("- Scripts using each command (of " + str(c["N"]) + "): "
             + ", ".join(f"{x['command']} {x['scripts']}" for x in c["commands"]) + "\n")

    L.append("## Table 4: Next to the Caruca paper's PaSh check\n")
    t4 = n["table4"]
    rows = []
    for r in t4["agreement"]:
        rows.append([r["label"], r["lines"], r["same_inputs_outputs"]["text"], r["same_split_decision"]["text"],
                     r["commands_all_lines_agree"]["text"], r["pash_own_gives_no_split_answer"],
                     r["pash_own_splits_only_with_special_merge_source_says_no"], r["source_files_raised"]])
    L.append("Agreement with PaSh's own files on the suite's own command lines (each distinct command line "
             "for which the source has its own files and PaSh's own files exist):\n")
    L.append(table(["Source", "Command lines", "Same inputs and outputs", "Same split decision",
                    "Commands with every line agreeing", "Lines where PaSh's own files give no split answer (left out)",
                    "Of the disagreements: PaSh's own split only with a special merge step, source says no split",
                    "Lines where the source's files raised an error"], rows) + "\n")
    L.append(table(["What was checked", *[nm[s] for s in src]], [
        ["Suite output identical with the files swapped in", *[t4["output_identical"][s]["text"] for s in src]],
        ["Parts PaSh ran in parallel", *[t4["parts_parallel"][s]["text"] for s in src]],
        ["Median speed-up against bash", *[("–" if t4["median_speedup"][s] is None else f"{t4['median_speedup'][s]:.2f}x") for s in src]],
    ]) + "\n")

    L.append("## Appendix A1: the scripts\n")
    L.append(table(["2022 set", "Koala group", "Script", "Path in Koala", "Stands for", "How close", "Run here", "Input bytes"],
                   [[r["published_set"], r["group"], r["script"], f"`{r['path']}`", (f"`{r['published_script']}`" if r["published_script"] else None),
                     r["closeness"], ("yes" + (f" ({r['launches']} launches, counted once)" if r["launches"] > 1 else "")) if r["run"] else "no",
                     r["input_bytes"] if r["input_bytes"] is not None else "–"] for r in n["A1"]]) + "\n")

    L.append("## Appendix A3: why parts were not run in parallel\n")
    for mode, title, tot in (("distinct", "Distinct parts", {s: n["A3_parts_total"] for s in src}),
                             ("per_execution", "Per execution (a loop's part counts once per pass)", n["A3_executions_total"])):
        L.append(f"{title}. Each cell: the same under PaSh's own files / only with this source.\n")
        d = n["A3"][mode]
        rows = [[lab, *[f"{d[lab].get(s, {}).get('shared', 0)} / {d[lab].get(s, {}).get('only', 0)}" for s in src]]
                for lab in sorted(d)]
        rows.append(["parts considered", *[str(tot[s]) for s in src]])
        L.append(table(["Reason", *[nm[s] for s in src]], rows) + "\n")

    L.append("## Appendix A4: every use whose result differs from PaSh's own\n")
    rows = [[r["script"], f"`{r['invocation']}`", *[r["result"][s] for s in src],
             ", ".join(f"{nm[s]}: {'yes' if v else '**no**'}" for s, v in r["output_same_as_bash"].items() if s != ref)]
            for r in n["A4"]]
    L.append(table(["Script", "Command line", *[nm[s] for s in src], "Output same as bash"], rows) if rows else "None.")
    L.append("\nWhy the use was left whole, where it was:\n")
    for r in n["A4"]:
        for s, w in r["why_not"].items():
            L.append(f"- {r['script']} `{r['invocation']}`, {nm[s]}: {w}")
    L.append("\nThe files' answers on each command line the source has its own files for:\n")
    L.append(table(["Source", "Command line", "Same inputs and outputs", "Source's answer", "PaSh's own answer"],
                   [[nm[r["source"]], f"`{r['invocation']}`", {True: "yes", False: "**no**", None: "–"}[r["same_io"]],
                     r["source_answer"], r["pash_own_answer"]] for r in n["A4_answers"]]) + "\n")

    L.append("## Appendix A5: times per script (seconds, median and min–max)\n")
    cols = ["bash", *src] + [k for k in n["A5"][0] if k not in ("script", "bash", *src)] if n["A5"] else []
    rows = []
    for r in n["A5"]:
        cells = []
        for s in cols:
            t = r.get(s)
            cells.append("–" if not t else f"{t['median']:.2f} ({t['min']:.2f}–{t['max']:.2f}, {t['n']} runs)")
        rows.append([r["script"], *cells])
    L.append(table(["Script", *[nm[s] for s in cols]], rows) + "\n")

    L.append("## Appendix A6 (from the records): controls and run windows\n")
    if n["A6_controls"]:
        L.append(table(["When", "Control", "Commands split", "Output same as bash"],
                       [[c["phase"], c["label"], ", ".join(c["split_commands"]) or "none",
                         "yes" if c["output_same_as_bash"] else "**no**"] for c in n["A6_controls"]]) + "\n")
    L.append(table(["Record", "When", "Script", "Start", "End", "VM load at start", "VM load at end", "Koala changed",
                    "Mac power check"],
                   [[w["what"], w["phase"], w["id"], w["start"], w["end"], w["load_start"], w["load_end"],
                     "yes" if w["koala_changed"] else "no", w.get("power_check", "no power check")]
                    for w in n["A6_windows"]]) + "\n")

    L.append("## Checks the script made on the records\n")
    L.append(table(["Check", "Result", "Detail"],
                   [[c["check"], "passed" if c["passed"] else "**not passed**", c["detail"]] for c in n["checks"]]) + "\n")
    return "\n".join(L)


if __name__ == "__main__":
    main()
