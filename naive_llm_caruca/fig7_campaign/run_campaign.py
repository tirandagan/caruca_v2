"""Batch driver for task 019: run the naive agent on Fig. 7's commands one at a time, billed through OpenRouter,
and keep the cost of every run and of the whole campaign (ai_docs/tasks/019_fig7_commands_naive_campaign.md).

    python3 run_campaign.py --pilot                  # dd ls cut test convert, then stop for Tiran
    python3 run_campaign.py --main                   # the other 74, in Fig. 7 order
    python3 run_campaign.py --repeats                # head cut dd cp sort, twice more each, while the budget allows
    python3 run_campaign.py --commands cut,sort      # any list
    python3 run_campaign.py --costs                  # only rewrite costs.md from the ledger
    options: --model ID (default anthropic/claude-fable-5.1)  --dry-run  --cap 8  --ceiling 150

For each command: refuse to start if money spent + the per-session cap would pass the ceiling; make a clone
of naive-golden (new_run_vm.sh); hand it the billing file; read the key's OpenRouter usage; run naive-run with
a wall-clock limit; read usage again; collect the run (collect_run.sh, which scans for the key and deletes the
clone); classify its tries (classify_tries.py); append a line to ledger.jsonl; rewrite costs.md. Commands
already in the ledger are skipped, so a stopped batch resumes where it stopped. Stops on billing or model
errors. After the pilot and every 20 runs it re-projects the total and stops if the projection passes the
ceiling. The key is read from the repo's .env and never printed or written to the repo.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ARM = os.path.dirname(HERE)
REPO = os.path.dirname(ARM)
LEDGER = os.path.join(HERE, "ledger.jsonl")
STATE = os.path.join(HERE, "campaign_state.json")
COSTS = os.path.join(HERE, "costs.md")
TRIES = os.path.join(HERE, "tries")
PILOT = ["dd", "ls", "cut", "test", "convert"]
REPEATS = ["head", "cut", "dd", "cp", "sort"]
WALL_LIMIT = 90 * 60          # seconds; the cost cap normally ends a long session first


def key():
    for ln in open(os.path.join(REPO, ".env")):
        if ln.startswith("OPENROUTER_API_KEY="):
            return ln.split("=", 1)[1].strip().strip("\"'")
    sys.exit("no OPENROUTER_API_KEY in .env")


def usage(k, stable=True):
    """The key's cumulative OpenRouter usage in dollars; with stable, read until two readings 10 s apart agree."""
    def once():
        req = urllib.request.Request("https://openrouter.ai/api/v1/key", headers={"Authorization": f"Bearer {k}"})
        return float(json.load(urllib.request.urlopen(req, timeout=30))["data"]["usage"])
    last = once()
    if not stable:
        return last
    for _ in range(12):
        time.sleep(10)
        now = once()
        if abs(now - last) < 1e-6:
            return now
        last = now
    return last


def usage_after(k, before, expect=None, max_wait=300):
    """The key's usage once a session's charge has arrived. OpenRouter's counter lags: the $0.30 smoke test
    showed up 60-80 s after the session ended (2026-10-27), and two equal readings 10 s apart were both still
    $0. So wait until the counter has moved by at least half the expected cost (Claude Code's own figure), or
    max_wait seconds, then until two readings 30 s apart agree."""
    t0 = time.time()
    last = usage(k, stable=False)
    while time.time() - t0 < max_wait and last - before < 0.5 * (expect or 0.01):
        time.sleep(15)
        last = usage(k, stable=False)
    while time.time() - t0 < max_wait + 300:
        time.sleep(30)
        now = usage(k, stable=False)
        if abs(now - last) < 1e-6:
            return now
        last = now
    return last


def commands():
    rows = []
    for ln in open(os.path.join(HERE, "commands.txt")):
        if ln.startswith("#") or not ln.strip():
            continue
        c, g, ex, tool, opts, est = ln.rstrip("\n").split("\t")
        rows.append({"command": c, "group": g, "example": ex == "1", "tool": tool == "1", "estimate": float(est)})
    return rows


def ledger():
    return [json.loads(l) for l in open(LEDGER)] if os.path.exists(LEDGER) else []


def state(k):
    if os.path.exists(STATE):
        return json.load(open(STATE))
    st = {"zero_usage": usage(k), "created": datetime.datetime.now().isoformat(timespec="seconds"),
          "note": "OpenRouter usage of the key when the campaign began; spent = usage now - zero_usage"}
    json.dump(st, open(STATE, "w"), indent=1)
    return st


def sh(cmd, timeout=None, log=None):
    with open(log, "a") if log else open(os.devnull, "w") as out:
        p = subprocess.run(cmd, shell=isinstance(cmd, str), stdout=out if log else subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True, timeout=timeout)
    return p


def result_event(folder):
    """The session's final event from stream.jsonl (cost, tokens, durations, models used)."""
    res, toks = None, {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
    seen = {}
    p = os.path.join(folder, "stream.jsonl")
    if not os.path.exists(p):
        return None, toks
    for ln in open(p, encoding="utf-8", errors="replace"):
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue
        if r.get("type") == "result":
            res = r
        m = r.get("message") if isinstance(r.get("message"), dict) else None
        if r.get("type") == "assistant" and m and isinstance(m.get("usage"), dict):
            seen[m.get("id") or len(seen)] = m["usage"]
    for u in seen.values():
        toks["input"] += u.get("input_tokens", 0)
        toks["output"] += u.get("output_tokens", 0)
        toks["cache_read"] += u.get("cache_read_input_tokens", 0)
        toks["cache_write"] += u.get("cache_creation_input_tokens", 0)
    return res, toks


def run_env(folder):
    out = {}
    for ln in open(os.path.join(folder, "run.env"), encoding="utf-8", errors="replace"):
        if "=" in ln:
            a, b = ln.rstrip("\n").split("=", 1)
            out.setdefault(a, b)
    return out


def projection(rows, done, ceiling, spent):
    """Money spent plus every remaining command's estimate, scaled by actual/estimate so far."""
    est = {r["command"]: r["estimate"] for r in rows}
    fin = [d for d in done if d.get("status") in ("ok", "capped") and d.get("billed_usd") is not None]
    ratio = (sum(d["billed_usd"] for d in fin) / sum(est.get(d["command"], 1.5) for d in fin)) if fin else 1.0
    left = [r for r in rows if not any(d["command"] == r["command"] and d.get("repeat", 1) == 1
                                       and d.get("status") in ("ok", "capped") for d in done)]
    return spent + ratio * sum(r["estimate"] for r in left), ratio, len(left)


def write_costs(rows, ceiling, spent=None):
    done = ledger()
    est = {r["command"]: r for r in rows}
    lines = ["# Task 019: cost of every run, and of the campaign", "",
             f"Rewritten after every run by `run_campaign.py` ({datetime.datetime.now():%Y-%m-%d %H:%M}). "
             f"Budget: target $120, ceiling ${ceiling:.0f}. **Billed** is OpenRouter's own usage counter for the key, "
             "read before and after each session; *Claude Code's figure* is the session's own estimate, kept for "
             "comparison with runs 3 to 10. Times are the session's wall clock.", "",
             "| # | Command | Group | Run | Status | Estimate | **Billed** | Claude Code's figure | Input / output / cache read / cache write tokens | Wall time | Turns |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    tot = 0.0
    for i, d in enumerate(done, 1):
        r = est.get(d["command"], {})
        b = d.get("billed_usd")
        tot += b or 0
        t = d.get("tokens") or {}
        lines.append(f"| {i} | `{d['command']}` | {r.get('group', '')}{' (example)' if r.get('example') else ''} | "
                     f"{d.get('repeat', 1)} | {d.get('status')} | ${r.get('estimate', 0):.2f} | "
                     f"**{'$%.2f' % b if b is not None else '?'}** | "
                     f"{'$%.2f' % d['claude_cost_usd'] if d.get('claude_cost_usd') is not None else ''} | "
                     f"{t.get('input', 0):,} / {t.get('output', 0):,} / {t.get('cache_read', 0):,} / {t.get('cache_write', 0):,} | "
                     f"{d.get('wall_s', 0):.0f} s | {d.get('turns', '')} |")
    other = []
    v1p = os.path.join(HERE, "caruca_side", "v1_llm_ledger.jsonl")
    v1 = [json.loads(l) for l in open(v1p)] if os.path.exists(v1p) else []
    v1tot = sum(x.get("billed_usd") or 0 for x in v1)
    smoke = os.path.join(HERE, "smoke_test.json")
    sm = json.load(open(smoke)).get("billed_usd", 0) if os.path.exists(smoke) else 0
    unrec = json.load(open(STATE)).get("unrecorded_charges", []) if os.path.exists(STATE) else []
    unrec_tot = sum(u["usd"] for u in unrec)
    lines += ["", "| Total | Money |", "|---|---|",
              f"| Agent sessions ({len(done)} runs) | **${tot:.2f}** |",
              f"| Caruca's model step ({len(v1)} commands) | ${v1tot:.2f} |",
              f"| Smoke test | ${sm:.2f} |",
              f"| Charges billed but not recorded by a run ({'; '.join(u['what'][:60] for u in unrec) or 'none'}) | ${unrec_tot:.2f} |",
              f"| **All billed** (sum of the rows above) | **${tot + v1tot + sm + unrec_tot:.2f}** |"]
    if spent is not None:
        proj, ratio, left = projection(rows, done, ceiling, spent)
        lines += [f"| OpenRouter's counter since the campaign began | ${spent:.2f} |",
                  f"| Left before the ${ceiling:.0f} ceiling | ${ceiling - spent:.2f} |",
                  f"| Projected total for the 79 commands (actual/estimate so far: {ratio:.2f}; {left} not yet run) | ${proj:.2f} |"]
    open(COSTS, "w").write("\n".join(lines) + "\n")


def one(row, repeat, args, k, st):
    c = row["command"]
    name = f"naive-run-{c}" + (f"-r{repeat}" if repeat > 1 else "")
    log = os.path.join(HERE, "logs", f"{datetime.datetime.now():%Y%m%d_%H%M%S}_{name}.log")
    os.makedirs(os.path.dirname(log), exist_ok=True)
    rec = {"command": c, "repeat": repeat, "clone": name, "started_driver": datetime.datetime.now().isoformat(timespec="seconds")}
    if args.dry_run:
        print(f"[dry-run] would run {c} (repeat {repeat}) in {name}")
        return None
    t0 = time.time()
    p = sh([os.path.join(ARM, "new_run_vm.sh"), name], log=log)
    if p.returncode:
        rec.update(status="error", error="new_run_vm.sh failed")
        return rec
    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        os.chmod(f.name, 0o600)
        f.write(f"OPENROUTER_KEY={k}\nMODEL={args.model}\nEFFORT=medium\nCOST_CAP={args.cap}\n")
    try:
        sh(["limactl", "copy", f.name, f"{name}:~/.naive-billing"], log=log)
    finally:
        os.unlink(f.name)
    sh(["limactl", "shell", name, "--", "bash", "-lc", "chmod 600 ~/.naive-billing; ls ~/.naive-billing"], log=log)
    before = usage(k)
    rec["overhead_before_s"] = round(time.time() - t0, 1)
    # was the caruca VM measuring Caruca's side meanwhile? (it shares the Mac's processors)
    busy = subprocess.run(["limactl", "shell", "caruca", "--", "pgrep", "-fc", "refused_share.py"],
                          capture_output=True, text=True)
    rec["caruca_vm_busy"] = busy.returncode == 0 and busy.stdout.strip() not in ("", "0")
    try:
        p = sh(["limactl", "shell", name, "--", "bash", "-lc", f"cd ~/naive-arm && ~/bin/naive-run -y {c} PROMPT_v1.md"],
               timeout=WALL_LIMIT, log=log)
        rec["naive_run_exit"] = p.returncode
    except subprocess.TimeoutExpired:
        sh(["limactl", "shell", name, "--", "bash", "-lc", "pkill -TERM -x claude"], log=log)
        time.sleep(20)
        rec["naive_run_exit"] = "timeout"
    t1 = time.time()
    out = subprocess.run([os.path.join(ARM, "collect_run.sh"), name], capture_output=True, text=True)
    open(log, "a").write(out.stdout + out.stderr)
    m = re.findall(r"collected runs/([^:]+):", out.stdout)
    rec["overhead_after_s"] = round(time.time() - t1, 1)
    if not m:
        rec.update(status="error", error="nothing collected")
        return rec
    folder = os.path.join(ARM, "runs", m[-1])
    rec["run_folder"] = os.path.relpath(folder, REPO)
    rec["key_redacted"] = os.path.exists(os.path.join(folder, "KEY_REDACTED.txt"))
    e = run_env(folder)
    res, toks = result_event(folder)
    after = usage_after(k, before, (res or {}).get("total_cost_usd"))
    rec["billed_usd"] = round(after - before, 6)
    rec.update(model=e.get("model"), effort=e.get("effort"), package=e.get("package"), logger=e.get("logger"),
               audit_lost=e.get("audit_lost"), tokens=toks)
    try:
        st0 = datetime.datetime.fromisoformat(e["started"]); st1 = datetime.datetime.fromisoformat(e["finished"])
        rec["wall_s"] = (st1 - st0).total_seconds()
    except (KeyError, ValueError):
        pass
    if res:
        rec.update(claude_cost_usd=res.get("total_cost_usd"), duration_ms=res.get("duration_ms"),
                   duration_api_ms=res.get("duration_api_ms"), turns=res.get("num_turns"),
                   is_error=res.get("is_error"), subtype=res.get("subtype"),
                   models_used=sorted((res.get("modelUsage") or {}).keys()),
                   result_text=str(res.get("result", ""))[:300])
    capped = "cost cap reached" in open(os.path.join(folder, "stream.actions.log"), errors="replace").read() \
        if os.path.exists(os.path.join(folder, "stream.actions.log")) else False
    txt = (rec.get("result_text") or "") + open(log, errors="replace").read()[-4000:]
    if re.search(r"402|[Ii]nsufficient credits|401|[Uu]nauthori[sz]ed|invalid api key|No endpoints found|model .* not (found|available)", txt) and not res:
        rec["status"] = "billing_or_model_error"
    elif rec.get("naive_run_exit") in (2, 3, 4):
        rec["status"] = "error"
    elif capped:
        rec["status"] = "capped"
    elif rec.get("naive_run_exit") == "timeout":
        rec["status"] = "timeout"
    elif res and not res.get("is_error"):
        rec["status"] = "ok"
    else:
        rec["status"] = "error"
    try:
        os.makedirs(TRIES, exist_ok=True)
        sys.path.insert(0, HERE)
        import classify_tries
        rec["tries"] = classify_tries.main(folder, os.path.join(TRIES, os.path.basename(folder) + ".json"))
    except Exception as ex:  # a classification failure must not lose the run's cost record
        rec["tries_error"] = repr(ex)[:300]
    return rec


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pilot", action="store_true"); g.add_argument("--main", action="store_true")
    g.add_argument("--repeats", action="store_true"); g.add_argument("--commands"); g.add_argument("--costs", action="store_true")
    ap.add_argument("--model", default="anthropic/claude-fable-5.1")
    ap.add_argument("--cap", type=float, default=8.0)
    ap.add_argument("--ceiling", type=float, default=150.0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    rows = commands()
    k = key()
    if args.costs:
        st = state(k)
        write_costs(rows, args.ceiling, usage(k, stable=False) - st["zero_usage"])
        print(open(COSTS).read())
        return
    caf = subprocess.Popen(["caffeinate", "-ims", "-w", str(os.getpid())])
    by = {r["command"]: r for r in rows}
    if args.pilot:
        plan = [(by[c], 1) for c in PILOT]
    elif args.main:
        plan = [(r, 1) for r in rows if r["command"] not in PILOT]
    elif args.repeats:
        plan = [(by[c], n) for n in (2, 3) for c in REPEATS]
    else:
        plan = [(by[c], 1) for c in args.commands.split(",")]
    st = state(k)
    since_check = 0
    for row, rep in plan:
        done = ledger()
        if any(d["command"] == row["command"] and d.get("repeat", 1) == rep and d.get("status") in ("ok", "capped")
               for d in done):
            print(f"skip {row['command']} (repeat {rep}): already in the ledger")
            continue
        spent = usage(k, stable=False) - st["zero_usage"]
        if spent + args.cap > args.ceiling:
            print(f"STOP: spent ${spent:.2f}; one more session could pass the ${args.ceiling:.0f} ceiling")
            break
        if args.repeats:
            nxt = 1.0 * row["estimate"]
            proj, ratio, _ = projection(rows, done, args.ceiling, spent)
            if spent + ratio * nxt > args.ceiling or proj > args.ceiling:
                print(f"STOP: repeats would pass the ceiling (spent ${spent:.2f}, next about ${ratio * nxt:.2f})")
                break
        print(f"== {row['command']} (repeat {rep}); spent so far ${spent:.2f}", flush=True)
        rec = one(row, rep, args, k, st)
        if rec is None:
            continue
        with open(LEDGER, "a") as f:
            f.write(json.dumps(rec) + "\n")
        spent = usage(k, stable=False) - st["zero_usage"]
        write_costs(rows, args.ceiling, spent)
        tr = rec.get("tries") or {}
        print(f"   {rec['status']}: billed ${rec.get('billed_usd', 0):.2f}, {rec.get('wall_s', 0):.0f} s, "
              f"tries {tr.get('tries')}, refused {tr.get('classes', {}).get('refused', 0)}; total spent ${spent:.2f}", flush=True)
        if rec["status"] == "billing_or_model_error":
            print("STOP: billing or model error; see the run's log"); break
        since_check += 1
        if not args.repeats and since_check >= 20:
            since_check = 0
            proj, ratio, left = projection(rows, ledger(), args.ceiling, spent)
            print(f"   checkpoint: projected total ${proj:.2f} (ratio {ratio:.2f}, {left} left)")
            if proj > args.ceiling:
                print("STOP: the projection passes the ceiling; ask Tiran"); break
    if args.pilot:
        proj, ratio, left = projection(rows, ledger(), args.ceiling, usage(k, stable=False) - st["zero_usage"])
        print(f"pilot done: projected total for the 79 ${proj:.2f} (actual/estimate {ratio:.2f}); report to Tiran before --main")
    caf.terminate()


if __name__ == "__main__":
    main()
