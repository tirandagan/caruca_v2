#!/usr/bin/env python3
"""E0 redundancy sweep: --number hint vs emitted vs unique lines, v1 defaults, all commands."""
import csv, subprocess, sys, time
from pathlib import Path

CARUCA = str(Path.home() / "dev/stevens/caruca/caruca/.venv/bin/caruca")
MAN = Path.home() / "dev/stevens/caruca/caruca/src/caruca/doc_sources/man"
OUT = sys.argv[1]
CAP = 500_000  # line cap for emission counting

with open(OUT, "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["command", "number_hint", "emitted_lines", "unique_lines",
                "truncated", "number_secs", "emit_secs", "error"])
    for f in sorted(MAN.glob("*.txt")):
        cmd = f.stem
        t0 = time.time()
        try:
            r = subprocess.run([CARUCA, "generate", cmd, "--number"],
                               capture_output=True, text=True, timeout=90)
            hint = r.stdout.strip().splitlines()[-1].strip() if r.stdout.strip() else ""
            int(hint)
        except subprocess.TimeoutExpired:
            w.writerow([cmd, "", "", "", "", round(time.time()-t0, 1), "", "number_timeout"]); fh.flush(); continue
        except (ValueError, IndexError):
            w.writerow([cmd, "", "", "", "", round(time.time()-t0, 1), "",
                        f"number_unparseable_rc{r.returncode}"]); fh.flush(); continue
        t1 = time.time()
        emitted = 0; uniq = set(); trunc = "no"; err = ""
        try:
            p = subprocess.Popen([CARUCA, "generate", cmd], stdout=subprocess.PIPE,
                                 stderr=subprocess.DEVNULL, text=True)
            deadline = time.time() + 300
            for line in p.stdout:
                emitted += 1
                if len(uniq) < CAP:
                    uniq.add(line)
                if emitted >= CAP or time.time() > deadline:
                    trunc = "yes"; p.kill(); break
            p.wait(timeout=10)
        except Exception as e:
            err = f"emit_{type(e).__name__}"
        w.writerow([cmd, hint, emitted, len(uniq), trunc,
                    round(t1-t0, 1), round(time.time()-t1, 1), err])
        fh.flush()
print("SWEEP DONE")
