#!/usr/bin/env python3
"""Task 022 runner. Runs INSIDE the Lima VM `pash`; reads this folder through the read-only Mac mount.

    python3 run_pash.py build              # per-side annotation folders, input file, stand-in programs
    python3 run_pash.py controls           # the checks that PaSh is really running
    python3 run_pash.py answers            # each side's answers in the VM against the Mac's records
    python3 run_pash.py select             # benchmark lines + disagreement lines + named cases
    python3 run_pash.py run [--cmd C ...] [--limit N]   # bash once, then PaSh once per side
    python3 run_pash.py timing             # repeats on a larger input, for lines that split correctly

Everything is written under ~/t022 in the VM (T022_ROOT). Nothing in PaSh's install is changed: each side
is a private copy of the installed pash_annotations package, chosen with pa.sh --local-annotations-dir.
"""

import argparse
import gzip
import hashlib
import json
import os
import random
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
COMP = HERE.parent
sys.path.insert(0, str(COMP))
import score_pash as SP  # noqa: E402  (WORKER, cls, DATA, GEN; stdlib only)

ROOT = Path(os.environ.get("T022_ROOT", Path.home() / "t022"))
STOCK = Path.home() / "pash/python_pkgs/lib/python3.12/site-packages/pash_annotations"
PASH_TOP = os.environ.get("PASH_TOP", str(Path.home() / "pash/src/pash"))
WIDTH = 8
TIMEOUT = 60
COMMANDS = SP.COMMANDS
SPLITTABLE = ["cat", "cut", "grep", "sort"]  # the only commands for which any side allows a split
OUT = ROOT / "out"
INPUT = ROOT / "input/in.txt"
BIG = ROOT / "input/big.txt"
SHIM = ROOT / "shim"


def jl(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt") as f:
        return [json.loads(x) for x in f if x.strip()]


def sha(b):
    return hashlib.sha256(b).hexdigest()[:16]


def file_sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


# ------------------------------------------------------------------ sides

def all_sides():
    sides = jl(COMP / "sides.jsonl")
    for c in COMMANDS:
        sides.append({"cmd": c, "side": "none", "family": "control", "dir": None})
    return sides


def side_dir(s):
    return ROOT / "sides" / s["cmd"] / re.sub(r"[^A-Za-z0-9_.-]", "_", s["side"])


def three_files(pkg, c):
    C = SP.cls(c)
    return [pkg / SP.DATA / f"{c}.json",
            pkg / SP.GEN / f"InputOutputInfoGenerator{C}.py",
            pkg / SP.GEN / f"ParallelizabilityInfoGenerator{C}.py"]


def build_side(s, root=None):
    """Private copy of the installed package with this side's three files for ONE command."""
    root = root or side_dir(s)
    if root.exists():
        shutil.rmtree(root)
    pkg = root / "pash_annotations"
    shutil.copytree(STOCK, pkg, ignore=shutil.ignore_patterns("__pycache__"))
    c, C = s["cmd"], SP.cls(s["cmd"])
    files = three_files(pkg, c)
    if s["side"] == "none":
        for f in files:
            f.unlink(missing_ok=True)
    elif s["dir"]:
        d = Path(s["dir"])
        shutil.copy(d / f"{c}.json", files[0])
        for kind, dst in zip(("InputOutputInfoGenerator", "ParallelizabilityInfoGenerator"), files[1:]):
            src = d / f"{kind}{C}.py"
            if src.exists():
                shutil.copy(src, dst)
            else:
                dst.unlink(missing_ok=True)
        add_to_name_table(pkg, c)
    return {"cmd": c, "side": s["side"], "folder": str(root),
            "files": {f.name: (file_sha(f) if f.exists() else None) for f in files}}


def add_to_name_table(pkg, c):
    """PaSh only looks up commands in a fixed name table; cp and split are not in it."""
    ag = pkg / "annotation_generation/AnnotationGeneration.py"
    t = ag.read_text()
    head = "DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {\n"
    if f'"{c}":' not in t:
        assert head in t
        ag.write_text(t.replace(head, head + f'    "{c}": "{SP.cls(c)}",\n', 1))


def make_input(path, n_lines, seed):
    """Text lines with repeated keys, numbers out of order, several delimiters, tabs and duplicates."""
    random.seed(seed)
    words = [w.strip() for w in open("/usr/share/dict/words") if w.strip().isalpha()][:30000]
    path.parent.mkdir(parents=True, exist_ok=True)
    prev = None
    with open(path, "w") as f:
        for _ in range(n_lines):
            if prev and random.random() < 0.03:
                f.write(prev)  # exact duplicate of the line before
                continue
            a, b, c = random.choice(words), random.choice(words), random.choice(words)
            prev = (f"{random.randint(0, 999)} {a},{b.upper()}:{random.randint(0, 99)} "
                    f"\"{c}\"({a[:3]}).x=y\t{b}\t{random.randint(0, 9)}\n")
            f.write(prev)


def cmd_build(args):
    OUT.mkdir(parents=True, exist_ok=True)
    built = [build_side(s) for s in all_sides()]
    make_input(INPUT, 80000, 22)
    make_input(BIG, 1200000, 23)
    SHIM.mkdir(parents=True, exist_ok=True)
    real = {}
    for c in COMMANDS:
        real[c] = shutil.which(c, path="/usr/bin:/bin")
        (SHIM / c).write_text(
            "#!/bin/bash\n"
            f"printf '%s\\t%s\\n' {c} \"$*\" >> \"${{STANDIN_LOG:-/dev/null}}\"\n"
            f"exec {real[c]} \"$@\"\n")
        (SHIM / c).chmod(0o755)
    info = {"sides": built, "input": {"path": str(INPUT), "bytes": INPUT.stat().st_size, "sha": file_sha(INPUT)},
            "big": {"path": str(BIG), "bytes": BIG.stat().st_size, "sha": file_sha(BIG)}, "real": real}
    (OUT / "build.json").write_text(json.dumps(info, indent=1, sort_keys=True))
    print(f"built {len(built)} side folders; input {INPUT.stat().st_size:,} bytes; big {BIG.stat().st_size:,} bytes")


# ------------------------------------------------------------------ making a line runnable

VAL = {  # GNU options that take a separate value (so the next word is not an operand)
    "cat": set(), "rm": set(),
    "cut": {"-b", "-c", "-d", "-f", "--bytes", "--characters", "--delimiter", "--fields", "--output-delimiter"},
    "sort": {"-k", "-t", "-S", "-T", "-o", "--key", "--field-separator", "--buffer-size", "--temporary-directory",
             "--output", "--parallel", "--batch-size", "--compress-program", "--random-source", "--files0-from",
             "--sort"},
    "grep": {"-e", "-f", "-m", "-A", "-B", "-C", "-d", "-D", "--regexp", "--file", "--max-count",
             "--after-context", "--before-context", "--context", "--directories", "--devices", "--include",
             "--exclude", "--exclude-dir", "--exclude-from", "--label", "--binary-files"},
    "split": {"-a", "-b", "-C", "-l", "-n", "-t", "--suffix-length", "--bytes", "--line-bytes", "--lines",
              "--number", "--separator", "--additional-suffix", "--filter"},
    "wc": {"--files0-from"},
    "cp": {"-t", "-S", "--target-directory", "--suffix"},
}
OUT_OPTS = {"sort": {"-o", "--output"}}
DIR_OPTS = {"sort": {"-T", "--temporary-directory"}}
IN_OPTS = {"sort": {"--random-source"}, "grep": {"-f", "--file"}}
READS_STDIN = {"cat", "cut", "sort", "wc", "grep", "split"}


def tokenize(cmd, words):
    """[(kind, index, name)] for words[1:]; kind in option, value, operand. GNU rules."""
    val = VAL[cmd]
    longs = [v for v in val if v.startswith("--")]
    out, i, only_operands = [], 1, False
    while i < len(words):
        w = words[i]
        if only_operands or w == "-" or not w.startswith("-"):
            out.append(("operand", i, w))
        elif w == "--":
            only_operands = True
        elif w.startswith("--"):
            name = w.split("=", 1)[0]
            full = [v for v in longs if v.startswith(name)]
            out.append(("option", i, full[0] if len(full) == 1 else name))
            if "=" not in w and len(full) == 1 and i + 1 < len(words):
                i += 1
                out.append(("value", i, full[0]))
        else:
            for j, ch in enumerate(w[1:], 1):
                out.append(("option", i, "-" + ch))
                if "-" + ch in val:
                    if j == len(w) - 1 and i + 1 < len(words):
                        i += 1
                        out.append(("value", i, "-" + ch))
                    break
        i += 1
    return out


def situation(cmd, line):
    try:
        toks = tokenize(cmd, shlex.split(line))
    except ValueError:
        return None
    return (tuple(sorted({n for k, _, n in toks if k == "option"})), sum(1 for k, _, _ in toks if k == "operand"))


def rel(word):
    """A path that stays inside the work folder."""
    if os.path.isabs(word):
        if os.path.exists(word) and not word.startswith(("/tmp", "/home", "/Users")):
            return word  # a real system file such as /usr/share/dict/words or /dev/null
        return word.lstrip("/") or "root"
    return word


def bind(cmd, line):
    """line -> {script, line_run, make: [(kind, path)], stdin: bool, baseline}. make kinds: input, small, dir, tree."""
    words = shlex.split(line)
    toks = tokenize(cmd, words)
    opts = {n for k, _, n in toks if k == "option"}
    make, stdin = [], False
    operands = [(i, w) for k, i, w in toks if k == "operand"]
    for k, i, name in toks:
        if k != "value":
            continue
        if name in OUT_OPTS.get(cmd, ()):
            words[i] = rel(words[i])
        elif name in DIR_OPTS.get(cmd, ()):
            words[i] = rel(words[i])
            make.append(("dir", words[i]))
        elif name in IN_OPTS.get(cmd, ()):
            words[i] = rel(words[i])
            make.append(("pattern" if cmd == "grep" else "input", words[i]))
    recursive = bool(opts & {"-r", "-R", "--recursive", "--dereference-recursive"})
    if cmd in ("cat", "cut", "sort", "wc"):
        inputs = operands
    elif cmd == "grep":
        has_pat = bool(opts & {"-e", "-f", "--regexp", "--file"})
        inputs = operands if has_pat else operands[1:]
    elif cmd == "split":
        inputs = operands[:1]
        for i, w in operands[1:2]:
            words[i] = rel(w)
    elif cmd == "cp":
        inputs = []
        for i, w in operands[:-1]:
            words[i] = rel(w)
            make.append(("small", words[i]))
        for i, w in operands[-1:]:
            words[i] = rel(w)
    elif cmd == "rm":
        inputs = []
        for i, w in operands:
            words[i] = rel(w)
            make.append(("tree" if (recursive or w.endswith("/")) else "small", words[i]))
    for i, w in inputs:
        if w == "-":
            stdin = True
            continue
        words[i] = rel(w)
        if not os.path.isabs(words[i]):
            make.append(("tree" if (cmd == "grep" and recursive) else "input", words[i]))
    if cmd in READS_STDIN and not inputs and not (cmd == "grep" and recursive):
        stdin = True
    line_run = shlex.join(words)
    # Standard input comes from a pipe (PaSh falls back to bash on `< file`). When the command under test
    # is cat itself, the feeder must not be cat, or the side's cat files would also decide what happens
    # to the feeder; `tail -n +1 FILE` passes the file through and PaSh's own tail files never split it.
    feeder = f"tail -n +1 {INPUT}" if cmd == "cat" else f"cat {INPUT}"
    script = (f"{feeder} | {line_run}" if stdin else line_run) + "\n"
    return {"script": script, "line_run": line_run, "make": make, "stdin": stdin, "baseline": 1}


def prepare(w, b, source=None):
    """Fresh work folder: w/cwd is the working directory, so ../x stays inside w."""
    if w.exists():
        shutil.rmtree(w)
    cwd = w / "cwd"
    cwd.mkdir(parents=True)
    src = source or INPUT
    for kind, path in b["make"]:
        p = (cwd / path)
        if p.exists() or p.is_symlink():
            continue
        if kind == "dir":
            p.mkdir(parents=True, exist_ok=True)
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        if kind == "input":
            shutil.copyfile(src, p)
        elif kind == "small":
            p.write_text("small file\nsecond line\n")
        elif kind == "pattern":
            p.write_text("ab\n")
        elif kind == "tree":
            p.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, p / "part1.txt")
            (p / "sub").mkdir()
            (p / "sub/part2.txt").write_text("abc small file\nsecond line\n")
    return cwd


def manifest(w):
    rows = []
    for p in sorted(w.rglob("*")):
        r = str(p.relative_to(w))
        if p.is_symlink():
            rows.append((r, "link", os.readlink(p)))
        elif p.is_dir():
            rows.append((r, "dir", ""))
        elif p.is_file():
            rows.append((r, "file", f"{p.stat().st_size}:{file_sha(p)}"))
        else:
            rows.append((r, "other", ""))
    return sha(json.dumps(rows).encode()), len(rows)


# ------------------------------------------------------------------ running

def run_script(argv, cwd, out_path, env=None, timeout=TIMEOUT):
    t0 = time.perf_counter()
    with open(out_path, "wb") as o:
        p = subprocess.Popen(argv, cwd=cwd, stdout=o, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                             env=env, start_new_session=True)
        try:
            _, err = p.communicate(timeout=timeout)
            rc, timed_out = p.returncode, False
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            _, err = p.communicate()
            rc, timed_out = None, True
    return {"rc": rc, "timed_out": timed_out, "seconds": round(time.perf_counter() - t0, 3),
            "stderr": err.decode(errors="replace")[-1500:]}


TB = re.compile(r"Traceback \(most recent call last\):\n(?:.*\n)*?(?=\S)(\S.*)\n")


def read_log(path, cmd):
    if not path.exists() or path.stat().st_size == 0:
        return None
    t = path.read_text(errors="replace")
    t = re.sub(r"/tmp/pash_\w+/+[0-9a-f]*/?", "TMP/", t)
    tracebacks = []
    for m in re.finditer(r"Traceback \(most recent call last\):\n((?:  .*\n)+)(\S[^\n]*)", t):
        frames = re.findall(r'File ".*?/([^/"]+)", line (\d+), in (\w+)', m.group(1))
        where = "{}:{} {}".format(*frames[-1]) if frames else "?"
        tracebacks.append(f"{m.group(2).strip()[:200]} @ {where}")
    notes = sorted({ln.strip()[:240] for ln in t.splitlines()
                    if re.search(r"considered side-effectful|not yet implemented|Unparallelizable|"
                                 r"No region was parallelized|not parallelizable", ln)})
    ms = re.findall(r"Compilation time: ([\d.]+)", t)
    return {
        "bytes": len(t),
        "r_split": len(re.findall(r"runtime/r_split ", t)),
        "split_file": len(re.findall(r"runtime/(?:split|auto-split)[ .]", t)),
        "r_merge": len(re.findall(r"runtime/r_merge ", t)),
        "workers_in_log": len(re.findall(r"r_wrap bash -c ' *" + re.escape(cmd) + r"\b", t))
                          + len(re.findall(r"^\{ " + re.escape(cmd) + r" .*fifo.*& \}$", t, re.M)),
        "no_region": "No region was parallelized" in t,
        "tracebacks": tracebacks,
        "notes": notes,
        "compile_ms": sum(float(x) for x in ms) if ms else None,
    }


def standin_count(path, cmd):
    """Copies of the command started, leaving out PaSh's own housekeeping calls.

    Housekeeping calls name a file under PaSh's temporary folder (`cat /tmp/pash_x//pash_123`, `rm ...`).
    A worker copy either has the line's own arguments, or has a file argument replaced by one of PaSh's
    pipes (`.../#fifo12`); both are counted. For sort this includes PaSh's merge steps (`sort -m` on pipes).
    PaSh itself removes its pipes with rm and joins pieces with cat, so for those two commands a call
    naming a pipe is PaSh's own and is not counted.
    """
    own = internal = 0
    if path.exists():
        for ln in path.read_text(errors="replace").splitlines():
            name, _, rest = ln.partition("\t")
            if name != cmd:
                continue
            if "/tmp/pash_" in rest and ("#fifo" not in rest or cmd in ("rm", "cat")):
                internal += 1
            else:
                own += 1
    return own, internal


def classify(log, n_cmd, baseline, res):
    if res["timed_out"]:
        return "timed out", "over the time limit"
    if log is None:
        return "unknown", "no log written"
    markers = log["r_split"] + log["split_file"]
    if markers > 0 and not log["no_region"] and n_cmd > baseline:
        return "split", ""
    if markers == 0 and n_cmd <= baseline:
        if log["tracebacks"]:
            return "PaSh error", log["tracebacks"][-1]
        return "not split", "; ".join(log["notes"])[:300]
    if markers > 0 and not log["no_region"] and log["workers_in_log"] >= 2 and n_cmd <= baseline:
        # PaSh's generated script holds several worker copies, but they only start when a piece of input
        # reaches them, and none (or one) did: PaSh split a stream that carried no data for this command
        return "split, workers idle", (f"PaSh's script has {log['workers_in_log']} worker copies; "
                                       f"{n_cmd} started, because the stream PaSh split carried no input")
    return "unknown", f"signals disagree: split steps in log={markers}, copies started={n_cmd}, expected unsplit={baseline}"


def cmd_reclassify(args):
    """Apply classify() again to the stored signals. Only rows marked unknown may change."""
    path = OUT / "pash_runs.jsonl"
    rows, changed = jl(path), Counter()
    for r in rows:
        if r.get("side") == "*":
            continue
        fake = {"timed_out": r["state"] == "timed out"}
        state, why = classify(r["log"], r["copies"], r["baseline"], fake)
        if state != r["state"]:
            assert r["state"] == "unknown", (r["id"], r["side"], r["state"], state)
            changed[(r["state"], state)] += 1
            r["state"], r["why"] = state, why
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print(dict(changed), Counter(r["state"] for r in rows))


def pash_env(standin_log):
    env = dict(os.environ)
    env["PATH"] = f"{SHIM}:{env['PATH']}"
    env["STANDIN_LOG"] = str(standin_log)
    env["PASH_TOP"] = PASH_TOP
    return env


def run_pash(script, cwd, side_folder, rdir, tag, cmd, timeout=TIMEOUT, width=WIDTH):
    log, standin, out = rdir / f"{tag}.log", rdir / f"{tag}.standin", rdir / f"{tag}.out"
    for f in (log, standin):
        f.unlink(missing_ok=True)
    argv = [f"{PASH_TOP}/pa.sh", "-w", str(width), "-d", "2", "--log_file", str(log)]
    if side_folder:
        argv += ["--local-annotations-dir", str(side_folder)]
    res = run_script(argv + [str(script)], cwd, out, env=pash_env(standin), timeout=timeout)
    res["log"] = read_log(log, cmd)
    res["copies"], res["pash_internal_calls"] = standin_count(standin, cmd)
    return res, log, out


def answers_for(side, lines):
    """Ask this side's files, inside the VM, through its folder (the scorer's own worker)."""
    p = subprocess.run([sys.executable, "-I", "-c", SP.WORKER, str(side_dir(side)), side["cmd"], SP.cls(side["cmd"])],
                       input="".join(json.dumps({"id": i, "line": ln}) + "\n" for i, ln in lines),
                       capture_output=True, text=True)
    if p.returncode:
        return {i: {"io_outcome": "worker crashed", "par_outcome": "worker crashed",
                    "crash": p.stderr.strip().splitlines()[-1][:300] if p.stderr.strip() else ""} for i, _ in lines}
    return {r["id"]: r for r in map(json.loads, p.stdout.splitlines())}


def brief(a):
    return {"io": a.get("io_outcome"), "par": a.get("par_outcome"),
            "allows_split": a.get("par_outcome") == "answered" and bool(a.get("par")),
            "recipes": sorted({f'{r["split"]}>{r["aggregate"]}' for r in a.get("par") or []}),
            "exception": a.get("io_exception") or a.get("par_exception") or a.get("crash")}


def do_line(row, sides, out_f, done):
    cmd, lid = row["cmd"], row["id"]
    todo = [s for s in sides if s["cmd"] == cmd and (lid, s["side"]) not in done]
    if not todo:
        return
    if row["line"] is None:  # task 021's cleanup could not turn the benchmark text into one command line
        if (lid, "*") not in done:
            out_f.write(json.dumps({"id": lid, "cmd": cmd, "set": row["set"], "line": row.get("raw"), "side": "*",
                                    "state": "not runnable", "why": row.get("unusable") or "no usable line"}) + "\n")
            done.add((lid, "*"))
        return
    try:
        b = bind(cmd, row["line"])
    except Exception as e:  # noqa: BLE001
        out_f.write(json.dumps({"id": lid, "cmd": cmd, "set": row["set"], "line": row["line"], "side": "*",
                                "state": "not runnable", "why": f"{type(e).__name__}: {e}"}) + "\n")
        return
    rdir = ROOT / "runs" / lid
    rdir.mkdir(parents=True, exist_ok=True)
    script = rdir / "script.sh"
    script.write_text(b["script"])
    cwd = prepare(rdir / "w", b)
    # the reference run uses the same stand-in programs, so a program name printed by the command
    # (`sort --help` prints it) is the same in both runs
    base = run_script(["bash", str(script)], cwd, rdir / "bash.out", env=pash_env(rdir / "bash.standin"))
    base_sha, base_size = file_sha(rdir / "bash.out"), (rdir / "bash.out").stat().st_size
    base_manifest = manifest(rdir / "w")
    for s in todo:
        ans = brief(answers_for(s, [(lid, b["line_run"])])[lid])
        cwd = prepare(rdir / "w", b)
        tag = re.sub(r"[^A-Za-z0-9_.-]", "_", s["side"])
        res, log, out = run_pash(script, cwd, side_dir(s), rdir, tag, cmd)
        state, why = classify(res["log"], res["copies"], b["baseline"], res)
        o_sha, o_size = file_sha(out), out.stat().st_size
        man = manifest(rdir / "w")
        rec = {"id": lid, "cmd": cmd, "set": row["set"], "line": row["line"], "line_run": b["line_run"],
               "script": b["script"].strip().replace(str(INPUT), "in.txt"), "side": s["side"], "family": s["family"],
               "answer": ans, "state": state, "why": why, "copies": res["copies"], "baseline": b["baseline"],
               "pash_internal_calls": res["pash_internal_calls"], "log": res["log"],
               "rc": res["rc"], "bash_rc": base["rc"], "rc_same": res["rc"] == base["rc"],
               "out_same": o_sha == base_sha, "out_bytes": o_size, "bash_out_bytes": base_size,
               "files_same": man == base_manifest, "seconds": res["seconds"], "bash_seconds": base["seconds"],
               "stderr": res["stderr"][-400:], "bash_stderr": base["stderr"][-200:]}
        if not rec["out_same"]:
            keep = OUT / "diffs" / f"{lid}__{tag}"
            keep.mkdir(parents=True, exist_ok=True)
            for src, name in ((out, "pash.out"), (rdir / "bash.out", "bash.out")):
                with open(src, "rb") as f:
                    (keep / name).write_bytes(f.read(4000))
        if res["log"] is not None:
            (OUT / "logs").mkdir(parents=True, exist_ok=True)
            with open(log, "rb") as f, gzip.open(OUT / "logs" / f"{lid}__{tag}.log.gz", "wb") as g:
                g.write(f.read())
        out_f.write(json.dumps(rec, sort_keys=True) + "\n")
        out_f.flush()
        done.add((lid, s["side"]))
    shutil.rmtree(rdir, ignore_errors=True)


def cmd_run(args):
    lines = jl(OUT / "lines_run.jsonl")
    if args.cmd:
        lines = [r for r in lines if r["cmd"] in args.cmd]
    if args.set:
        lines = [r for r in lines if r["set"] in args.set]
    if args.limit:
        keep, per = [], Counter()
        for r in lines:
            if per[(r["cmd"], r["set"])] < args.limit:
                per[(r["cmd"], r["set"])] += 1
                keep.append(r)
        lines = keep
    sides = all_sides()
    if args.side:
        sides = [s for s in sides if any(s["side"].startswith(x) for x in args.side)]
    out_path = OUT / (args.out or "pash_runs.jsonl")
    if args.redo_unknown and out_path.exists():
        # rows marked unknown are run again (used once, after the copy counter was corrected); the rows
        # they replace are kept in a side file so the correction can be inspected
        rows = jl(out_path)

        def again(r):
            return (r.get("state") in ("unknown", "not runnable")
                    or (r.get("cmd") == "cat" and r.get("script", "").startswith("cat in.txt |")))
        redo = [r for r in rows if again(r)]
        with open(OUT / "replaced_rows.jsonl", "a") as f:
            for r in redo:
                f.write(json.dumps(r, sort_keys=True) + "\n")
        with open(out_path, "w") as f:
            for r in rows:
                if not again(r):
                    f.write(json.dumps(r, sort_keys=True) + "\n")
        print(f"re-running {len(redo)} rows (marked unknown, or cat fed by cat)")
    done = {(r["id"], r["side"]) for r in jl(out_path)} if out_path.exists() else set()
    t0 = time.time()
    with open(out_path, "a") as f:
        for n, row in enumerate(lines, 1):
            do_line(row, sides, f, done)
            if n % 10 == 0:
                print(f"{n}/{len(lines)} lines, {time.time() - t0:.0f}s", flush=True)
    print(f"done: {len(lines)} lines in {time.time() - t0:.0f}s; input sha now {file_sha(INPUT)}")


# ------------------------------------------------------------------ which lines

NAMED = [  # the cases task 021 flagged by name
    ("sort", "sort -n -u"), ("sort", "sort -n -s"), ("sort", "sort -g -u"), ("sort", "sort -h -s"),
    ("sort", "sort -k 1,1 -u"), ("sort", "sort -m"), ("sort", "sort -u"),
    ("cut", "cut -z -c 1-3"), ("cut", "cut -z -d , -f 1"),
    ("grep", "grep ab f1 f2"), ("grep", "grep -r ab d1"), ("grep", "grep -c ab f1 f2"), ("grep", "grep -m 5 ab"),
    ("grep", "grep -A 1 ab"), ("grep", "grep -n ab"), ("grep", "grep -c ab"), ("grep", "grep ab"),
    ("cat", "cat -n"), ("cat", "cat -n f1"), ("cat", "cat -n f1 f2"), ("cat", "cat f1 f2"),
]


def cmd_select(args):
    lines = jl(COMP / "lines.jsonl")
    answers = jl(COMP / "answers.jsonl.gz")
    by = defaultdict(dict)
    for a in answers:
        by[a["id"]][a["side"]] = a
    rows = []
    for r in lines:
        if "A" in r["sets"]:
            if r["line"] is None:
                rows.append({"id": r["id"], "cmd": r["cmd"], "set": "benchmark", "line": None,
                             "unusable": r["unusable"], "raw": r["raw"]})
            else:
                rows.append({"id": r["id"], "cmd": r["cmd"], "set": "benchmark", "line": r["line"]})
    seen = {(r["cmd"], r["line"]) for r in rows}
    picked = Counter()
    for cmd in SPLITTABLE:
        groups = defaultdict(list)
        for r in lines:
            if r["cmd"] != cmd or "A" in r["sets"] or not r["line"]:
                continue
            k = situation(cmd, r["line"])
            if k is not None:
                groups[k].append(r)
        kept = []
        for k, rs in groups.items():
            a = by[rs[0]["id"]]
            allow = {s: (x.get("par_outcome") == "answered" and bool(x.get("par"))) for s, x in a.items()
                     if s != "pash-own"}
            crash = any("exception" in (x.get("io_outcome"), x.get("par_outcome")) for x in a.values())
            if len(set(allow.values())) > 1 or crash:
                kept.append((len(rs), k, rs))
        kept.sort(key=lambda t: (-t[0], str(t[1])))
        for size, k, rs in kept:
            if picked[cmd] >= args.cap:
                break
            for r in rs[:3]:  # the first of the group's lines that runs cleanly under bash
                if (cmd, r["line"]) in seen:
                    break
                try:
                    b = bind(cmd, r["line"])
                except Exception:  # noqa: BLE001
                    continue
                rdir = ROOT / "runs" / "select"
                rdir.mkdir(parents=True, exist_ok=True)
                (rdir / "s.sh").write_text(b["script"])
                cwd = prepare(rdir / "w", b)
                res = run_script(["bash", str(rdir / "s.sh")], cwd, rdir / "o", timeout=20)
                if res["rc"] == 0 and (rdir / "o").stat().st_size > 0:
                    rows.append({"id": r["id"], "cmd": cmd, "set": "disagreement", "line": r["line"],
                                 "group_size": size, "situation": [list(k[0]), k[1]]})
                    seen.add((cmd, r["line"]))
                    picked[cmd] += 1
                    break
    for n, (cmd, line) in enumerate(NAMED):
        rows.append({"id": f"{cmd}-named{n:02d}", "cmd": cmd, "set": "named", "line": line})
    with open(OUT / "lines_run.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    print(Counter((r["cmd"], r["set"]) for r in rows))


# ------------------------------------------------------------------ checks that PaSh is really running

def one_control(name, script_text, side_folder, cmd, make=()):
    rdir = ROOT / "runs" / f"control_{name}"
    if rdir.exists():
        shutil.rmtree(rdir)
    rdir.mkdir(parents=True)
    script = rdir / "script.sh"
    script.write_text(script_text + "\n")
    b = {"make": list(make)}
    cwd = prepare(rdir / "w", b)
    base = run_script(["bash", str(script)], cwd, rdir / "bash.out", env=pash_env(rdir / "bash.standin"))
    cwd = prepare(rdir / "w", b)
    res, log, out = run_pash(script, cwd, side_folder, rdir, "pash", cmd)
    baseline = len(re.findall(r"(?:^|\|)\s*" + re.escape(cmd) + r"\b", script_text))
    state, why = classify(res["log"], res["copies"], baseline, res)
    rec = {"control": name, "script": script_text.replace(str(INPUT), "in.txt"), "command_watched": cmd,
           "annotation_folder": str(side_folder) if side_folder else "installed package",
           "state": state, "why": why, "copies_started": res["copies"],
           "split_steps_in_log": (res["log"] or {}).get("r_split", 0) + (res["log"] or {}).get("split_file", 0),
           "exit_code": res["rc"], "bash_exit_code": base["rc"],
           "output_same_as_bash": file_sha(out) == file_sha(rdir / "bash.out"),
           "output_bytes": out.stat().st_size, "tracebacks": (res["log"] or {}).get("tracebacks"),
           "notes": (res["log"] or {}).get("notes")}
    shutil.rmtree(rdir, ignore_errors=True)
    return rec


def cmd_controls(args):
    S = {(s["cmd"], s["side"]): s for s in all_sides()}
    recs = []
    v = subprocess.run(["bash", "-lc", f"cd {PASH_TOP} && git rev-parse --short HEAD; "
                        f"{Path.home()}/pash/python_pkgs/bin/pip show pash-annotations | sed -n 2p; "
                        "sort --version | head -1; nproc; uname -srm"], capture_output=True, text=True).stdout.split("\n")
    installed = {"pash_commit": v[0], "pash_annotations": v[1], "coreutils": v[2], "cores": v[3], "kernel": v[4]}
    grep_script = f"cat {INPUT} | grep '\\(.\\).*\\1\\(.\\).*\\2' | wc -l"
    # 2. a script known to split must split (installed package, then an untouched copy of it)
    recs.append(one_control("known_good_installed", grep_script, None, "grep") | {"expect": "split"})
    recs.append(one_control("known_good_copy", grep_script, side_dir(S[("grep", "pash-own")]), "grep") | {"expect": "split"})
    # 3. the folder must be what decides: same script, grep's files removed from the copy
    recs.append(one_control("folder_decides", grep_script, side_dir(S[("grep", "none")]), "grep") | {"expect": "not split"})
    # 5. a wrong answer must be caught: v1's main-grammar sort files allow splitting `sort -n -u`
    recs.append(one_control("wrong_answer_caught", f"cat {INPUT} | sort -n -u", side_dir(S[("sort", "v1-main")]), "sort")
                | {"expect": "split, output differs from bash"})
    recs.append(one_control("same_line_pash_own", f"cat {INPUT} | sort -n -u", side_dir(S[("sort", "pash-own")]), "sort")
                | {"expect": "output same as bash"})
    # 6. this morning's silent fallback, and the same script with `head -n 5`
    recs.append(one_control("silent_fallback", f"cat {INPUT} | sort -n | uniq -c | sort -rn | head -5", None, "sort")
                | {"expect": "PaSh error (ran as plain bash)"})
    recs.append(one_control("silent_fallback_fixed", f"cat {INPUT} | sort -n | uniq -c | sort -rn | head -n 5", None, "sort")
                | {"expect": "split"})
    recs.append(one_control("input_redirect", f"cut -d ' ' -f 1 < {INPUT}", None, "cut") | {"expect": "PaSh error"})
    out = {"when": time.strftime("%Y-%m-%d %H:%M:%S %z"), "installed": installed, "controls": recs}
    name = args.out or "controls.json"
    (OUT / name).write_text(json.dumps(out, indent=1))
    print(json.dumps(installed))
    for r in recs:
        print(f'{r["control"]:24} state={r["state"]:10} copies={r["copies_started"]:3} same_output={r["output_same_as_bash"]}'
              f'  expect: {r["expect"]}  {r["why"][:110]}')


def cmd_answers(args):
    """Check 4: each side's folder, asked inside the VM, must give the answers recorded on the Mac."""
    lines = [r for r in jl(COMP / "lines.jsonl") if r["line"]]
    mac = {(a["id"], a["side"]): a for a in jl(COMP / "answers.jsonl.gz")}
    by_cmd = defaultdict(list)
    for r in lines:
        by_cmd[r["cmd"]].append((r["id"], r["line"]))
    fields = ("parse", "io_outcome", "io", "par_outcome", "par", "io_exception", "par_exception")
    total = same = 0
    diffs = []
    for s in jl(COMP / "sides.jsonl"):
        got = answers_for(s, by_cmd[s["cmd"]])
        n = ok = 0
        for lid, _ in by_cmd[s["cmd"]]:
            m, g = mac.get((lid, s["side"])), got.get(lid)
            n += 1
            if m is not None and g is not None and all(m.get(f) == g.get(f) for f in fields):
                ok += 1
            elif len(diffs) < 40:
                diffs.append({"id": lid, "side": s["side"], "mac": {f: (m or {}).get(f) for f in fields},
                              "vm": {f: (g or {}).get(f) for f in fields}})
        total += n
        same += ok
        print(f'{s["cmd"]:6} {s["side"]:28} {ok}/{n}', flush=True)
    (OUT / "answers_check.json").write_text(json.dumps({"same": same, "total": total, "examples_of_differences": diffs}, indent=1))
    print(f"TOTAL same {same}/{total}")


# ------------------------------------------------------------------ timing

def cmd_timing(args):
    """Five repeats on the larger input, for lines that split with the right output under some side."""
    runs = jl(OUT / "pash_runs.jsonl")
    lines = {r["id"]: r for r in jl(OUT / "lines_run.jsonl")}
    good = defaultdict(list)
    for r in runs:
        if r["state"] == "split" and r["out_same"] and r["bash_rc"] == 0:
            good[r["id"]].append(r["side"])
    chosen = sorted(good)
    if args.limit:
        per, keep = Counter(), []
        for i in chosen:
            c = lines[i]["cmd"]
            if per[c] < args.limit:
                per[c] += 1
                keep.append(i)
        chosen = keep
    S = {(s["cmd"], s["side"]): s for s in all_sides()}
    global INPUT
    small = INPUT
    with open(OUT / "timing.jsonl", "a") as f:
        for n, lid in enumerate(chosen, 1):
            row = lines[lid]
            cmd = row["cmd"]
            INPUT = BIG
            b = bind(cmd, row["line"])
            INPUT = small
            rdir = ROOT / "runs" / f"timing_{lid}"
            rdir.mkdir(parents=True, exist_ok=True)
            script = rdir / "script.sh"
            script.write_text(b["script"])
            bash_t = []
            for _ in range(args.repeats):
                cwd = prepare(rdir / "w", b, source=BIG)
                bash_t.append(run_script(["bash", str(script)], cwd, rdir / "bash.out", timeout=300,
                                         env=pash_env(rdir / "b.standin"))["seconds"])
            ref = file_sha(rdir / "bash.out")
            for side in sorted(set(good[lid]) | {"none"}):
                ts, states, same = [], [], []
                for _ in range(args.repeats):
                    cwd = prepare(rdir / "w", b, source=BIG)
                    res, log, out = run_pash(script, cwd, side_dir(S[(cmd, side)]), rdir, "t", cmd, timeout=300)
                    ts.append(res["seconds"])
                    states.append(classify(res["log"], res["copies"], b["baseline"], res)[0])
                    same.append(file_sha(out) == ref)
                f.write(json.dumps({"id": lid, "cmd": cmd, "line": row["line"], "side": side, "bash_seconds": bash_t,
                                    "pash_seconds": ts, "states": states, "out_same": same,
                                    "input_bytes": BIG.stat().st_size}) + "\n")
                f.flush()
            shutil.rmtree(rdir, ignore_errors=True)
            print(f"{n}/{len(chosen)} {lid}", flush=True)


# ------------------------------------------------------------------ cause of each wrong output

def pieces_of(path, round_robin):
    """The pieces PaSh would hand out: 1 MB line-aligned batches (round robin), else WIDTH equal parts."""
    data = open(path, "rb").read().splitlines(keepends=True)
    size = 1_000_000 if round_robin else max(1, sum(map(len, data)) // WIDTH + 1)
    out, cur, n = [], [], 0
    for ln in data:
        cur.append(ln)
        n += len(ln)
        if n >= size:
            out.append(b"".join(cur))
            cur, n = [], 0
    if cur:
        out.append(b"".join(cur))
    return out


def cmd_causes(args):
    """Re-run each wrong output by hand: the command on each piece, outputs joined in order.

    hand-made split also wrong -> the annotation's claim is wrong for this input (unsafe annotation)
    hand-made split right      -> the difference comes from PaSh, not from the claim
    """
    runs = [r for r in jl(OUT / "pash_runs.jsonl") if r.get("side") != "*" and not r["out_same"]]
    S = {(s["cmd"], s["side"]): s for s in all_sides()}
    rdir = ROOT / "runs" / "cause"
    with open(OUT / "causes.jsonl", "w") as f:
        for r in runs:
            cmd, s = r["cmd"], S[(r["cmd"], r["side"])]
            b = bind(cmd, r["line"])
            a = answers_for(s, [(r["id"], b["line_run"])])[r["id"]]
            recipes = a.get("par") or []
            if rdir.exists():
                shutil.rmtree(rdir)
            rdir.mkdir(parents=True)
            script = rdir / "script.sh"
            script.write_text(b["script"])
            shas = []
            for k in (1, 2):  # is the command itself repeatable on the whole input?
                cwd = prepare(rdir / "w", b)
                run_script(["bash", str(script)], cwd, rdir / f"whole{k}.out", env=pash_env(rdir / "b.standin"))
                shas.append(file_sha(rdir / f"whole{k}.out"))
            cwd = prepare(rdir / "w", b)
            res, log, out = run_pash(script, cwd, side_dir(s), rdir, "p", cmd)
            state = classify(res["log"], res["copies"], b["baseline"], res)[0]
            pash_sha = file_sha(out)
            rec = {"id": r["id"], "side": r["side"], "cmd": cmd, "script": r["script"], "pash_state_again": state,
                   "pash_wrong_again": pash_sha != shas[0],
                   "recipes": sorted({f'{x["split"]}>{x["map"]}>{x["aggregate"]}' for x in recipes})}
            inputs = [p for k, p in b["make"] if k == "input"]
            plain = bool(recipes) and all(x["aggregate"] == "CONCATENATE" and x["map"] == "SAME_AS_SEQ" for x in recipes)
            if shas[0] != shas[1]:
                rec["cause"] = "the command's own output changes from run to run"
            elif state == "split, workers idle":
                rec["cause"] = ("the side's files misdescribe the input: PaSh split a stream the command "
                                "does not read, so the worker copies got nothing")
            elif state != "split":
                rec["cause"] = f"PaSh did not split on the re-run ({state})"
            elif not plain:
                rec["cause"] = "not hand-checked: the merge step is not plain joining"
            elif not ((b["stdin"] and not inputs) or (len(inputs) == 1 and not b["stdin"])):
                rec["cause"] = "not hand-checked: more than one input"
            else:
                rr = any(x["split"].startswith("ROUND_ROBIN") for x in recipes)
                joined = b""
                for piece in pieces_of(INPUT, rr):
                    (rdir / "piece.txt").write_bytes(piece)
                    cwd = prepare(rdir / "w", b)
                    if inputs:
                        (cwd / inputs[0]).write_bytes(piece)
                        text = b["script"]
                    else:
                        text = b["script"].replace(str(INPUT), str(rdir / "piece.txt"))
                    (rdir / "piece.sh").write_text(text)
                    run_script(["bash", str(rdir / "piece.sh")], cwd, rdir / "piece.out", env=pash_env(rdir / "b.standin"))
                    joined += (rdir / "piece.out").read_bytes()
                hand = sha(joined)
                # sha() and file_sha() both give the first 16 hex digits of sha256
                rec["hand_split_equals_whole"] = hand == shas[0]
                rec["hand_split_equals_pash"] = hand == pash_sha
                rec["cause"] = ("the difference comes from PaSh: splitting and joining by hand gives the right output"
                                if hand == shas[0] else
                                "unsafe annotation: splitting and joining by hand also gives a different output")
            f.write(json.dumps(rec, sort_keys=True) + "\n")
            f.flush()
            print(rec["side"][:24].ljust(24), rec["script"][:50].ljust(50), "|", rec["cause"], flush=True)
    shutil.rmtree(rdir, ignore_errors=True)


# ------------------------------------------------------------------ whole benchmark scripts

NAIVE_FIRST = {  # the Fig. 7 campaign's first run of each command (one prompt, one setup)
    "cat": "naive:2026-10-28_100411", "cp": "naive:2026-10-28_114133", "cut": "naive:2026-10-27_230555",
    "grep": "naive:2026-10-28_135447", "rm": "naive:2026-10-28_105951", "sort": "naive:2026-10-28_140825",
    "split": "naive:2026-10-28_134035", "wc": "naive:2026-10-28_091448",
}
EXTRA = ["tr", "uniq", "awk", "sed", "head", "tail", "comm", "xargs", "col", "iconv", "paste", "tee", "diff",
         "file", "fmt", "rev", "seq", "nl"]


def build_set(name, chosen):
    """One folder holding a side's files for all eight commands at once."""
    root = ROOT / "sets" / name
    if root.exists():
        shutil.rmtree(root)
    pkg = root / "pash_annotations"
    shutil.copytree(STOCK, pkg, ignore=shutil.ignore_patterns("__pycache__"))
    for c, s in chosen.items():
        files = three_files(pkg, c)
        if s["side"] == "none":
            for f in files:
                f.unlink(missing_ok=True)
        elif s["dir"]:
            d = Path(s["dir"])
            shutil.copy(d / f"{c}.json", files[0])
            for kind, dst in zip(("InputOutputInfoGenerator", "ParallelizabilityInfoGenerator"), files[1:]):
                src = d / f"{kind}{SP.cls(c)}.py"
                if src.exists():
                    shutil.copy(src, dst)
                else:
                    dst.unlink(missing_ok=True)
            add_to_name_table(pkg, c)
    return root


def counts(path):
    c = Counter()
    if path.exists():
        for ln in path.read_text(errors="replace").splitlines():
            name, _, rest = ln.partition("\t")
            # same rule as standin_count(): PaSh's own housekeeping calls are left out
            if "/tmp/pash_" in rest and ("#fifo" not in rest or name in ("rm", "cat")):
                continue
            c[name] += 1
    return c


def cmd_scripts(args):
    bench = Path.home() / "pash/evaluation/benchmarks"
    S = {(s["cmd"], s["side"]): s for s in all_sides()}
    sets = {
        "v1-pash": {c: S[(c, "v1-pash")] for c in COMMANDS},
        "v1-main": {c: S.get((c, "v1-main"), S[(c, "v1-pash")]) for c in COMMANDS},
        "naive": {c: S[(c, NAIVE_FIRST[c])] for c in COMMANDS},
        "pash-own": {},
        "none": {c: S[(c, "none")] for c in COMMANDS},
    }
    folders = {n: build_set(n, ch) for n, ch in sets.items()}
    shim = ROOT / "shim_all"
    shim.mkdir(exist_ok=True)
    for c in COMMANDS + EXTRA:
        real = shutil.which(c, path="/usr/bin:/bin")
        if real:
            (shim / c).write_text(f"#!/bin/bash\nprintf '%s\\t%s\\n' {c} \"$*\" >> \"${{STANDIN_LOG:-/dev/null}}\"\n"
                                  f"exec {real} \"$@\"\n")
            (shim / c).chmod(0o755)
    # the suites' own inputs could not be fetched (their server did not answer), so the scripts read
    # this task's prepared text instead; the scripts themselves are run unchanged
    data = ROOT / "bench_input"
    if data.exists():
        shutil.rmtree(data)
    (data / "unix50").mkdir(parents=True)
    for n in ["1", "2", "3", "4", "5", "6", "7", "8", "10", "11", "12"] + [f"9.{i}" for i in range(1, 10)]:
        os.link(INPUT, data / "unix50" / f"{n}.txt")
    subprocess.run(f"sort /usr/share/dict/words > {data}/dict.txt; ls /usr/bin/* | head -400 > {data}/all_cmds.txt",
                   shell=True, check=True)
    suite_env = {
        "oneliners": {"IN": str(BIG if args.big else INPUT), "dict": str(data / "dict.txt")},
        "unix50": {"IN_PRE": str(data / "unix50")},
    }
    out_path = OUT / "scripts.jsonl"
    done = {(r["script"], r["set"]) for r in jl(out_path)} if out_path.exists() else set()
    with open(out_path, "a") as f:
        for suite in ("oneliners", "unix50"):
            names = sorted(p.name for p in (bench / suite).glob("*.sh") if ".aux." not in p.name)
            for name in names:
                tag = f"{suite}/{name}"
                rdir = ROOT / "runs" / f"script_{suite}_{name}"
                if rdir.exists():
                    shutil.rmtree(rdir)
                rdir.mkdir(parents=True)

                def fresh():
                    w = rdir / "w"
                    if w.exists():
                        shutil.rmtree(w)
                    w.mkdir()
                    for p in (bench / suite).glob("*.sh"):
                        shutil.copy(p, w / p.name)
                    return w

                env = dict(os.environ)
                env.update(suite_env[suite])
                if suite == "oneliners" and name == "shortest-scripts.sh":
                    env["IN"] = str(data / "all_cmds.txt")
                env["PATH"] = f"{shim}:{env['PATH']}"
                env["PASH_TOP"] = PASH_TOP
                w = fresh()
                env["STANDIN_LOG"] = str(rdir / "bash.standin")
                base = run_script(["bash", str(w / name)], w, rdir / "bash.out", env=env, timeout=args.timeout)
                base_counts = counts(rdir / "bash.standin")
                ref = file_sha(rdir / "bash.out")
                for sname, folder in folders.items():
                    if (tag, sname) in done:
                        continue
                    w = fresh()
                    log, standin, out = rdir / "p.log", rdir / "p.standin", rdir / "p.out"
                    for x in (log, standin):
                        x.unlink(missing_ok=True)
                    env["STANDIN_LOG"] = str(standin)
                    res = run_script([f"{PASH_TOP}/pa.sh", "-w", str(WIDTH), "-d", "2", "--log_file", str(log),
                                      "--local-annotations-dir", str(folder), str(w / name)], w, out, env=env,
                                     timeout=args.timeout)
                    lg = read_log(log, "sort")
                    got = counts(standin)
                    more = {c: n for c, n in got.items() if n > base_counts.get(c, 0)}
                    if res["timed_out"]:
                        state = "timed out"
                    elif lg is None:
                        state = "unknown"
                    elif lg["r_split"] + lg["split_file"] > 0 and more:
                        state = "split"
                    elif lg["r_split"] + lg["split_file"] == 0 and not more:
                        state = "PaSh error" if lg["tracebacks"] else "not split"
                    else:
                        state = "unknown"
                    rec = {"suite": suite, "script": tag, "set": sname, "state": state, "split_commands": more,
                           "copies": dict(got), "bash_copies": dict(base_counts),
                           "split_steps_in_log": (lg or {}).get("r_split", 0) + (lg or {}).get("split_file", 0),
                           "out_same": file_sha(out) == ref, "out_bytes": out.stat().st_size,
                           "bash_out_bytes": (rdir / "bash.out").stat().st_size, "rc": res["rc"],
                           "bash_rc": base["rc"], "seconds": res["seconds"], "bash_seconds": base["seconds"],
                           "tracebacks": sorted(set((lg or {}).get("tracebacks") or [])),
                           "notes": (lg or {}).get("notes"), "stderr": res["stderr"][-300:],
                           "input_bytes": (BIG if (args.big and suite == "oneliners") else INPUT).stat().st_size}
                    if lg is not None:
                        (OUT / "logs_scripts").mkdir(parents=True, exist_ok=True)
                        with open(log, "rb") as a, gzip.open(OUT / "logs_scripts" / f"{suite}_{name}__{sname}.log.gz", "wb") as g:
                            g.write(a.read())
                    f.write(json.dumps(rec, sort_keys=True) + "\n")
                    f.flush()
                shutil.rmtree(rdir, ignore_errors=True)
                print(tag, flush=True)


MID = ROOT / "input/mid.txt"
HEAVY = [  # lines whose command does real work per input line, so a split can show in the time
    ("grep", "grep '\\(.\\).*\\1\\(.\\).*\\2\\(.\\).*\\3\\(.\\).*\\4'"),
    ("grep", "grep -i '\\(.\\).*\\1\\(.\\).*\\2\\(.\\).*\\3\\(.\\).*\\4' f1"),
]


def cmd_heavy(args):
    """Every side of the command, five repeats, larger input. Output is checked against bash each time."""
    global INPUT
    small = INPUT
    out_path = OUT / "timing_heavy.jsonl"
    out_path.unlink(missing_ok=True)
    if not MID.exists():
        make_input(MID, 300000, 24)
    with open(out_path, "a") as f:
        for n, (cmd, line) in enumerate(HEAVY):
            INPUT = MID
            b = bind(cmd, line)
            INPUT = small
            rdir = ROOT / "runs" / f"heavy_{n}"
            rdir.mkdir(parents=True, exist_ok=True)
            script = rdir / "script.sh"
            script.write_text(b["script"])
            bash_t = []
            for _ in range(args.repeats):
                cwd = prepare(rdir / "w", b, source=MID)
                bash_t.append(run_script(["bash", str(script)], cwd, rdir / "bash.out", timeout=600,
                                         env=pash_env(rdir / "b.standin"))["seconds"])
            ref = file_sha(rdir / "bash.out")
            for s in [x for x in all_sides() if x["cmd"] == cmd]:
                ans = brief(answers_for(s, [("h", b["line_run"])])["h"])
                ts, states, same, copies = [], [], [], []
                for _ in range(args.repeats):
                    cwd = prepare(rdir / "w", b, source=MID)
                    res, log, out = run_pash(script, cwd, side_dir(s), rdir, "t", cmd, timeout=600)
                    ts.append(res["seconds"])
                    states.append(classify(res["log"], res["copies"], b["baseline"], res)[0])
                    same.append(file_sha(out) == ref)
                    copies.append(res["copies"])
                f.write(json.dumps({"cmd": cmd, "line": line, "script": b["script"].strip().replace(str(MID), "mid.txt"),
                                    "side": s["side"], "allows_split": ans["allows_split"], "bash_seconds": bash_t,
                                    "pash_seconds": ts, "states": states, "out_same": same, "copies": copies,
                                    "input_bytes": MID.stat().st_size}) + "\n")
                f.flush()
                print(cmd, line[:30], s["side"], states[0], ts, flush=True)
            shutil.rmtree(rdir, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="what", required=True)
    sub.add_parser("build")
    c = sub.add_parser("controls"); c.add_argument("--out")
    sub.add_parser("answers")
    s = sub.add_parser("select"); s.add_argument("--cap", type=int, default=40)
    r = sub.add_parser("run")
    r.add_argument("--cmd", nargs="*"); r.add_argument("--set", nargs="*"); r.add_argument("--side", nargs="*")
    r.add_argument("--limit", type=int); r.add_argument("--out"); r.add_argument("--redo-unknown", action="store_true")
    t = sub.add_parser("timing"); t.add_argument("--limit", type=int, default=3); t.add_argument("--repeats", type=int, default=5)
    b = sub.add_parser("scripts"); b.add_argument("--big", action="store_true"); b.add_argument("--timeout", type=int, default=300)
    sub.add_parser("causes")
    sub.add_parser("reclassify")
    h = sub.add_parser("heavy"); h.add_argument("--repeats", type=int, default=5)
    args = ap.parse_args()
    {"heavy": cmd_heavy, "reclassify": cmd_reclassify, "build": cmd_build, "controls": cmd_controls, "answers": cmd_answers, "select": cmd_select,
     "run": cmd_run, "timing": cmd_timing, "scripts": cmd_scripts, "causes": cmd_causes}[args.what](args)


if __name__ == "__main__":
    main()
