#!/usr/bin/env python3
"""Run a batch of command lines for the program-checked facts (inside the probe VM; standard library).

Task 019 copy of naive_llm_caruca/scoring/facts_probe.py (2026-10-28): adds `in.ppm`/`in2.ppm`, a 2x2 image
ImageMagick reads, to every folder, and an "image" fixture kind (the same image), for convert.

    python3 facts_probe.py jobs.json > results.json

jobs.json: {"jobs": [{"id", "argv": [...], "stdin": str|null, "fixtures": {"relpath_1": kind, ...}}]}
Each job runs once in a fresh empty folder holding `in.txt`, `in2.txt` ("a\nb\n", sorted, so `sort
--check` passes), `target`, `target2` and, for binwalk, `target.bin`/`target2.bin` (a gzip stream holding
a tar archive, so binwalk has something to find). Placeholder words `relpath_1`/`abspath_1` (v1's path
names) get a fixture: "file" (text), "dir", "files0" (a NUL-terminated list naming in.txt), "random"
(4 KiB of random bytes) or "absent". `abspath_1` is rewritten to the absolute path. LC_ALL=C, 10-second
limit, 4 jobs at a time. Recorded: exit status, the first 300 characters of stderr, whether it timed
out, and any new file whose name starts with "=" (the sign of a value written after "=" being taken as
a file name, e.g. `sort -o=x`).
"""
import gzip, io, json, os, re, shutil, subprocess, sys, tarfile, tempfile
from concurrent.futures import ThreadPoolExecutor

JOBS = json.load(open(sys.argv[1]))["jobs"]
ENV = {"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": os.environ.get("HOME", "/tmp")}


def binwalk_sample():
    tar_bytes = io.BytesIO()
    with tarfile.open(fileobj=tar_bytes, mode="w") as tar:
        data = b"hello from a tar member\n" * 20
        info = tarfile.TarInfo("member.txt")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    return b"\x00" * 64 + gzip.compress(tar_bytes.getvalue()) + b"\x00" * 64


SAMPLE = binwalk_sample()


PPM = "P3\n2 2\n255\n0 0 0 255 255 255 0 0 0 255 255 255\n"


def fixture(path, kind):
    if kind == "image":
        open(path, "w").write(PPM)
    elif kind == "dir":
        os.mkdir(path)
    elif kind == "files0":
        open(path, "wb").write(b"in.txt\0")
    elif kind == "random":
        open(path, "wb").write(os.urandom(4096))
    elif kind == "file":
        open(path, "w").write("a\nb\n")


def run(job):
    d = tempfile.mkdtemp(prefix="t018facts.")
    try:
        for name in ("in.txt", "in2.txt"):
            open(os.path.join(d, name), "w").write("a\nb\n")
        for name in ("target", "target2"):
            open(os.path.join(d, name), "w").write("x\n")
        for name in ("target.bin", "target2.bin"):
            open(os.path.join(d, name), "wb").write(SAMPLE)
        for name in ("in.ppm", "in2.ppm"):
            open(os.path.join(d, name), "w").write(PPM)
        for ph, kind in (job.get("fixtures") or {}).items():
            fixture(os.path.join(d, ph), kind)
        before = set(os.listdir(d))
        argv = [re.sub(r"abspath_\d+", lambda m: os.path.join(d, m.group(0)), w) for w in job["argv"]]
        try:
            p = subprocess.run(argv, cwd=d, env=ENV, input=(job.get("stdin") or "").encode(),
                               capture_output=True, timeout=10)
            res = {"exit": p.returncode, "stderr": p.stderr.decode(errors="replace").strip()[:300],
                   "timed_out": False}
        except subprocess.TimeoutExpired:
            res = {"exit": None, "stderr": "", "timed_out": True}
        res["eq_files"] = sorted(f for f in set(os.listdir(d)) - before if f.startswith("="))
        return job["id"], res
    finally:
        shutil.rmtree(d, ignore_errors=True)


with ThreadPoolExecutor(4) as pool:
    results = dict(pool.map(run, JOBS))
json.dump(results, sys.stdout)
