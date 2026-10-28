#!/usr/bin/env python3
"""Inside the probe VM: ask each annotation what PaSh would do with a set of command lines, and test every
claim that the work may be split by running the command (task 019 quality check; standard library only).

    python3 ann19_vm.py jobs.json > out.json

jobs.json: {"command": cmd, "package": dir holding an unpacked pash_annotations 0.2.4,
            "arms": {label: dir with <cmd>.json and the two classes, or "" for PaSh's own}, "lines": [...]}

Each arm gets its own copy of the package with its three files laid in, and the command added to the
package's list of annotated commands when it is not there (PaSh looks up only the commands it names; dd, ls,
test and convert are not among them). The classes are called directly, so an exception is recorded rather
than swallowed as PaSh's own lookup does.

The split check, for every line: the line is run on the whole input and on its pieces, and the pieces'
outputs are joined in order. The input is a 120-line text (about 2 KB), given where the line reads it: its in.txt operand,
dd's if= file, or else standard input; the output is standard output plus dd's of= file. "Consecutive pieces"
means cut into 2 and into 3 parts at line boundaries; "one file at a time" (lines with in.txt and in2.txt)
means each operand run alone. A split is safe when every piece run exits as the whole run does and the
joined output equals the whole output; "one file at a time" uses in.txt and in2.txt (in2.txt added after
in.txt when the line names only in.txt). Cutting the input is meaningful only when the line's result depends
on it: a line whose exit status and output are the same for a different input (test; convert, which reads
its image; dd count=0) has no safe cut.
"""
import json, os, re, shutil, subprocess, sys, tempfile

JOB = json.load(open(sys.argv[1]))
CMD = JOB["command"]
NAME = CMD[0].upper() + CMD[1:]
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": os.environ.get("HOME", "/tmp")}
BASE = [w for w in (
    "alpha:beta:gamma", "Alpha:Beta:Gamma", "one\ttwo\tthree", "  leading spaces", "trailing spaces  ",
    "", "12:7:3", "12:7:3", "zeta", "eta:theta", "a", "b", "b", "c", "x:y", "x:y:z:w", "UPPER lower",
    "42", "-7", "3.14", "the quick brown fox", "jumps over", "the lazy dog", "", "last but one",
    "repeat", "repeat", "repeat", "tail:end", "done")]
# 120 lines, about 2 KB: larger than a few of dd's 512-byte blocks, so count= and skip= change the result
TEXT = "".join(f"{w}\n" if i % 3 else f"{i:03d} {w}\n" for i, w in enumerate(BASE * 4))
PPM = "P3\n2 2\n255\n0 0 0 255 255 255 0 0 0 255 255 255\n"

GEN = r'''
import enum, json, sys
sys.path.insert(0, sys.argv[1])
from pash_annotations.parser.parser import parse
import pash_annotations.annotation_generation.AnnotationGeneration as AG

def plain(x, depth=0):
    if depth > 6:
        return repr(x)
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    if isinstance(x, (list, tuple)):
        return [plain(v, depth + 1) for v in x]
    if isinstance(x, enum.Enum):
        return x.name
    if hasattr(x, "__dict__"):
        return {"_": type(x).__name__, **{k: plain(v, depth + 1) for k, v in vars(x).items()}}
    return repr(x)

out = {}
for line in json.loads(sys.argv[2]):
    rec = {}
    try:
        inv = parse(line)
        rec["parsed"] = {"flags_options": [str(f) for f in inv.flag_option_list], "operands": [str(o) for o in inv.operand_list]}
    except Exception as e:
        out[line] = {"parse_error": f"{type(e).__name__}: {e}"[:300]}
        continue
    for kind in ("InputOutputInfoGenerator", "ParallelizabilityInfoGenerator"):
        cls = getattr(AG, kind + sys.argv[3], None)
        if cls is None:
            rec[kind] = {"error": "no class"}
            continue
        try:
            obj = cls(parse(line))
            obj.generate_info()
            info = obj.get_info()
            if kind == "ParallelizabilityInfoGenerator":
                pl = info.get_inferred_parallelizer_list() if info is not None else []
                rec[kind] = {"parallelizers": [plain(p) for p in pl], "commutative": getattr(info, "is_commutative", None)}
            else:
                rec[kind] = plain(info)
        except Exception as e:
            rec[kind] = {"error": f"{type(e).__name__}: {e}"[:300]}
    out[line] = rec
print(json.dumps(out))
'''


def arm_package(label, src):
    d = tempfile.mkdtemp(prefix="t019ann.")
    shutil.copytree(os.path.join(JOB["package"], "pash_annotations"), os.path.join(d, "pash_annotations"))
    if src:
        pkg = os.path.join(d, "pash_annotations")
        shutil.copy(os.path.join(src, f"{CMD}.json"), os.path.join(pkg, "parser/command_flag_option_info/data", f"{CMD}.json"))
        for kind in ("InputOutputInfoGenerator", "ParallelizabilityInfoGenerator"):
            f = os.path.join(src, f"{kind}{NAME}.py")
            if os.path.exists(f):
                shutil.copy(f, os.path.join(pkg, "annotation_generation/annotation_generators", f"{kind}{NAME}.py"))
        ag = os.path.join(pkg, "annotation_generation/AnnotationGeneration.py")
        s = open(ag).read()
        if f'"{CMD}":' not in s:
            s = s.replace("DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {",
                          f'DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {{\n    "{CMD}": "{NAME}",', 1)
            open(ag, "w").write(s)
    return d


def run(argv, stdin_text, work):
    try:
        p = subprocess.run(argv, cwd=work, env=ENV, input=stdin_text.encode() if stdin_text is not None else b"",
                           capture_output=True, timeout=10)
        return p.returncode, p.stdout
    except subprocess.TimeoutExpired:
        return "timeout", b""


# the other input for the "does the result depend on the input" test: every line different (upper case),
# in reverse order, plus one line with tabs and colons (repair of 2026-10-28: a reordering alone left
# `cut -s -f 1`'s output unchanged, so that line was wrongly taken to ignore its input)
ALT = "".join(reversed(TEXT.upper().splitlines(keepends=True))) + "AN EXTRA\tLINE\tX:Y:Z\n"


def split_check(line):
    words = line.split()
    work = tempfile.mkdtemp(prefix="t019split.")
    try:
        open(os.path.join(work, "in2.txt"), "w").write("second file\nzz\n")
        open(os.path.join(work, "in.ppm"), "w").write(PPM)
        for w in words:
            for ph in re.findall(r"relpath_\d+", w):
                open(os.path.join(work, ph), "w").write("a\nb\n")
        # where the line reads the input being split: its in.txt operand, dd's if= file, or standard input
        carrier = next((i for i, w in enumerate(words) if w == "in.txt"), None)
        if carrier is None:
            carrier = next((i for i, w in enumerate(words) if CMD == "dd" and w.startswith("if=")), None)
        out_file = next((w[3:] for w in words if CMD == "dd" and w.startswith("of=")), None)

        def go(text, tag):
            argv = list(words)
            if carrier is not None:
                name = f"input_{tag}.txt"
                open(os.path.join(work, name), "w").write(text)
                argv[carrier] = ("if=" + name) if argv[carrier].startswith("if=") else name
            if out_file:
                try:
                    os.remove(os.path.join(work, out_file))
                except FileNotFoundError:
                    pass
            rc, out = run(argv, None if carrier is not None else text, work)
            if out_file and os.path.exists(os.path.join(work, out_file)):
                out += open(os.path.join(work, out_file), "rb").read()
            return rc, out

        lines = TEXT.splitlines(keepends=True)
        whole_rc, whole = go(TEXT, "whole")
        alt_rc, alt = go(ALT, "alt")
        res = {"whole_exit": whole_rc, "whole_bytes": len(whole), "reads_input": (whole_rc, whole) != (alt_rc, alt)}
        ok = res["reads_input"]   # pieces are run only when the result depends on the input
        for parts in ((2, 3) if ok else ()):
            size = -(-len(lines) // parts)
            joined = b""
            for i in range(parts):
                rc, out = go("".join(lines[i * size:(i + 1) * size]), f"p{parts}_{i}")
                ok = ok and rc == whole_rc
                joined += out
            ok = ok and joined == whole
        # cutting the input is meaningful only for a line whose result depends on that input
        res["consecutive"] = ok and res["reads_input"]
        if "in.txt" in words:
            # one file at a time: the line with in.txt and in2.txt (added after in.txt when the line has only
            # in.txt), against each file alone, joined in order
            two = list(words) if "in2.txt" in words else \
                [x for w in words for x in ((w, "in2.txt") if w == "in.txt" else (w,))]
            open(os.path.join(work, "in.txt"), "w").write(TEXT)
            joined, good = b"", True
            whole2_rc, whole2 = run(two, None, work)
            for keep in ("in.txt", "in2.txt"):
                rc, out = run([w for w in two if w not in ("in.txt", "in2.txt") or w == keep], None, work)
                good = good and rc == whole2_rc
                joined += out
            res["one_file_at_a_time"] = good and joined == whole2
        return res
    finally:
        shutil.rmtree(work, ignore_errors=True)


result = {"command": CMD, "arms": {}, "split": {}}
for label, src in JOB["arms"].items():
    d = arm_package(label, src)
    p = subprocess.run(["python3", "-I", "-c", GEN, d, json.dumps(JOB["lines"]), NAME], capture_output=True, text=True)
    result["arms"][label] = json.loads(p.stdout) if p.returncode == 0 else {"error": p.stderr[-800:]}
    shutil.rmtree(d, ignore_errors=True)
for line in JOB["lines"]:
    result["split"][line] = split_check(line)
json.dump(result, sys.stdout)
