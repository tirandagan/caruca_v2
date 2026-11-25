#!/usr/bin/env python3
"""Koala scripts under bash and under PaSh with several sets of annotation files.

Runs INSIDE the Lima VM `pash`; reads this folder, the naive LLM's files and Caruca's files through the
read-only Mac mount.

    python3 run_koala.py build                  # annotation sets, stand-in programs, manifest.json
    python3 run_koala.py discover [--group G]   # how each Koala script is started (see below)
    python3 run_koala.py answers  [--script S]  # each set's annotation answer for each command invocation
    python3 run_koala.py run      [--script S] [--repeats 5] [--sets ...]   # instrumented + plain timed runs
    python3 run_koala.py controls [--script S]  # the checks that the folder decides

S is "<group>/<script name>", e.g. oneliners/spell. Sets: pash-own, naive, caruca-pash, caruca-main, and
the control sets. In every set a command the set has no files for keeps PaSh's own files.

How a script is started is not written by hand. `discover` makes a shadow copy of each Koala group (a
git folder whose entries are links to the real group, except its launcher, which is copied, and its
`outputs`/`tmp` folders, which are its own), runs the group's own launcher (`execute.sh`, small size;
web-search at min) with Koala's shell hook KOALA_SHELL pointed at a recorder, and keeps each call: the
arguments, working folder, environment and the file standard output went to. `run` replays those calls
with bash or PaSh. Files a script writes under the shadow group's `outputs` are hashed too.

Work is written under ~/t024 in the VM (T024_ROOT); results go to ~/t024/out and are copied out.
Nothing in PaSh's install, PaSh's source or the Koala checkout is changed: each set is a private copy of
the installed pash_annotations package, chosen for one run with `pash --local-annotations-dir`.

Copied from task 022's runner (naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/
pash_runs/run_pash.py): three_files, build_set, add_to_name_table, the stand-in programs and the rule
that leaves out PaSh's own housekeeping calls (counts), read_log, run_script, and the scorer's WORKER.
Changed: the stand-in records each argument separately (spell.sh passes a newline as an argument), and
the logs are read for this PaSh's "Received data: Compile" / "Optimized script saved in" lines.
"""

import argparse
import gzip
import hashlib
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LEDGER = REPO / "naive_llm_caruca/fig7_campaign/ledger.jsonl"
SIDES = REPO / "naive_llm_caruca/comparisons/2026-11-11_pash_annotations_v1_vs_naive/sides.jsonl"
ROOT = Path(os.environ.get("T024_ROOT", Path.home() / "t024"))
OUT = ROOT / "out"
STOCK = Path.home() / "pash/python_pkgs/lib/python3.12/site-packages/pash_annotations"
PASH = Path.home() / "pash/python_pkgs/bin/pash"
PASH_SRC = Path.home() / "pash"
KOALA = Path.home() / "koala"
SHADOW = ROOT / "shadow"
SHIM = ROOT / "shim"
SHIM_LOOKUP = ":".join(["/usr/local/legacy-bin", "/usr/local/bin", "/usr/bin", "/bin",
                        str(Path.home() / "koala/.tools/nodejs18/bin")])
WIDTH = 8
TIMEOUT = 1800
GEN = "annotation_generation/annotation_generators"
DATA = "parser/command_flag_option_info/data"
GROUPS = {"oneliners": "--small", "unixfun": "--small", "covid": "--small", "nlp": "--small",
          "weather": "--small", "web-search": "--min"}
# Tiran, 2026-11-24: also analytics (without port-scan), file-mod, bio.sh at min, the two pkg scripts once
# at min. Discovered by default only once the inputs worker has written orchestration/inputs_setup.md.
EXTRA_GROUPS = {"analytics": "--small", "file-mod": "--small", "bio": "--min"}  # pkg skipped (Tiran)
KEEP_ONLY = {"bio": {"bio"}}
LEAVE_OUT = {"analytics": {"port-scan"}}
ONCE = {"pkg"}  # one timed repeat
INPUTS_READY = Path(__file__).resolve().parent / "orchestration/inputs_setup.md"
if INPUTS_READY.exists():
    GROUPS = GROUPS | EXTRA_GROUPS
OWN_DIRS = {"outputs", "tmp", "plots"}  # folders a group writes into; the shadow copy has its own
COVERAGE = HERE / "orchestration/coverage.jsonl"  # the inventory worker's list of commands per script


def cls(cmd):
    return "".join(p.capitalize() for p in cmd.split("_"))


def jl(path):
    op = gzip.open if str(path).endswith(".gz") else open
    with op(path, "rt") as f:
        return [json.loads(x) for x in f if x.strip()]


def file_sha(p, full=False):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest() if full else h.hexdigest()[:16]


# ------------------------------------------------------------------ annotation sources and sets

def naive_runs():
    """The Fig. 7 campaign's first run of each command, and the folder holding its three files."""
    return {r["command"]: {"source": "naive LLM, " + r["run_folder"].split("/")[-1],
                           "run_folder": r["run_folder"], "dir": REPO / r["run_folder"] / "output/annotation"}
            for r in jl(LEDGER) if r["repeat"] == 1}


def naive_repeat(cmd, repeat):
    r = next(r for r in jl(LEDGER) if r["command"] == cmd and r["repeat"] == repeat)
    return {"source": "naive LLM, " + r["run_folder"].split("/")[-1], "run_folder": r["run_folder"],
            "dir": REPO / r["run_folder"] / "output/annotation"}


def caruca_files(main):
    """Caruca's (v1's) files: the v1-pash rows, or with main=True the v1-main row where a command has one."""
    rows = [r for r in jl(SIDES) if r["side"] in ("v1-pash", "v1-main")]
    out = {r["cmd"]: r for r in rows if r["side"] == "v1-pash"}
    if main:
        out.update({r["cmd"]: r for r in rows if r["side"] == "v1-main"})
    return {c: {"source": f"Caruca, {r['side']} ({'/'.join(Path(r['dir']).parts[-3:])})", "dir": Path(r["dir"])}
            for c, r in out.items()}


def three_files(pkg, c):
    C = cls(c)
    return [pkg / DATA / f"{c}.json",
            pkg / GEN / f"InputOutputInfoGenerator{C}.py",
            pkg / GEN / f"ParallelizabilityInfoGenerator{C}.py"]


def add_to_name_table(pkg, c):
    """PaSh only looks up commands in a fixed name table; most of the outside commands are not in it."""
    ag = pkg / "annotation_generation/AnnotationGeneration.py"
    t = ag.read_text()
    head = "DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {\n"
    if f'"{c}":' not in t:
        assert head in t
        ag.write_text(t.replace(head, head + f'    "{c}": "{cls(c)}",\n', 1))


def stock_commands():
    t = (STOCK / "annotation_generation/AnnotationGeneration.py").read_text()
    body = t.split("DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {", 1)[1].split("}", 1)[0]
    return sorted(re.findall(r'"([^"]+)"\s*:', body))


def sources_of(replace=None, remove=()):
    """{cmd: source text} for every command PaSh would find files for in a set."""
    used = {c: "PaSh's own" for c in stock_commands()}
    used.update({c: v["source"] for c, v in (replace or {}).items()})
    used.update({c: "none (files removed)" for c in remove})
    return used


def source_kind(used, c):
    """Tiran's split: ours (the set's own files), pash-own (PaSh's, the set has none), none (nobody has one)."""
    s = used.get(c)
    if s is None or s.startswith("none"):
        return "none"
    return "pash-own" if s == "PaSh's own" else "ours"


def build_set(name, replace=None, remove=()):
    """Private copy of the installed package. `replace`: {cmd: {"dir", "source"}} whose three files replace
    PaSh's (or are added). `remove`: commands whose three files are deleted (no annotation at all).
    Returns {cmd: source} for every command PaSh would look up in this set."""
    root = ROOT / "sets" / name
    if root.exists():
        shutil.rmtree(root)
    pkg = root / "pash_annotations"
    shutil.copytree(STOCK, pkg, ignore=shutil.ignore_patterns("__pycache__"))
    used = {c: "PaSh's own" for c in stock_commands()}
    for c, v in (replace or {}).items():
        d, dst = Path(v["dir"]), three_files(pkg, c)
        for s, t in zip(three_files(Path("."), c), dst):
            shutil.copy(d / s.name, t)
        add_to_name_table(pkg, c)
        used[c] = v["source"]
    for c in remove:
        for f in three_files(pkg, c):
            f.unlink(missing_ok=True)
        used[c] = "none (files removed)"
    return root, used


def sets_wanted():
    nv = naive_runs()
    return {
        "pash-own": {},
        "pash-own-copy": {},  # timing control: a second, byte-identical copy of PaSh's own files
        "naive": {"replace": nv},
        # the naive set with sed's files from the campaign's second sed run (orchestrator, 2026-11-24)
        "naive-sed2": {"replace": nv | {"sed": naive_repeat("sed", 2)}},
        "caruca-pash": {"replace": caruca_files(main=False)},
        "caruca-main": {"replace": caruca_files(main=True)},
        # controls: the folder must decide what splits
        "naive-no-sort": {"replace": nv, "remove": ["sort"]},
        "naive-col-pash-own": {"replace": {c: v for c, v in nv.items() if c != "col"}},
        "naive-cat-pash-own": {"replace": {c: v for c, v in nv.items() if c != "cat"}},
        "naive-sed-pash-own": {"replace": {c: v for c, v in nv.items() if c != "sed"}},
    }


MAIN_SETS = ["bash", "pash-own", "naive", "naive-sed2", "caruca-pash", "caruca-main", "pash-own-copy"]
TIMING_ONLY_SETS = {"pash-own-copy"}
DISPLAY_NAMES = {"bash": "Plain bash", "pash-own": "PaSh's own files", "naive": "Naive LLM's files",
                 "caruca-pash": "Caruca's files, PaSh grammar", "caruca-main": "Caruca's files, main grammar",
                 "pash-own-copy": "PaSh's own files, second copy",
                 "naive-sed2": "Naive LLM, sed file v2",
                 "naive-no-sort": "Control: naive LLM's files, sort's files removed",
                 "naive-col-pash-own": "Control: naive LLM's files, PaSh's own col files",
                 "naive-cat-pash-own": "Control: naive LLM's files, PaSh's own cat files",
                 "naive-sed-pash-own": "Control: naive LLM's files, PaSh's own sed files"}
CONTROL_SETS = ["bash", "naive", "naive-no-sort", "naive-col-pash-own", "naive-cat-pash-own", "naive-sed-pash-own"]


def pkg_hash(pkg):
    h = hashlib.sha256()
    for p in sorted(pkg.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            h.update(str(p.relative_to(pkg)).encode() + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()[:16]


def make_shim(names):
    """A stand-in for each program, first on PATH: one record per start, each argument kept separately."""
    if SHIM.exists():
        shutil.rmtree(SHIM)
    SHIM.mkdir(parents=True)
    real = {}
    for c in sorted(names):
        r = shutil.which(c, path=SHIM_LOOKUP)
        if not r:  # no stand-in for a program that is not installed: a script's own test for it must fail
            continue
        real[c] = r
        # the stand-in hands over to the next program of that name on the search path, so a group's own
        # builds (file-mod's /usr/local/legacy-bin) are used exactly as without it
        (SHIM / c).write_text(
            "#!/bin/bash\n"
            "if [ -n \"$STANDIN_LOG\" ]; then _a=; [ $# -gt 0 ] && printf -v _a '\\x1f%s' \"$@\"; "
            f"printf '%s%s\\x1e' {c} \"$_a\" >> \"$STANDIN_LOG\"; fi\n"
            "IFS=:\n"
            f"for _d in $PATH; do [ \"$_d\" = \"{SHIM}\" ] && continue; "
            f"[ -f \"$_d/{c}\" ] && [ -x \"$_d/{c}\" ] && exec \"$_d/{c}\" \"$@\"; done\n"
            f"exec {r} \"$@\"\n")
        (SHIM / c).chmod(0o755)
    return real


def script_programs(text):
    """Program names a script may start: words of the script (comments removed) that are on the system."""
    text = re.sub(r"(^|\s)#.*", r"\1", text)
    words = set(re.findall(r"(?<![\w$/.-])([a-z][a-z0-9_]*)(?![\w/.-])", text))
    return {w for w in words if shutil.which(w, path="/usr/local/bin:/usr/bin:/bin")} - {"bash", "sh", "env"}


def coverage_rows():
    return jl(COVERAGE) if COVERAGE.exists() else []


def coverage_commands(sid):
    g, name = sid.split("#")[0].split("/", 1)
    return sorted({c for r in coverage_rows() if r["group"] == g and r["script"] == name for c in r["commands"]})


def all_script_programs():
    progs = set()
    for g in GROUPS:
        for p in (KOALA / g / "scripts").rglob("*.sh"):
            progs |= script_programs(p.read_text(errors="replace"))
    return progs


def cmd_build(args):
    OUT.mkdir(parents=True, exist_ok=True)
    built = {}
    for name, spec in sets_wanted().items():
        root, used = build_set(name, **spec)
        built[name] = {"folder": str(root), "package_sha": pkg_hash(root / "pash_annotations"),
                       "source_per_command": dict(sorted(used.items()))}
    real = make_shim(all_script_programs() | {c for r in coverage_rows() for c in r["commands"]} | {"sort", "cat", "rm"})
    (OUT / "sets.json").write_text(json.dumps({"display_names": DISPLAY_NAMES, "main": MAIN_SETS,
                                               "timing_only": sorted(TIMING_ONLY_SETS), "controls": CONTROL_SETS},
                                              indent=1))
    sh = lambda c, cwd=None: subprocess.run(c, shell=True, capture_output=True, text=True, cwd=cwd).stdout.strip()

    def hashes(srcs):
        return {c: {"source": v["source"], "dir": str(v["dir"]),
                    "files": {f.name: file_sha(Path(v["dir"]) / f.name, True) for f in three_files(Path("."), c)}}
                for c, v in sorted(srcs.items())}
    stock_files = sorted(p for p in STOCK.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    man = {
        "when": time.strftime("%Y-%m-%d %H:%M:%S %z"),
        "machine": {"vm": "Lima VM `pash` on a Mac", "uname": sh("uname -srm"), "cpus": sh("nproc"),
                    "os": sh(". /etc/os-release; echo $PRETTY_NAME"), "coreutils": sh("sort --version | head -1"),
                    "bash": sh("bash --version | head -1"), "python": sys.version.split()[0]},
        "pash": {"commit": sh("git rev-parse HEAD", PASH_SRC), "dirty_files": sh("git status --short", PASH_SRC),
                 "annotations_version": sh(f"{PASH.parent}/pip show pash-annotations | sed -n 2p"),
                 "stock_package": str(STOCK), "stock_package_sha": pkg_hash(STOCK), "stock_files": len(stock_files),
                 "stock_commands": stock_commands(),
                 "settings": f"pash -w {WIDTH} -d 2 --log_file <file> --local-annotations-dir <set> <script> <args>"},
        "koala": {"commit": sh("git rev-parse HEAD", KOALA), "dirty_files": sh("git status --short", KOALA),
                  "sizes": GROUPS},
        "caruca_v2_commit": sh("git rev-parse HEAD", REPO),
        "caruca_v1_branch_commit": sh("git rev-parse HEAD", next(iter(caruca_files(False).values()))["dir"]),
        "naive": {"rule": "fig7_campaign/ledger.jsonl, the row with repeat 1 for each command",
                  "commands": hashes(naive_runs())},
        "caruca": {"rule": "sides.jsonl of the task-021 comparison: v1-pash rows; caruca-main takes the v1-main "
                           "row where a command has one", "caruca-pash": hashes(caruca_files(False)),
                   "caruca-main": hashes(caruca_files(True))},
        "sets": built, "stand_in_programs": real,
    }
    (OUT / "manifest.json").write_text(json.dumps(man, indent=1, sort_keys=True))
    print(f"built {len(built)} sets; stand-ins for {len(real)} programs")


# ------------------------------------------------------------------ discovering how scripts are started

RECORDER = r'''#!/usr/bin/env python3
import json, os, sys
rec = {"argv": sys.argv[1:], "cwd": os.getcwd(), "env": dict(os.environ),
       "stdout": os.path.realpath("/proc/self/fd/1")}
with open(os.environ["KOALA_RECORD"], "a") as f:
    f.write(json.dumps(rec) + "\n")
'''


def shadow_group(g):
    """Shadow copy of a Koala group: links to the real entries, its own launcher copy and output folders."""
    d = SHADOW / g
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    for e in (KOALA / g).iterdir():
        if e.name in OWN_DIRS:
            (d / e.name).mkdir()
        elif e.name == "execute.sh":
            shutil.copy(e, d / e.name)
        else:
            (d / e.name).symlink_to(e)
    for name in OWN_DIRS:
        (d / name).mkdir(exist_ok=True)
    # launchers that use $TOP/.tools (web-search's node) need Koala's tool folder at the shadow's top
    if not (SHADOW / ".tools").exists() and (KOALA / ".tools").exists():
        (SHADOW / ".tools").symlink_to(KOALA / ".tools")
    return d


def input_sizes(words, gdir, n_args):
    """Files and folders under the group's inputs named by the script's arguments (the first n_args words)
    or its environment. An entry inside another entry is not counted again. Environment entries can be
    left over from an earlier script of the same launcher, so each entry says where it came from."""
    out, seen = [], set()
    for i, w in enumerate(words):
        p = Path(w)
        if not w.startswith("/") or not p.exists():
            continue
        real = p.resolve()
        if "inputs" not in real.parts and "min_inputs" not in real.parts:
            continue
        if real in seen:
            continue
        seen.add(real)
        n = real.stat().st_size if real.is_file() else sum(x.stat().st_size for x in real.rglob("*") if x.is_file())
        out.append({"path": home(str(p)), "real": real, "bytes": n, "from": "argument" if i < n_args else "environment"})
    out = [x for x in out if not any(y is not x and y["real"] in x["real"].parents for y in out)]
    for x in out:
        x.pop("real")
    return out


def cmd_discover(args):
    OUT.mkdir(parents=True, exist_ok=True)
    SHADOW.mkdir(parents=True, exist_ok=True)
    if not (SHADOW / ".git").exists():  # launchers find their top folder with git
        subprocess.run(["git", "init", "-q", str(SHADOW)], check=True)
    rec_prog = ROOT / "recorder.py"
    rec_prog.write_text(RECORDER)
    rec_prog.chmod(0o755)
    path = OUT / "invocations.jsonl"
    keep = [r for r in jl(path)] if path.exists() else []
    groups = args.group or list(GROUPS)
    sizes = GROUPS | EXTRA_GROUPS
    keep = [r for r in keep if r["group"] not in groups]
    base = dict(os.environ)
    for g in groups:
        d = shadow_group(g)
        log = ROOT / f"record_{g}.jsonl"
        log.unlink(missing_ok=True)
        env = dict(base, KOALA_SHELL=str(rec_prog), KOALA_RECORD=str(log))
        p = subprocess.run(["bash", str(d / "execute.sh"), sizes[g]], cwd=d, env=env, capture_output=True,
                           text=True, timeout=600)
        with open(OUT / "discover_log.jsonl", "a") as dl:
            dl.write(json.dumps({"group": g, "when": time.strftime("%Y-%m-%d %H:%M:%S %z"), "exit": p.returncode,
                                 "stderr_tail": p.stderr[-800:]}) + "\n")
        for r in (jl(log) if log.exists() else []):
            script = Path(r["argv"][0])
            name = script.name.removesuffix(".sh")
            if (g in KEEP_ONLY and name not in KEEP_ONLY[g]) or name in LEAVE_OUT.get(g, ()):
                continue
            env_kept = {k: v for k, v in r["env"].items()
                        if k not in ("KOALA_SHELL", "KOALA_RECORD", "_", "SHLVL", "OLDPWD", "PWD")}
            out_name = Path(r["stdout"]).name
            size = sizes[g].lstrip("-")
            hfile = KOALA / g / "hashes" / size / (out_name.removesuffix(".out") + ".hash")
            inputs = input_sizes(r["argv"][1:] + [v for k2, v in env_kept.items()
                                                   if k2 not in ("PATH", "HOME", "SHELL", "XDG_DATA_DIRS")], d,
                                 len(r["argv"]) - 1)
            keep.append({"id": f"{g}/{name}", "group": g, "script": name, "argv": r["argv"], "cwd": r["cwd"],
                         "inputs": inputs, "input_bytes": sum(x["bytes"] for x in inputs),
                         "input_bytes_from_arguments": sum(x["bytes"] for x in inputs if x["from"] == "argument"),
                         "env": env_kept, "stdout_was": r["stdout"],
                         "expected_hash": hfile.read_text().strip() if hfile.exists() else None,
                         "expected_hash_file": str(hfile.relative_to(KOALA)) if hfile.exists() else None})
        n = sum(1 for r in keep if r["group"] == g)
        print(f"{g:11} launcher exit {p.returncode}; {n} script calls recorded")
    ids = Counter(r["id"] for r in keep)
    for r in keep:  # a script started more than once by its launcher gets a numbered id
        if ids[r["id"]] > 1:
            r["id"] = f"{r['id']}#{sum(1 for x in keep[:keep.index(r)] if x['id'].split('#')[0] == r['id'])}"
    with open(path, "w") as f:
        for r in keep:
            f.write(json.dumps(r, sort_keys=True) + "\n")


def script_path(inv):
    """The script file; a launcher may give it relative to the folder it runs from (unixfun: ./scripts/N.sh)."""
    p = Path(inv["argv"][0])
    return p if p.is_absolute() else Path(inv["cwd"]) / p


def invocation(sid):
    rows = {r["id"]: r for r in jl(OUT / "invocations.jsonl")}
    if sid not in rows:
        sys.exit(f"unknown script {sid}; run `discover` first. Known: {sorted(rows)}")
    return rows[sid]


# ------------------------------------------------------------------ running

def script_env(inv, standin_log=None, shim=True):
    env = dict(inv["env"])
    env["HOME"] = str(Path.home())
    env["PATH"] = f"{PASH.parent}:{env.get('PATH', '/usr/bin:/bin')}"
    if shim:
        env["PATH"] = f"{SHIM}:{env['PATH']}"
    env.pop("STANDIN_LOG", None)
    if standin_log:
        env["STANDIN_LOG"] = str(standin_log)
    return env


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


def read_log(path, progs):
    if not path.exists() or path.stat().st_size == 0:
        return None
    t = path.read_text(errors="replace")
    t = re.sub(r"/tmp/pash_\w+/+[0-9a-f]*/?", "TMP/", t)
    tracebacks = []
    for m in re.finditer(r"Traceback \(most recent call last\):\n((?:  .*\n)+)(\S[^\n]*)", t):
        frames = re.findall(r'File ".*?/([^/"]+)", line (\d+), in (\w+)', m.group(1))
        where = "{}:{} {}".format(*frames[-1]) if frames else "?"
        tracebacks.append(f"{m.group(2).strip()[:200]} @ {where}")
    warnings = sorted({ln.strip()[:300] for ln in t.splitlines() if "WARNING" in ln or "Exception caught" in ln})
    workers = {}
    for c in progs:
        n = len(re.findall(r"r_wrap bash -c ' *" + re.escape(c) + r"\b", t)) \
            + len(re.findall(r"^\{ " + re.escape(c) + r" .*#fifo.*& \}$", t, re.M))
        if n:
            workers[c] = n
    return {
        "bytes": len(t),
        "regions_sent": len(re.findall(r"Received data: Compile", t)),
        "regions_parallel": len(re.findall(r"Optimized script saved in", t)),
        "r_split": len(re.findall(r"runtime/r_split ", t)),
        "worker_copies_in_script": workers,
        "warnings": warnings,
        "tracebacks": tracebacks,
    }


def counts(path):
    """Starts per program, leaving out PaSh's housekeeping calls (task 022's rule): a call naming a file
    under PaSh's temporary folder is PaSh's own, unless it names one of PaSh's pipes and the program is
    not rm or cat (PaSh removes its pipes with rm and joins pieces with cat)."""
    c, calls = Counter(), []
    if path.exists():
        for rec in path.read_bytes().decode(errors="replace").split("\x1e"):
            if not rec:
                continue
            name, *argv = rec.split("\x1f")
            rest = " ".join(argv)
            if "/tmp/pash_" in rest and ("#fifo" not in rest or name in ("rm", "cat")):
                continue
            c[name] += 1
            calls.append([name] + argv)
    return c, calls


def outputs_manifest(gdir):
    rows = []
    for p in sorted(x for d in sorted(OWN_DIRS) for x in (gdir / d).rglob("*")):
        if p.is_file():
            rows.append([str(p.relative_to(gdir)), p.stat().st_size, file_sha(p, True)])
    return rows


def run_one(sname, inv, rdir, tag, shim=True):
    """sname 'bash' or a set name. The group's shadow output folders are emptied before each run."""
    gdir = SHADOW / inv["group"]
    for name in OWN_DIRS:
        shutil.rmtree(gdir / name, ignore_errors=True)
        (gdir / name).mkdir()
    stdout_was = Path(inv["stdout_was"])
    if str(stdout_was).startswith(str(gdir)):  # the launcher's own output folder, e.g. outputs/small/
        stdout_was.parent.mkdir(parents=True, exist_ok=True)
    standin, log, out = rdir / f"{tag}.standin", rdir / f"{tag}.log", rdir / f"{tag}.out"
    for f in (standin, log):
        f.unlink(missing_ok=True)
    env = script_env(inv, standin if shim else None, shim)
    script, rest = inv["argv"][0], inv["argv"][1:]
    if sname == "bash":
        argv = ["bash", script] + rest
    else:
        argv = [str(PASH), "-w", str(WIDTH), "-d", "2", "--log_file", str(log),
                "--local-annotations-dir", str(ROOT / "sets" / sname), script] + rest
    res = run_script(argv, inv["cwd"], out, env=env)
    res["files"] = outputs_manifest(gdir)
    return res, standin, log, out


def state_of(lg, more, res):
    if res["timed_out"]:
        return "timed out"
    if lg is None:
        return "unknown (no log)"
    if lg["regions_parallel"] > 0 and lg["r_split"] > 0 and (more is None or more):
        return "split"
    if lg["regions_parallel"] == 0 and not more:
        return "fell back to bash" if lg["regions_sent"] else "nothing sent to PaSh"
    if lg["regions_parallel"] > 0 and lg["r_split"] == 0 and not more:
        return "compiled, nothing split"
    return "unknown (signals disagree)"


REGION_HELPER = r'''
# Runs with PaSh's own Python. Reads PaSh's pickled regions and gives, per region, its text and every
# command use with its words (variables filled in from the values PaSh logged); and a comparison key
# (command name + options and their values, parsed by the set's own parser data) for any command line.
import sys, pickle, json, os, shlex
top, setroot = os.environ["PASH_TOP"], os.environ["SET_ROOT"]
sys.path[:0] = [setroot, top + "/compiler", top]
try:
    from pash_annotations.parser.parser import parse
    from pash_annotations.datatypes.BasicDatatypes import Option
except Exception:
    parse = None
req = json.load(sys.stdin)
def word(a, vs):
    out, exact = "", True
    for c in a:
        n = type(c).__name__
        if n in ("CArgChar", "EArgChar"):
            out += chr(c.char)
        elif n == "QArgChar":
            s, e = word(c.arg, vs); out += s; exact = exact and e
        elif n == "VArgChar" and getattr(c, "fmt", None) == "Normal" and c.var in vs:
            out += vs[c.var]
        else:
            exact = False
            try:
                out += c.pretty()
            except Exception:
                out += "?"
    return out, exact
def walk(o, acc, vs, depth=0):
    if depth > 400:
        return
    if type(o).__name__ == "CommandNode" and o.arguments:
        ws = [word(a, vs) for a in o.arguments]
        acc.append({"argv": [w for w, _ in ws], "exact": all(e for _, e in ws)})
    if isinstance(o, (list, tuple)):
        for x in o:
            walk(x, acc, vs, depth + 1)
    elif hasattr(o, "__dict__"):
        for v in vars(o).values():
            walk(v, acc, vs, depth + 1)
def key(argv):
    if not argv:
        return "[]"
    if parse is not None:
        try:
            inv = parse(shlex.join(argv))
            fos = sorted([str(fo.get_name()), str(fo.get_arg()) if isinstance(fo, Option) else ""]
                         for fo in inv.flag_option_list)
            return json.dumps([argv[0], fos])
        except Exception:
            pass
    return json.dumps([argv[0], sorted(t for t in argv[1:] if t.startswith("-"))])
regions = {}
for f, vs in req["irs"].items():
    try:
        r = pickle.load(open(f, "rb"))
        uses = []
        walk(r, uses, vs)
        for u in uses:
            u["key"] = key(u["argv"])
        regions[f] = {"text": "\n".join(x.pretty() for x in r), "uses": uses}
    except Exception as e:
        regions[f] = {"error": repr(e)[:300]}
print(json.dumps({"regions": regions, "keys": {json.dumps(a): key(a) for a in req["argvs"]}}))
'''

PASH_PATH_HELPER = r'''
# Runs with PaSh's own Python, on the region and variables file PaSh kept (debug level 2). Replays PaSh's
# own steps: read the variables file, expand the region with PaSh's expansion code, turn each command into
# PaSh's command object with PaSh's parse_arg_list_to_command_invocation, and ask the set's two generators
# with that object. Words therefore reach the files exactly as inside PaSh (a quoted word keeps its
# quotes). Unlike PaSh, exceptions are recorded, not swallowed.
import sys, os, json, pickle, importlib
top, setroot = os.environ["PASH_TOP"], os.environ["SET_ROOT"]
sys.path[:0] = [setroot, top + "/compiler", top]
import config
from sh_expand import env_vars_util
from sh_expand.expand import expand_command, ExpansionState
from annotations_utils.util_parsing import parse_arg_list_to_command_invocation, format_arg_chars
from pash_annotations.datatypes.BasicDatatypes import Option, WhichClassForArg
import pash_annotations.annotation_generation.AnnotationGeneration as AG
GEN = "pash_annotations.annotation_generation.annotation_generators."
bash_version = tuple(int(x) for x in os.environ.get("PASH_BASH_VERSION", "5 2 21").split())
def kind_of(t):
    which, acc = t
    if which == WhichClassForArg.FILESTD:
        return acc.kind.name if acc is not None else "FILESTD?"
    return which.name
def recipe(p):
    out = {"split": p.get_splitter().kind.name}
    try:
        out["implemented"] = bool(p.are_all_parts_implemented())  # PaSh only uses recipes that pass this
    except Exception:
        out["implemented"] = None
    for k, f in (("aggregate", lambda: p.get_aggregator_spec().get_kind().name),
                 ("map", lambda: p.get_mapper_spec().kind.name)):
        try:
            out[k] = f()
        except Exception:
            out[k] = "?"
    return out
def ask(kind, cmd_inv):
    rep = AG.DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.get(cmd_inv.cmd_name)
    if rep is None:
        return "not in name table", None, None
    try:
        klass = getattr(importlib.import_module(GEN + kind + rep), kind + rep)
    except ModuleNotFoundError:
        return "no class", None, None
    except Exception as e:
        return "exception", None, "import: " + type(e).__name__ + ": " + str(e)[:300]
    try:
        g = klass(cmd_inv); g.generate_info(); info = g.get_info()
    except Exception as e:
        return "exception", None, type(e).__name__ + ": " + str(e)[:300]
    return ("no answer", None, None) if info is None else ("answered", info, None)
def commands(o, acc, depth=0):
    if depth > 400:
        return
    if type(o).__name__ == "CommandNode" and o.arguments:
        acc.append(o)
    if isinstance(o, (list, tuple)):
        for x in o:
            commands(x, acc, depth + 1)
    elif hasattr(o, "__dict__"):
        for v in vars(o).values():
            commands(v, acc, depth + 1)
req = json.load(sys.stdin)
out = {}
for f, var_file in req.items():
    res = {"uses": []}
    try:
        variables = env_vars_util.read_vars_file(var_file, bash_version) if var_file else {}
        region = pickle.load(open(f, "rb"))
        region = region if isinstance(region, list) else [region]
        nodes = []
        for ast in region:
            try:
                commands(expand_command(ast, ExpansionState(variables)), nodes)
            except Exception as e:
                res.setdefault("expansion_errors", []).append(type(e).__name__ + ": " + str(e)[:300])
                commands(ast, nodes)
        for n in nodes:
            u = {"words": [format_arg_chars(a) for a in n.arguments]}
            try:
                ci = parse_arg_list_to_command_invocation(n.arguments[0], n.arguments[1:])
            except Exception as e:
                u["parse_error"] = type(e).__name__ + ": " + str(e)[:300]
                res["uses"].append(u)
                continue
            u["flagoptions"] = [[fo.get_name(), format_arg_chars(fo.get_arg().arg_char_list) if isinstance(fo, Option) and hasattr(fo.get_arg(), "arg_char_list") else (str(fo.get_arg()) if isinstance(fo, Option) else None)] for fo in ci.flag_option_list]
            u["operands"] = [str(o.get_name()) for o in ci.operand_list]
            io_o, io, io_e = ask("InputOutputInfoGenerator", ci)
            par_o, par, par_e = ask("ParallelizabilityInfoGenerator", ci)
            u["io_outcome"], u["io_exception"] = io_o, io_e
            if io is not None:
                u["io"] = {"flagoptions": [kind_of(t) for t in io.flagoption_list_typer],
                           "operands": [kind_of(t) for t in io.operand_list_typer],
                           "stdin": io.implicit_use_of_streaming_input is not None,
                           "stdout": io.implicit_use_of_streaming_output is not None}
            u["par_outcome"], u["par_exception"] = par_o, par_e
            u["par"] = [recipe(p) for p in par.parallelizer_list] if par is not None else []
            res["uses"].append(u)
    except Exception as e:
        res["error"] = type(e).__name__ + ": " + str(e)[:300]
    out[f] = res
print(json.dumps(out))
'''


CRASH = re.compile(r"\b(NameError|AttributeError|KeyError|TypeError|AssertionError|IndexError|ValueError|"
                   r"UnboundLocalError|ImportError|ModuleNotFoundError|RecursionError|Traceback)\b")
COMPILE = re.compile(r"Received data: Compile:(\S+?)\| Variable File:(\S+?)\| Input IR File:(\S+)")
EXPANSION = re.compile(r"^Expansion: Var: (\S+) value: (.*)$", re.M)
RUNTIME_TOOL = re.compile(r"/runtime/(r_split|r_merge|r_unwrap|dgsh-tee|wait_for_output_and_sigpipe_rest|"
                          r"auto-split|split|eager)\b")

# fixed labels that open the reason of a part whose outcome is "other" (report plan 5.5)
OTHER_ALLOWED_NOT_SPLIT = "allowed by the files, not split by PaSh"
OTHER_NOTHING_SPLITTABLE = "nothing in this part can be split under this source's files"
OTHER_NO_ANSWER = "the source has files for a command, but they gave no answer"
OTHER_UNREADABLE = "the part's text could not be read back"
OTHER_UNKNOWN = "not classified"


def home(s):
    return s.replace(str(Path.home()), "~")


def file_answer_of(a):
    if a is None:
        return "no files"
    if a.get("exception"):
        return "raised"
    if a["parallelizability_outcome"] in ("no class", "not in name table") and \
            a["io_outcome"] in ("no class", "not in name table"):
        return "no files"
    if a["parallelizability_outcome"] != "answered":
        return "no answer"
    if not a["allows_split"]:
        return "says no split"
    if not any(x.get("implemented", True) for x in a["split_recipes"]):
        return "allows only a split PaSh has not implemented"
    return "allows a split"


def pash_answer(u):
    """An answer row (answers.jsonl shape) from one use replayed through PaSh's own parsing."""
    if u.get("parse_error"):
        return {"io_outcome": "parse failed", "parallelizability_outcome": "parse failed", "allows_split": False,
                "split_recipes": [], "exception": u["parse_error"], "io": None}
    par = u.get("par") or []
    return {"io_outcome": u.get("io_outcome"), "parallelizability_outcome": u.get("par_outcome"),
            "allows_split": u.get("par_outcome") == "answered" and bool(par), "split_recipes": par,
            "exception": u.get("io_exception") or u.get("par_exception"), "io": u.get("io"),
            "words": u.get("words"), "flagoptions": u.get("flagoptions"), "operands": u.get("operands")}


def answers_path(sid):
    """One answers file per script (answers/<group>_<script>.jsonl): loops make some scripts' files large."""
    return OUT / "answers" / (sid.replace("/", "_") + ".jsonl")


def load_answers(sid):
    """{(set, line): answer row} and {(set, command): [rows]} from the script's answers file."""
    by_line, by_cmd = {}, {}
    path = answers_path(sid)
    for r in (jl(path) if path.exists() else []):
        if r["id"] == sid and r.get("method") == "direct, quotes removed":
            by_line[(r["set"], r["line"])] = r
            by_cmd.setdefault((r["set"], r["command"]), []).append(r)
    return by_line, by_cmd


def ask_files(sname, argv):
    """Call the set's files directly for one command line (cached), as answers.jsonl does."""
    k = (sname, json.dumps(argv))
    if k not in _ASKED:
        p = subprocess.run([sys.executable, "-I", "-c", WORKER, str(ROOT / "sets" / sname), argv[0], cls(argv[0])],
                           input=json.dumps({"id": 0, "line": shlex.join(argv)}) + "\n", capture_output=True, text=True)
        if p.returncode or not p.stdout.strip():
            a = {"io_outcome": "worker crashed", "par_outcome": "worker crashed",
                 "crash": (p.stderr.strip().splitlines() or [""])[-1][:300]}
        else:
            a = json.loads(p.stdout.splitlines()[-1])
        par = a.get("par") or []
        _ASKED[k] = {"io_outcome": a.get("io_outcome"), "parallelizability_outcome": a.get("par_outcome"),
                     "allows_split": a.get("par_outcome") == "answered" and bool(par),
                     "split_recipes": par, "exception": a.get("io_exception") or a.get("par_exception")
                     or a.get("crash") or a.get("parse_error")}
    return _ASKED[k]


_ASKED = {}


def worker_argvs(body):
    """Each command line in PaSh's parallel script, with PaSh's pipes and redirections taken out."""
    out = []
    for ln in body.splitlines():
        s = ln.strip()
        if not (s.startswith("{ ") and s.endswith("}")) or s.startswith("{ {"):
            continue
        m = re.search(r"r_wrap bash -c '(.*?)'", s)
        txt = m.group(1) if m else s[2:].rstrip("}").strip().rstrip("&").strip()
        if not m and (RUNTIME_TOOL.search(txt) or txt.startswith(("mkfifo", "rm -f"))):
            continue
        try:
            toks = shlex.split(txt)
        except ValueError:
            continue
        clean, skip, fifo_args = [], False, 0
        for t in toks:
            if skip:
                skip = False
                continue
            if re.fullmatch(r"\d*(<|>|>>|<>)", t):
                skip = True
                continue
            if "#fifo" in t:
                fifo_args += 1
                continue
            clean.append(t)
        if clean and not clean[0].startswith("/"):
            out.append({"argv": clean, "fifo_operands": fifo_args})
    return out


def regions_of(log, sname, used, answers, more):
    """Split PaSh's log at each part it was sent; give each part its text, its command uses and one outcome.
    Returns (regions, uses, PaSh's temporary folder)."""
    by_line, by_cmd = answers
    if not log.exists():
        return [], [], None, (Counter(), Counter())
    raw = log.read_text(errors="replace")
    ms = list(COMPILE.finditer(raw))
    prefix = None
    if ms:
        m0 = re.match(r"(/tmp/pash_\w+)/", ms[0].group(1))
        prefix = m0.group(1) if m0 else None
    segs, irs, bodies, var_files = [], {}, [], {}
    for i, m in enumerate(ms):
        seg = raw[m.end(): ms[i + 1].start() if i + 1 < len(ms) else len(raw)]
        segs.append(seg)
        irs.setdefault(m.group(3).strip(), {}).update(dict(EXPANSION.findall(seg)))
        var_files[m.group(3).strip()] = m.group(2).strip()
        body = ""
        if "Optimized script saved in" in seg:
            target = Path(m.group(1).replace("//", "/"))
            body = target.read_text(errors="replace") if target.exists() else ""
        bodies.append(worker_argvs(body) if body else None)
    helper = {"regions": {}, "keys": {}}
    pash_path, pash_path_error = {}, None
    if irs:
        env = dict(os.environ, PASH_TOP=str(PASH_SRC / "src/pash"), SET_ROOT=str(ROOT / "sets" / sname))
        req = {"irs": irs, "argvs": [json.loads(x) for x in sorted({json.dumps(w["argv"]) for b in bodies if b for w in b})]}
        p = subprocess.run([str(PASH.parent / "python3"), "-c", REGION_HELPER], input=json.dumps(req),
                           capture_output=True, text=True, env=env)
        if p.stdout.strip():
            helper = json.loads(p.stdout)
        # the same parts replayed through PaSh's own expansion and parsing: what the files really get
        env["PASH_TMP_PREFIX"] = (prefix or "/tmp") + "/"
        # (once per distinct part text: a loop sends the same part many times)
        rep_of, first = {}, {}
        for f in irs:
            txt = (helper["regions"].get(f) or {}).get("text")
            rep_of[f] = first.setdefault(txt, f) if txt is not None else f
        q = subprocess.run([str(PASH.parent / "python3"), "-c", PASH_PATH_HELPER],
                           input=json.dumps({f: var_files[f] for f in set(rep_of.values())}),
                           capture_output=True, text=True, env=env)
        got = json.loads(q.stdout) if q.stdout.strip() else {}
        pash_path = {f: got[r] for f, r in rep_of.items() if r in got}
        if not q.stdout.strip():
            pash_path_error = q.stderr.strip()[-300:]
    regions, uses_out = [], []
    for i, (m, seg) in enumerate(zip(ms, segs)):
        ri = helper["regions"].get(m.group(3).strip(), {})
        pp = pash_path.get(m.group(3).strip(), {})
        pp_uses = pp.get("uses") or []
        text = ri.get("text") or ""
        sha = hashlib.sha256(text.encode()).hexdigest()[:16]
        uses = ri.get("uses") or []
        pp_ok = len(pp_uses) == len(uses)
        workers = bodies[i]
        wkeys = Counter(helper["keys"].get(json.dumps(w["argv"])) for w in (workers or []))
        ukeys = Counter(u["key"] for u in uses)
        wexact = Counter(json.dumps(w["argv"]) for w in (workers or []))  # worker words, PaSh's pipes removed
        uexact = Counter(json.dumps(u["argv"]) for u in uses)
        reason = "; ".join(sorted({ln.strip()[:300] for ln in seg.splitlines()
                                   if re.search(r"WARNING|Exception|Error|not implemented|not provided", ln)}))
        region_parallel = workers is not None
        rows = []
        for pos, u in enumerate(uses, 1):
            argv = u["argv"]
            c = argv[0] if argv else ""
            line = shlex.join(argv)
            a = by_line.get((sname, line))
            ref = {"id": a["id"], "position": a["position"]} if a else None
            if a is None and c:
                a = ask_files(sname, argv)
            src = source_kind(used, c)
            direct = file_answer_of(a) if src != "none" else "no files"
            ppu = pp_uses[pos - 1] if pp_ok else None
            if ppu is not None:
                pa = pash_answer(ppu)
                fa = file_answer_of(pa) if src != "none" else "no files"
                pash_words = ppu.get("words")
            else:
                pa, fa, pash_words = a, direct, None
            if workers is None:
                copies, attributed = None, None
            else:
                ex = json.dumps(u["argv"])
                if ukeys[u["key"]] == 1:  # the only use with this command and these options
                    copies, attributed = wkeys.get(u["key"], 0), "by command line"
                elif uexact[ex] == 1 and wexact.get(ex):  # same options as another use; the words tell them apart
                    copies, attributed = wexact[ex], "by command line (exact words)"
                else:  # two uses that cannot be told apart
                    copies = sum(n for k, n in wkeys.items() if k and json.loads(k)[0] == c) // ukeys[u["key"]]
                    attributed = "by name only"
            split = None if copies is None else (copies >= 2 and (more is None or c in more))
            if split:
                why = None
            elif workers is None:
                why = "part not run in parallel"
            elif fa == "allows a split":
                why = OTHER_ALLOWED_NOT_SPLIT
            elif fa == "allows only a split PaSh has not implemented":
                why = "file allows only a split PaSh has not implemented"
            else:
                why = {"says no split": "file says no split", "no answer": "no answer", "raised": "raised",
                       "no files": "no files"}[fa]
            rows.append({"region": i + 1, "region_text_sha": sha, "position": pos, "command": c,
                         "invocation": home(shlex.join(pash_words)) if pash_words else home(line),
                         "invocation_as": "as PaSh passes it" if pash_words else "rebuilt, quotes removed",
                         "line": line, "exact_words": u["exact"], "answer_ref": ref,
                         "source": src, "source_detail": used.get(c, "none"), "file_answer": fa,
                         "answer_method": "as PaSh passes them" if ppu is not None else "direct, quotes removed",
                         "direct_file_answer": direct, "direct_differs": direct != fa,
                         "pash_answer": pa if ppu is not None else None,
                         "exception": (pa or {}).get("exception"),
                         "recipes": [x["split"] + ">" + x["aggregate"] + ("" if x.get("implemented", True) else " (not implemented)")
                                     for x in (pa or {}).get("split_recipes") or []],
                         "copies": copies, "copies_attributed": attributed, "split": split, "why_not_split": why,
                         "outside_pash": False})
        split_cmds = sorted({r["command"] for r in rows if r["split"]})
        if text == "" and ri.get("error") is not None:
            outcome, reason = "other", f"{OTHER_UNREADABLE}: {ri['error']}"
        elif region_parallel:
            refused = sorted({r["command"] for r in rows
                              if r["file_answer"] in ("says no split", "allows only a split PaSh has not implemented")})
            if split_cmds:
                outcome = "parallelized"
            elif any(r["why_not_split"] == OTHER_ALLOWED_NOT_SPLIT for r in rows):
                outcome, reason = "other", OTHER_ALLOWED_NOT_SPLIT + (": " + reason if reason else "")
            elif refused:
                outcome = "refused by annotation"
                reason = ("annotation allows no split for: " + ", ".join(refused)) + ("; " + reason if reason else "")
            else:
                outcome, reason = "other", OTHER_NOTHING_SPLITTABLE + (": " + reason if reason else "")
        elif (mm := re.search(r"InputOutputInformation for (\S+) not provided", seg)):
            c = mm.group(1)
            hit = [r for r in rows if r["command"] == c]
            if any(r["file_answer"] == "raised" for r in hit):
                outcome = "annotation raised"
                reason += "; the files, called directly, raised: " + next(r["exception"] for r in hit if r["exception"])
            elif source_kind(used, c) == "none":
                outcome = "missing annotation"
            else:
                outcome = "other"
                reason = f"{OTHER_NO_ANSWER} ({c}: {used.get(c)}); " + reason
        elif re.search(r"not implemented|NotImplementedError", seg, re.I):
            outcome = "unsupported construct"
        elif CRASH.search(seg):
            outcome = "pash crash"
        else:
            outcome = "other"
            reason = f"{OTHER_UNKNOWN}: " + (reason or seg.strip()[:300])
        regions.append({"region": i + 1, "text_sha": sha, "text": text[:600],
                        "pash_path": "replayed" if pp_ok else (pp.get("error") or pash_path_error or
                                                                 f"use count differs ({len(pp_uses)} vs {len(uses)})"),
                        "expansion_errors": pp.get("expansion_errors"),
                        "commands": [{"command": r["command"], "position": r["position"], "source": r["source"],
                                      "source_detail": r["source_detail"], "file_answer": r["file_answer"],
                                      "recipes": r["recipes"], "exception": r["exception"]} for r in rows],
                        "outcome": outcome, "reason": reason[:800], "split_commands": split_cmds,
                        "worker_lines": None if workers is None else
                        sorted(Counter(home(shlex.join(w["argv"])) for w in workers).items())})
        uses_out.extend(rows)
    # one record per distinct part text, outcome and split commands, with how many executions it stands for
    seen, keep = {}, set()
    for r in regions:
        k = (r["text_sha"], r["outcome"], tuple(r["split_commands"]))
        if k in seen:
            seen[k]["executions"] += 1
        else:
            seen[k] = r
            r["executions"] = 1
            keep.add(r["region"])
    for r in regions:
        r["emit"] = r["region"] in keep
    all_lines = Counter(u["line"] for u in uses_out)
    all_cmds = Counter(u["command"] for u in uses_out)
    uses_out = [u for u in uses_out if u["region"] in keep]
    for u in uses_out:
        u["executions"] = next(r["executions"] for r in regions if r["region"] == u["region"])
    return regions, uses_out, prefix, (all_lines, all_cmds)


def outside_uses(bash_calls, all_lines, sname, used, answers, all_cmds=None):
    """Starts under bash that are not a command use in any part sent to PaSh: per command, the starts under
    bash minus the uses of that command in every execution of every part. One row per command. (Matching by
    full command line undercounts loop parts, whose variables are not always filled in.)"""
    by_line, by_cmd = answers
    starts = Counter(a[0] for a in bash_calls)
    inside = all_cmds or Counter()
    out = []
    for c, n in sorted(starts.items()):
        k = n - inside.get(c, 0)
        if k <= 0:
            continue
        src = source_kind(used, c)
        fa = Counter(file_answer_of(a) for a in by_cmd.get((sname, c), [])) if src != "none" else Counter({"no files": 1})
        out.append({"region": None, "region_text_sha": None, "position": None, "command": c,
                    "invocation": None, "line": None, "exact_words": None, "answer_ref": None,
                    "source": src, "source_detail": used.get(c, "none"),
                    "file_answer": fa.most_common(1)[0][0] if fa else "no files", "file_answers": dict(fa),
                    "exception": None, "recipes": None, "copies": None, "copies_attributed": None, "split": None,
                    "why_not_split": "started, but not a command use in any part sent to PaSh (outside every "
                                     "part, or started by another program)",
                    "outside_pash": True, "executions": k})
    return out


def outside_uses_by_line(bash_calls, all_lines, sname, used, answers):
    """Uses started under bash that are in no part sent to PaSh (matched by full command line, against every
    execution of every part). One row per distinct command line, with how many starts it stands for."""
    by_line, _ = answers
    left = Counter(all_lines)
    outside = Counter()
    for argv in bash_calls:
        line = shlex.join(argv)
        if left[line] > 0:
            left[line] -= 1
            continue
        outside[line] += 1
    out = []
    for line, n in outside.items():
        argv = shlex.split(line)
        a = by_line.get((sname, line))
        src = source_kind(used, argv[0])
        out.append({"region": None, "region_text_sha": None, "position": None, "command": argv[0],
                    "invocation": home(line), "line": line, "exact_words": True,
                    "answer_ref": {"id": a["id"], "position": a["position"]} if a else None,
                    "source": src, "source_detail": used.get(argv[0], "none"),
                    "file_answer": file_answer_of(a) if src != "none" else "no files",
                    "exception": (a or {}).get("exception"), "recipes": None, "copies": None,
                    "copies_attributed": None, "split": None, "why_not_split": "ran outside every part sent to PaSh",
                    "outside_pash": True, "executions": n})
    return out


OUTCOMES = ["parallelized", "refused by annotation", "missing annotation", "annotation raised",
            "unsupported construct", "pash crash", "other"]


def region_counts(regions):
    """Per execution and per distinct region text (a distinct region takes its first outcome)."""
    first = {}
    for r in regions:
        first.setdefault(r["text_sha"], r["outcome"])
    per_exec, distinct = Counter(r["outcome"] for r in regions), Counter(first.values())
    # Tiran, 2026-11-24: every region not parallelized counts against the set, whatever the cause
    return {"regions": len(regions), "distinct_regions": len(first),
            "not_parallelized": len(regions) - per_exec.get("parallelized", 0),
            "distinct_not_parallelized": len(first) - distinct.get("parallelized", 0),
            "per_execution": {o: per_exec.get(o, 0) for o in OUTCOMES},
            "per_distinct": {o: distinct.get(o, 0) for o in OUTCOMES},
            "distinct_with_varying_outcome": sum(1 for h in first if len({r["outcome"] for r in regions
                                                                           if r["text_sha"] == h}) > 1)}


def vm_state():
    return {"when": time.strftime("%Y-%m-%d %H:%M:%S %z"),
            "uptime": subprocess.run(["uptime"], capture_output=True, text=True).stdout.strip(),
            "koala_git_status": subprocess.run(["git", "status", "--short"], cwd=KOALA, capture_output=True,
                                               text=True).stdout.strip()}


def cmd_run(args):
    sids = args.script or ["oneliners/spell"]
    sets = args.sets or MAIN_SETS
    timing_only = [s for s in sets if s in TIMING_ONLY_SETS]
    prefix_name = "controls_" if args.out == "controls.jsonl" else ""
    out_path = OUT / (args.out or "results.jsonl")
    phase = getattr(args, "phase", None)
    win = {"start": time.strftime("%Y-%m-%d %H:%M:%S %z")}
    with open(out_path, "a") as f, open(OUT / f"{prefix_name}regions.jsonl", "a") as rf, \
            open(OUT / f"{prefix_name}occurrences.jsonl", "a") as of, open(OUT / "run_windows.jsonl", "a") as wf:
        for sid in sids:
            inv = invocation(sid)
            rdir = ROOT / "runs" / sid.replace("/", "_")
            rdir.mkdir(parents=True, exist_ok=True)
            progs = script_programs(script_path(inv).read_text(errors="replace")) | set(coverage_commands(sid))
            answers = load_answers(sid)
            if not answers[0]:
                sys.exit(f"no answers for {sid}: run `answers --script {sid}` first")
            wanted = sets_wanted()
            used_by = {s: sources_of(**wanted[s]) for s in sets if s != "bash"}
            ref_sha = ref_files = base_counts = bash_calls = None
            before = vm_state()
            # pass 1 "instrumented": stand-ins on PATH, starts counted, uses recorded.
            # pass 2 "plain": no stand-ins, for timing; timing-only sets (the second copy of PaSh's own files)
            # run here only. The order of sets is rotated from repeat to repeat.
            first = getattr(args, "first_repeat", None) or 1
            for mode in (getattr(args, "modes", None) or ("instrumented", "plain")):
                order = [s for s in sets if s not in timing_only] if mode == "instrumented" else list(sets)
                for rep in range(first, first + (1 if inv["group"] in ONCE else args.repeats)):
                    # bash first in every repeat, so every source is compared with bash's output of the same
                    # repeat (found 2026-11-24 23:40: rotating bash out of first place left no reference);
                    # the order of the other sources still rotates from repeat to repeat
                    rest = [s for s in order if s != "bash"]
                    k = (rep - 1) % max(1, len(rest))
                    this_order = (["bash"] if "bash" in order else []) + rest[k:] + rest[:k]
                    for sname in this_order:
                        tag = f"{sname}_{mode}_{rep}"
                        res, standin, log, out = run_one(sname, inv, rdir, tag, shim=(mode == "instrumented"))
                        o_sha = file_sha(out, True)
                        got, calls = counts(standin) if mode == "instrumented" else (None, None)
                        if sname == "bash":  # the reference is the same repeat's bash run
                            ref_sha, ref_files = o_sha, res["files"]
                        if sname == "bash" and mode == "instrumented" and base_counts is None:
                            base_counts, bash_calls = got, calls
                        lg = read_log(log, progs) if sname != "bash" else None
                        more = None
                        if got is not None and sname != "bash":
                            # only the script's own commands: PaSh itself starts programs such as dirname
                            more = {c: n for c, n in got.items() if c in progs and n > (base_counts or {}).get(c, 0)}
                        regions, uses, tmp, all_lines = ([], [], None, (Counter(), Counter())) if sname == "bash" else \
                            regions_of(log, sname, used_by[sname], answers, more)
                        if mode == "instrumented" and sname != "bash":
                            uses = uses + outside_uses(bash_calls or [], all_lines[0], sname, used_by[sname], answers,
                                                       all_lines[1])
                            base = {"group": inv["group"], "script": inv["script"], "id": sid, "set": sname,
                                    "mode": mode, "repeat": rep, "phase": phase}
                            for r in regions:
                                if r.get("emit"):
                                    rf.write(json.dumps(base | {k: v for k, v in r.items() if k != "emit"},
                                                        sort_keys=True) + "\n")
                            for u in uses:
                                u = dict(u)
                                u.pop("line", None)
                                u.pop("pash_answer", None)
                                of.write(json.dumps(base | u, sort_keys=True) + "\n")
                        if mode == "instrumented" and rep == 1 and sname != "bash":
                            # what the files answered inside PaSh (replayed on PaSh's kept files)
                            with open(answers_path(sid), "a") as af:
                                for u in uses:
                                    if u.get("answer_method") != "as PaSh passes them":
                                        continue
                                    pa = u["pash_answer"]
                                    af.write(json.dumps({
                                        "group": inv["group"], "script": inv["script"], "id": sid, "set": sname,
                                        "method": "as PaSh passes them", "region": u["region"],
                                        "region_text_sha": u["region_text_sha"], "position": u["position"],
                                        "command": u["command"], "invocation": u["invocation"],
                                        "source": u["source"], "files_from": u["source_detail"],
                                        "io_outcome": pa["io_outcome"], "io": pa["io"],
                                        "parallelizability_outcome": pa["parallelizability_outcome"],
                                        "allows_split": pa["allows_split"], "split_recipes": pa["split_recipes"],
                                        "file_answer": u["file_answer"], "exception": pa["exception"],
                                        "direct_file_answer": u["direct_file_answer"],
                                        "direct_differs": u["direct_differs"]}, sort_keys=True) + "\n")
                        if tmp and tmp.startswith("/tmp/pash_"):
                            shutil.rmtree(tmp, ignore_errors=True)  # PaSh keeps its temp folder at debug level 2
                        rc_ = region_counts(regions) if sname != "bash" else None
                        split = sorted({c for r in regions for c in r["split_commands"]}) if sname != "bash" else None
                        rec = {"group": inv["group"], "script": inv["script"], "id": sid, "set": sname,
                               "mode": mode, "repeat": rep, "phase": phase, "order": this_order,
                               "bash_out_sha256": ref_sha,
                               "output_files_sha": hashlib.sha256(json.dumps(res["files"]).encode()).hexdigest()[:16],
                               "state": "reference" if sname == "bash" else state_of(lg, more, res),
                               "split_commands": split,
                               "regions_sent": (lg or {}).get("regions_sent"),
                               "regions_parallel": (lg or {}).get("regions_parallel"),
                               "region_outcomes": rc_,
                               "pash_crashes": (rc_ or {}).get("per_execution", {}).get("pash crash"),
                               "no_region_parallelized_warning": ("No region was parallelized" in
                                                                  (log.read_text(errors="replace") if log.exists() else ""))
                               if sname != "bash" else None,
                               "ours_commands": sorted(c for c in progs if source_kind(used_by[sname], c) == "ours")
                               if sname != "bash" else None,
                               "starts_per_command": dict(got) if got is not None else None,
                               "more_starts_than_bash": more,
                               "worker_copies_in_pash_script": (lg or {}).get("worker_copies_in_script"),
                               "out_sha256": o_sha, "out_bytes": out.stat().st_size,
                               "same_as_bash": o_sha == ref_sha,
                               "output_files_same_as_bash": res["files"] == ref_files,
                               "output_files": len(res["files"]),
                               "matches_koala_hash": (o_sha == inv["expected_hash"]) if inv["expected_hash"] else None,
                               "rc": res["rc"], "seconds": res["seconds"],
                               "fallback_reasons": (lg or {}).get("warnings"),
                               "tracebacks": sorted(set((lg or {}).get("tracebacks") or [])),
                               "stderr": res["stderr"][-300:]}
                        if log.exists() and rep == 1:
                            (OUT / "logs").mkdir(exist_ok=True)
                            with open(log, "rb") as a, gzip.open(OUT / "logs" / f"{prefix_name}{sid.replace('/', '_')}__{sname}__{mode}.log.gz", "wb") as g:
                                g.write(a.read())
                        f.write(json.dumps(rec, sort_keys=True) + "\n")
                        f.flush()
                        print(f"{sid} {sname:20} {mode:12} r{rep} {rec['state']:18} {res['seconds']:7.3f}s "
                              f"same={rec['same_as_bash']} koala={rec['matches_koala_hash']} split={rec['split_commands']}",
                              flush=True)
                        for x in (standin, log, out):
                            x.unlink(missing_ok=True)
            after = vm_state()
            wf.write(json.dumps({"what": args.out or "results.jsonl", "phase": phase, "id": sid, "sets": sets,
                                 "repeats": args.repeats, "start": before["when"], "end": after["when"],
                                 "uptime_start": before["uptime"], "uptime_end": after["uptime"],
                                 "koala_git_status_start": before["koala_git_status"],
                                 "koala_git_status_end": after["koala_git_status"],
                                 "koala_changed": before["koala_git_status"] != after["koala_git_status"]}) + "\n")
            wf.flush()
    win["end"] = time.strftime("%Y-%m-%d %H:%M:%S %z")
    print(win)


def cmd_controls(args):
    """Controls are the same runs on the control sets; kept in files of their own. Run at the start and at
    the end of a batch (phase start / end)."""
    args.sets, args.out, args.repeats = CONTROL_SETS, "controls.jsonl", 1
    args.script = args.script or ["oneliners/spell"]
    cmd_run(args)


def cmd_batch(args):
    """The whole batch: the controls on spell, every script one after another, the controls again.
    A script that fails in the runner is recorded in batch_errors.jsonl and the batch goes on."""
    import traceback
    sids = args.script or [r["id"] for r in jl(OUT / "invocations.jsonl")]
    done = {r["id"] for r in jl(OUT / "results.jsonl") if r.get("phase") == args.phase} \
        if (OUT / "results.jsonl").exists() and args.resume else set()
    if not args.resume and not args.no_controls:
        cmd_controls(argparse.Namespace(script=None, phase="start"))
    for sid in sids:
        if sid in done:
            continue
        try:
            cmd_run(argparse.Namespace(script=[sid], sets=args.sets, out=None, repeats=args.repeats,
                                       phase=args.phase, modes=args.modes, first_repeat=args.first_repeat))
        except Exception as e:  # noqa: BLE001
            with open(OUT / "batch_errors.jsonl", "a") as f:
                f.write(json.dumps({"id": sid, "when": time.strftime("%Y-%m-%d %H:%M:%S %z"),
                                    "error": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc()[-2000:]}) + "\n")
            print(f"BATCH ERROR {sid}: {type(e).__name__}: {e}", flush=True)
        with open(OUT / "batch_progress.txt", "a") as f:  # read by the copier on the Mac side
            f.write(sid + "\n")
    if not args.no_controls:
        cmd_controls(argparse.Namespace(script=None, phase="end"))
    print("BATCH DONE", flush=True)


# ------------------------------------------------------------------ answers

WORKER = r'''
import json, sys, time, traceback, importlib, shlex
root, cmd, Cmd = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, root)
from pash_annotations.parser.parser import parse
from pash_annotations.datatypes.BasicDatatypes import Flag, Option, WhichClassForArg
import pash_annotations.annotation_generation.AnnotationGeneration as AG
GEN = "pash_annotations.annotation_generation.annotation_generators."
def load(kind):
    try:
        return getattr(importlib.import_module(GEN + kind + Cmd), kind + Cmd), None
    except ModuleNotFoundError:
        return None, "no class"
    except Exception as e:
        return None, "import error: " + type(e).__name__ + ": " + str(e)[:300]
IO, io_load = load("InputOutputInfoGenerator")
PAR, par_load = load("ParallelizabilityInfoGenerator")
def kind_of(t):
    which, acc = t
    if which == WhichClassForArg.FILESTD:
        return acc.kind.name if acc is not None else "FILESTD?"
    return which.name
def recipe(p):
    sp = p.get_splitter().kind.name
    ag = p.get_aggregator_spec()
    try:
        a = ag.get_kind().name
    except Exception:
        a = type(ag).__name__
    m = p.get_mapper_spec()
    try:
        mk = m.kind.name
    except Exception:
        mk = type(m).__name__
    try:
        imp = bool(p.are_all_parts_implemented())
    except Exception:
        imp = None
    return {"split": sp, "map": mk, "aggregate": a, "implemented": imp}
for raw in sys.stdin:
    row = json.loads(raw)
    out = {"id": row["id"], "in_pash_name_table": cmd in AG.DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES}
    t0 = time.perf_counter()
    try:
        inv = parse(row["line"])
        out["parse"] = {"flagoptions": [[fo.get_name(), str(fo.get_arg()) if isinstance(fo, Option) else None] for fo in inv.flag_option_list],
                        "operands": [str(o.get_name()) for o in inv.operand_list]}
    except Exception as e:
        out["parse"] = None; out["parse_error"] = type(e).__name__ + ": " + str(e)[:200]
        out["io_outcome"] = out["par_outcome"] = "parse failed"
        print(json.dumps(out)); continue
    if IO is None:
        out["io_outcome"] = io_load
    else:
        try:
            g = IO(inv); g.generate_info(); info = g.get_info()
            if info is None:
                out["io_outcome"] = "no answer"
            else:
                out["io_outcome"] = "answered"
                out["io"] = {"flagoptions": [kind_of(t) for t in info.flagoption_list_typer],
                             "operands": [kind_of(t) for t in info.operand_list_typer],
                             "stdin": info.implicit_use_of_streaming_input is not None,
                             "stdout": info.implicit_use_of_streaming_output is not None}
        except Exception as e:
            out["io_outcome"] = "exception"; out["io_exception"] = type(e).__name__ + ": " + str(e)[:300]
    if PAR is None:
        out["par_outcome"] = par_load
    else:
        try:
            g = PAR(inv); g.generate_info(); info = g.get_info()
            if info is None:
                out["par_outcome"] = "no answer"; out["par"] = []
            else:
                out["par_outcome"] = "answered"
                out["par"] = [recipe(p) for p in info.parallelizer_list]
                out["par_rr_cat"] = bool(info.round_robin_compatible_with_cat)
                out["par_commutative"] = bool(info.is_commutative)
        except Exception as e:
            out["par_outcome"] = "exception"; out["par_exception"] = type(e).__name__ + ": " + str(e)[:300]
    out["seconds"] = round(time.perf_counter() - t0, 6)
    print(json.dumps(out))
'''


def add_answers(sids, sets):
    """Direct answers for sets added after the answers step, from the saved bash start records (no new bash
    run). Rows already in the script's answers file for these sets are replaced; other rows are kept."""
    for sid in sids:
        inv = invocation(sid)
        calls, seen = [], set()
        for argv in json.loads((OUT / f"{sid.replace('/', '_')}.bash_calls.json").read_text()):
            k = shlex.join(argv)
            if k not in seen:
                seen.add(k)
                calls.append(argv)
        path = answers_path(sid)
        keep = [r for r in jl(path) if not (r["set"] in sets and r.get("method") == "direct, quotes removed")] \
            if path.exists() else []
        new = []
        for s, used in sets.items():
            by_cmd = {}
            for n, argv in enumerate(calls, 1):
                by_cmd.setdefault(argv[0], []).append((n, argv))
            for cmd, items in by_cmd.items():
                p = subprocess.run([sys.executable, "-I", "-c", WORKER, str(ROOT / "sets" / s), cmd, cls(cmd)],
                                   input="".join(json.dumps({"id": n, "line": shlex.join(a)}) + "\n" for n, a in items),
                                   capture_output=True, text=True)
                outs = {r["id"]: r for r in map(json.loads, p.stdout.splitlines())} if p.stdout.strip() else {}
                for n, argv in items:
                    a = outs.get(n) or {"io_outcome": "worker crashed", "par_outcome": "worker crashed"}
                    par = a.get("par") or []
                    new.append({"group": inv["group"], "script": inv["script"], "id": sid, "position": n,
                                "command": cmd, "invocation": shlex.join(argv).replace(str(Path.home()), "~"),
                                "line": shlex.join(argv), "set": s, "source": source_kind(used, cmd),
                                "method": "direct, quotes removed",
                                "files_from": used.get(cmd, "none (PaSh has no files)"),
                                "in_pash_name_table": a.get("in_pash_name_table"),
                                "io_outcome": a.get("io_outcome"), "io": a.get("io"),
                                "parallelizability_outcome": a.get("par_outcome"),
                                "allows_split": a.get("par_outcome") == "answered" and bool(par),
                                "split_recipes": par,
                                "exception": a.get("io_exception") or a.get("par_exception") or a.get("crash")
                                or a.get("parse_error")})
        with open(path, "w") as f:
            for r in keep + new:
                f.write(json.dumps(r, sort_keys=True) + "\n")
        cpath = OUT / "commands.jsonl"
        crow = [r for r in jl(cpath) if not (r["id"] == sid and r["set"] in sets)] if cpath.exists() else []
        seen = set()
        for r in new:
            if (r["command"], r["set"]) not in seen:
                seen.add((r["command"], r["set"]))
                crow.append({"group": r["group"], "script": r["script"], "id": sid, "command": r["command"],
                             "set": r["set"], "source": r["source"], "source_detail": r["files_from"]})
        with open(cpath, "w") as f:
            for r in crow:
                f.write(json.dumps(r, sort_keys=True) + "\n")
        print(f"added answers {sid}: {len(new)} rows for {sorted(sets)}", flush=True)


def invocations_of(sid):
    """The script's command invocations, exactly as started under plain bash (from the stand-in records)."""
    inv = invocation(sid)
    rdir = ROOT / "runs" / sid.replace("/", "_")
    rdir.mkdir(parents=True, exist_ok=True)
    res, standin, log, out = run_one("bash", inv, rdir, "answers_bash")
    _, calls = counts(standin)
    with open(OUT / "answers_bash_runs.jsonl", "a") as f:
        f.write(json.dumps({"id": sid, "seconds": res["seconds"], "rc": res["rc"], "timed_out": res["timed_out"],
                            "starts": len(calls), "out_bytes": out.stat().st_size,
                            "stderr": res["stderr"][-300:]}) + "\n")
    (OUT / f"{sid.replace('/', '_')}.bash_calls.json").write_text(json.dumps(calls, indent=0))
    seen, rows = set(), []
    for argv in calls:
        line = shlex.join(argv)
        if line not in seen:
            seen.add(line)
            rows.append(argv)
    return rows


def cmd_answers(args):
    sids = args.script or ["oneliners/spell"]
    sets = {name: sources_of(**spec) for name, spec in sets_wanted().items()}
    if getattr(args, "add_sets", None):
        return add_answers(sids, {s: sets[s] for s in args.add_sets})
    (OUT / "answers").mkdir(parents=True, exist_ok=True)
    allrows, rows = [], []
    seen_vs = []
    for sid in sids:
        inv = invocation(sid)
        calls = invocations_of(sid)
        started, listed = sorted({a[0] for a in calls}), coverage_commands(sid)
        seen_vs.append({"id": sid, "started_under_bash": started, "listed_by_inventory": listed,
                        "started_not_listed": sorted(set(started) - set(listed)),
                        "listed_not_started": sorted(set(listed) - set(started))})
        got = {}
        for s in sets:  # one worker per set and command, all its lines at once
            by_cmd = {}
            for n, argv in enumerate(calls, 1):
                by_cmd.setdefault(argv[0], []).append((n, argv))
            for cmd, items in by_cmd.items():
                p = subprocess.run([sys.executable, "-I", "-c", WORKER, str(ROOT / "sets" / s), cmd, cls(cmd)],
                                   input="".join(json.dumps({"id": n, "line": shlex.join(a)}) + "\n" for n, a in items),
                                   capture_output=True, text=True)
                outs = {r["id"]: r for r in map(json.loads, p.stdout.splitlines())} if p.stdout.strip() else {}
                for n, _ in items:
                    got[(s, n)] = outs.get(n) or {"io_outcome": "worker crashed", "par_outcome": "worker crashed",
                                                  "crash": (p.stderr.strip().splitlines() or [""])[-1][:300]}
        for n, argv in enumerate(calls, 1):
            cmd = argv[0]
            for s, used in sets.items():
                a = got[(s, n)]
                par = a.get("par") or []
                rows.append({"group": inv["group"], "script": inv["script"], "id": sid, "position": n,
                             "command": cmd, "invocation": shlex.join(argv).replace(str(Path.home()), "~"),
                             "line": shlex.join(argv), "set": s, "source": source_kind(used, cmd),
                             "method": "direct, quotes removed",
                             "files_from": used.get(cmd, "none (PaSh has no files)"),
                             "in_pash_name_table": a.get("in_pash_name_table"),
                             "io_outcome": a.get("io_outcome"), "io": a.get("io"),
                             "parallelizability_outcome": a.get("par_outcome"),
                             "allows_split": a.get("par_outcome") == "answered" and bool(par),
                             "split_recipes": par,
                             "exception": a.get("io_exception") or a.get("par_exception") or a.get("crash")
                             or a.get("parse_error")})
                r = rows[-1]
        print(f"answers {sid}: {len(calls)} distinct command lines", flush=True)
        with open(answers_path(sid), "w") as f:
            for r in rows:
                f.write(json.dumps(r, sort_keys=True) + "\n")
        allrows.extend({k: r[k] for k in ("id", "command", "set", "group", "script", "files_from")} for r in rows)
        rows = []
    rows = allrows
    vpath = OUT / "standin_vs_inventory.jsonl"
    old = [r for r in jl(vpath) if r["id"] not in sids] if vpath.exists() else []
    with open(vpath, "w") as f:
        for r in old + seen_vs:
            f.write(json.dumps(r, sort_keys=True) + "\n")
    # commands.jsonl: one row per group, script, command, set, source
    seen, crow = set(), []
    for r in rows:
        k = (r["id"], r["command"], r["set"])
        if k in seen:
            continue
        seen.add(k)
        crow.append({"group": r["group"], "script": r["script"], "id": r["id"], "command": r["command"],
                     "set": r["set"], "source": source_kind(sets[r["set"]], r["command"]),
                     "source_detail": r["files_from"]})
    cpath = OUT / "commands.jsonl"
    crow = [r for r in jl(cpath) if r["id"] not in sids] + crow if cpath.exists() else crow
    with open(cpath, "w") as f:
        for r in crow:
            f.write(json.dumps(r, sort_keys=True) + "\n")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="what", required=True)
    sub.add_parser("build")
    d = sub.add_parser("discover"); d.add_argument("--group", nargs="*")
    b = sub.add_parser("batch"); b.add_argument("--script", nargs="*"); b.add_argument("--resume", action="store_true")
    b.add_argument("--repeats", type=int, default=3)
    b.add_argument("--no-controls", action="store_true")
    b.add_argument("--sets", nargs="*"); b.add_argument("--phase", default="main")
    b.add_argument("--modes", nargs="*", choices=["instrumented", "plain"])
    b.add_argument("--first-repeat", type=int, default=1)
    for n in ("answers", "run", "controls"):
        p = sub.add_parser(n)
        p.add_argument("--script", nargs="*")
        if n == "answers":
            p.add_argument("--add-sets", nargs="*")
        if n in ("run", "controls"):
            p.add_argument("--phase")
        if n == "run":
            p.add_argument("--repeats", type=int, default=3)  # Tiran, 2026-11-24
            p.add_argument("--sets", nargs="*")
            p.add_argument("--out")
    args = ap.parse_args()
    {"build": cmd_build, "discover": cmd_discover, "answers": cmd_answers, "run": cmd_run, "batch": cmd_batch,
     "controls": cmd_controls}[args.what](args)


if __name__ == "__main__":
    main()
