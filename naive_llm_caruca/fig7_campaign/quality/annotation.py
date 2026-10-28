#!/usr/bin/env python3
"""Task 019 quality check, behaviour half: what each run's PaSh annotation says about a fixed set of command
lines, and whether its claims that the work may be split hold when the command is run (ann19_vm.py).

The command lines, the same for every annotation: the command with no options, and every sample value of
every real option in any graded syntax file (at most five per option, written as the syntax check writes
them), each alone, with the operands of a minimal valid line (cut also gets `-f 1` when no selector is
present; ls gets two files so that "one file at a time" can be tested). For `test`, every real operator
with a file operand (`test -f in.txt`, `test in.txt -nt in.txt`).

Lines the program refuses (non-zero exit on the whole input, e.g. `dd bs=1m`; for test, an exit other than 0
or 1) are not uses and are not graded.

Repairs, 2026-10-28, after a first pass over the Fable pilot's annotations and the Opus ones then finished
(ls, cut, test), before Opus's convert: (1) the check's second input now differs on every line, since a
reordering alone left `cut -s -f 1` unchanged and that line was taken to ignore its input, so every split
claim for it was marked wrong, PaSh's own included; (2) a claim to run one file at a time is tested on a
two-file version of a one-file line, not on cutting the input; (3) test's exit 1 is an answer, not a
refusal. Before: cut Fable 50/52, Opus 75/79, PaSh's own 50/54; dd Fable 56/62.
Grades per annotation, never blended:
  claims right   each way of splitting the annotation lists for a line (a splitter that cuts the input into
                 consecutive pieces or deals it out in turn, or runs one file at a time, with the command
                 itself on each piece and the outputs joined in order) is right when the split check finds
                 that split safe; claims with another way of joining are listed, not graded
  missed         lines with no claim although cutting the input into consecutive pieces is safe
  errors         lines where the annotation's class raised an exception (PaSh then has no information)
  agreement      lines where the input/output reading (operands, standard input and output, option
                 arguments) equals another annotation's, PaSh's own for `cut`

    .venv/bin/python naive_llm_caruca/fig7_campaign/quality/annotation.py dd ls cut test convert

Needs t019-probe running and pash_annotations 0.2.4 unpacked at PKG (the PyPI wheel, sha256 ff475a6f…).
"""
import json, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import quality  # noqa: E402

PKG = Path("/private/tmp/claude-501/-Users-tirandagan-dev-stevens-caruca-v2/847af186-9ee1-4722-b197-efbac4d5092a/scratchpad/pa/pkg")
PASH_OWN = {"cut"}  # of the five, the only command PaSh 0.2.4 annotates itself
VM = quality.PROBE_VM
SELECTORS = {"-b", "-c", "-f", "--bytes", "--characters", "--fields"}


def lines_for(cmd):
    res = json.loads((quality.RESULTS / f"{cmd}.json").read_text())
    if cmd == "test":
        out = ["test -f in.txt"]
        for s, v in sorted(res["probe"]["spellings"].items()):
            kinds = v.get("test_kind") or []
            if "one operand" in kinds:
                out.append(f"test {s} in.txt")
            if "two operands" in kinds:
                out.append(f"test in.txt {s} in.txt")
        return list(dict.fromkeys(out))
    sp = res["probe"]["spellings"]
    real = lambda s: bool(sp.get(s, {}).get("accepted"))  # noqa: E731
    optional = lambda s: sp.get(s, {}).get("value") == "optional"  # noqa: E731
    ops = {"cut": ["in.txt"], "ls": ["in.txt", "in2.txt"], "dd": [], "convert": ["in.ppm", "out.png"]}[cmd]
    # every sample value of every real option in any graded file, written as the syntax check writes it
    uses = [[]]
    for path in quality.sources(cmd).values():
        for n in (quality.facts19.load_grammar(cmd, path) or {}).get("nodes", []):
            if not n["flag"] or not any(real(x) for x in [n["flag"], *n["alias"]]):
                continue
            if n["takes_value"]:
                for f in quality.facts19.sample(n["forms"]):
                    w = quality.facts19.space_words(n, f, real)
                    uses.append([f"{w[0]}={w[1]}"] if len(w) == 2 and (optional(w[0]) or not w[0].startswith("-")) else w)
            else:
                uses.append([n["flag"] if real(n["flag"]) else next(x for x in n["alias"] if real(x))])
    out = []
    for words in uses:
        words = [w.replace("abspath_", "relpath_") for w in words]
        if any(w.split("=", 1)[0] in ("--help", "--version") for w in words):
            continue
        extra = ["-f", "1"] if cmd == "cut" and not any(w.split("=", 1)[0] in SELECTORS or
                                                         (w[:2] in {"-b", "-c", "-f"} and len(w) > 2) for w in words) else []
        out.append(" ".join([cmd, *words, *extra, *ops]))
    return list(dict.fromkeys(out))


def claims(rec):
    p = (rec or {}).get("ParallelizabilityInfoGenerator") or {}
    if "error" in p:
        return None
    out = []
    for x in p.get("parallelizers", []):
        out.append(((x.get("splitter") or {}).get("kind"), (x.get("core_mapper_spec") or {}).get("kind"),
                    (x.get("core_aggregator_spec") or {}).get("kind")))
    return out


def io_view(rec):
    io = (rec or {}).get("InputOutputInfoGenerator")
    if not isinstance(io, dict) or "error" in io:
        return None
    return json.dumps({k: io.get(k) for k in ("flagoption_list_typer", "operand_list_typer",
                                               "implicit_use_of_streaming_input", "implicit_use_of_streaming_output")},
                      sort_keys=True)


def grade(cmd, out):
    split = out["split"]
    g = {}
    for label, recs in out["arms"].items():
        if "error" in recs:
            g[label] = {"error": recs["error"]}
            continue
        right = checked = missed = safe_lines = errors = 0
        wrong, unchecked, missed_lines = [], [], []
        refused = 0
        for line, rec in recs.items():
            s = split[line]
            if s.get("whole_exit") not in ((0, 1) if cmd == "test" else (0,)):  # refused: not a use to split
                # (test's exit 1 is the answer "false")
                refused += 1
                continue
            c = claims(rec)
            if c is None or "parse_error" in rec:
                errors += 1
                c = []
            if s.get("consecutive"):
                safe_lines += 1
            for spl, mapper, agg in c:
                if agg != "CONCATENATE" or mapper not in ("SAME_AS_SEQ", None):
                    unchecked.append([line, spl, mapper, agg])
                    continue
                checked += 1
                if spl == "INDIV_FILES":
                    ok = bool(s.get("one_file_at_a_time"))
                else:
                    ok = bool(s.get("consecutive"))
                right += ok
                if not ok:
                    wrong.append([line, spl])
            if not c and s.get("consecutive"):
                missed += 1
                missed_lines.append(line)
        g[label] = {"lines": len(recs), "lines_refused_by_the_program": refused, "claims_checked": checked, "claims_right": right, "claims_wrong": wrong,
                    "claims_not_checked": unchecked, "missed": missed, "missed_lines": missed_lines,
                    "lines_safe_to_cut": safe_lines, "errors": errors,
                    "errors_detail": {l: (r.get("parse_error") or r.get("ParallelizabilityInfoGenerator", {}).get("error")
                                          or r.get("InputOutputInfoGenerator", {}).get("error"))
                                      for l, r in recs.items() if "parse_error" in r or claims(r) is None
                                      or io_view(r) is None}}
    labels = [l for l in out["arms"] if "error" not in out["arms"][l]]
    agree = {}
    for i, a in enumerate(labels):
        for b in labels[i + 1:]:
            same = [line for line in out["arms"][a] if io_view(out["arms"][a][line]) is not None
                    and io_view(out["arms"][a][line]) == io_view(out["arms"][b].get(line))]
            agree[f"{a} = {b}"] = [len(same), len(out["arms"][a])]
    return g, agree


def run(cmd):
    rows = quality.runs(cmd)
    arms = {label: Path(quality.REPO / d["run_folder"] / "output" / "annotation") for label, d in rows.items()}
    lines = lines_for(cmd)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["tar", "-C", str(PKG), "-czf", f"{tmp}/pkg.tgz", "pash_annotations"], check=True)
        subprocess.run(["limactl", "copy", f"{tmp}/pkg.tgz", f"{VM}:/tmp/t019pkg.tgz"], check=True)
        subprocess.run(["limactl", "shell", VM, "--", "bash", "-c",
                        "rm -rf /tmp/t019pkg /tmp/t019arms && mkdir -p /tmp/t019pkg /tmp/t019arms && "
                        "tar -C /tmp/t019pkg -xzf /tmp/t019pkg.tgz"], check=True)
        vm_arms = {}
        for i, (label, p) in enumerate(arms.items()):
            subprocess.run(["limactl", "copy", "-r", str(p), f"{VM}:/tmp/t019arms/{i}"], check=True)
            vm_arms[label] = f"/tmp/t019arms/{i}"
        if cmd in PASH_OWN:
            vm_arms["PaSh's own"] = ""
        job = Path(tmp) / "job.json"
        job.write_text(json.dumps({"command": cmd, "package": "/tmp/t019pkg", "arms": vm_arms, "lines": lines}))
        subprocess.run(["limactl", "copy", str(job), f"{VM}:/tmp/t019annjob.json"], check=True)
        subprocess.run(["limactl", "copy", str(HERE / "ann19_vm.py"), f"{VM}:/tmp/t019ann.py"], check=True)
        p = subprocess.run(["limactl", "shell", VM, "--", "python3", "/tmp/t019ann.py", "/tmp/t019annjob.json"],
                           capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-1500:])
    out = json.loads(p.stdout)
    out["grades"], out["io_agreement"] = grade(cmd, out)
    (quality.RESULTS / f"annotation_{cmd}.json").write_text(json.dumps(out, indent=1))
    return out


def table(commands):
    rows, agree = [], []
    for c in commands:
        f = quality.RESULTS / f"annotation_{c}.json"
        if not f.is_file():
            continue
        d = json.loads(f.read_text())
        for label, g in d["grades"].items():
            if "error" in g:
                rows.append(f"| `{c}` | {label} | error: {g['error'][:80]} | | | |")
                continue
            rows.append(f"| `{c}` | {label} | {g['claims_right']}/{g['claims_checked']} | {len(g['claims_not_checked'])} | "
                        f"{g['missed']} of {g['lines_safe_to_cut']} | {g['errors']} of {g['lines']} |")
        for pair, (n, t) in d["io_agreement"].items():
            agree.append(f"| `{c}` | {pair} | {n}/{t} |")
    text = "\n".join(["## Annotation behaviour: claims that the work may be split, tested by running the command", "",
                      "| Command | Annotation | Claims right / checked | Claims not checked (other joining) | "
                      "Missed (safe to cut, no claim) | Lines where the class failed |", "|---|---|---|---|---|---|", *rows, "",
                      "## Input/output reading: lines where two annotations agree", "",
                      "| Command | Pair | Lines agreeing |", "|---|---|---|", *agree, ""])
    (quality.RESULTS / "annotation_summary.md").write_text(text)
    print(text)


if __name__ == "__main__":
    cmds = sys.argv[1:] or quality.COMMANDS
    if cmds != ["--table"]:
        for c in cmds:
            run(c)
    table(quality.COMMANDS)
