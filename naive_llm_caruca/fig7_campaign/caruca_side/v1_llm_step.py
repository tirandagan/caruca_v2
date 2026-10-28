"""Caruca's own model step (GPT-4o via DSPy), rerun once per command through OpenRouter, with its cost
recorded (task 019, 3.3 d).

    python3 v1_llm_step.py --first3          # cut, sort, head: check the relay's figures against the key's usage
    python3 v1_llm_step.py                   # every Fig. 7 command with a bundled manual (77; skips done ones)

Runs v1's `caruca syntax-spec <cmd>` unchanged from v1's `.venv-llm` (DSPy 2.4.9, the only environment where
v1's llm.py still imports), with OPENAI_API_KEY = the OpenRouter key and OPENAI_BASE_URL pointing at a relay on
127.0.0.1 (memory: project_v1_llm_via_openrouter). The relay passes each request to OpenRouter untouched and
records the reply's id, model, token counts and time; afterwards each call's billed cost is read from
OpenRouter (`GET /api/v1/generation?id=…`), and the key's usage before and after each command is the
cross-check. DSPy's disk cache is off (DSP_CACHEBOOL=false), so every attempt reaches the model. v1 reads only
doc_sources/man/<cmd>.txt, which `uglifyjs` and `mogrify` lack. v1's checkout must be unchanged by the run
(`git status` before and after). Output: v1_llm/<cmd>.py and caruca_side/v1_llm_ledger.jsonl.
"""
import argparse
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import run_campaign as rc  # noqa: E402

V1 = os.path.expanduser("~/dev/stevens/caruca")
CARUCA = os.path.join(V1, "caruca", ".venv-llm", "bin", "caruca")
MAN = os.path.join(V1, "caruca", "src", "caruca", "doc_sources", "man")
OUTDIR = os.path.join(os.path.dirname(HERE), "v1_llm")
LEDGER = os.path.join(HERE, "v1_llm_ledger.jsonl")
UPSTREAM = "https://openrouter.ai/api"
CALLS = []


class Relay(http.server.BaseHTTPRequestHandler):
    current = None

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        url = UPSTREAM + self.path            # /v1/chat/completions -> https://openrouter.ai/api/v1/chat/completions
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Authorization": self.headers.get("Authorization", ""), "Content-Type": "application/json"})
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                status, data = r.status, r.read()
        except urllib.error.HTTPError as e:
            status, data = e.code, e.read()
        rec = {"command": Relay.current, "status": status, "seconds": round(time.time() - t0, 2),
               "request_bytes": len(body)}
        try:
            d = json.loads(data)
            rec.update(id=d.get("id"), model=d.get("model"), usage=d.get("usage"),
                       error=(d.get("error") or {}).get("message") if isinstance(d.get("error"), dict) else None)
        except ValueError:
            rec["error"] = data[:200].decode("utf-8", "replace")
        CALLS.append(rec)
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *a):
        pass


def generation_cost(k, gid):
    for _ in range(12):
        try:
            req = urllib.request.Request(f"https://openrouter.ai/api/v1/generation?id={gid}",
                                         headers={"Authorization": f"Bearer {k}"})
            d = json.load(urllib.request.urlopen(req, timeout=30))["data"]
            return {"total_cost": d.get("total_cost"), "native_tokens_prompt": d.get("native_tokens_prompt"),
                    "native_tokens_completion": d.get("native_tokens_completion"),
                    "tokens_prompt": d.get("tokens_prompt"), "tokens_completion": d.get("tokens_completion"),
                    "provider": d.get("provider_name"), "model": d.get("model")}
        except (urllib.error.HTTPError, KeyError, ValueError):
            time.sleep(5)
    return None


def git_status():
    return subprocess.run(["git", "-C", V1, "status", "--porcelain"], capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--first3", action="store_true")
    ap.add_argument("--ceiling", type=float, default=150.0)
    ap.add_argument("--no-key-check", action="store_true",
                    help="skip the key-usage cross-check (OpenRouter's counter lags about a minute per command); "
                         "the per-call bill from the generation endpoint is still recorded. Used after --first3 "
                         "matched it exactly for cut, sort and head (2026-10-27)")
    args = ap.parse_args()
    k = rc.key()
    st = rc.state(k)
    cmds = ["cut", "sort", "head"] if args.first3 else [r["command"] for r in rc.commands()]
    done = set()                         # a command is done only if v1 exited 0 and every call succeeded
    if os.path.exists(LEDGER):
        for l in open(LEDGER):
            r = json.loads(l)
            if r["exit"] == 0 and r["calls"] and all(x.get("status") == 200 for x in r["call_records"]):
                done.add(r["command"])
    os.makedirs(OUTDIR, exist_ok=True)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Relay)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}/v1"
    g0 = git_status()
    for c in cmds:
        if c in done:
            print(f"skip {c}: in the ledger"); continue
        if not os.path.exists(os.path.join(MAN, c + ".txt")):
            print(f"skip {c}: v1 has no bundled manual for it"); continue
        spent = rc.usage(k, stable=False) - st["zero_usage"]
        if spent + 1.0 > args.ceiling:
            print(f"STOP: spent ${spent:.2f}"); break
        Relay.current = c
        n0 = len(CALLS)
        before = None if args.no_key_check else rc.usage(k)
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ, OPENAI_API_KEY=k, OPENAI_BASE_URL=base, DSP_CACHEBOOL="false",
                       DSP_CACHEDIR=os.path.join(tmp, "dspcache"))
            t0 = time.time()
            p = subprocess.run([CARUCA, "syntax-spec", c], cwd=tmp, env=env, capture_output=True, text=True, timeout=900)
            wall = time.time() - t0
        calls = CALLS[n0:]
        for x in calls:
            if x.get("id"):
                x["generation"] = generation_cost(k, x["id"])
        after = None if args.no_key_check else rc.usage_after(
            k, before, sum((x.get("generation") or {}).get("total_cost") or 0 for x in calls))
        code = p.stdout
        out = os.path.join(OUTDIR, c + ".py")
        if code.strip():
            open(out, "w").write(code)
        try:
            compile(code, out, "exec"); parses = True
        except SyntaxError:
            parses = False
        rec = {"command": c, "exit": p.returncode, "wall_s": round(wall, 1), "calls": len(calls),
               "billed_usd": round(sum((x.get("generation") or {}).get("total_cost") or 0 for x in calls), 6),
               "key_usage_delta_usd": None if after is None else round(after - before, 6),
               "prompt_tokens": sum(((x.get("usage") or {}).get("prompt_tokens") or 0) for x in calls),
               "completion_tokens": sum(((x.get("usage") or {}).get("completion_tokens") or 0) for x in calls),
               "models": sorted({x.get("model") or "" for x in calls}),
               "output_lines": len(code.splitlines()), "parses": parses,
               "defines_spec": f"{c}_syntax_spec" in code,
               "stderr_tail": [l for l in p.stderr.splitlines() if "sk-or" not in l][-3:],
               "call_records": [{kk: x.get(kk) for kk in ("status", "seconds", "id", "model", "usage", "generation", "error")}
                                for x in calls],
               "date": time.strftime("%Y-%m-%dT%H:%M:%S")}
        with open(LEDGER, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(f"{c}: {rec['calls']} call(s), billed ${rec['billed_usd']:.4f} (key delta {rec['key_usage_delta_usd']}), "
              f"{rec['wall_s']:.0f} s, {rec['output_lines']} lines, parses {parses}", flush=True)
        if git_status() != g0:
            print("STOP: v1's checkout changed during the run"); break
        if any(x.get("status") in (401, 402) for x in calls):
            print("STOP: billing error from OpenRouter"); break
    srv.shutdown()


if __name__ == "__main__":
    main()
