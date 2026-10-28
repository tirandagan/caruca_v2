#!/usr/bin/env python3
"""Caruca's refused share and time per test run, from Caruca's own generator and tracer (task 019, 3.3 c, e).

For one command, v1's curated syntax file is expanded by v1's `string_invocations` at 1 and at 2 options per
line (v1's CLI defaults otherwise: no skip list, max-arity 1, plain relations), and the lines are run by v1's
`Tracer` (parallel 10, simple stdin and content, 2-second limit per run), as `scoring/trace_usefulness.py`
does. Every traced test run is then classed by the same rule as the agent's tries
(`fig7_campaign/classify_tries.py`: refused / other non-zero / accepted / signal / unfinished / unclassified),
from the exit code and error text v1's tracer records.

v1 generates the same line more than once (memory: caruca_v1_enumeration_redundancy) and traces every copy;
each distinct line is traced once here and weighted by how many copies v1 generates, so the "as v1 runs"
shares count what v1 would actually run. At 1 option every distinct line is traced (above LIMIT1 lines, a
fixed-seed sample); at 2 options a fixed-seed sample of SAMPLE2 distinct lines (default 1,000).

Runs inside the `caruca` VM from a scratch folder (the tracer writes tracer.log into the current folder):
    cd $(mktemp -d) && ~/caruca-venv/bin/python -I <repo>/naive_llm_caruca/fig7_campaign/caruca_side/refused_share.py CMD OUT.json
"""
import collections
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

CMD, OUT = sys.argv[1], Path(sys.argv[2])
SAMPLE2 = int(os.environ.get("SAMPLE2", "1000"))
LIMIT1 = int(os.environ.get("LIMIT1", "6000"))
SEED = 19
V1_SRC = Path("/Users/tirandagan/dev/stevens/caruca/caruca/src")
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(V1_SRC))
sys.path.insert(0, str(HERE.parent))

from caruca.cli.generate import string_invocations  # noqa: E402
from caruca.tracer.tracer import Tracer  # noqa: E402
import classify_tries  # noqa: E402


if os.environ.get("KILL_WATCHDOG") == "1":
    # `kill`: v1 generates `kill -s STOP 0`, which stops the test's own process group, including the `timeout`
    # meant to end it, so v1's tracer waits forever (seen 2026-10-27). Run only in its own process namespace as
    # process 1 (refused_all.sh), where this thread sends SIGCONT to every other process every 3 s, so v1's
    # 2-second limit can end them. The lines run are unchanged; their outcomes are classed as usual.
    import signal
    import threading

    def _resume():
        while True:
            time.sleep(3)
            try:
                os.kill(-1, signal.SIGCONT)
            except OSError:
                pass
    threading.Thread(target=_resume, daemon=True).start()


def klass(rc, stderr):
    """v1 records the exit status as subprocess does: negative for a signal, None if the run timed out."""
    run = {"stderr": stderr or "", "signal": -rc if isinstance(rc, int) and rc < 0 else None,
           "exit_code": rc if isinstance(rc, int) and rc >= 0 else None}
    return classify_tries.classify(run, CMD)


def measure(k):
    invs = list(string_invocations(CMD, None, None, 1, False, k))
    copies = collections.Counter(str(i) for i in invs)
    first = {}
    for i in invs:
        first.setdefault(str(i), i)
    keys = sorted(first)
    limit = LIMIT1 if k == 1 else SAMPLE2
    chosen = keys if len(keys) <= limit else random.Random(SEED).sample(keys, limit)
    start = time.time()
    traces = Tracer(10, "simple", "simple", "").run([first[x] for x in chosen])
    secs = time.time() - start
    cls, cls_v1 = collections.Counter(), collections.Counter()
    msgs = collections.Counter()
    runs = 0
    lines_refused = 0
    for s in traces:
        w = copies[s.true_str]
        line_cls = set()
        for c in s.configs:
            runs += 1
            kc = klass(c.return_code, c.stderr)
            cls[kc] += 1
            cls_v1[kc] += w
            line_cls.add(kc)
            if kc in ("refused", "unclassified"):
                msgs[(kc, (c.stderr or "").strip().splitlines()[0][:120] if (c.stderr or "").strip() else "")] += 1
        lines_refused += line_cls == {"refused"}
    total_v1 = sum(cls_v1.values())
    return {
        "max_count": k, "generated_lines": len(invs), "distinct_lines": len(keys), "traced_lines": len(chosen),
        "sampled": len(chosen) < len(keys), "test_runs_traced": runs, "seconds": round(secs, 1),
        "seconds_per_test_run": round(secs / runs, 5) if runs else None,
        "classes": dict(cls), "refused_share": round(cls["refused"] / runs, 4) if runs else None,
        "classes_as_v1_runs": dict(cls_v1),
        "refused_share_as_v1_runs": round(cls_v1["refused"] / total_v1, 4) if total_v1 else None,
        "lines_all_runs_refused": lines_refused,
        "top_messages": [[c, m, n] for (c, m), n in msgs.most_common(12)],
    }


def version(pkg_of):
    p = subprocess.run(["dpkg", "-S", pkg_of], capture_output=True, text=True).stdout.split(":")[0]
    v = subprocess.run(["dpkg-query", "-W", "-f=${Version}", p], capture_output=True, text=True).stdout if p else ""
    return f"{p} {v}".strip()


binary = subprocess.run(["bash", "-c", f"type -P {CMD}"], capture_output=True, text=True).stdout.strip()
rec = {"command": CMD, "binary": binary, "package": version(os.path.realpath(binary)) if binary else None,
       "settings": "v1 curated syntax file; max-arity 1; plain relations; Tracer(parallel 10, stdin simple, "
                   "content simple, timeout 2 s)", "machine": "Lima VM caruca, 8 vCPU, Apple M5 Pro",
       "started": time.strftime("%Y-%m-%dT%H:%M:%S"), "kill_watchdog": os.environ.get("KILL_WATCHDOG") == "1"}
for k in (1, 2):
    try:
        rec[f"k{k}"] = measure(k)
    except Exception as e:  # one failing setting must not lose the other
        rec[f"k{k}"] = {"error": repr(e)[:400]}
rec["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
OUT.parent.mkdir(parents=True, exist_ok=True)
json.dump(rec, open(OUT, "w"), indent=1)
print(json.dumps({k: rec.get(k) for k in ("command", "package")}),
      {k: (rec[k].get("refused_share"), rec[k].get("test_runs_traced"), rec[k].get("seconds")) for k in ("k1", "k2")})
