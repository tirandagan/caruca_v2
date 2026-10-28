#!/usr/bin/env python3
"""Ask the real command which option spellings it accepts and whether each takes a value.

Task 019 copy of naive_llm_caruca/scoring/probe_binary.py (task 018's tool, left unchanged), extended on
2026-10-28 for dd, ls, test and convert before any file of the Opus 5.5 comparison was scored. Additions,
each applied to every file alike: `convert` is asked with two image files around the spelling, since it
refuses any single argument ("missing required argument"); `+name` spellings are probed as `-name` ones are;
`test` is asked whether a spelling works as a one-operand operator (`test S a.txt`) or a two-operand one
(`test a.txt S a.txt`), since a lone word is always true; dd's `name=` words and test's operators are read
from their own --help and manual. Repair, 2026-10-28, after a first pass over the Fable pilot files only:
`)` is tried as the closing half of a grouping and every test spelling as `test S abc -eq 3` (GNU's `-l`),
since a file listing either was marked wrong although test accepts both (before: Fable's test file 52/65).
Everything else is as in task 018:

Runs inside a throwaway clone of the naive-arm VM image (the same binaries the agent saw),
with the standard library only:

    python3 probe_binary.py CMD candidates.json > probe.json

`candidates.json` is {"spellings": [...]}: every option spelling named by any syntax file being
scored. The probe adds every spelling it can find in `CMD --help` and the manual page, so the
union of sources defines what "all the options" means; the binary decides which are real.

Each spelling is run at most twice, with stdin from /dev/null, in a fresh empty folder holding
one small text file, with LC_ALL=C and a 3-second limit:

  long  (--name)  `CMD --name` and `CMD --name=zzinvalid`
  short (-x)      `CMD -x`
  word  (bs, if)  `CMD word=1`   (dd-style operands)

and classified by GNU's own error messages: "unrecognized option" / "invalid option" /
"unrecognized operand" mean the spelling does not exist; "requires an argument" means it needs a
value; "doesn't allow an argument" means it takes none; anything else means it was accepted.
"Valid arguments are:" lists are kept, since they are the command describing its own values.
"""
import json, os, re, shutil, subprocess, sys, tempfile

CMD = sys.argv[1]
GIVEN = json.load(open(sys.argv[2]))["spellings"]
TIMEOUT = 3
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": os.environ.get("HOME", "/tmp")}

# GNU getopt's messages, then Python argparse's (binwalk): an unknown option there is taken as a file
# name ("Cannot open file --bogus"), a missing value is "expected one argument", and a value given to an
# option that takes none is "ignored explicit argument"
NOT_ACCEPTED = re.compile(r"unrecognized option|invalid option --|unrecognized operand|unknown option|illegal option"
                          r"|unrecognized arguments")
AMBIGUOUS = re.compile(r"is ambiguous")
REQUIRES = re.compile(r"requires an argument|expected one argument")
NO_VALUE = re.compile(r"doesn't allow an argument|ignored explicit argument")
VALUE_ITEM = re.compile(r"[‘'`]([^’'`]+)[’'`]")


def not_accepted(spelling, stderr):
    return bool(NOT_ACCEPTED.search(stderr)) or f"Cannot open file {spelling} " in stderr


PPM = "P3\n2 2\n255\n0 0 0 255 255 255 0 0 0 255 255 255\n"   # a 2x2 image ImageMagick reads


def run(argv):
    work = tempfile.mkdtemp(prefix="t018probe.")
    with open(os.path.join(work, "a.txt"), "w") as f:
        f.write("one\ntwo\nthree\n")
    with open(os.path.join(work, "in.ppm"), "w") as f:
        f.write(PPM)
    try:
        p = subprocess.run(argv, cwd=work, env=ENV, stdin=subprocess.DEVNULL, capture_output=True,
                           timeout=TIMEOUT, text=True, errors="replace")
        out = {"argv": argv, "rc": p.returncode, "stderr": p.stderr[:600], "timed_out": False}
    except subprocess.TimeoutExpired:
        out = {"argv": argv, "rc": None, "stderr": "", "timed_out": True}
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return out


def valid_values(stderr):
    if "Valid arguments are:" not in stderr:
        return []
    tail = stderr.split("Valid arguments are:", 1)[1]
    values = []
    for line in tail.splitlines():
        if not line.strip().startswith("-"):
            if values:
                break
            continue
        values += VALUE_ITEM.findall(line)
    return values


def probe(spelling):
    if CMD == "convert" and not (spelling[:1] in "-+" and len(spelling) >= 2):
        # convert has no option words without a leading - or +; such a word is read as an image file name
        return {"accepted": False, "valid_values": [], "runs": [], "note": "not an option word for convert"}
    if CMD == "convert":
        # an unknown spelling is named as such; one that takes a value swallows in.ppm and then fails
        r0 = run([CMD, spelling, "in.ppm", "out.png"])
        runs = [r0]
        if NOT_ACCEPTED.search(r0["stderr"]):
            verdict = {"accepted": False}
        elif r0["rc"] == 0 or r0["timed_out"]:
            verdict = {"accepted": True, "value": "none"}
        else:
            verdict = {"accepted": True, "value": "required"}
        verdict["valid_values"] = []
        verdict["runs"] = runs
        return verdict
    if CMD == "test":
        # exit 0 or 1 is an answer; 2 is test's "not an expression"
        # two-operand operators are tried on file names and on integers (-eq and the like need integers)
        r0, r1, r1n = run([CMD, spelling, "a.txt"]), run([CMD, "a.txt", spelling, "a.txt"]), run([CMD, "1", spelling, "1"])
        runs = [r0, r1, r1n]
        kinds = [k for k, r in (("one operand", r0), ("two operands", r1)) if r["rc"] in (0, 1)]
        if "two operands" not in kinds and r1n["rc"] in (0, 1):
            kinds.append("two operands")
        if "one operand" not in kinds:  # -t takes a file-descriptor number
            r0n = run([CMD, spelling, "1"])
            runs.append(r0n)
            if r0n["rc"] in (0, 1):
                kinds.append("one operand")
        if spelling in ("(", ")"):  # the two halves of a grouping
            r2 = run([CMD, "(", "a.txt", ")"])
            runs.append(r2)
            if r2["rc"] in (0, 1):
                kinds.append("grouping")
        if not kinds:  # GNU's -l STRING, the string's length inside an integer comparison
            r3 = run([CMD, spelling, "abc", "-eq", "3"])
            runs.append(r3)
            if r3["rc"] in (0, 1):
                kinds.append("length of a string")
        return {"accepted": bool(kinds), "value": None, "test_kind": kinds, "valid_values": [], "runs": runs}
    if spelling.startswith("--"):
        r0, r1 = run([CMD, spelling]), run([CMD, spelling + "=zzinvalid"])
        runs = [r0, r1]
        if not_accepted(spelling, r0["stderr"]):
            verdict = {"accepted": False}
        elif AMBIGUOUS.search(r0["stderr"]):
            verdict = {"accepted": False, "ambiguous": True}
        elif REQUIRES.search(r0["stderr"]):
            verdict = {"accepted": True, "value": "required"}
        elif NO_VALUE.search(r1["stderr"]):
            verdict = {"accepted": True, "value": "none"}
        else:
            verdict = {"accepted": True, "value": "optional"}
        verdict["valid_values"] = valid_values(r1["stderr"]) or valid_values(r0["stderr"])
    elif spelling.startswith("-") and len(spelling) >= 2:
        r0 = run([CMD, spelling])
        runs = [r0]
        if not_accepted(spelling, r0["stderr"]):
            verdict = {"accepted": False}
        elif REQUIRES.search(r0["stderr"]):
            verdict = {"accepted": True, "value": "required"}
        else:
            verdict = {"accepted": True, "value": "none"}
        verdict["valid_values"] = valid_values(r0["stderr"])
    else:
        r0 = run([CMD, spelling + "=1"])
        runs = [r0]
        verdict = {"accepted": not NOT_ACCEPTED.search(r0["stderr"]), "value": "required", "valid_values": []}
    verdict["runs"] = runs
    return verdict


def from_docs():
    """Option spellings named by the command's own --help and manual page."""
    found = {}
    man = subprocess.run(["man", "-P", "cat", CMD], env={**ENV, "MANWIDTH": "200"},
                         capture_output=True, text=True, errors="replace").stdout
    help_out = subprocess.run([CMD, "--help"], env=ENV, stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, errors="replace", timeout=TIMEOUT).stdout
    if CMD == "dd":  # dd's options are name=VALUE words at the start of --help's lines
        for line in help_out.splitlines():
            m = re.match(r"\s+([a-z]+)=", line)
            if m:
                found.setdefault(m.group(1), set()).add("help")
        return {k: sorted(v) for k, v in found.items()}
    if CMD == "test":  # operators stand anywhere in the manual's expression lines
        for line in man.splitlines():
            for s in re.findall(r"(?<![\w-])(-[a-zA-Z]{1,2}|!=|==|=|!|\()(?![\w-])", line):
                found.setdefault(s, set()).add("man")
        return {k: sorted(v) for k, v in found.items()}
    lead = r"\s*[-+]" if CMD == "convert" else r"\s*-"
    spell = r"(?<![\w-])([-+]{1,2}[A-Za-z0-9][A-Za-z0-9-]*)" if CMD == "convert" else r"(?<![\w-])(--?[A-Za-z0-9][A-Za-z0-9-]*)"
    for source, text in (("help", help_out), ("man", man)):
        for line in text.splitlines():
            if not re.match(lead, line):
                continue
            # an option line: spellings first, then two or more spaces, then the description
            head = re.split(r"\s{2,}", line.strip())[0]
            for s in re.findall(spell, head):
                found.setdefault(s, set()).add(source)
    return {k: sorted(v) for k, v in found.items()}


def version():
    # GNU tools answer --version; binwalk has none and names its version in --help's first line
    for flag in ("--version", "--help"):
        try:
            p = subprocess.run([CMD, flag], env=ENV, capture_output=True, text=True, timeout=TIMEOUT)
        except Exception:
            continue
        lines = [l.strip() for l in (p.stdout + p.stderr).splitlines() if l.strip()]
        # binwalk takes --version as a file name and answers with an error, so require a clean answer
        if lines and p.returncode == 0 and "error" not in lines[0].lower() and re.search(r"\d+\.\d+", lines[0]):
            return lines[0]
    return "unavailable"


docs = from_docs()
sources = {s: ["syntax files"] for s in GIVEN}
for s, where in docs.items():
    sources.setdefault(s, []).extend(where)

result = {"command": CMD, "binary": shutil.which(CMD), "version": version(), "spellings": {}}
for s in sorted(sources):
    entry = probe(s)
    entry["named_by"] = sources[s]
    result["spellings"][s] = entry
json.dump(result, sys.stdout, indent=1, ensure_ascii=False)
