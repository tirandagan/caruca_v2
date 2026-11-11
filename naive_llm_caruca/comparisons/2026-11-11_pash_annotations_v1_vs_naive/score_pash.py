"""Scorer for task 021: v1's PaSh annotations against the naive LLM's (and PaSh's own).

Counts only; it never judges. Qualitative assessment is done separately (README.md, rubric.md).

    python3 score_pash.py all            # sides -> lines -> answers -> io sets -> tables
    python3 score_pash.py sides|lines|answers|iosets|tables

Every side's three files are loaded into a private copy of pash-annotations 0.2.4 (one copy per
side, under the scratch folder), and each line is parsed with that side's parser table and passed
to that side's classes, called directly so that an exception PaSh would swallow is recorded.
"""

import ast
import gzip
import hashlib
import itertools
import json
import os
import random
import re
import shlex
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARM = HERE.parents[1]  # naive_llm_caruca/
V1 = Path(os.environ.get("CARUCA_V1", Path.home() / "dev/stevens/caruca"))
V1_OUT = V1 / "caruca/save_pash_py"
INVOCATIONS = V1 / "eval/command-invocations.txt"
TRIES = ARM / "fig7_campaign/tries"
STOCK = Path(os.environ.get(
    "PASH_ANNOTATIONS",
    Path.home() / ".cache/uv/archive-v0/QbrdQstfYG3j7LuuIEFCo/pash_annotations"))
SCRATCH = Path(os.environ.get("SCORER_SCRATCH", "/tmp/score_pash"))

COMMANDS = ["cat", "cp", "cut", "grep", "rm", "sort", "split", "wc"]
SAMPLE_SEEN = {"tee", "uniq", "grep", "rm"}  # the agent was shown PaSh's own files for these
GEN = "annotation_generation/annotation_generators"
DATA = "parser/command_flag_option_info/data"


def cls(cmd):
    return "".join(p.capitalize() for p in cmd.split("_"))


def _open(path, mode):
    # gzip with a fixed mtime so the same rows give the same bytes
    if str(path).endswith(".gz"):
        if "w" in mode:
            return gzip.GzipFile(filename="", mode="wb", fileobj=open(path, "wb"), mtime=0)
        return gzip.open(path, "rt")
    return open(path, mode)


def jdump(rows, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if str(path).endswith(".gz"):
        with _open(path, "w") as f:
            for r in rows:
                f.write((json.dumps(r, sort_keys=True) + "\n").encode())
        return
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True) + "\n")


def jload(path):
    with _open(path, "r") as f:
        return [json.loads(l) for l in f if l.strip()]


# ---------------------------------------------------------------- sides

def find_sides():
    sides = []
    for cmd in COMMANDS:
        for g in ("pash", "main"):
            d = V1_OUT / cmd / f"{g}_grammar/trace_1"
            if (d / f"{cmd}.json").exists():
                sides.append({"cmd": cmd, "side": f"v1-{g}", "family": "v1", "dir": str(d)})
        for run in sorted((ARM / "runs").iterdir()):
            for sub in ("annotation", "pash"):
                d = run / "output" / sub
                if (d / f"{cmd}.json").exists():
                    sides.append({"cmd": cmd, "side": f"naive:{run.name[:17]}", "family": "naive",
                                  "dir": str(d), "run": run.name})
        if (STOCK / DATA / f"{cmd}.json").exists() or (STOCK / GEN / f"InputOutputInfoGenerator{cls(cmd)}.py").exists():
            sides.append({"cmd": cmd, "side": "pash-own", "family": "reference", "dir": None})
    jdump(sides, HERE / "sides.jsonl")
    return sides


# ---------------------------------------------------------------- lines

REDIR = re.compile(r"^(\d*|&)(>>?|<<?|>&|<&)(.*)$")


def bind(segment):
    """Shell fragment -> the words PaSh's annotation code would see, or (None, reason)."""
    if "$(" in segment or "`" in segment or "<(" in segment or ">(" in segment:
        return None, "command substitution"
    s = re.sub(r"\$\{(\w+)\}", r"\1", segment)
    s = re.sub(r"\$(\w+)", lambda m: ("ARG" + m.group(1)) if m.group(1).isdigit() else m.group(1), s)
    try:
        words = shlex.split(s)
    except ValueError as e:
        return None, f"shlex: {e}"
    out, skip = [], False
    for w in words:
        if skip:
            skip = False
            continue
        m = REDIR.match(w)
        if m and not w.startswith("-"):
            if m.group(3) == "":
                skip = True
            continue
        out.append(w)
    return out, None


def set_a(cmd):
    rows = []
    for n, raw in enumerate(INVOCATIONS.read_text().splitlines(), 1):
        for seg in re.split(r"\|\||&&|\||;", raw):
            seg = seg.strip().lstrip("({!").strip()
            if not seg or seg.split()[0] != cmd:
                continue
            words, why = bind(seg)
            rows.append({"set": "A", "source": f"command-invocations.txt:{n}", "raw": raw,
                         "line": shlex.join(words) if words else None, "unusable": why})
    return rows


def set_c_v1(cmd):
    rows = {}
    for d in sorted((V1_OUT / cmd).glob("*_grammar/trace_*")):
        tr = json.load(gzip.open(d / "traces.json.gz"))
        for inv in tr:
            ok = any(c["return_code"] == 0 for c in inv["configs"])
            key = inv["true_str"]
            r = rows.setdefault(key, {"set": "C-v1", "source": f"{d.parent.name}", "raw": key,
                                      "line": key, "unusable": None, "v1_succeeded": ok})
            r["v1_succeeded"] = r["v1_succeeded"] or ok
    return list(rows.values())


def set_c_naive(cmd):
    rows = {}
    for f in sorted(TRIES.glob(f"*_naive-run-{cmd}*_{cmd}_*.json")):
        d = json.load(open(f))
        for t in d["tries"]:
            if t.get("help_or_version") or not t["argv"]:
                continue
            argv = list(t["argv"])
            argv[0] = cmd
            line = shlex.join(argv)
            r = rows.setdefault(line, {"set": "C-naive", "source": d["summary"]["run"][:17], "raw": line,
                                       "line": line, "unusable": None, "agent_classes": []})
            r["agent_classes"].append(f'{t["phase"]}/{t["class"]}')
    for r in rows.values():
        r["agent_classes"] = sorted(set(r["agent_classes"]))
    return list(rows.values())


def build_lines():
    all_rows = []
    for cmd in COMMANDS:
        seen = {}
        for r in set_a(cmd) + set_c_v1(cmd) + set_c_naive(cmd):
            r["cmd"] = cmd
            key = r["line"] or f"unusable:{r['source']}"
            if key in seen:
                seen[key]["sets"] = sorted(set(seen[key]["sets"]) | {r["set"]})
                continue
            r["sets"] = [r["set"]]
            seen[key] = r
        for i, r in enumerate(seen.values()):
            r["id"] = f"{cmd}-{i:05d}"
            all_rows.append(r)
    jdump(all_rows, HERE / "lines.jsonl")
    return all_rows


# ---------------------------------------------------------------- answers (worker runs per side)

def make_package(side):
    """Private copy of the stock package with the side's three files in place."""
    key = hashlib.sha256(json.dumps(side, sort_keys=True).encode()).hexdigest()[:12]
    root = SCRATCH / f"{side['cmd']}_{key}"
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(STOCK, root / "pash_annotations", ignore=shutil.ignore_patterns("__pycache__"))
    pkg = root / "pash_annotations"
    if side["dir"]:
        c, d = side["cmd"], Path(side["dir"])
        shutil.copy(d / f"{c}.json", pkg / DATA / f"{c}.json")
        for kind in ("InputOutputInfoGenerator", "ParallelizabilityInfoGenerator"):
            src = d / f"{kind}{cls(c)}.py"
            dst = pkg / GEN / f"{kind}{cls(c)}.py"
            if src.exists():
                shutil.copy(src, dst)
            elif dst.exists():
                dst.unlink()  # the side has no such class: PaSh's own must not stand in for it
    return root


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
    return {"split": sp, "map": mk, "aggregate": a}
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


def build_answers(sides=None, lines=None):
    sides = sides or jload(HERE / "sides.jsonl")
    lines = lines or jload(HERE / "lines.jsonl")
    by_cmd = defaultdict(list)
    for l in lines:
        if l["line"]:
            by_cmd[l["cmd"]].append(l)
    rows = []
    for side in sides:
        root = make_package(side)
        p = subprocess.run([sys.executable, "-I", "-c", WORKER, str(root), side["cmd"], cls(side["cmd"])],
                           input="".join(json.dumps({"id": l["id"], "line": l["line"]}) + "\n" for l in by_cmd[side["cmd"]]),
                           capture_output=True, text=True)
        if p.returncode:
            sys.exit(f"worker failed for {side}:\n{p.stderr[-3000:]}")
        for raw in p.stdout.splitlines():
            r = json.loads(raw)
            r.update(cmd=side["cmd"], side=side["side"], family=side["family"])
            rows.append(r)
    jdump(rows, HERE / "answers.jsonl.gz")
    return rows


# ---------------------------------------------------------------- io sets

IN_KINDS = {"CONFIG_INPUT", "STREAM_INPUT", "CONTAINER_FOR_INPUT", "EXCLUDES_FROM_INPUT", "OTHER_INPUT"}
OUT_KINDS = {"STREAM_OUTPUT", "OTHER_OUTPUT"}


def io_set(a):
    """{(word, role, direction): kind}. Roles: operand, option value, stdin, stdout."""
    if a.get("io_outcome") != "answered":
        return None
    s = {}
    for (name, arg), k in zip(a["parse"]["flagoptions"], a["io"]["flagoptions"]):
        if k in IN_KINDS | OUT_KINDS:
            s[(arg, "option value", "read" if k in IN_KINDS else "written")] = k
    for w, k in zip(a["parse"]["operands"], a["io"]["operands"]):
        if k in IN_KINDS | OUT_KINDS:
            s[(w, "operand", "read" if k in IN_KINDS else "written")] = k
    if a["io"]["stdin"]:
        s[("<stdin>", "stdin", "read")] = "STREAM_INPUT"
    if a["io"]["stdout"]:
        s[("<stdout>", "stdout", "written")] = "STREAM_OUTPUT"
    return s


def classify_pair(sa, sb):
    if sa is None or sb is None:
        return ("no answer: both" if sa is None and sb is None else "no answer: first" if sa is None else "no answer: second"), []
    ka, kb = {(w, d) for w, _, d in sa}, {(w, d) for w, _, d in sb}
    if ka == kb:
        cls_ = "identical"
    elif ka > kb:
        cls_ = "first larger"
    elif kb > ka:
        cls_ = "second larger"
    elif ka & kb:
        cls_ = "overlapping"
    else:
        cls_ = "disjoint"
    diffs = []
    role_a = {w: r for w, r, _ in sa}
    role_b = {w: r for w, r, _ in sb}
    dir_a = defaultdict(set)
    dir_b = defaultdict(set)
    for w, _, d in sa:
        dir_a[w].add(d)
    for w, _, d in sb:
        dir_b[w].add(d)
    for w in sorted(set(dir_a) | set(dir_b)):
        da, db = dir_a.get(w, set()), dir_b.get(w, set())
        if da == db:
            continue
        roles = {role_a.get(w), role_b.get(w)} - {None}
        if w == "<stdin>":
            t = "standard input differs"
        elif w == "<stdout>":
            t = "standard output differs"
        elif "option value" in roles:
            t = "option value typed differently"
        elif da and db:
            t = "operand direction differs"
        else:
            t = "operand used by one side only"
        diffs.append({"word": w, "first": sorted(da), "second": sorted(db), "type": t})
    # kind-only differences (same word and direction, different PaSh kind)
    kinds_a = {(w, d): k for (w, _, d), k in sa.items()}
    kinds_b = {(w, d): k for (w, _, d), k in sb.items()}
    for key in sorted(set(kinds_a) & set(kinds_b)):
        if kinds_a[key] != kinds_b[key]:
            diffs.append({"word": key[0], "first": [kinds_a[key]], "second": [kinds_b[key]], "type": "kind only"})
    return cls_, diffs


def split_of(a):
    if a.get("par_outcome") != "answered":
        return None if a.get("par_outcome") in ("exception", "parse failed") else frozenset()
    return frozenset((p["split"], p["aggregate"]) for p in a["par"])


def build_iosets(answers=None):
    answers = answers or jload(HERE / "answers.jsonl.gz")
    by_line = defaultdict(dict)
    for a in answers:
        by_line[a["id"]][a["side"]] = a
    rows = []
    for lid, sides in sorted(by_line.items()):
        for s1, s2 in itertools.combinations(sorted(sides), 2):
            a, b = sides[s1], sides[s2]
            c, diffs = classify_pair(io_set(a), io_set(b))
            pa, pb = split_of(a), split_of(b)
            rows.append({"id": lid, "cmd": a["cmd"], "first": s1, "second": s2, "io_class": c, "diffs": diffs,
                         "same_parse": a.get("parse") == b.get("parse"),
                         "split_first": sorted(map(list, pa)) if pa is not None else None,
                         "split_second": sorted(map(list, pb)) if pb is not None else None,
                         "split_same": pa == pb})
    jdump(rows, HERE / "io_sets.jsonl.gz")
    return rows


# ---------------------------------------------------------------- tables

def pct(n, d):
    return f"{n}/{d} ({100 * n / d:.0f}%)" if d else "0/0"


def positional(a):
    """word -> role by position, so that lines differing only in file names group together."""
    names = {"<stdin>": "stdin", "<stdout>": "stdout"}
    for i, w in enumerate(a["parse"]["operands"], 1):
        names.setdefault(w, f"operand {i}")
    for name, arg in a["parse"]["flagoptions"]:
        if arg is not None:
            names.setdefault(arg, f"value of {name}")
    return names


def describe(a):
    if a is None:
        return "—"
    if a.get("parse") is None:
        return "parse failed"
    s = io_set(a)
    if s is None:
        io = a["io_outcome"]
    else:
        pos = positional(a)
        r = sorted(pos.get(w, w) for w, _, d in s if d == "read")
        w_ = sorted(pos.get(w, w) for w, _, d in s if d == "written")
        io = f"reads {', '.join(r) or 'nothing'}; writes {', '.join(w_) or 'nothing'}"
    sp = split_of(a)
    if sp is None:
        par = a["par_outcome"]
    elif not sp:
        par = "no split" if a["par_outcome"] == "answered" else f"no split ({a['par_outcome']})"
    else:
        par = "split: " + "; ".join(f"{x} → {y}" for x, y in sorted(sp))
    return f"{io} | {par}"


def build_tables():
    lines = {l["id"]: l for l in jload(HERE / "lines.jsonl")}
    answers = jload(HERE / "answers.jsonl.gz")
    pairs = jload(HERE / "io_sets.jsonl.gz")
    sides = jload(HERE / "sides.jsonl")
    out = ["# Numbers: v1 vs the naive LLM vs PaSh's own (task 021, scorer output)", "",
           "Made by `score_pash.py`. Counts only. Each rate is out of the lines that side was asked about.", ""]

    out += ["## Completeness: what each side gives PaSh", "",
            "| Command | Side | Lines | Input/output answered | No answer | Exception | No class | Parse failed | Split allowed |",
            "|---|---|---|---|---|---|---|---|---|"]
    for cmd in COMMANDS:
        for s in [x["side"] for x in sides if x["cmd"] == cmd]:
            rows = [a for a in answers if a["cmd"] == cmd and a["side"] == s]
            c = Counter(a["io_outcome"] for a in rows)
            n = len(rows)
            nsplit = sum(1 for a in rows if split_of(a))
            out.append(f"| {cmd} | {s} | {n} | {pct(c['answered'], n)} | {c['no answer']} | {c['exception']} | "
                       f"{c['no class']} | {c['parse failed']} | {pct(nsplit, n)} |")
    out.append("")

    out += ["## Input/output sets: v1 against each naive run (Greenberg's question)", "",
            "Per line, the set of (file or stream, read/written) each side gives PaSh. "
            "\"v1 larger\" means v1's set contains the agent's and more.", "",
            "| Command | v1 | Naive run | Lines | Identical | v1 larger | Agent larger | Overlapping | Disjoint | v1 no answer | Agent no answer | Both none |",
            "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    vn = [p for p in pairs if p["first"].startswith("naive") and p["second"].startswith("v1")]
    groups = defaultdict(list)
    for p in vn:
        groups[(p["cmd"], p["second"], p["first"])].append(p)
    for (cmd, v, nv), ps in sorted(groups.items()):
        c = Counter(p["io_class"] for p in ps)
        n = len(ps)
        out.append(f"| {cmd} | {v} | {nv} | {n} | {pct(c['identical'], n)} | {c['second larger']} | "
                   f"{c['first larger']} | {c['overlapping']} | {c['disjoint']} | {c['no answer: second']} | "
                   f"{c['no answer: first']} | {c['no answer: both']} |")
    out.append("")

    out += ["## Input/output differences by type (v1 vs naive, lines where both answer)", "",
            "| Command | Type | Elements | Lines | Example (line: word, v1 → agent) |", "|---|---|---|---|---|"]
    for cmd in COMMANDS:
        by_t = defaultdict(list)
        for p in vn:
            if p["cmd"] != cmd:
                continue
            for d in p["diffs"]:
                by_t[d["type"]].append((p, d))
        for t, items in sorted(by_t.items(), key=lambda x: -len(x[1])):
            p, d = items[0]
            ex = f"`{lines[p['id']]['line']}`: {d['word']}, {d['second'] or ['—']} → {d['first'] or ['—']}"
            out.append(f"| {cmd} | {t} | {len(items)} | {len({p['id'] for p, _ in items})} | {ex} |")
    out.append("")

    out += ["## Splitting: v1 against each naive run", "",
            "| Command | v1 | Naive run | Lines both answer | Both split | Only v1 splits | Only agent splits | Neither | Same recipes when both split | Agent's recipes include v1's |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for (cmd, v, nv), ps in sorted(groups.items()):
        both = [p for p in ps if p["split_first"] is not None and p["split_second"] is not None]
        bs = [p for p in both if p["split_first"] and p["split_second"]]
        ov = sum(1 for p in both if p["split_second"] and not p["split_first"])
        oa = sum(1 for p in both if p["split_first"] and not p["split_second"])
        ne = sum(1 for p in both if not p["split_first"] and not p["split_second"])
        same = sum(1 for p in bs if p["split_same"])
        incl = sum(1 for p in bs if {tuple(x) for x in p["split_second"]} <= {tuple(x) for x in p["split_first"]})
        out.append(f"| {cmd} | {v} | {nv} | {len(both)} | {len(bs)} | {ov} | {oa} | {ne} | {pct(same, len(bs))} | {pct(incl, len(bs))} |")
    out.append("")

    out += ["## Consistency: naive runs of the same command against each other", "",
            "| Command | Pair | Lines | Same input/output set | Same splitting |", "|---|---|---|---|---|"]
    nn = defaultdict(list)
    for p in pairs:
        if p["first"].startswith("naive") and p["second"].startswith("naive"):
            nn[(p["cmd"], p["first"], p["second"])].append(p)
    for p_key, ps in sorted(nn.items()):
        out.append(f"| {p_key[0]} | {p_key[1]} / {p_key[2]} | {len(ps)} | "
                   f"{pct(sum(p['io_class'] == 'identical' for p in ps), len(ps))} | {pct(sum(p['split_same'] for p in ps), len(ps))} |")
    out.append("")

    exc = Counter()
    for a in answers:
        if a.get("io_outcome") == "exception":
            exc[(a["cmd"], a["side"], "input/output", a["io_exception"])] += 1
        if a.get("par_outcome") == "exception":
            exc[(a["cmd"], a["side"], "parallelizability", a["par_exception"])] += 1
    out += ["## Exceptions raised by a side's classes", "",
            "An input/output exception means PaSh gets no answer and treats the command as side-effectful; "
            "a parallelizability exception means PaSh does not split it.", "",
            "| Command | Side | Class | Lines | Exception |", "|---|---|---|---|---|"]
    out += [f"| {c} | {s} | {k} | {n} | `{e}` |" for (c, s, k, e), n in sorted(exc.items())] or ["| — | | | | none |"]
    out.append("")
    (HERE / "numbers.md").write_text("\n".join(out) + "\n")

    (HERE / "decision_tables").mkdir(exist_ok=True)
    for cmd in COMMANDS:
        names = [x["side"] for x in sides if x["cmd"] == cmd]
        md = render_table(cmd, names, {n: n for n in names}, {"A": "A (benchmark)", "C-v1": "C-v1", "C-naive": "C-naive"},
                          lines, answers)
        (HERE / "decision_tables" / f"{cmd}.md").write_text(md)


def render_table(cmd, names, label, set_label, lines, answers):
    """Rows grouped by identical answer pattern (positions, not file names), differing groups first."""
    by_line = defaultdict(dict)
    for a in answers:
        if a["cmd"] == cmd:
            by_line[a["id"]][a["side"]] = a
    pats = defaultdict(list)
    for lid, ss in by_line.items():
        pats[tuple(describe(ss.get(n)) for n in names)].append(lid)
    order = sorted(names, key=lambda n: label[n])
    idx = {n: i for i, n in enumerate(names)}
    md = [f"# Decision table: {cmd}", "",
          "Each group is a set of lines on which every side answers the same way. Files are named by position "
          "(operand 1, value of -o). Groups where the sides differ come first.", "",
          "Answer format: what the side says is read and written | how PaSh may split it.", "",
          "Sides: " + ", ".join(f"`{label[n]}`" for n in order), ""]
    ordered = sorted(pats.items(), key=lambda kv: (len(set(kv[0])) == 1, -len(kv[1]), kv[0]))
    for pat, lids in ordered:
        lids = sorted(lids)
        ex = [lines[l]["line"] for l in lids[:4]]
        sets_ = Counter(set_label[s] for l in lids for s in lines[l]["sets"])
        md.append(f"### {len(lids)} line(s){'' if len(set(pat)) == 1 else ' — sides differ'}; from {dict(sorted(sets_.items()))}")
        md.append("Examples: " + "; ".join(f"`{e}`" for e in ex))
        md.append("")
        md += [f"- **{label[n]}**: {pat[idx[n]]}" for n in order]
        md.append("")
    return "\n".join(md) + "\n"


def strip_code(text):
    """Remove comments and docstrings, so that neither side is recognisable by its notes."""
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)) and node.body and \
                isinstance(node.body[0], ast.Expr) and isinstance(getattr(node.body[0], "value", None), ast.Constant) \
                and isinstance(node.body[0].value.value, str):
            node.body = node.body[1:] or [ast.Pass()]
    return ast.unparse(tree) + "\n"


def build_packets(seed=20261111, folder="packets", commands=COMMANDS):
    """Blind packets for the qualitative assessment: v1 and naive sides relabelled A, B, C... at random;
    PaSh's own shown openly as R. The key is written apart and not given to the assessor."""
    lines = {l["id"]: l for l in jload(HERE / "lines.jsonl")}
    answers = jload(HERE / "answers.jsonl.gz")
    sides = jload(HERE / "sides.jsonl")
    rng = random.Random(seed)
    for cmd in commands:
        mine = [s for s in sides if s["cmd"] == cmd]
        blind = [s for s in mine if s["family"] != "reference"]
        letters = [chr(ord("A") + i) for i in range(len(blind))]
        rng.shuffle(letters)
        label = {s["side"]: l for s, l in zip(blind, letters)}
        label.update({s["side"]: "R" for s in mine if s["family"] == "reference"})
        v1_l = ", ".join(sorted(label[s["side"]] for s in blind if s["family"] == "v1"))
        nv_l = ", ".join(sorted(label[s["side"]] for s in blind if s["family"] == "naive"))
        set_label = {"A": "benchmark lines", "C-v1": f"test lines of {v1_l}", "C-naive": f"test lines of {nv_l}"}
        out = HERE / folder / cmd
        if out.exists():
            shutil.rmtree(out)
        out.mkdir(parents=True)
        for s in mine:
            d = out / f"side_{label[s['side']]}"
            d.mkdir()
            src = Path(s["dir"]) if s["dir"] else STOCK
            for f in (f"{cmd}.json", f"InputOutputInfoGenerator{cls(cmd)}.py", f"ParallelizabilityInfoGenerator{cls(cmd)}.py"):
                p = (src / f) if s["dir"] else (STOCK / (DATA if f.endswith(".json") else GEN) / f)
                if p.exists():
                    t = p.read_text()
                    (d / f).write_text(strip_code(t) if f.endswith(".py") else json.dumps(json.loads(t), indent=1) + "\n")
                else:
                    (d / f"MISSING_{f}.txt").write_text("This side has no such file.\n")
        names = [s["side"] for s in mine]
        (out / "decision_table.md").write_text(render_table(cmd, names, label, set_label, lines, answers))
        key = {label[s["side"]]: {k: s.get(k) for k in ("side", "family", "dir", "run")} for s in mine}
        kd = HERE / "assessments" / "keys" / folder
        kd.mkdir(parents=True, exist_ok=True)
        (kd / f"{cmd}.json").write_text(json.dumps(key, indent=1, sort_keys=True) + "\n")


RATING_FIELDS = ["io_correct", "io_complete", "split_safe", "split_coverage", "parser_table", "confidence"]


def front_matter(path):
    """The rubric's fixed front matter: top-level `key: value`, and `ratings:` -> side -> field: value."""
    text = path.read_text().split("\n")
    assert text[0].strip() == "---", path
    fm, ratings, side = {}, {}, None
    for line in text[1:]:
        if line.strip() == "---":
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        if line.strip().startswith("- "):  # block-style list item under the last top-level key
            side = None
            continue
        k, _, v = line.strip().partition(":")
        v = v.split(" #")[0].strip()
        if indent == 0:
            fm[k] = v
            side = None
        elif indent == 2 and v == "":
            side = k
            ratings[side] = {}
        elif side:
            ratings[side][k] = v
    fm["ratings"] = ratings
    return fm


def build_unblinded():
    """Map each assessment's letters back to real sides; compare original and swapped assessments."""
    sides = {(s["cmd"], s["side"]): s for s in jload(HERE / "sides.jsonl")}
    rows, by = [], {}
    for folder, sub in (("packets", ""), ("packets_swap", "swap")):
        for cmd in COMMANDS:
            f = HERE / "assessments" / sub / f"{cmd}.md"
            if not f.exists():
                continue
            fm = front_matter(f)
            key = json.loads((HERE / "assessments" / "keys" / folder / f"{cmd}.json").read_text())
            for letter, r in sorted(fm["ratings"].items()):
                real = key[letter]["side"]
                row = {"cmd": cmd, "pass": sub or "first", "letter": letter, "side": real,
                       "family": sides[(cmd, real)]["family"], **{k: r.get(k) for k in RATING_FIELDS},
                       "rubric": fm.get("rubric"), "model": fm.get("assessor_model")}
                rows.append(row)
                by[(cmd, real, row["pass"])] = row
    jdump(rows, HERE / "assessments" / "unblinded.jsonl")
    md = ["# Assessments with the letters revealed", "",
          "Made by `score_pash.py unblind` from the assessments' front matter and the keys. "
          "Ratings are the assessor's, unchanged.", "",
          "| Command | Side | Letter | Inputs/outputs right | Answers given | Splitting safe | Splitting allowed | Parser table | Confidence |",
          "|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        if r["pass"] == "first":
            md.append(f"| {r['cmd']} | {r['side']} | {r['letter']} | " + " | ".join(str(r[k]) for k in RATING_FIELDS) + " |")
    md += ["", "## Stability: the same side assessed twice under different letters", "",
           "| Command | Side | Fields the same (of 6) | Fields that changed |", "|---|---|---|---|"]
    same_total = n_total = 0
    for (cmd, side, p), r in sorted(by.items()):
        if p != "swap" or (cmd, side, "first") not in by:
            continue
        o = by[(cmd, side, "first")]
        changed = [f"{k}: {o[k]} → {r[k]}" for k in RATING_FIELDS if o[k] != r[k]]
        same_total += 6 - len(changed)
        n_total += 6
        md.append(f"| {cmd} | {side} | {6 - len(changed)} | {'; '.join(changed) or '—'} |")
    md += ["", f"Overall: {pct(same_total, n_total)} of rating fields unchanged.", ""]
    (HERE / "assessments" / "unblinded.md").write_text("\n".join(md) + "\n")


def main():
    step = sys.argv[1] if len(sys.argv) > 1 else "all"
    if step in ("sides", "all"):
        find_sides()
    if step in ("lines", "all"):
        build_lines()
    if step in ("answers", "all"):
        build_answers()
    if step in ("iosets", "all"):
        build_iosets()
    if step in ("tables", "all"):
        build_tables()
    if step in ("packets", "all"):
        build_packets()
    if step == "unblind":
        build_unblinded()
    if step == "packets-swap":  # same commands, letters drawn again: for the stability check
        build_packets(seed=7, folder="packets_swap", commands=["cut", "sort", "rm"])


if __name__ == "__main__":
    main()
