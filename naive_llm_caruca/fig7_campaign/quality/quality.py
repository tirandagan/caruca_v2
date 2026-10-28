#!/usr/bin/env python3
"""Task 019 quality check: grade the files each run produced, every fact settled by running the program.

First use (2026-10-28): the model comparison Tiran asked for. The five pilot commands (dd, ls, cut, test,
convert) were run once with Fable 5.1 at medium effort (the campaign's model) and once with Opus 5.5 at
extra-high effort; this grades both runs' files with the same rules, fixed before either was scored.

For each command, the files graded are: each agent run's syntax file (output/<cmd>.py) and its PaSh parser
table (output/annotation/<cmd>.json), and, for context, Caruca's reference grammar, Caruca's shipped GPT-4o
grammar and the GPT-4o grammar Caruca's own model step made again on 2026-10-27
(caruca_side/v1_llm_step.py). Grades, never blended:

  Syntax file   task 018's program-checked accuracy, facts a to h (facts19.py, a copy of task 018's with
                the additions it lists). For `test` only facts a (every real operator is listed) and b
                (every listed spelling is real), since test is an expression language, not options before
                operands.
  Parser table  facts a, b and c (a flag takes no value, an option takes one) for the table's spellings,
                judged by the same probe of the program (probe19.py).
  Answer key    agreement with Caruca's reference grammar (task 018's paper-comparable score).
  Cost          from the campaign ledger: OpenRouter's bill, wall time, turns, tokens, program runs.

    .venv/bin/python naive_llm_caruca/fig7_campaign/quality/quality.py dd ls cut test convert
    .venv/bin/python naive_llm_caruca/fig7_campaign/quality/quality.py --table

Needs the VM t019-probe running. Writes results/<cmd>.json and results/summary.md beside this file.
"""
import json, subprocess, sys, tempfile, time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAMPAIGN = HERE.parent
REPO = CAMPAIGN.parents[1]
sys.path.insert(0, str(REPO / "naive_llm_caruca/scoring"))
import score_t018 as t018  # noqa: E402  task 018's scorer: its generic parts are reused unchanged
sys.path.insert(0, str(HERE))
import facts19  # noqa: E402

V1 = Path.home() / "dev/stevens/caruca"
PROBE_VM = "t019-probe"
RESULTS = HERE / "results"
ARMS = {"main": "fable 5.1 medium", "opus55-xhigh": "opus 5.5 xhigh"}
COMMANDS = ["dd", "ls", "cut", "test", "convert"]


def ledger():
    return [json.loads(l) for l in open(CAMPAIGN / "ledger.jsonl")]


def runs(cmd):
    """label -> ledger row, for every finished run of cmd (first repeat only)."""
    out = {}
    for d in ledger():
        if d["command"] == cmd and d.get("repeat", 1) == 1 and d.get("status") == "ok":
            out[ARMS.get(d.get("arm", "main"), d.get("arm"))] = d
    return out


def sources(cmd):
    out = {"reference": V1 / f"caruca/src/caruca/syntax_specs/{cmd}.py",
           "gpt-4o (shipped)": V1 / f"outputs/llm-dsl-generation/{cmd}.py",
           "gpt-4o (rerun 2026-10-27)": CAMPAIGN / f"v1_llm/{cmd}.py"}
    for label, d in runs(cmd).items():
        out[label] = REPO / d["run_folder"] / "output" / f"{cmd}.py"
    return {k: v for k, v in out.items() if v.is_file()}


def tables(cmd):
    out = {}
    for label, d in runs(cmd).items():
        p = REPO / d["run_folder"] / "output" / "annotation" / f"{cmd}.json"
        if p.is_file():
            out[label] = p
    return out


def table_spellings(path):
    """(spelling, takes a value) for every entry of a PaSh parser table."""
    t = json.loads(path.read_text())
    out = []
    for e in t.get("flag", []):
        for s in ([e] if isinstance(e, str) else e):
            out.append((s, False))
    for e in t.get("option", []):
        for s in e[:-1]:
            if isinstance(s, str):
                out.append((s, True))
    return out


def probe(cmd, spellings):
    with tempfile.TemporaryDirectory() as tmp:
        cand = Path(tmp) / "candidates.json"
        cand.write_text(json.dumps({"spellings": sorted(spellings)}))
        subprocess.run(["limactl", "copy", str(cand), f"{PROBE_VM}:/tmp/t019_candidates.json"], check=True)
        subprocess.run(["limactl", "copy", str(HERE / "probe19.py"), f"{PROBE_VM}:/tmp/t019_probe.py"], check=True)
        p = subprocess.run(["limactl", "shell", PROBE_VM, "--", "python3", "/tmp/t019_probe.py", cmd,
                            "/tmp/t019_candidates.json"], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"probe failed for {cmd}: {p.stderr[-800:]}")
    return json.loads(p.stdout)


def table_score(cmd, entries, probed):
    """Facts a, b, c for a parser table, as task 018's binary_score grades a syntax file's spellings."""
    sp = probed["spellings"]
    name = lambda s: s.split("=", 1)[0] if s.startswith("--") else s  # noqa: E731
    real = {name(s) for s, v in sp.items() if v["accepted"]}
    listed = {s for s, _ in entries}
    says = {}
    for s, v in entries:
        if sp.get(s, {}).get("accepted"):
            says.setdefault(s, set()).add(v)
    types = {"a listed": [len(real & {name(s) for s in listed}), len(real)],
             "b real": [sum(1 for s in listed if sp.get(s, {}).get("accepted")), len(listed)]}
    wrong = {"a listed": sorted(real - {name(s) for s in listed}),
             "b real": sorted(s for s in listed if not sp.get(s, {}).get("accepted"))}
    if cmd != "test":
        agree, bad = 0, []
        for s, v in sorted(says.items()):
            b = sp[s]["value"]
            if b == "optional" or v == {b == "required"}:
                agree += 1
            else:
                bad.append([s, "table: " + " and ".join("option" if x else "flag" for x in sorted(v)), f"binary: {b}"])
        types["c value"] = [agree, len(says)]
        wrong["c value"] = bad
    return {"types": types, "right": sum(r for r, _ in types.values()), "total": sum(t for _, t in types.values()),
            "wrong": wrong}


def score(cmd):
    files, tabs = sources(cmd), tables(cmd)
    print(f"== {cmd}: {', '.join(files)}; tables: {', '.join(tabs)}", flush=True)
    started = time.time()
    spellings = set()
    for path in files.values():
        for e in t018.flag_entries(path, cmd) or []:
            spellings.update([e["flag"], *e["alias"]])
    for path in tabs.values():
        spellings.update(s for s, _ in table_spellings(path))
    probed = probe(cmd, spellings)
    out = {"command": cmd, "scored": datetime.now().isoformat(timespec="seconds"), "probe_vm": PROBE_VM,
           "binary_version": probed["version"], "caruca_v1_commit": t018.v1.v1_commit(), "files": {}, "tables": {}}
    score2 = {}
    for label, path in files.items():
        entries = t018.flag_entries(path, cmd)
        score2[label] = t018.binary_score(entries, probed)
        out["files"][label] = {"path": str(path.relative_to(REPO) if path.is_relative_to(REPO) else path),
                               "real_binary": score2[label]}
        if label != "reference":
            out["files"][label]["answer_key"] = t018.answer_key(cmd, path)
    if cmd == "test":
        for label, s2 in score2.items():
            if "error" in s2:
                out["files"][label]["program_checked"] = s2
                continue
            types = {"a listed": [s2["real_spellings_in_file"], s2["real_spellings_all_sources"]],
                     "b real": [s2["spellings_accepted"], s2["spellings_in_file"]]}
            out["files"][label]["program_checked"] = {
                "types": types, "right": sum(r for r, _ in types.values()), "total": sum(t for _, t in types.values()),
                "wrong": {"a listed": s2["real_spellings_missing"], "b real": s2["spellings_rejected"]}}
    else:
        print("   program-checked facts", flush=True)
        facts, fruns = facts19.program_facts(cmd, files, score2, probed)
        for label, f in facts.items():
            out["files"][label]["program_checked"] = f
        out["facts_runs"] = fruns
    for label, path in tabs.items():
        out["tables"][label] = {"path": str(path.relative_to(REPO)), **table_score(cmd, table_spellings(path), probed)}
    out["runs"] = {label: {k: d.get(k) for k in ("run_folder", "model", "effort", "billed_usd", "wall_s", "turns",
                                                  "tokens", "status")} | {"tries": (d.get("tries") or {}).get("tries"),
                                                                          "refused": (d.get("tries") or {}).get("classes", {}).get("refused")}
                   for label, d in runs(cmd).items()}
    out["probe"] = probed
    out["scoring_seconds"] = round(time.time() - started)
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{cmd}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False, default=str))


def pct(r, t):
    return "n/a" if not t else f"{r:,}/{t:,} ({100 * r / t:.0f}%)"


def table(commands=COMMANDS):
    data = [json.loads((RESULTS / f"{c}.json").read_text()) for c in commands if (RESULTS / f"{c}.json").is_file()]
    syn, tab, key, cost = [], [], [], []
    pooled = {}
    for d in data:
        c = d["command"]
        for label, r in d["files"].items():
            pc = r.get("program_checked", {})
            if "error" in pc:
                syn.append(f"| `{c}` | {label} | {pc['error']} | |")
            if "types" in pc:
                cells = " | ".join(f"{v[0]}/{v[1]}" for v in pc["types"].values())
                syn.append(f"| `{c}` | {label} | **{pct(pc['right'], pc['total'])}** | {cells} |")
                p = pooled.setdefault(label, [0, 0, 0, 0])
                p[0] += pc["right"]; p[1] += pc["total"]
            ak = (r.get("answer_key") or {}).get("v1-specs", {})
            if ak.get("counts"):
                k = ak["counts"]
                key.append(f"| `{c}` | {label} | {k['matched']}/{k['reference_flags']} | {k['spurious']} |")
        for label, t in d["tables"].items():
            cells = " | ".join(f"{k}: {v[0]}/{v[1]}" for k, v in t["types"].items())
            tab.append(f"| `{c}` | {label} | **{pct(t['right'], t['total'])}** | {cells} |")
            p = pooled.setdefault(label, [0, 0, 0, 0])
            p[2] += t["right"]; p[3] += t["total"]
        for label, r in d["runs"].items():
            tk = r.get("tokens") or {}
            cost.append(f"| `{c}` | {label} | ${r['billed_usd']:.2f} | {r['wall_s']:.0f} s | {r['turns']} | "
                        f"{tk.get('output', 0):,} | {r.get('tries') or 0:,} | {r.get('refused') or 0:,} |")
    pool = [f"| {label} | {pct(p[0], p[1])} | {pct(p[2], p[3])} | **{pct(p[0] + p[2], p[1] + p[3])}** |"
            for label, p in pooled.items() if p[3]]
    text = "\n".join([
        "## Pooled over the commands: facts right / all facts", "",
        "| Run | Syntax files | Parser tables | Both |", "|---|---|---|---|", *pool, "",
        "## Syntax file: program-checked accuracy (task 018's facts; `test`: a and b only)", "",
        "| Command | File | Right | Per fact type (a listed, b real, c value, d kind, e equals, f repeat, g files, h rules) |",
        "|---|---|---|---|", *syn, "",
        "## Parser table (PaSh's `<cmd>.json`): facts a, b, c", "",
        "| Command | Run | Right | Per fact type |", "|---|---|---|---|", *tab, "",
        "## Agreement with Caruca's reference grammar", "",
        "| Command | File | Reference options matched | Extra options |", "|---|---|---|---|", *key, "",
        "## Cost (OpenRouter's bill)", "",
        "| Command | Run | Billed | Wall time | Turns | Output tokens (as streamed) | Program runs | Refused (provisional) |",
        "|---|---|---|---|---|---|---|---|", *cost, ""])
    (RESULTS / "summary.md").write_text(text)
    print(text)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args != ["--table"]:
        for cmd in args:
            score(cmd)
    table()
