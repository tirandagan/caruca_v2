"""Join the two logs of one naive run into one record per program run.

- `tries.log`: written by naive_llm_caruca/vm/exec-log.bt (bpftrace). Kernel-side facts: when each program
  started (S), its parent (F), its exit status (X), the first bytes of its error output (W).
- `audit.log`: the kernel audit records of every successful execve (rule key `naive-exec`, added by
  naive-run). The complete argument list (EXECVE), the executable (SYSCALL `exe=`) and the file named in
  the call (PATH item 0, with CWD for relative names).

A process can run several programs in turn (`env cut …` runs `env`, then `cut`, in one process); each is
a separate run, ending at the next start in that process or at its exit. Audit and bpftrace events for the
same process are matched in order. Wall-clock times come from the audit timestamps; bpftrace's boot-time
clock is aligned to them by the median offset over all matched starts.

    python3 execlog.py tries.log audit.log [PATH_MAP]    # summary of the commonest programs
"""
import collections
import json
import re
import statistics
import sys

TAG = re.compile(r"^([BFSWX])\t(\d+)(?:\t|$)")
AUDIT = re.compile(r"^type=(\w+) msg=audit\(([\d.]+):(\d+)\): (.*)$")
ARG = re.compile(r"\ba(\d+)(?:\[\d+\])?=(\"[^\"]*\"|[0-9A-F]+|\(null\))")


def unescape(r):
    """bpftrace's %r prints non-printable bytes as \\xNN; rebuild the bytes and decode them as UTF-8, so that
    GNU's curly quotes (\\xe2\\x80\\x98) come back as one character, not three."""
    out, i = bytearray(), 0
    for m in re.finditer(r"\\x([0-9a-fA-F]{2})", r):
        out += r[i:m.start()].encode("utf-8")
        out.append(int(m.group(1), 16))
        i = m.end()
    out += r[i:].encode("utf-8")
    return out.decode("utf-8", "replace")


def unhex(v):
    """audit writes a value in quotes when it is plain, and as hex when it holds spaces or odd bytes."""
    if v.startswith('"'):
        return v[1:-1]
    if v == "(null)":
        return ""
    try:
        return bytes.fromhex(v).decode("utf-8", "replace")
    except ValueError:
        return v


def field(body, name, text=False):
    """A field's value; text fields (exe, name, cwd) may be hex-encoded, numbers never are."""
    m = re.search(rf"(?<![A-Za-z_]){name}=(\"[^\"]*\"|[^\s\x1d]+)", body)
    if not m:
        return None
    return unhex(m.group(1)) if text else m.group(1)


def read_audit_events(path):
    """Every audit event in the file, in order: {"ts": epoch seconds, "<record type>": [record bodies]}."""
    events = collections.OrderedDict()
    for ln in open(path, encoding="utf-8", errors="replace"):
        m = AUDIT.match(ln.rstrip("\n"))
        if m:
            t, ts, ev, body = m.groups()
            events.setdefault(ev, {"ts": float(ts)}).setdefault(t, []).append(body)
    return list(events.values())


def read_audit(path, since=None):
    """Successful execve events at or after `since` (epoch seconds), in order: pid, ppid, wall time, argv,
    exe, the name passed, cwd."""
    starts = []
    for ev in read_audit_events(path):
        sc = (ev.get("SYSCALL") or [""])[0]
        if "success=yes" not in sc or "EXECVE" not in ev or 'key="naive-exec"' not in sc:
            continue
        if since is not None and ev["ts"] < since:
            continue
        body = " ".join(ev["EXECVE"])
        argc = int(re.search(r"argc=(\d+)", body).group(1))
        args = collections.defaultdict(str)
        for k, v in ARG.findall(body):
            args[int(k)] += unhex(v)
        name = None
        for p in ev.get("PATH", []):
            if re.search(r"\bitem=0\b", p):
                name = field(p, "name", text=True)
        starts.append({
            "pid": int(field(sc, "pid")), "ppid": int(field(sc, "ppid")), "start": ev["ts"],
            "argv": [args.get(i, "") for i in range(argc)], "exe": field(sc, "exe", text=True),
            "name": name, "cwd": field((ev.get("CWD") or [""])[0], "cwd", text=True), "uid": int(field(sc, "uid")),
        })
    return starts


def read_trace(path):
    lines = []
    for raw in open(path, encoding="utf-8", errors="replace"):
        raw = raw.rstrip("\n")
        if TAG.match(raw):
            lines.append(raw.split("\t"))
    return lines


def read(trace_path, audit_path, since=None):
    """One record per program run, in start order. `since`: the logger's start, epoch seconds (run.env)."""
    starts = read_audit(audit_path, since)
    by_pid = collections.defaultdict(list)
    for s in starts:
        by_pid[s["pid"]].append(s)
    parent, s_events = {}, collections.defaultdict(list)
    runs, current = [], {}
    pending = {pid: collections.deque(v) for pid, v in by_pid.items()}
    offsets = []
    for f in read_trace(trace_path):
        tag, ns = f[0], int(f[1])
        if tag == "F":
            parent[int(f[3])] = int(f[2])
        elif tag == "S":
            pid = int(f[2])
            if pid in current:
                runs[current[pid]].setdefault("end_ns", ns)
            a = pending.get(pid)
            s = a.popleft() if a else None
            run = dict(s) if s else {"pid": pid, "ppid": parent.get(pid), "argv": None, "exe": None,
                                     "name": None, "cwd": None, "start": None}
            run.update({"path": "\t".join(f[3:]), "start_ns": ns, "stderr": "", "status": None})
            if s:
                offsets.append(s["start"] - ns / 1e9)
            runs.append(run)
            current[pid] = len(runs) - 1
        elif tag == "W":
            pid = int(f[2])
            if pid in current:
                runs[current[pid]]["stderr"] += unescape("\t".join(f[4:]))
        elif tag == "X":
            pid = int(f[2])
            if pid in current:
                r = runs[current.pop(pid)]
                r["status"] = int(f[3])
                r.setdefault("end_ns", ns)
    off = statistics.median(offsets) if offsets else None
    unmatched_audit = sum(len(q) for q in pending.values())
    for r in runs:
        st = r["status"]
        r["exit_code"] = None if st is None or st & 0x7F else (st >> 8) & 0xFF
        r["signal"] = None if st is None or not st & 0x7F else st & 0x7F
        r["seconds"] = (r["end_ns"] - r["start_ns"]) / 1e9 if "end_ns" in r else None
        if r["start"] is None and off is not None:
            r["start"] = off + r["start_ns"] / 1e9
        r["end"] = off + r["end_ns"] / 1e9 if off is not None and "end_ns" in r else None
    for r in runs:                       # parents of processes that never ran a program of their own (subshells)
        r.setdefault("ppid", None)
        if r["ppid"] is None:
            r["ppid"] = parent.get(r["pid"])
    read.parent = parent                 # pid -> parent pid, from fork events
    return runs, {"audit_starts": len(starts), "trace_starts": len(runs),
                  "audit_without_trace": unmatched_audit,
                  "trace_without_audit": sum(r["argv"] is None for r in runs),
                  "clock_offset_s": off,
                  "clock_spread_ms": (max(offsets) - min(offsets)) * 1000 if offsets else None}


def path_map(path):
    m = {}
    for ln in open(path, encoding="utf-8"):
        if "\t" in ln:
            a, b = ln.rstrip("\n").split("\t", 1)
            m[a] = b
    return m


if __name__ == "__main__":
    runs, check = read(sys.argv[1], sys.argv[2])
    pm = path_map(sys.argv[3]) if len(sys.argv) > 3 else {}
    count = collections.Counter(pm.get(r["path"], r["path"]) for r in runs)
    print(json.dumps({"check": check, "commonest": dict(count.most_common(15))}, indent=1))
