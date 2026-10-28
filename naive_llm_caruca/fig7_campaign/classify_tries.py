"""Sort every run of the target program in one naive run into the classes of task 019, section 3.2.

    python3 classify_tries.py <run folder> [--json OUT]      # prints a summary; --json writes every try

Reads the run folder that naive-run wrote: run.env, tries.log and audit.log (joined by execlog.py),
paths.tsv, audit_output.log, and the session transcript. The rules are fixed here, before any real run
was classified (2026-10-27):

1. A start counts only if it is the target program (its file, after symbolic links, is the run's
   binary_real, or `[` for `test`) and it descends from the session's `claude` process, with no
   machinery program in between (MACHINERY: `man` and its formatters, package tools).
2. Working-tool use is excluded from the tries and listed for checking by hand:
   T1 every file operand is one of the task's own materials (formats/, samples/, output/, the prompts, a
      manual page);
   T2 it is a later stage of a pipeline (after `|`) whose first command reads a manual (`man …`) or a task
      material, in the shell command the agent ran;
   T3 it has no file operand and the agent's command writes its output into output/ (`cat > output/x`);
   T4 it is the last stage of a pipeline whose first command is one of the agent's own scripts or a
      lookup program (FIRST_STAGE_TOOLS), i.e. it trims or sorts the agent's own output for reading.
3. Each try is classed by exit status and error output: refused (the program rejected the command line:
   REFUSED patterns, or the program's own usage exit code), other non-zero (RUNTIME patterns, or a
   non-zero exit with no message), accepted (exit 0; --help/--version counted apart), ended by a signal,
   unfinished (still running when the loggers stopped), or unclassified (a message no pattern matches;
   listed for assignment by hand).
4. Exploring vs testing: before or after the first deliverable file appeared in output/ (audit watch).
"""
import collections
import datetime
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import execlog  # noqa: E402

MACHINERY = {"man", "mandb", "groff", "nroff", "troff", "grotty", "preconv", "tbl", "eqn", "pic", "less",
             "pager", "apt", "apt-get", "apt-cache", "dpkg", "dpkg-query", "pip", "pip3", "snap", "sudo"}
FIRST_STAGE_TOOLS = {"man", "python3", "python", "bash", "sh", "find", "ls", "dpkg", "dpkg-query",
                     "apt-cache", "which", "type", "file", "strings", "env", "printenv", "ps", "pgrep"}
MATERIAL = re.compile(r"(^|/)(formats|samples|output|prompts)(/|$)|^/usr/share/man/|\.md$|PROMPT_v\d")
HELP = {"--help", "--version", "-help", "-version"}
# the program rejected the command line itself (an option, an operand count, an option's value)
REFUSED = re.compile("|".join([
    r"invalid option", r"unrecognized option", r"unknown option", r"illegal option", r"bad option",
    r"missing operand", r"extra operand", r"requires an argument", r"doesn't allow an argument",
    r"option requires", r"invalid argument", r"invalid number", r"invalid (line|field|byte|character)",
    r"invalid (date|suffix|format|mode|unit|block size|count|time|signal|precision|width|base|byte)",
    r"ambiguous argument", r"is ambiguous", r"Try '[^']*--help'", r"--help' for more information",
    r"missing argument", r"unary operator expected", r"binary operator expected", r"integer expression expected",
    r"unknown command", r"unterminated `s' command", r"unknown option to `s'", r"no previous regular expression",
    r"Unknown (option|reader|writer|output format|input format|extension)", r"Unsupported option",
    r"no images defined", r"missing an argument", r"unrecognized (argument|operand)", r"usage:", r"Usage:",
    r"must be (specified|a single|positive|nonzero)", r"cannot (combine|be used together|both)",
    r"only one .* may be specified", r"mutually exclusive", r"conflicting", r"too many arguments",
]))
# the command line was accepted, and the program failed on the files or the system
RUNTIME = re.compile("|".join([
    r"No such file or directory", r"Permission denied", r"Is a directory", r"Not a directory",
    r"cannot (open|stat|access|create|remove|read|write)", r"Operation not permitted", r"File exists",
    r"Directory not empty", r"No such process", r"Read-only file system", r"not found",
    r"No space left", r"Bad file descriptor", r"Device or resource busy", r"Input/output error",
    r"unable to open image", r"Broken pipe", r"failed to", r"No match",
]))
# exit codes that mean "bad command line" for programs that print no recognisable message
USAGE_EXIT = {"unzip": {10}, "test": {2}, "[": {2}}


def env(folder):
    out = {}
    for ln in open(os.path.join(folder, "run.env"), encoding="utf-8", errors="replace"):
        if "=" in ln:
            k, v = ln.rstrip("\n").split("=", 1)
            out.setdefault(k, v)
    return out


def ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def tool_calls(folder):
    """Bash calls of the session, with their command text and start/end (epoch seconds)."""
    files = sorted(glob.glob(os.path.join(folder, "transcript_*.jsonl")))
    uses, ends = {}, {}
    for f in files:
        for ln in open(f, encoding="utf-8", errors="replace"):
            try:
                r = json.loads(ln)
            except json.JSONDecodeError:
                continue
            m = r.get("message") if isinstance(r.get("message"), dict) else {}
            for b in m.get("content") or [] if isinstance(m.get("content"), list) else []:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and r.get("timestamp"):
                    uses[b["id"]] = {"n": len(uses) + 1, "tool": b.get("name"), "start": ts(r["timestamp"]),
                                     "text": (b.get("input") or {}).get("command", "")}
                elif b.get("type") == "tool_result" and r.get("timestamp"):
                    ends[b.get("tool_use_id")] = ts(r["timestamp"])
    calls = []
    for i, u in uses.items():
        u["end"] = ends.get(i)
        calls.append(u)
    return sorted(calls, key=lambda c: c["start"])


def first_write(folder, since=None):
    """The first deliverable file written into output/ at or after `since`, from the audit watch (epoch s)."""
    p = os.path.join(folder, "audit_output.log")
    if not os.path.exists(p):
        return None
    best = None
    for ev in execlog.read_audit_events(p):
        if since is not None and ev["ts"] < since:
            continue
        names = [execlog.field(x, "name", text=True) or "" for x in ev.get("PATH", [])]
        if any("." in os.path.basename(n) for n in names):
            best = ev["ts"] if best is None else min(best, ev["ts"])
    return best


def operands(argv):
    ops, after = [], False
    for a in argv[1:]:
        if after or not a.startswith("-") or a == "-":
            ops.append(a)
        elif a == "--":
            after = True
    return ops


def pipeline_stages(text):
    """Every pipeline in the command text, as lists of stages (each stage a string)."""
    out = []
    for line in re.split(r"\n|;|&&|\|\|", text):
        stages = [s.strip() for s in re.split(r"(?<!\|)\|(?!\|)", line) if s.strip()]
        if len(stages) > 1:
            out.append(stages)
    return out


def working_tool(run, cmd, call, cwd_task):
    argv = run["argv"] or []
    ops = operands(argv)
    if ops and all(MATERIAL.search(o) for o in ops):
        return "T1"
    text = call["text"] if call else ""
    shown = " ".join([cmd] + argv[1:]).strip()
    for stages in pipeline_stages(text):
        for i, st in enumerate(stages[1:], 1):
            words = st.split()
            if not words or os.path.basename(words[0]) not in (cmd, "[") or not shown.startswith(
                    " ".join([cmd] + words[1:]).strip()[:len(shown)].strip()):
                continue
            first = stages[0].split()
            f0 = os.path.basename(first[0]) if first else ""
            if f0 == "man" or any(MATERIAL.search(w) for w in first[1:]):
                return "T2"
            if i == len(stages) - 1 and (f0 in FIRST_STAGE_TOOLS or f0.startswith("./") or f0.endswith((".py", ".sh"))):
                return "T4"
    if not ops and cwd_task and re.search(rf"(^|[\s;&|(]){re.escape(cmd)}\b[^|;&\n]*(>\s*\S*output/|<<)", text):
        return "T3"
    return None


def classify(run, cmd):
    st = run["stderr"] or ""
    if run["signal"]:
        return "signal"
    if run["exit_code"] is None:
        return "unfinished"
    if run["exit_code"] == 0:
        return "accepted"
    if run["exit_code"] in USAGE_EXIT.get(cmd, set()):
        return "refused"
    if RUNTIME.search(st) and not REFUSED.search(st):
        return "other_nonzero"
    if REFUSED.search(st):
        return "refused"
    if not st.strip():
        return "other_nonzero"
    return "unclassified"


def main(folder, out_json=None):
    e = env(folder)
    cmd, real = e["command"], e.get("binary_real") or e.get("binary")
    since = float(e["logger_since"]) if e.get("logger_since") else None
    runs, check = execlog.read(os.path.join(folder, "tries.log"), os.path.join(folder, "audit.log"), since)
    parent = getattr(execlog.read, "parent", {})
    pm = execlog.path_map(os.path.join(folder, "paths.tsv")) if os.path.exists(os.path.join(folder, "paths.tsv")) else {}
    resolved = lambda r: pm.get(r["path"], r["path"])
    targets = {real} | ({os.path.join(os.path.dirname(real), "[")} if cmd == "test" else set())
    by_pid = collections.defaultdict(list)
    for r in runs:
        by_pid[r["pid"]].append(r)

    def program_at(pid, t_ns):
        """The program the process was running at boot-clock time t_ns."""
        best = None
        for r in by_pid.get(pid, []):
            if r["start_ns"] <= t_ns:
                best = r
        return best

    # the session's claude process (a script's argv starts with its interpreter, so look at the first two words)
    session = [r for r in runs if r["argv"] and "--model" in r["argv"]
               and any(os.path.basename(w) == "claude" for w in r["argv"][:2])]
    session_pid = session[0]["pid"] if session else None
    calls = tool_calls(folder)
    fw = first_write(folder, since)
    task_dir = os.path.join(os.path.dirname(e.get("prompt_file", "/x/prompts/x")).rsplit("/prompts", 1)[0], "naive-arm")

    tries, excluded, outside = [], [], 0
    for r in runs:
        if resolved(r) not in targets and r["exe"] not in targets:
            continue
        chain, pid, seen = [], r["ppid"], set()
        while pid and pid not in seen and len(chain) < 64:
            seen.add(pid)
            p = program_at(pid, r["start_ns"])
            chain.append((pid, os.path.basename(resolved(p)) if p else None))
            pid = parent.get(pid) or (p["ppid"] if p else None)
        pids = [c[0] for c in chain]
        if session_pid not in pids:
            outside += 1
            continue
        above = [name for _, name in chain[:pids.index(session_pid)] if name]
        # the latest Bash call begun before this start, if the start falls inside it (0.5 s slack at the end)
        call = None
        for c in calls:
            if c["tool"] == "Bash" and c["start"] <= r["start"] + 0.05:
                call = c
        if call and call["end"] is not None and r["start"] > call["end"] + 0.5:
            call = None
        rec = {"argv": r["argv"], "argv_cut": False, "exit_code": r["exit_code"], "signal": r["signal"],
               "stderr": (r["stderr"] or "")[:256], "start": r["start"], "seconds": r["seconds"],
               "cwd": r["cwd"], "parents": above[:6], "tool_call": call["n"] if call else None}
        mach = sorted(set(above) & MACHINERY)
        if mach:
            rec["excluded"] = "machinery:" + ",".join(mach)
            excluded.append(rec)
            continue
        wt = working_tool(r, os.path.basename(real) if cmd != "test" else "test", call, (r["cwd"] or "") == task_dir)
        if wt:
            rec["excluded"] = "working_tool:" + wt
            excluded.append(rec)
            continue
        rec["class"] = classify(r, cmd)
        rec["help_or_version"] = bool(set(r["argv"] or []) & HELP)
        rec["phase"] = "exploring" if fw is None or r["start"] < fw else "testing"
        tries.append(rec)

    cls = collections.Counter(t["class"] for t in tries)
    by_phase = collections.Counter((t["phase"], t["class"]) for t in tries)
    argsets = {tuple(t["argv"][1:]) for t in tries if t["argv"]}
    optsets = {frozenset(w.split("=", 1)[0] for w in t["argv"][1:]
                         if w.startswith("-") or (cmd == "dd" and re.match(r"^[a-z]+=", w)))
               for t in tries if t["argv"]}
    refused = [t for t in tries if t["class"] == "refused"]
    per_call = collections.defaultdict(list)
    for t in tries:
        if t["tool_call"]:
            per_call[t["tool_call"]].append(t["class"])
    all_refused_calls = [n for n, cs in per_call.items() if cs and all(c == "refused" for c in cs)]
    call_secs = {c["n"]: (c["end"] - c["start"]) if c["end"] else 0 for c in calls}
    builtin = 0
    if cmd in ("test", "kill"):
        pat = re.compile(r"(^|[\s;&|(]|then|do)(test|\[|kill)\s") if cmd == "test" else re.compile(r"(^|[\s;&|(]|then|do)kill\s")
        builtin = sum(len(pat.findall(c["text"])) for c in calls if c["tool"] == "Bash")
    summary = {
        "run": os.path.basename(folder.rstrip("/")), "command": cmd, "binary": real,
        "logger_check": check, "session_found": session_pid is not None, "first_write": fw,
        "tries": len(tries), "classes": dict(cls),
        "by_phase": {f"{p}/{c}": n for (p, c), n in sorted(by_phase.items())},
        "help_or_version": sum(t["help_or_version"] for t in tries),
        "distinct_argument_lists": len(argsets), "distinct_option_sets": len(optsets),
        "refused_share": round(len(refused) / len(tries), 4) if tries else None,
        "refused_program_seconds": round(sum(t["seconds"] or 0 for t in refused), 3),
        "calls_all_refused": len(all_refused_calls),
        "calls_all_refused_seconds": round(sum(call_secs.get(n, 0) for n in all_refused_calls), 1),
        "excluded": dict(collections.Counter(x["excluded"] for x in excluded)),
        "outside_session": outside,
        "builtin_mentions_in_commands": builtin if cmd in ("test", "kill") else None,
        "unclassified_messages": sorted({t["stderr"].strip()[:120] for t in tries if t["class"] == "unclassified"}),
    }
    if out_json:
        json.dump({"summary": summary, "tries": tries, "excluded": excluded}, open(out_json, "w"), indent=1)
    return summary


if __name__ == "__main__":
    a = sys.argv[1:]
    out = a[a.index("--json") + 1] if "--json" in a else None
    print(json.dumps(main(a[0], out), indent=1))
