#!/usr/bin/env python3
"""Check that the Mac was awake and on mains power during every timed run window (report plan 5.3).

Runs on the Mac, standard library only:

    python3 -I timing_check.py --windows <records>/run_windows.jsonl --out <records>/timing_check.jsonl

Reads the run windows the builder recorded, the Mac's power log (`pmset -g log`) and its battery status
(`pmset -g batt`), and writes one line per window: the sleep and wake events inside it, whether the Mac
was asleep when it started, the power source in force at its start and end (the last "Using AC" /
"Using Batt" entry in the power log at or before that moment), and whether the window is valid. A
window is valid only when there is no sleep or wake event inside it, the Mac was not asleep at its
start, the power source at both ends is mains power, and the VM's clock (which the windows use) is
within 5 s of the Mac's (which the power log uses). The offset comes from one read-only `date` call in
the VM when this script runs, recorded on every line; it is the offset now, not at the window.
count_report.py fails every window that is
not valid.

Times inside the Lima VM include any time the Mac slept, so a window with a sleep has wrong times.
`--pmset-log FILE` reads a saved copy of the power log instead of calling pmset (for re-checking later:
macOS keeps only a few days of the log).
"""
import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

FMT = "%Y-%m-%d %H:%M:%S %z"
LINE = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d [+-]\d{4}) (\S+(?: \S+)*?)\s{2,}\t?(.*)$")
SLEEP_TYPES = {"Sleep", "Wake", "DarkWake"}
POWER = re.compile(r"Using (AC|Batt|BATT)\b", re.I)


def die(msg):
    sys.exit(f"timing_check.py: {msg}")


def read_power_log(path):
    text = Path(path).read_text(errors="replace") if path else \
        subprocess.run(["pmset", "-g", "log"], capture_output=True, text=True, check=True).stdout
    events, power = [], []
    for raw in text.splitlines():
        m = LINE.match(raw)
        if not m:
            continue
        t = datetime.strptime(m.group(1), FMT)
        kind, rest = m.group(2).strip(), m.group(3).strip()
        if kind in SLEEP_TYPES:
            events.append({"time": m.group(1), "t": t, "type": kind, "text": rest[:200]})
        p = POWER.search(rest)
        if p:
            power.append((t, "mains" if p.group(1).upper() == "AC" else "battery", m.group(1)))
    if not events and not power:
        die("the power log has no sleep, wake or power-source entries; is this the output of `pmset -g log`?")
    events.sort(key=lambda e: e["t"])
    power.sort()
    first = min([e["t"] for e in events] + [p[0] for p in power])
    return events, power, first


def power_at(power, t):
    before = [p for p in power if p[0] <= t]
    if not before:
        return {"source": None, "seen_at": None}
    return {"source": before[-1][1], "seen_at": before[-1][2]}


MAX_OFFSET = 5.0   # seconds; a larger gap between the VM's clock and the Mac's fails every window


def vm_clock_offset(vm):
    """One read-only `date` call in the VM. Offset = VM time minus Mac time, at the middle of the call."""
    t0 = time.time()
    r = subprocess.run(["limactl", "shell", vm, "--", "date", "+%s.%N"], capture_output=True, text=True, timeout=60)
    t1 = time.time()
    if r.returncode != 0:
        die(f"could not read the clock of VM '{vm}': {r.stderr.strip()[:300]}")
    return round(float(r.stdout.strip()) - (t0 + t1) / 2, 3), round(t1 - t0, 3)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--windows", type=Path, required=True, help="run_windows.jsonl")
    ap.add_argument("--out", type=Path, required=True, help="where timing_check.jsonl goes")
    ap.add_argument("--pmset-log", type=Path, help="a saved copy of `pmset -g log` (default: run pmset)")
    ap.add_argument("--vm", default="pash", help="the Lima VM whose clock the windows use (default: pash)")
    ap.add_argument("--clock-offset", type=float,
                    help="a VM-minus-Mac clock offset measured earlier, in seconds, instead of asking the VM")
    a = ap.parse_args()

    if not a.windows.exists():
        die(f"not found: {a.windows}")
    events, power, log_starts = read_power_log(a.pmset_log)
    batt_now = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True).stdout.strip() \
        if not a.pmset_log else None
    checked_at = datetime.now().astimezone().strftime(FMT)
    if a.clock_offset is not None:
        offset, call_s, offset_how = a.clock_offset, None, "given with --clock-offset"
    else:
        offset, call_s = vm_clock_offset(a.vm)
        offset_how = f"`date` in VM {a.vm} against the Mac's clock, at {checked_at}"

    out = []
    for n, line in enumerate(a.windows.read_text().splitlines(), 1):
        if not line.strip():
            continue
        w = json.loads(line)
        for f in ("what", "phase", "id", "start", "end"):
            if f not in w:
                die(f"{a.windows.name}:{n}: field '{f}' is missing")
        s, e = datetime.strptime(w["start"], FMT), datetime.strptime(w["end"], FMT)
        inside = [{k: v for k, v in ev.items() if k != "t"} for ev in events if s <= ev["t"] <= e]
        last_before = [ev for ev in events if ev["t"] < s]
        asleep = bool(last_before) and last_before[-1]["type"] == "Sleep"
        p_start, p_end = power_at(power, s), power_at(power, e)
        problems = []
        if s < log_starts:
            problems.append("the power log does not reach back to this window")
        if inside:
            problems.append(f"{len(inside)} sleep or wake events inside the window")
        if asleep:
            problems.append("the last power-log event before the window is a sleep")
        if abs(offset) > MAX_OFFSET:
            problems.append(f"the VM's clock differs from the Mac's by {offset:+.1f} s (limit {MAX_OFFSET:g} s)")
        for when, p in (("start", p_start), ("end", p_end)):
            if p["source"] != "mains":
                problems.append(f"power source at the {when}: {p['source'] or 'not recorded'}")
        out.append({"what": w["what"], "phase": w["phase"], "id": w["id"], "start": w["start"], "end": w["end"],
                    "sleep_wake_events": inside, "asleep_at_start": asleep,
                    "power_at_start": p_start, "power_at_end": p_end,
                    "vm_clock_offset_s": offset, "vm_clock_offset_how": offset_how,
                    "vm_clock_call_s": call_s,
                    "valid": not problems, "problems": problems,
                    "checked_at": checked_at, "power_log": str(a.pmset_log) if a.pmset_log else "pmset -g log",
                    "battery_status_when_checked": batt_now})
    a.out.write_text("".join(json.dumps(r) + "\n" for r in out))
    bad = [r for r in out if not r["valid"]]
    print(f"wrote {a.out}: {len(out) - len(bad)} of {len(out)} windows valid")
    for r in bad:
        print(f"  not valid: {r['what']} {r['phase']} {r['id']} {r['start']}: {'; '.join(r['problems'])}")


if __name__ == "__main__":
    main()
