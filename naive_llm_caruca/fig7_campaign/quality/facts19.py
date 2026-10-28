"""Program-checked accuracy: facts about a command's syntax, every one settled by running the program.

Task 019 copy of naive_llm_caruca/scoring/facts.py (task 018's tool, left unchanged), extended on 2026-10-28
for dd, ls and convert before any file of the Opus 5.5 comparison was scored; the facts and the rule are
task 018's. Additions, each applied to every file alike: the probe VM is t019-probe (a clone of the golden
image the campaign's agents ran in); operands for ls (two text files), dd (none: dd reads standard input,
and a file operand is refused) and convert (an input image and an output file, its minimal valid line);
convert's "-" check reads an image from standard input; a placeholder file after a convert option is an
image; and a dd-style option (a spelling without a leading dash) gets its sample values after "=", the only
way dd takes a value, just as an optional value does below. `test` is not scored here (an expression
language, not options before operands): only facts a and b, from the probe.

Repair, 2026-10-28, after a first pass over the Fable 5.1 pilot files only (no Opus file scored yet): dd's
minimal valid line also gets `of=out.bin` (unless the options give `of=`), the way cut's gets `-f 1`.
Without it dd wrote to the probe's pipe, where `seek=1` fails ("cannot seek: Illegal seek") whatever the
file says: every dd file, Caruca's reference included, failed fact d for seek. Before the repair: dd's
reference 58/69, both GPT-4o files 58/69, Fable 66/82.

Repair, 2026-10-28, same first pass: for convert, a pair of options counts as refused together (fact h) only
when ImageMagick's message is about the command line (unrecognized option, missing or invalid argument,
unbalanced parenthesis). Its other refusals of a pair are about the 2x2 test image ("image size differs",
"image depth not supported", "no images defined"), so nearly every pair failed for every file: before the
repair, h was 1/56 for the reference and the shipped GPT-4o file and 1/1024 for Fable (convert totals
856/1,274, 836/1,274 and 1,695/2,849). Task 018's text follows.

The headline grade of task 018: facts a file gets right / all facts about it. The fact list and the
rule were fixed on 2026-10-27, before any file was scored with them (task 018, section 2.2):

  a listed  each real option spelling (named by any file, the manual or --help, and accepted by the
            program) appears in the file                                  [from score 2's probe]
  b real    each spelling the file lists is accepted by the program       [from score 2's probe]
  c value   each listed real spelling takes a value or not, as the program does; a value the program
            treats as optional agrees with either reading                 [from score 2's probe]
            (no value type in v1's format fits GNU `sort -y` exactly: bare `-y` is refused, `-y 5`
            ignores the 5, `-y abc` reads abc as a file; checked on coreutils 9.4, 2026-10-27. Fact c
            follows getopt, which requires a value, so a file listing `-y` as a flag counts wrong)
  d kind    each listed real option that takes a value: its sample values, written after a space (after
            "=" where the program takes the value only that way, i.e. an optional value), are accepted in
            a minimal valid command line
  e equals  each listed real option the file marks with "=": the forms v1's generator writes (first
            spelling, "=", value) are accepted and create no file whose name starts with "="
  f repeat  each listed real value-taking option where the program refuses a repeat, or the file
            allows one: the two agree (repeats the program accepts and the file does not claim are not
            counted, since most are harmless "last one wins")
  g files   four facts: whether 0, 1 and 2 file operands are allowed with no options, and whether "-"
            means standard input
  h rules   each pair of listed real options that the program refuses together (each being accepted
            alone) or that the file never allows in one layout: the two agree; plus whether a command
            line with no options at all is valid. A refusal whose message quotes one of the two sample
            values is about that value, not the pairing, and is not counted

Sample values: at most 5 per option (v1's first two forms, the middle one and the last two). A minimal
valid command line adds the operands each command needs (`cut` also gets `-f 1` when no selector is
present). --help and --version are left out of d to h, since they end the run early.
"""
import json, math, re, shlex, subprocess, tempfile
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1_PY = Path.home() / "dev/stevens/caruca/caruca/.venv/bin/python"
PROBE_VM = "t019-probe"
# v1's Arity enum (ir/environment.py): ONE_OR_MORE is an alias of AT_LEAST_ONE and ZERO_OR_ONE of OPTIONAL,
# so a loaded node always reports the first name
REPEATABLE = {"ZERO_OR_MORE", "AT_LEAST_ONE"}
REQUIRED = {"EXACTLY_ONE", "EXACTLY_TWO", "AT_LEAST_ONE"}
ARITY_RANGE = {"EXACTLY_ONE": (1, 1), "EXACTLY_TWO": (2, 2), "OPTIONAL": (0, 1), "ZERO_OR_MORE": (0, math.inf),
               "AT_LEAST_ONE": (1, math.inf)}
SHORT_CIRCUIT = {"--help", "--version"}
CUT_SELECTORS = {"-b", "-c", "-f", "--bytes", "--characters", "--fields"}
OPERANDS = {"cut": ["in.txt", "in2.txt"], "sort": ["in.txt", "in2.txt"], "rm": ["target", "target2"],
            "binwalk": ["target.bin", "target2.bin"],
            "ls": ["in.txt", "in2.txt"], "dd": ["in.txt", "in2.txt"], "convert": ["in.ppm", "out.png"]}
# what a minimal valid command line has after the options, where it is not the first file operand
MIN_OPERANDS = {"dd": [], "convert": ["in.ppm", "out.png"]}
# the "-" check: the operands and what standard input holds
PPM = "P3\n2 2\n255\n0 0 0 255 255 255 0 0 0 255 255 255\n"
STDIN_CHECK = {"convert": (["-", "out.png"], PPM)}
DEFAULT_FIXTURE = {"convert": "image"}
# ImageMagick's messages about the command line itself; its other refusals are about the images
IM_COMMAND_LINE = re.compile(r"unrecognized option|missing required argument|invalid argument for option"
                             r"|option requires an argument|unbalanced parenthesis")
# what a placeholder path must be for the option it follows to make sense
FIXTURE = {("sort", "-T"): "dir", ("sort", "--temporary-directory"): "dir", ("sort", "--files0-from"): "files0",
           ("sort", "--random-source"): "random", ("sort", "-o"): "absent", ("sort", "--output"): "absent",
           ("binwalk", "-C"): "dir", ("binwalk", "--directory"): "dir"}
PLACEHOLDER = re.compile(r"(?:rel|abs)path_\d+")


def load_grammar(cmd, path):
    p = subprocess.run([str(V1_PY), "-I", str(HERE / "facts_grammar.py"), cmd, str(path)],
                       capture_output=True, text=True)
    return json.loads(p.stdout) if p.returncode == 0 else None


def sample(forms):
    return forms if len(forms) <= 5 else [forms[0], forms[1], forms[len(forms) // 2], forms[-2], forms[-1]]


def spellings(node):
    return [node["flag"], *node["alias"]]


def is_selector(w):
    return w.split("=", 1)[0] in CUT_SELECTORS or (len(w) > 2 and w[:2] in {"-b", "-c", "-f"} and w[1] != "-")


def context(cmd, words, operands=None, raw=False):
    """The command, the option words, and what a minimal valid command line needs around them."""
    if operands is None:
        operands = [] if cmd == "sort" and any(w.startswith("--files0-from") for w in words) else \
            MIN_OPERANDS.get(cmd, OPERANDS[cmd][:1])
    extra = ["-f", "1"] if cmd == "cut" and not raw and not any(is_selector(w) for w in words) else []
    # dd writes to standard output unless told otherwise, and output-side options (seek=, oflag=) need a
    # file there (repair of 2026-10-28, see the header)
    if cmd == "dd" and not raw and not any(w.startswith("of=") for w in words):
        extra = ["of=out.bin"]
    return [cmd, *words, *extra, *operands]


def fixtures_for(cmd, words):
    fx = {}
    for i, w in enumerate(words):
        for ph in PLACEHOLDER.findall(w):
            opt = words[i - 1] if w == ph and i > 0 else w.split("=", 1)[0]
            fx[ph] = FIXTURE.get((cmd, opt), DEFAULT_FIXTURE.get(cmd, "file"))
    return fx


def renumber(words, n):
    """Give a second option its own placeholder files, so two options never share one."""
    return [PLACEHOLDER.sub(lambda m: m.group(0)[:-1] + str(n), w) for w in words]


def space_words(node, form, real):
    words = shlex.split(form)
    if len(words) == 1:
        for sp in spellings(node):
            if words[0].startswith(sp + "="):
                value = words[0][len(sp) + 1:]
                words = [sp] + ([value] if value else [])
                break
    if words and words[0] == node["flag"] and not real(node["flag"]):  # spelling already judged in b
        words[0] = next((s for s in spellings(node) if real(s)), words[0])
    return words


def run_jobs(jobs):
    with tempfile.TemporaryDirectory() as tmp:
        f = Path(tmp) / "jobs.json"
        f.write_text(json.dumps({"jobs": [{"id": k, **v} for k, v in jobs.items()]}))
        for src, dst in ((f, "/tmp/t019_jobs.json"), (HERE / "facts19_probe.py", "/tmp/t019_facts_probe.py")):
            subprocess.run(["limactl", "copy", str(src), f"{PROBE_VM}:{dst}"], check=True, capture_output=True)
        p = subprocess.run(["limactl", "shell", PROBE_VM, "--", "python3", "/tmp/t019_facts_probe.py",
                            "/tmp/t019_jobs.json"], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f"facts probe failed: {p.stderr[-800:]}")
    return json.loads(p.stdout)


def program_facts(cmd, files, score2, probed):
    """files: label -> syntax file path; score2: label -> binary_score() record (facts a, b, c);
    probed: probe_binary.py's output. Returns label -> {"types": {type: [right, total]}, "right",
    "total", "wrong": {type: [...]}}, and a summary of the runs."""
    real = lambda s: bool(probed["spellings"].get(s, {}).get("accepted"))  # noqa: E731
    optional = lambda s: probed["spellings"].get(s, {}).get("value") == "optional"  # noqa: E731
    grammars = {label: load_grammar(cmd, path) for label, path in files.items()}
    jobs = {}

    def job(argv, stdin=None):
        key = json.dumps([argv, stdin])
        jobs.setdefault(key, {"argv": argv, "stdin": stdin, "fixtures": fixtures_for(cmd, argv[1:])})
        return key

    # batch 1: sample values (d), "=" forms (e), flags alone, file operands (g), no-option line (h)
    plan = {}
    for label, g in grammars.items():
        for i, n in enumerate((g or {}).get("nodes", [])):
            if not n["flag"] or n["flag"] in SHORT_CIRCUIT or not any(real(s) for s in spellings(n)):
                continue
            if n["takes_value"]:
                words_list = [space_words(n, f, real) for f in sample(n["forms"])]
                # an optional value can only be given after "=" (GNU getopt_long), so write it that way
                # and a dd-style option (no leading dash) takes its value only after "=" (task 019)
                words_list = [[f"{w[0]}={w[1]}"] if len(w) == 2 and (optional(w[0]) or not w[0].startswith("-"))
                              else w for w in words_list]
                plan[(label, i, "d")] = [(job(context(cmd, w)), w) for w in words_list]
                if n["equals"]:
                    plan[(label, i, "e")] = [(job(context(cmd, shlex.split(f))), None) for f in sample(n["forms"])]
            else:
                w = [n["flag"] if real(n["flag"]) else next(s for s in spellings(n) if real(s))]
                plan[(label, i, "alone")] = [(job(context(cmd, w)), w)]
    ops = OPERANDS[cmd]
    gjobs = {"0 files": job(context(cmd, [], operands=[])), "1 file": job(context(cmd, [], operands=ops[:1])),
             "2 files": job(context(cmd, [], operands=ops)),
             "'-' is standard input": job(context(cmd, [], operands=STDIN_CHECK.get(cmd, (["-"],))[0]),
                                          stdin=STDIN_CHECK.get(cmd, (None, "a\nb\n"))[1])}
    no_options = job(context(cmd, [], raw=True))
    results = run_jobs(jobs)

    def ok(key, strict_eq=False):
        r = results[key]
        good = r["timed_out"] or r["exit"] == 0
        return good and not (strict_eq and r["eq_files"])

    # option groups across all files (a spelling and its aliases are one option)
    parent = {}

    def find(s):
        parent.setdefault(s, s)
        while parent[s] != s:
            parent[s] = parent[parent[s]]
            s = parent[s]
        return s

    for g in grammars.values():
        for n in (g or {}).get("nodes", []):
            if n["flag"]:
                for s in spellings(n)[1:]:
                    parent[find(s)] = find(n["flag"])
    group_of = lambda s: find(s)  # noqa: E731

    # one valid use per option group: a flag alone, or the first accepted sample value (files in order)
    usage = {}
    for (label, i, kind), runs in plan.items():
        if kind in ("d", "alone"):
            n = grammars[label]["nodes"][i]
            for key, words in runs:
                if ok(key) and group_of(n["flag"]) not in usage:
                    usage[group_of(n["flag"])] = words
                    break

    # batch 2: repeats (f) and pairs (h)
    jobs.clear()
    value_groups = {group_of(n["flag"]) for g in grammars.values() for n in (g or {}).get("nodes", [])
                    if n["flag"] and n["takes_value"]}
    repeat = {grp: job(context(cmd, usage[grp] + usage[grp])) for grp in usage if grp in value_groups}
    pair = {(a, b): job(context(cmd, usage[a] + renumber(usage[b], 2)))
            for a, b in combinations(sorted(usage), 2)}
    results.update(run_jobs(jobs))

    out = {}
    for label, g in grammars.items():
        if g is None:
            out[label] = {"error": "the file does not load under v1's syntax module"}
            continue
        s2 = score2[label]
        types = {"a listed": [s2["real_spellings_in_file"], s2["real_spellings_all_sources"]],
                 "b real": [s2["spellings_accepted"], s2["spellings_in_file"]],
                 "c value": [s2["value_agree"], s2["value_checked"]]}
        wrong = {"a listed": s2["real_spellings_missing"], "b real": s2["spellings_rejected"],
                 "c value": s2["value_disagreements"]}
        for kind in ("d", "e"):
            per_flag = {}
            for (lab, i, k), runs in plan.items():
                if lab == label and k == kind:
                    flag = g["nodes"][i]["flag"]
                    # no sample values at all (e.g. a minimum with no maximum) means v1 never writes the
                    # option, so the fact cannot be right
                    good = bool(runs) and all(ok(key, strict_eq=(kind == "e")) for key, _ in runs)
                    per_flag[flag] = per_flag.get(flag, True) and good
            name = {"d": "d kind", "e": "e equals"}[kind]
            types[name] = [sum(per_flag.values()), len(per_flag)]
            wrong[name] = sorted(f for f, v in per_flag.items() if not v)

        nodes = g["nodes"]
        flagged = [n for n in nodes if n["flag"]]
        in_file = {group_of(n["flag"]) for n in flagged}
        # f: repeats
        f_right = f_total = 0
        wrong["f repeat"] = []
        for grp in sorted(in_file & set(repeat)):
            prog = ok(repeat[grp])
            claims = any(n["arity"] in REPEATABLE for n in flagged if group_of(n["flag"]) == grp)
            if not prog or claims:
                f_total += 1
                if prog == claims:
                    f_right += 1
                else:
                    wrong["f repeat"].append([grp, "file: may repeat" if claims else "file: once", "program: " +
                                              ("accepts a repeat" if prog else "refuses a repeat")])
        types["f repeat"] = [f_right, f_total]
        # g: file operands
        layouts = sorted({n["syntax"] for n in nodes})
        ranges = []
        for s in layouts:
            lo = hi = 0
            for n in nodes:
                if n["syntax"] == s and not n["flag"]:
                    a, b = ARITY_RANGE.get(n["arity"], (0, math.inf))
                    lo, hi = lo + a, hi + b
            ranges.append((lo, hi))
        file_says = {"0 files": any(lo <= 0 <= hi for lo, hi in ranges),
                     "1 file": any(lo <= 1 <= hi for lo, hi in ranges),
                     "2 files": any(lo <= 2 <= hi for lo, hi in ranges),
                     "'-' is standard input": any(n["dash_as_stdin"] for n in nodes if not n["flag"])}
        g_right = sum(file_says[k] == ok(v) for k, v in gjobs.items())
        types["g files"] = [g_right, len(gjobs)]
        wrong["g files"] = [[k, f"file: {'yes' if file_says[k] else 'no'}", f"program: {'yes' if ok(v) else 'no'}"]
                            for k, v in gjobs.items() if file_says[k] != ok(v)]
        # h: rules between options, and whether no options at all is valid
        layout_groups = {s: {group_of(n["flag"]) for n in flagged if n["syntax"] == s} for s in layouts}
        h_right = h_total = 0
        wrong["h rules"] = []
        for (a, b), key in pair.items():
            if a not in in_file or b not in in_file:
                continue
            refused = not ok(key)
            values = [w for w in usage[a] + usage[b] if len(w) > 1 and not w.startswith("-")]
            if refused and any(v in results[key]["stderr"] for v in values):
                continue  # the program objects to a sample value, not to the pairing
            if refused and cmd == "convert" and not IM_COMMAND_LINE.search(results[key]["stderr"]):
                continue  # ImageMagick objects to the image, not to the command line (repair, see the header)
            forbidden = not any(a in gs and b in gs for gs in layout_groups.values())
            if refused or forbidden:
                h_total += 1
                if refused == forbidden:
                    h_right += 1
                else:
                    wrong["h rules"].append([a, b, "file forbids, program accepts" if forbidden else
                                             "program refuses, file allows: " + results[key]["stderr"][:90]])
        zero_ok_file = any(not any(n["arity"] in REQUIRED for n in flagged if n["syntax"] == s) for s in layouts)
        h_total += 1
        if zero_ok_file == ok(no_options):
            h_right += 1
        else:
            wrong["h rules"].append(["no options at all", f"file: {'valid' if zero_ok_file else 'invalid'}",
                                     f"program: {'valid' if ok(no_options) else 'invalid'}"])
        types["h rules"] = [h_right, h_total]
        out[label] = {"types": types, "right": sum(r for r, _ in types.values()),
                      "total": sum(t for _, t in types.values()), "wrong": wrong}
    return out, {"usage": {k: v for k, v in usage.items()}, "runs": len(results)}
