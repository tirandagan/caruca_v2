#!/usr/bin/env python3
"""Task 022: build numbers_pash.md from the run records. Counts only; it never judges.

    python3 count_runs.py          # reads pash_runs.jsonl.gz, causes.jsonl, timing.jsonl, scripts.jsonl here
"""

import gzip
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATES = ["split", "not split", "PaSh error", "unknown", "timed out"]
ORDER = ["cat", "cut", "grep", "sort", "cp", "rm", "split", "wc"]


def jl(path):
    if not path.exists():
        return []
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt") as f:
        return [json.loads(x) for x in f if x.strip()]


def side_order(s):
    return (0 if s.startswith("v1-pash") else 1 if s.startswith("v1-main") else 2 if s.startswith("naive") else
            3 if s == "pash-own" else 4, s)


def label(s):
    return {"v1-pash": "v1, PaSh grammar", "v1-main": "v1, main grammar", "pash-own": "PaSh's own",
            "none": "no annotation"}.get(s, s.replace("naive:", "naive LLM, run "))


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c).replace("|", "\\|") for c in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    runs = [r for r in jl(HERE / "pash_runs.jsonl.gz") if r.get("side") != "*"]
    not_runnable = [r for r in jl(HERE / "pash_runs.jsonl.gz") if r.get("side") == "*"]
    causes = {(c["id"], c["side"]): c for c in jl(HERE / "causes.jsonl")}
    md = ["# Numbers: PaSh runs with each side's annotation files (task 022)", "",
          "Made by `count_runs.py` from `pash_runs.jsonl.gz`. Counts only. One PaSh run per command line and side, "
          "8 workers. \"Split\" needs both signals: split steps in PaSh's log and more than one copy of the command "
          "started. \"Split set up, workers got no input\" means PaSh's generated script holds several worker copies "
          "but the stream it split carried no data, so the copies never started. \"PaSh error\" means PaSh's compiler "
          "raised an exception and the script ran as plain bash. Each count is out of the runs in its row.", ""]

    by = defaultdict(list)
    for r in runs:
        by[(r["cmd"], r["side"])].append(r)
    lines_per_cmd = {c: len({r["id"] for r in runs if r["cmd"] == c}) for c in ORDER}

    # 1 ------------------------------------------------------------ what PaSh did
    md += ["## What PaSh did, per command and side", ""]
    rows = []
    for c in ORDER:
        for s in sorted({s for (cc, s) in by if cc == c}, key=side_order):
            rs = by[(c, s)]
            n = len(rs)
            st = Counter(r["state"] for r in rs)
            allow = sum(1 for r in rs if r["answer"]["allows_split"])
            wrong = sum(1 for r in rs if not r["out_same"])
            rows.append([c, label(s), n, f"{allow}", st["split"], st["split, workers idle"], st["not split"],
                         st["PaSh error"], st["unknown"] + st["timed out"], f"**{wrong}**" if wrong else 0,
                         sum(1 for r in rs if not r["rc_same"]), sum(1 for r in rs if not r["files_same"])])
    md += [table(["Command", "Side", "Lines run", "Side allows a split", "PaSh split",
                  "Split set up, workers got no input", "Not split", "PaSh error", "Unknown",
                  "Output differs from bash", "Exit code differs", "Files left differ"], rows), ""]
    fam = defaultdict(Counter)
    for r in runs:
        f = r["side"] if not r["side"].startswith("naive") else "naive LLM (all runs)"
        fam[f][r["state"]] += 1
        fam[f]["runs"] += 1
        fam[f]["allows"] += r["answer"]["allows_split"]
        fam[f]["wrong"] += not r["out_same"]
    md += ["Pooled over the eight commands:", "",
           table(["Side", "Runs", "Side allows a split", "PaSh split", "Split set up, workers got no input",
                  "Not split", "PaSh error", "Unknown", "Output differs from bash"],
                 [[label(f), k["runs"], k["allows"], k["split"], k["split, workers idle"], k["not split"],
                   k["PaSh error"], k["unknown"] + k["timed out"], k["wrong"]]
                  for f, k in sorted(fam.items(), key=lambda kv: side_order(kv[0].replace("naive LLM (all runs)", "naive")))]), ""]

    md += ["## The same, split by where the line came from", "",
           "\"Benchmark\" lines come from PaSh's benchmark scripts. \"Disagreement\" lines were picked because the "
           "sides give PaSh different splitting answers, so they overstate how often the sides differ. "
           "\"Named\" lines are the cases task 021 flagged.", ""]
    rows = []
    for c in ORDER:
        for st in ("benchmark", "disagreement", "named"):
            for s in sorted({s for (cc, s) in by if cc == c}, key=side_order):
                rs = [r for r in by[(c, s)] if r["set"] == st]
                if not rs:
                    continue
                k = Counter(r["state"] for r in rs)
                wrong = sum(1 for r in rs if not r["out_same"])
                rows.append([c, st, label(s), len(rs), k["split"], k["split, workers idle"], k["not split"],
                             k["PaSh error"], f"**{wrong}**" if wrong else 0])
    md += [table(["Command", "Lines from", "Side", "Lines run", "PaSh split", "Split set up, workers got no input",
                  "Not split", "PaSh error", "Output differs from bash"], rows), ""]

    # 2 ------------------------------------------------------------ annotation against PaSh
    md += ["## When the side allows a split, does PaSh split?", "",
           "Only runs where the side's files allow a split.", ""]
    rows = []
    for c in ORDER:
        for s in sorted({s for (cc, s) in by if cc == c}, key=side_order):
            rs = [r for r in by[(c, s)] if r["answer"]["allows_split"]]
            if not rs:
                continue
            st = Counter(r["state"] for r in rs)
            why = Counter(r["why"].split(" @ ")[0][:70] for r in rs if r["state"] != "split")
            rows.append([c, label(s), len(rs), st["split"], st["split, workers idle"], st["PaSh error"],
                         st["not split"], st["unknown"],
                         "; ".join(f"{k} ({v})" for k, v in why.most_common(3))])
    md += [table(["Command", "Side", "Allowed", "PaSh split", "Split set up, workers got no input", "PaSh error",
                  "Not split", "Unknown", "Why not (count)"], rows), ""]
    never = sum(1 for r in runs if not r["answer"]["allows_split"] and r["state"].startswith("split"))
    md += [f"Runs where the side did **not** allow a split and PaSh split anyway: **{never}** "
           f"(must be 0, or the wrong folder was loaded).", ""]

    # 3 ------------------------------------------------------------ head to head
    md += ["## v1 against each naive run, line by line", "",
           "Lines where both were run. \"Split\" here includes a split that was set up but whose workers got no "
           "input. \"Wrong\" means the output differs from bash's.", ""]
    rows = []
    for c in ORDER:
        sides = sorted({s for (cc, s) in by if cc == c}, key=side_order)
        for v in [s for s in sides if s.startswith("v1")]:
            for nv in [s for s in sides if s.startswith("naive")]:
                a = {r["id"]: r for r in by[(c, v)]}
                b = {r["id"]: r for r in by[(c, nv)]}
                ids = sorted(set(a) & set(b))
                k = Counter((a[i]["state"].startswith("split"), b[i]["state"].startswith("split")) for i in ids)
                rows.append([c, label(v), label(nv), len(ids), k[(True, True)], k[(True, False)], k[(False, True)],
                             k[(False, False)], sum(1 for i in ids if not a[i]["out_same"]),
                             sum(1 for i in ids if not b[i]["out_same"])])
    md += [table(["Command", "v1 side", "Naive run", "Lines", "Both split", "Only v1 split", "Only the agent split",
                  "Neither", "v1 output wrong", "Agent output wrong"], rows), ""]

    # 4 ------------------------------------------------------------ wrong outputs
    md += ["## Every run whose output differs from bash", ""]
    groups = defaultdict(list)
    for r in runs:
        if not r["out_same"]:
            groups[(r["cmd"], r["script"])].append(r)
    rows = []
    for (c, script), rs in sorted(groups.items()):
        cause = Counter(causes.get((r["id"], r["side"]), {}).get("cause", "not checked") for r in rs)
        rows.append([c, f"`{script}`", "; ".join(sorted({label(r['side']) for r in rs}, key=str)),
                     "; ".join(sorted({r["state"] for r in rs})),
                     "; ".join(f"{k} ({v})" for k, v in cause.most_common())])
    md += [table(["Command", "Script", "Sides", "PaSh state", "Cause (runs)"], rows) if rows else "None.", ""]
    per_side = Counter((r["cmd"], r["side"]) for r in runs if not r["out_same"])
    md += ["Wrong outputs per side, by cause:", ""]
    rows = []
    for (c, s), n in sorted(per_side.items(), key=lambda kv: (ORDER.index(kv[0][0]), side_order(kv[0][1]))):
        cc = Counter(causes.get((r["id"], r["side"]), {}).get("cause", "not checked")
                     for r in by[(c, s)] if not r["out_same"])
        rows.append([c, label(s), f"{n} of {len(by[(c, s)])}", "; ".join(f"{k} ({v})" for k, v in cc.most_common())])
    md += [table(["Command", "Side", "Wrong outputs", "Cause (runs)"], rows) if rows else "None.", ""]

    # 5 ------------------------------------------------------------ PaSh errors
    md += ["## Errors inside PaSh, by message", ""]
    err = defaultdict(Counter)
    ex = {}
    for r in runs:
        if r["state"] == "PaSh error":
            err[r["why"]][(r["cmd"], r["family"])] += 1
            ex.setdefault(r["why"], r["script"])
    rows = [[f"`{w}`", sum(k.values()), "; ".join(f"{c} {fam} ({n})" for (c, fam), n in sorted(k.items())),
             f"`{ex[w]}`"] for w, k in sorted(err.items(), key=lambda kv: -sum(kv[1].values()))]
    md += [table(["Error", "Runs", "Command and side family (runs)", "Example script"], rows) if rows else "None.", ""]
    md += ["## Why PaSh did not split, where it gave a reason", ""]
    why = defaultdict(Counter)
    for r in runs:
        if r["state"] == "not split":
            w = r["why"]
            w = "InputOutputInformation not provided, so considered side-effectful" if "not provided so considered" in w else (w[:110] or "no reason logged")
            why[w][r["family"]] += 1
    rows = [[w, sum(k.values()), "; ".join(f"{f} ({n})" for f, n in sorted(k.items()))]
            for w, k in sorted(why.items(), key=lambda kv: -sum(kv[1].values()))]
    md += [table(["Reason in PaSh's log", "Runs", "Side family (runs)"], rows), ""]

    # 6 ------------------------------------------------------------ run to run
    md += ["## Run to run", "", "Share of lines on which two sides led PaSh to the same state and the same output.", ""]
    rows = []
    for c in ORDER:
        sides = sorted({s for (cc, s) in by if cc == c}, key=side_order)
        fam = [s for s in sides if s.startswith("naive")]
        pairs = [(a, b) for i, a in enumerate(fam) for b in fam[i + 1:]]
        if "v1-pash" in sides and "v1-main" in sides:
            pairs.append(("v1-pash", "v1-main"))
        for a, b in pairs:
            ra = {r["id"]: r for r in by[(c, a)]}
            rb = {r["id"]: r for r in by[(c, b)]}
            ids = sorted(set(ra) & set(rb))
            same = sum(1 for i in ids if ra[i]["state"] == rb[i]["state"] and ra[i]["out_same"] == rb[i]["out_same"])
            rows.append([c, label(a), label(b), f"{same} of {len(ids)}"])
    md += [table(["Command", "Side", "Side", "Same state and output"], rows) if rows else "No pairs.", ""]

    # 7 ------------------------------------------------------------ timing
    timing = jl(HERE / "timing.jsonl")
    if timing:
        md += ["## Speed, on the larger input", "",
               f"Input: {timing[0]['input_bytes']:,} bytes. Median of {len(timing[0]['pash_seconds'])} runs. "
               "Only lines that split with the right output under at least one side; \"no annotation\" is the "
               "unsplit PaSh run, which shows PaSh's own overhead.", ""]
        rows = []
        for t in sorted(timing, key=lambda t: (ORDER.index(t["cmd"]), t["id"], side_order(t["side"]))):
            b, p = statistics.median(t["bash_seconds"]), statistics.median(t["pash_seconds"])
            st = Counter(t["states"]).most_common(1)[0][0]
            rows.append([t["cmd"], f"`{t['line']}`", label(t["side"]), st, "yes" if all(t["out_same"]) else "**no**",
                         f"{b:.2f}", f"{p:.2f}", f"{b / p:.2f}x"])
        md += [table(["Command", "Line", "Side", "PaSh state", "Output right", "bash (s)", "PaSh (s)",
                      "bash time / PaSh time"], rows), ""]

    heavy = jl(HERE / "timing_heavy.jsonl")
    if heavy:
        md += ["## Speed, on a command that does real work per line", "",
               f"Input: {heavy[0]['input_bytes']:,} bytes. Median of {len(heavy[0]['pash_seconds'])} runs, every "
               "side of the command. The pattern makes grep work hard on each line, so a split can show.", ""]
        rows = []
        for t_ in heavy:
            b, p_ = statistics.median(t_["bash_seconds"]), statistics.median(t_["pash_seconds"])
            st = Counter(t_["states"]).most_common(1)[0][0]
            rows.append([f"`{t_['script']}`", label(t_["side"]), "yes" if t_["allows_split"] else "no", st,
                         "yes" if all(t_["out_same"]) else "**no**", f"{b:.2f}", f"{p_:.2f}", f"{b / p_:.2f}x"])
        md += [table(["Script", "Side", "Side allows a split", "PaSh state", "Output right", "bash (s)", "PaSh (s)",
                      "bash time / PaSh time"], rows), ""]

    # 8 ------------------------------------------------------------ whole scripts
    scripts = jl(HERE / "scripts.jsonl")
    if scripts:
        md += ["## Whole benchmark scripts, each side's eight commands loaded together", ""]
        sets = sorted({s["set"] for s in scripts}, key=lambda x: ["v1-pash", "v1-main", "naive", "pash-own", "none"].index(x))
        rows = []
        for st in sets:
            rs = [s for s in scripts if s["set"] == st]
            k = Counter(s["state"] for s in rs)
            rows.append([st, len(rs), k["split"], k["not split"], k["PaSh error"], k["unknown"] + k["timed out"],
                         sum(1 for s in rs if s["out_same"]), sum(1 for s in rs if not s["out_same"])])
        md += [table(["Set loaded", "Scripts", "PaSh split", "Not split", "PaSh error", "Unknown",
                      "Output same as bash", "Output differs"], rows), ""]
        md += ["Why a script was not split (the last error in PaSh's log, or none):", ""]
        why = defaultdict(Counter)
        for s in scripts:
            if s["state"] != "split" and s["set"] != "none":
                w = s["tracebacks"][-1] if s["tracebacks"] else ("no reason logged" if s["state"] == "not split" else s["state"])
                why[w][s["set"]] += 1
        md += [table(["Reason", "Scripts, per set"],
                     [[f"`{w}`", "; ".join(f"{k} ({v})" for k, v in sorted(c.items()))]
                      for w, c in sorted(why.items(), key=lambda kv: -sum(kv[1].values()))]), ""]
        md += ["Per script. A cell lists the commands that ran as more copies than under bash "
               "(PaSh's own tr, sed and similar files are in every set).", ""]
        names = sorted({s["script"] for s in scripts})
        rows = []
        for nme in names:
            row = [f"`{nme}`"]
            for st in sets:
                s = next((x for x in scripts if x["script"] == nme and x["set"] == st), None)
                if s is None:
                    row.append("")
                    continue
                cell = s["state"] + ("" if s["out_same"] else ", **output differs**")
                if s["state"] == "split":
                    cell += " (" + ", ".join(f"{c} x{n}" for c, n in sorted(s["split_commands"].items())) + ")"
                row.append(cell)
            rows.append(row)
        md += [table(["Script"] + sets, rows), ""]

    if not_runnable:
        md += ["## Lines not run", ""] + [f"- `{r['line']}`: {r['why']}" for r in not_runnable] + [""]
    md += ["## Lines run per command", "",
           table(["Command", "Lines"], [[c, lines_per_cmd[c]] for c in ORDER if lines_per_cmd[c]]), ""]
    (HERE / "numbers_pash.md").write_text("\n".join(md))
    print(f"{len(runs)} runs -> numbers_pash.md")


def controls():
    """controls.md: the checks that PaSh is really running, before and after the batch."""
    before, after = HERE / "controls_before.json", HERE / "controls_after.json"
    if not before.exists():
        return
    b = json.loads(before.read_text())
    a = json.loads(after.read_text()) if after.exists() else None
    what = {
        "known_good_installed": "A script known to split, with PaSh's installed files",
        "known_good_copy": "The same script, with an untouched copy of those files given as a folder",
        "folder_decides": "The same script, with grep's files removed from the folder copy",
        "wrong_answer_caught": "`sort -n -u` with v1's main-grammar sort files (they allow the split)",
        "same_line_pash_own": "`sort -n -u` with PaSh's own sort files",
        "silent_fallback": "This morning's script, ending in `head -5`",
        "silent_fallback_fixed": "The same script, ending in `head -n 5`",
        "input_redirect": "Input given with `< file`",
    }
    md = ["# Checks that PaSh is really running, and really reading the files it is given", "",
          f"Run inside the virtual machine `pash` before the batch ({b['when']})"
          + (f" and again after it ({a['when']})." if a else "."), "",
          "Installed: PaSh commit `{pash_commit}`, pash-annotations {pa}, {coreutils}, {cores} cores, {kernel}.".format(
              pa=b["installed"]["pash_annotations"].replace("Version: ", ""), **b["installed"]), "",
          "\"Copies started\" is the stand-in program's count of how many copies of the watched command ran.", ""]
    rows = []
    for i, r in enumerate(b["controls"]):
        ra = a["controls"][i] if a else None
        same = "yes" if r["output_same_as_bash"] else "**no**"
        got = f"{r['state']}; copies started: {r['copies_started']}; output same as bash: {same}"
        rows.append([what.get(r["control"], r["control"]), f"`{r['script']}`", r["command_watched"], r["expect"], got,
                     ("same" if ra and (ra["state"], ra["copies_started"], ra["output_same_as_bash"]) ==
                      (r["state"], r["copies_started"], r["output_same_as_bash"]) else
                      (f"{ra['state']}; copies started: {ra['copies_started']}" if ra else "")),
                     (r["why"] or "")[:150]])
    md += [table(["Check", "Script", "Command watched", "Expected", "Before the batch", "After the batch",
                  "PaSh's reason or error"], rows), ""]
    ac = HERE / "answers_check.json"
    if ac.exists():
        c = json.loads(ac.read_text())
        md += ["## Each side's folder gives the answers we expect", "",
               f"Every line of task 021's comparison was put to every side's files inside the virtual machine, through "
               f"the same folder PaSh is pointed at. **{c['same']:,} of {c['total']:,} answers are identical** to the "
               f"ones recorded on the Mac on 2026-11-11.", ""]
    runs = [r for r in jl(HERE / "pash_runs.jsonl.gz") if r.get("side") != "*"]
    never = sum(1 for r in runs if not r["answer"]["allows_split"] and r["state"].startswith("split"))
    md += ["## During the batch", "",
           f"- Runs where a side's files did not allow a split and PaSh split anyway: **{never} of {len(runs):,}**.",
           f"- Runs with no log, or whose two signals disagreed: **{sum(1 for r in runs if r['state'] == 'unknown')}**.",
           f"- Runs with the \"no annotation\" control that split: "
           f"**{sum(1 for r in runs if r['side'] == 'none' and r['state'].startswith('split'))} of "
           f"{sum(1 for r in runs if r['side'] == 'none')}**.", ""]
    (HERE / "controls.md").write_text("\n".join(md))


if __name__ == "__main__":
    main()
    controls()
