#!/usr/bin/env python3
"""Render Claude Code's stream-json output live, and keep both the raw stream and the rendering.

    claude -p "..." --output-format stream-json --verbose | naive-watch.py runs/<tag>.jsonl

Writes every raw event line to <tag>.jsonl, prints the actions to the terminal as they happen, and
writes the same text to <tag>.actions.log. Shown: the session setup, the assistant's visible text,
each tool call (name and input), each tool result (truncated), the final totals. Not shown: thinking.

Cost cap (task 019): with NAIVE_COST_CAP set (dollars), the session's running cost is estimated from each
assistant message's token usage at the NAIVE_PRICE_* rates (dollars per million tokens; defaults are
OpenRouter's Fable 5.1 prices, 2026-10-27), and the session is stopped (SIGTERM to every process named
`claude`) once the estimate passes the cap. The line "cost cap reached" in the log marks a stopped run.
Since 2026-10-28 the defaults follow the session's model (from its first event): Opus 5.5 sessions are
priced at Opus 5.5's rates, so the cap means about the same money for either model. The estimate still runs
low, since the stream shows only part of each message's output tokens (about half of Fable's bill).
"""
import json, os, subprocess, sys, datetime

RAW = open(sys.argv[1], "a", encoding="utf-8")
ACT = open(sys.argv[1].rsplit(".", 1)[0] + ".actions.log", "a", encoding="utf-8")
MAXRES = int(sys.argv[2]) if len(sys.argv) > 2 else 600
CAP = float(os.environ["NAIVE_COST_CAP"]) if os.environ.get("NAIVE_COST_CAP") else None
# OpenRouter's prices, dollars per million tokens (read 2026-10-28)
MODEL_PRICES = {"anthropic/claude-fable-5.1": {"input": 10.0, "output": 50.0, "cache_read": 0.25, "cache_write": 12.5},
                "anthropic/claude-opus-5.5": {"input": 4.0, "output": 20.0, "cache_read": 0.20, "cache_write": 5.0}}
PRICE = {k: float(os.environ.get(f"NAIVE_PRICE_{k.upper()}", v)) for k, v in
         MODEL_PRICES["anthropic/claude-fable-5.1"].items()}
usage_by_msg, capped = {}, False


def running_cost():
    t = 0.0
    for u in usage_by_msg.values():
        t += (u.get("input_tokens", 0) * PRICE["input"] + u.get("output_tokens", 0) * PRICE["output"]
              + u.get("cache_read_input_tokens", 0) * PRICE["cache_read"]
              + u.get("cache_creation_input_tokens", 0) * PRICE["cache_write"]) / 1e6
    return t

def say(s=""):
    print(s, flush=True); ACT.write(s + "\n"); ACT.flush()

def now():
    return datetime.datetime.now().strftime("%H:%M:%S")

def one_line(v, n):
    v = str(v).replace("\r", "").replace("\n", " ⏎ ")
    return v if len(v) <= n else v[:n] + f" …[{len(v)} chars]"

def show_input(name, inp):
    if not isinstance(inp, dict):
        return one_line(inp, 400)
    if name == "Bash" and "command" in inp:
        return inp["command"]
    parts = []
    for k, v in inp.items():
        if k in ("content", "new_string", "old_string"):
            parts.append(f"{k}=<{len(str(v))} chars>")
        else:
            parts.append(f"{k}={one_line(v, 200)}")
    return "  ".join(parts)

n = 0
for line in sys.stdin:
    RAW.write(line); RAW.flush()
    line = line.strip()
    if not line:
        continue
    try:
        r = json.loads(line)
    except json.JSONDecodeError:
        continue
    t = r.get("type")
    if t == "system" and r.get("subtype") == "init":
        for k, v in MODEL_PRICES.get(r.get("model"), {}).items():
            if f"NAIVE_PRICE_{k.upper()}" not in os.environ:
                PRICE[k] = v
        say(f"[{now()}] session {r.get('session_id','')}  model={r.get('model')}  permission_mode={r.get('permissionMode')}  cwd={r.get('cwd')}")
        say(f"           tools: {', '.join(r.get('tools', []))}")
        continue
    m = r.get("message") if isinstance(r.get("message"), dict) else None
    content = m.get("content") if m else None
    if t == "assistant" and m and isinstance(m.get("usage"), dict):
        usage_by_msg[m.get("id") or len(usage_by_msg)] = m["usage"]   # one message can arrive in several events
        if CAP is not None and not capped and running_cost() > CAP:
            capped = True
            say(f"[{now()}] cost cap reached: estimated ${running_cost():.2f} > ${CAP:.2f}; stopping the session")
            subprocess.run(["pkill", "-TERM", "-x", "claude"])
    if t == "assistant" and isinstance(content, list):
        for b in content:
            bt = b.get("type")
            if bt == "text" and b.get("text", "").strip():
                say(f"[{now()}] claude: {b['text'].strip()}")
            elif bt == "tool_use":
                n += 1
                say(f"[{now()}] #{n} ▶ {b.get('name')}: {show_input(b.get('name'), b.get('input'))}")
    elif t == "user" and isinstance(content, list):
        for b in content:
            if b.get("type") == "tool_result":
                c = b.get("content")
                if isinstance(c, list):
                    c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                tag = "✗ error" if b.get("is_error") else "◀"
                say(f"           {tag} {one_line(c if c is not None else '', MAXRES)}")
    elif t == "result":
        u = r.get("usage", {})
        say(f"[{now()}] done: turns={r.get('num_turns')}  duration={round((r.get('duration_ms') or 0)/1000)}s  "
            f"cost=${r.get('total_cost_usd')}  in={u.get('input_tokens')} out={u.get('output_tokens')}  "
            f"cache_read={u.get('cache_read_input_tokens')}  error={r.get('is_error')}  tool_calls={n}  "
            f"estimate=${running_cost():.2f}")
        if r.get("is_error") or r.get("subtype") not in (None, "success"):
            say(f"           subtype={r.get('subtype')}  {one_line(r.get('result',''), 400)}")
if capped:
    say(f"[{now()}] stopped at the cost cap; estimated ${running_cost():.2f}")
