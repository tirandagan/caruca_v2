#!/usr/bin/env python3
"""Rebuild pash_annotations_latest/: the naive LLM's PaSh annotation files, latest run per command.

Scans naive_llm_caruca/runs/*naive-run*/ for a PaSh output folder (output/annotation/ or the older
output/pash/), picks the newest run per command by the folder's timestamp prefix, copies that folder's
files byte for byte (cp -p semantics, no __pycache__) into <cmd>/, and writes README.md. Costs come from
fig7_campaign/ledger.jsonl, or for the October pilot runs from the run table in naive_llm_caruca/README.md.

    python3 refresh.py            # rebuild
    python3 refresh.py --dry-run  # print what would be copied, change nothing
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAIVE = HERE.parent
RUNS = NAIVE / "runs"
LEDGER = NAIVE / "fig7_campaign" / "ledger.jsonl"
NAIVE_README = NAIVE / "README.md"
PASH_DIRS = ("output/annotation", "output/pash")
FOLDER_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_(\d{6})_naive-run-.+_PROMPT_v\d+$")

# Notes Tiran's records attach to particular runs; keyed by run folder name.
RUN_NOTES = {
    "2026-11-24_125757_naive-run-sed-r2_sed_PROMPT_v1":
        "repeat 2, after the format-document repair (PaSh keeps quotes on operands)",
}
SUPERSEDED_WHY = {
    "2026-10-28_124823_naive-run-sed_sed_PROMPT_v1":
        "its file misreads quoted scripts because the format document never said PaSh keeps the quotes "
        "(an instrument gap, see [judgment_errors.md](../comparisons/2026-11-24_pash_suite_naive_vs_caruca/orchestration/judgment_errors.md), "
        "section 1); re-run as repeat 2",
}


def read_env(folder):
    env = {}
    p = folder / "run.env"
    if p.exists():
        for line in p.read_text(errors="replace").splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                env.setdefault(k.strip(), v.strip())
    return env


def ledger_costs():
    costs = {}
    if not LEDGER.exists():
        return costs
    for line in LEDGER.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        name = Path(r["run_folder"]).name
        if r.get("billed_usd") is not None:
            costs[name] = f"${r['billed_usd']:.2f} (billed)"
        elif r.get("claude_cost_usd") is not None:
            costs[name] = f"${r['claude_cost_usd']:.2f} (Claude Code's figure)"
        if r.get("repeat"):
            costs[name + "#repeat"] = r["repeat"]
    return costs


def readme_costs():
    """Costs of the pilot runs, from the run table rows that link to runs/<folder>/."""
    costs = {}
    if not NAIVE_README.exists():
        return costs
    for line in NAIVE_README.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.split("|")]
        cost = next((c for c in cells if re.fullmatch(r"\$[\d.,]+", c)), None)
        if not cost:
            continue
        m = re.search(r"\(runs/([^/)]+)/", line)
        if m:
            costs.setdefault(m.group(1), f"{cost} (run log)")
        # rows without a link: key by (date, command), e.g. "| 10 | 2026-10-26 | `dirname` (...) |"
        d = next((c for c in cells if re.fullmatch(r"\d{4}-\d{2}-\d{2}", c)), None)
        c = re.search(r"`([^`]+)`", line)
        if d and c:
            costs.setdefault((d, c.group(1)), f"{cost} (run log)")
    return costs


def scan():
    runs, without = [], []
    for folder in sorted(RUNS.iterdir()):
        m = FOLDER_RE.match(folder.name)
        if not folder.is_dir() or not m:
            continue
        env = read_env(folder)
        name_cmd = folder.name.split("_")[-3]
        cmd = env.get("command", name_cmd)
        if cmd != name_cmd:
            print(f"warning: {folder.name}: run.env says {cmd!r}, folder name says {name_cmd!r}",
                  file=sys.stderr)
        pash = [folder / d for d in PASH_DIRS if (folder / d).is_dir()]
        files = []
        if pash:
            files = sorted(p for p in pash[0].iterdir() if p.is_file())
        rec = dict(folder=folder, cmd=cmd, stamp=m.group(1) + m.group(2), date=m.group(1),
                   prompt=env.get("prompt_version", folder.name.rsplit("_", 1)[-1]),
                   pash=pash[0] if pash else None, files=files, all_pash=pash)
        (runs if files else without).append(rec)
    return runs, without


def stray_pash_files():
    """PaSh-format files anywhere in a run folder other than its PaSh output folder."""
    hits = []
    for folder in RUNS.iterdir():
        if not FOLDER_RE.match(folder.name):
            continue
        for p in folder.rglob("*InfoGenerator*.py"):
            rel = p.relative_to(folder).as_posix()
            if "__pycache__" not in rel and not any(rel.startswith(d + "/") for d in PASH_DIRS):
                hits.append(p)
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    runs, without = scan()
    by_cmd = {}
    for r in runs:
        by_cmd.setdefault(r["cmd"], []).append(r)
    for lst in by_cmd.values():
        lst.sort(key=lambda r: r["stamp"])
    costs = {**readme_costs(), **ledger_costs()}

    for r in runs:
        if len(r["all_pash"]) > 1:
            print(f"warning: {r['folder'].name} has both PaSh layouts; used {r['pash']}", file=sys.stderr)
    stray = stray_pash_files()
    for p in stray:
        print(f"warning: PaSh-format file outside the PaSh folder: {p}", file=sys.stderr)

    for cmd in sorted(by_cmd):
        latest = by_cmd[cmd][-1]
        for f in latest["files"]:
            print(f"copy {f.relative_to(NAIVE)} -> pash_annotations_latest/{cmd}/{f.name}")
    if args.dry_run:
        print(f"{len(by_cmd)} commands, {len(runs) + len(without)} run folders scanned (dry run)")
        return

    for child in HERE.iterdir():  # rebuild the command folders from scratch
        if child.is_dir():
            shutil.rmtree(child)
    for cmd, lst in by_cmd.items():
        dest = HERE / cmd
        dest.mkdir()
        for f in lst[-1]["files"]:
            shutil.copy2(f, dest / f.name)

    def link(r):
        n = r["folder"].name
        return f"[{n[:17]}…](../runs/{n}/)"

    out = [
        "# The naive LLM's PaSh annotation files, latest run per command",
        "",
        "One folder per command for which the naive LLM (a fresh Claude Code session given only the "
        "binary, its manual and the format descriptions) has written PaSh annotation files. Each folder "
        "holds byte-for-byte copies of the PaSh output folder of that command's **latest** run "
        "(`output/annotation/`, or `output/pash/` in the October pilot runs); the run's syntax file "
        "(`output/<cmd>.py`) is not copied. Nothing here is edited: the run folders under `../runs/` stay "
        "the record, and this folder is rebuilt from them by `refresh.py`.",
        "",
        f"{len(by_cmd)} commands, from {len(runs) + len(without)} run folders. "
        "Cost: \"billed\" is what the billing service charged (campaign ledger); \"Claude Code's figure\" "
        "is Claude Code's own estimate, used where no bill is available; \"run log\" is the cost in the run "
        "table of `../README.md` (pilot runs, which predate the ledger).",
        "",
        "| Command | Files | Run folder | Run date | Prompt | Cost | Note |",
        "|---|---|---|---|---|---|---|",
    ]
    for cmd in sorted(by_cmd):
        r = by_cmd[cmd][-1]
        n = r["folder"].name
        names = ", ".join(f"`{f.name}`" for f in r["files"])
        note = RUN_NOTES.get(n, "")
        rep = costs.get(n + "#repeat")
        if not note and rep and rep > 1:
            note = f"repeat {rep}"
        if not note and n not in costs:
            note = "pilot run (before the campaign ledger)"
        if not (r["folder"] / "output" / "annotation").is_dir():
            note = (note + "; " if note else "") + "older layout `output/pash/`"
        out.append(f"| `{cmd}` | {len(r['files'])}: {names} | {link(r)} | {r['date']} | {r['prompt']} "
                   f"| {costs.get(n) or costs.get((r['date'], cmd), '—')} | {note} |")

    out += ["", "## Runs without PaSh files", ""]
    if without:
        out += [f"- `{r['cmd']}`: {link(r)}" for r in without]
    else:
        out.append("None: every run folder has a PaSh output folder with files in it.")
    if stray:
        out += ["", "PaSh-format files found outside a run's PaSh folder:", ""]
        out += [f"- `{p.relative_to(NAIVE)}`" for p in stray]

    out += ["", "## Superseded runs", "",
            "Older runs of a command that has a later one. Their files are not copied here.", ""]
    for cmd in sorted(by_cmd):
        for r in by_cmd[cmd][:-1]:
            why = SUPERSEDED_WHY.get(r["folder"].name)
            out.append(f"- `{cmd}`: {link(r)} ({r['date']})" + (f": {why}" if why else ""))

    out += ["", "## How to refresh", "",
            "Run `python3 naive_llm_caruca/pash_annotations_latest/refresh.py` from the repository root "
            "(add `--dry-run` to see what it would copy). It scans every `runs/*_naive-run-*_PROMPT_v*` "
            "folder, takes the command from `run.env` (checked against the folder name), finds the PaSh "
            "folder (`output/annotation/` or `output/pash/`), keeps the run with the newest timestamp per "
            "command, deletes and recreates the command folders here, copies the files with their times "
            "kept (no `__pycache__`), and rewrites this README. Costs come from "
            "`fig7_campaign/ledger.jsonl`, or for pilot runs from `../README.md`. Notes on particular runs "
            "(such as why a run was superseded) live in `RUN_NOTES` and `SUPERSEDED_WHY` at the top of the "
            "script; add one there when a run is re-done for a reason.", ""]
    (HERE / "README.md").write_text("\n".join(out))
    print(f"{len(by_cmd)} commands, {len(runs) + len(without)} run folders scanned, "
          f"{len(without)} without PaSh files, {len(stray)} stray PaSh files")


if __name__ == "__main__":
    main()
