#!/usr/bin/env python3
"""Put the full run's records (full_run/) into the shape count_report.py reads, applying the two fix-ups.

Count only. The records in full_run/ are not changed; this writes plain-JSONL copies into --out:

- Fix-up 1 (recorder fault, full_run/README.md "Faults found and fixed", 23:40): every non-bash row's
  printed output is compared again with bash's run of the same script, phase, pass and repeat. Its
  output-file flag becomes: same/different by the files' hashes when both runs kept them; same when
  neither run wrote a file; "not checked" (null) when bash ran after it in that repeat (nothing to compare
  with); otherwise the recorded flag stands.
- Fix-up 2: web-search's timed rows that stopped with "node: No such file" are left out, and every row of
  a script, pass and repeat that has a redone phase (redo-r1, redo-r3) is replaced by the redone rows.

Phases are then folded into one ("main"): the timed repeats (phases main, repeats, redo-*) keep their
repeat numbers; the second sed file's own phase (sed2) supplies its rows for the 12 oneliners/unixfun
scripts, and that phase's bash rows (used only as fix-up 1's reference) are dropped, since bash's
reference runs are the main/repeats ones. The answers are concatenated from full_run/answers/.

    python3 -I prep_full_records.py --records full_run --out <scratch folder>
"""
import argparse
import glob
import gzip
import json
import shutil
from collections import Counter
from pathlib import Path


def jl(p):
    p = Path(p)
    if p.suffix == ".gz":
        with gzip.open(p, "rt") as f:
            return [json.loads(x) for x in f if x.strip()]
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def write(p, rows):
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--records", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    R, O = a.records, a.out
    O.mkdir(parents=True, exist_ok=True)
    log = Counter()

    res = jl(R / "results.jsonl.gz")
    log["result rows read"] = len(res)
    bash = {(r["id"], r["phase"], r["mode"], r["repeat"]): r for r in res if r["set"] == "bash"}
    for r in res:
        if r["set"] == "bash":
            continue
        b = bash[(r["id"], r["phase"], r["mode"], r["repeat"])]
        was = (r["same_as_bash"], r["output_files_same_as_bash"])
        r["same_as_bash"] = r["out_sha256"] == b["out_sha256"]
        bash_later = r["order"] is not None and r["order"].index("bash") > r["order"].index(r["set"])
        if r.get("output_files_sha") and b.get("output_files_sha"):
            r["output_files_same_as_bash"] = r["output_files_sha"] == b["output_files_sha"]
        elif r["output_files"] == 0 and b["output_files"] == 0:
            r["output_files_same_as_bash"] = True
        elif bash_later:
            r["output_files_same_as_bash"] = None
        log["fix-up 1: rows compared again"] += 1
        log["fix-up 1: printed-output flag changed"] += was[0] != r["same_as_bash"]
        log["fix-up 1: output-file flag changed"] += was[1] != r["output_files_same_as_bash"]

    broken = [r for r in res if r["mode"] == "plain" and r["id"] == "web-search/engine"
              and "node" in (r.get("stderr") or "") and "No such file" in (r.get("stderr") or "")]
    res = [r for r in res if r not in broken]
    redone = {(r["id"], r["mode"], r["repeat"]) for r in res if r["phase"].startswith("redo")}
    superseded = [r for r in res if not r["phase"].startswith("redo") and (r["id"], r["mode"], r["repeat"]) in redone]
    res = [r for r in res if r not in superseded]
    log["fix-up 2: timed rows without node left out"] = len(broken)
    log["fix-up 2: rows replaced by redone rows"] = len(superseded)
    sed2_bash = [r for r in res if r["phase"] == "sed2" and r["set"] == "bash"]
    res = [r for r in res if r not in sed2_bash]
    log["sed2 phase bash rows dropped after fix-up 1"] = len(sed2_bash)
    for r in res:
        r["phase_recorded"], r["phase"] = r["phase"], "main"
    key = Counter((r["id"], r["set"], r["mode"], r["repeat"]) for r in res)
    dup = [k for k, v in key.items() if v > 1]
    if dup:
        raise SystemExit(f"duplicate rows after folding phases: {dup[:5]}")
    write(O / "results.jsonl", res)
    log["result rows written"] = len(res)

    for name in ("regions", "occurrences"):
        rows = jl(R / f"{name}.jsonl.gz")
        for r in rows:
            r["phase_recorded"], r["phase"] = r["phase"], "main"
        write(O / f"{name}.jsonl", rows)
        log[f"{name} rows"] = len(rows)
    ans = []
    for f in sorted(glob.glob(str(R / "answers" / "*.jsonl.gz"))):
        ans += [x for x in jl(f) if x.get("method") == "as PaSh passes them"]
    write(O / "answers.jsonl", ans)
    log["answer rows (as PaSh passes them)"] = len(ans)
    write(O / "commands.jsonl", jl(R / "commands.jsonl.gz"))
    for f in ("invocations.jsonl", "controls.jsonl", "controls_occurrences.jsonl", "run_windows.jsonl",
              "sets.json", "sleep_events.jsonl"):
        if (R / f).exists():   # the Caruca rerun (full_run_caruca_all/) has no controls and no sleeps
            shutil.copy(R / f, O / f)
    (O / "prep_log.json").write_text(json.dumps(log, indent=1) + "\n")
    for k, v in log.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
