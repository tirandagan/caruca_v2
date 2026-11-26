#!/usr/bin/env python3
"""Draw the three evidence figures of the report, for the pilot (`spell`) or for the full run (86 scripts).

    uv run --with matplotlib==3.9.2 python figures_interim/make_figures_interim.py            # the pilot
    uv run --with matplotlib==3.9.2 python figures_interim/make_figures_interim.py \
        --records full_run --numbers numbers_full.json --out figures_full                     # the full run

Pilot (the default): reads validation_2026-11-24/occurrences.jsonl, results.jsonl and regions.jsonl (the
records numbers_pilot.json was counted from) and writes split_map.png, time_bars.png and uses_split.png
next to this script. Full run: reads full_run/'s occurrences.jsonl.gz and results.jsonl.gz and writes the
same three names into --out, drawn for 86 scripts (per command gains and losses; time against PaSh's own
files per script; command uses split), with the naive LLM's second sed file as a fifth series where a
figure is per source; plus setup_diagram.png (Figure 3, column width) and a5_scripts.png (addendum A5:
every script's time ÷ bash time, parts split and crashes, one page). Portrait page width (6.5 in), text 8 pt or larger, 300 dpi. Counts only what the
records hold; checks its counts against the numbers json and stops on a mismatch.
"""
import argparse
import gzip
import json
import math
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
_ap = argparse.ArgumentParser()
_ap.add_argument("--records", type=Path, default=RUN / "validation_2026-11-24")
_ap.add_argument("--numbers", type=Path, default=RUN / "numbers_pilot.json")
_ap.add_argument("--out", type=Path, default=HERE)
ARGS = _ap.parse_args()
R = ARGS.records.resolve()
OUT = ARGS.out.resolve()
OUT.mkdir(parents=True, exist_ok=True)

WIDTH, DPI = 6.5, 300
INK, INK2, GRID, SURFACE = "#1f1f1e", "#5f5e5a", "#e4e3df", "#ffffff"
# the same colours as make_charts.py (report plan section 2)
SOURCE_COLOR = {"pash-own": "#4a4a4a", "naive": "#2563EB", "caruca-pash": "#e8622b", "caruca-main": "#f0b060"}
ON_COLOR = {"pash-own": "white", "naive": "white", "caruca-pash": INK, "caruca-main": INK}
BASH = "#a8a7a2"
WHOLE = "#e4e3df"
SOURCES = ["pash-own", "naive", "caruca-pash", "caruca-main"]
# the fifth series (full run only): the naive LLM's second sed file, a light tint of the naive LLM's blue
SOURCE_COLOR["naive-sed2"] = "#9fbaf5"
ON_COLOR["naive-sed2"] = INK
LABEL = {"pash-own": "PaSh's own files\n(reference)", "naive": "Naive LLM's files",
         "caruca-pash": "Caruca's files,\nPaSh grammar", "caruca-main": "Caruca's files,\nmain grammar"}

from matplotlib import font_manager as _fm
import os as _os
_FONTS=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','..','..','..','scripts','md-to-pdf','fonts')
# Academic typography (2026-11-26): the report follows ACM acmart, so figures use Libertinus Sans and Inconsolata.
_ACAD=_os.path.join(_FONTS,'academic')
for _f in ('LibertinusSans-Regular.otf','LibertinusSans-Bold.otf','LibertinusSans-Italic.otf','Inconsolata.ttf'):
    _fm.fontManager.addfont(_os.path.join(_ACAD,_f))
plt.rcParams['font.family']='Libertinus Sans'
plt.rcParams['font.monospace']=['Inconsolata','DejaVu Sans Mono']
plt.rcParams.update({
    "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
})


def die(msg):
    sys.exit(f"make_figures_interim: {msg}")


def read_jsonl(p):
    return [json.loads(line) for line in open(p) if line.strip()]


def load_pilot():
    global occ, uses, numbers
    occ = [o for o in read_jsonl(R / "occurrences.jsonl")
           if o["id"] == "oneliners/spell" and o["mode"] == "instrumented" and o["repeat"] == 1 and not o["outside_pash"]]
    uses = {s: sorted((o for o in occ if o["set"] == s), key=lambda o: o["position"]) for s in SOURCES}
    for s in SOURCES:
        if [o["position"] for o in uses[s]] != list(range(1, 10)):
            die(f"{s}: expected command uses 1-9, got {[o['position'] for o in uses[s]]}")
        if [o["command"] for o in uses[s]] != [o["command"] for o in uses["pash-own"]]:
            die(f"{s}: commands differ from PaSh's own run")
    # the split decision is the same in all three instrumented repeats (checked, not assumed)
    for o in read_jsonl(R / "occurrences.jsonl"):
        if o["id"] == "oneliners/spell" and o["set"] in SOURCES and not o["outside_pash"]:
            if o["split"] != uses[o["set"]][o["position"] - 1]["split"]:
                die(f"{o['set']} use {o['position']} repeat {o['repeat']}: split differs from repeat 1")

    numbers = json.load(open(ARGS.numbers))
    if numbers["records"] != R.name:
        die(f"numbers_pilot.json is drawn from {numbers['records']}, not {R.name}")
    for row in numbers["table1"]:
        got = sum(o["split"] for o in uses[row["source"]])
        if got != row["uses_split"]["a"]:
            die(f"{row['source']}: {got} uses split, numbers_pilot.json says {row['uses_split']['a']}")



def short(o):
    words = o["invocation"].replace('\'"', "").replace('"\'', "").split()
    if o["command"] == "tr":
        return " ".join(words[:2]) if words[1].startswith("-") else " ".join(words[:3])
    if o["command"] in ("cat", "sed"):
        return o["command"]
    return " ".join(words[:2])


# ---------------------------------------------------------------- figure 1: split map
def split_map():
    ref = uses["pash-own"]
    differ = {i for i in range(9) if any(uses[s][i]["split"] != ref[i]["split"] for s in SOURCES)}
    fig, ax = plt.subplots(figsize=(WIDTH, 3.0))
    bw, bh, gap_x, gap_y = 0.86, 0.62, 0.14, 0.38
    x0 = 0
    rows_y = {s: -(k * (bh + gap_y)) for k, s in enumerate(SOURCES)}
    top = bh + 0.62
    bottom = rows_y[SOURCES[-1]] - 0.35
    for i in differ:  # shaded columns: where some source differs from PaSh's own files
        ax.add_patch(Rectangle((x0 + i * (bw + gap_x) - gap_x / 2, bottom), bw + gap_x, top - bottom - 0.1,
                               facecolor="#f3f2ee", edgecolor="none", zorder=0))
    for i, o in enumerate(ref):
        x = x0 + i * (bw + gap_x)
        name, _, args = short(o).partition(" ")
        ax.text(x + bw / 2, bh + 0.40, name, ha="center", va="center", fontsize=8.5, family="monospace")
        if args:
            ax.text(x + bw / 2, bh + 0.17, args, ha="center", va="center", fontsize=8, family="monospace",
                    color=INK2)
        if i < 8:
            ax.annotate("", xy=(x + bw + gap_x * 0.95, bh + 0.40), xytext=(x + bw + gap_x * 0.05, bh + 0.40),
                        arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.6, mutation_scale=6))
    for s in SOURCES:
        y = rows_y[s]
        c = SOURCE_COLOR[s]
        for i, o in enumerate(uses[s]):
            x = x0 + i * (bw + gap_x)
            split = o["split"]
            ax.add_patch(Rectangle((x, y), bw, bh, facecolor=c if split else SURFACE, edgecolor=c,
                                   linewidth=1.2, zorder=2))
            ax.text(x + bw / 2, y + bh / 2, "split" if split else "whole", ha="center", va="center",
                    fontsize=8, color=ON_COLOR[s] if split else INK2, zorder=3)
            if s != "pash-own" and o["source"] == "ours":  # the source brought its own files for this use
                ax.plot(x + bw - 0.09, y + bh - 0.10, marker="v", markersize=4.2, color=INK if split else c,
                        markeredgecolor=SURFACE if split else c, markeredgewidth=0.5, zorder=4)
        ax.text(-0.15, y + bh / 2, LABEL[s], ha="right", va="center", fontsize=8)
    ax.set_xlim(-1.75, 9 * (bw + gap_x))
    ax.set_ylim(bottom, top)
    ax.axis("off")
    handles = [Patch(facecolor=INK2, edgecolor=INK2, label="Filled: PaSh split this use"),
               Patch(facecolor=SURFACE, edgecolor=INK2, label="Empty: PaSh ran it whole"),
               plt.Line2D([], [], marker="v", linestyle="none", color=INK2, markersize=5,
                          label="The source's own files (elsewhere PaSh's own were filled in)"),
               Patch(facecolor="#f3f2ee", edgecolor="none", label="Shaded: a source differs from PaSh's own")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.0),
               handlelength=1.2, columnspacing=1.4)
    fig.tight_layout(rect=(0, 0.13, 1, 1))
    fig.savefig(OUT / "split_map.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- figure 2: time bars
def time_bars():
    res = [r for r in read_jsonl(R / "results.jsonl") if r["id"] == "oneliners/spell" and r["mode"] == "plain"]
    order = ["bash"] + SOURCES
    t = {}
    for s in order:
        secs = [r["seconds"] for r in res if r["set"] == s]
        if len(secs) != 3:
            die(f"{s}: expected 3 timed runs, got {len(secs)}")
        if not all(r["same_as_bash"] and r["output_files_same_as_bash"] for r in res if r["set"] == s):
            die(f"{s}: a timed run's output differs from bash")
        t[s] = (statistics.median(secs), min(secs), max(secs))
    a5 = numbers["A5"][0]
    for s in order:
        if abs(a5[s]["median"] - t[s][0]) > 1e-9:
            die(f"{s}: median {t[s][0]} differs from numbers_pilot.json {a5[s]['median']}")
    bash = t["bash"][0]
    labels = {"bash": "Plain bash", **{s: LABEL[s].replace("\n", " ") for s in SOURCES}}
    labels["pash-own"] = "PaSh's own files (reference)"
    fig, ax = plt.subplots(figsize=(WIDTH, 2.5))
    ys = list(range(len(order)))[::-1]
    for y, s in zip(ys, order):
        med, lo, hi = t[s]
        colour = BASH if s == "bash" else SOURCE_COLOR[s]
        ax.barh(y, med, height=0.58, color=colour, edgecolor=SURFACE, linewidth=1.5, zorder=2)
        ax.plot([lo, hi], [y, y], color=INK, lw=0.9, zorder=3, solid_capstyle="butt")
        for v in (lo, hi):
            ax.plot([v, v], [y - 0.12, y + 0.12], color=INK, lw=0.9, zorder=3)
        sp = bash / med
        note = "the baseline" if s == "bash" else (f"{sp:.2f}× faster" if sp > 1 else f"{sp:.2f}× (slower)")
        ax.text(hi + 0.025, y, f"{med:.2f} s · {note}", va="center", ha="left", fontsize=8, color=INK)
    ax.set_yticks(ys, [labels[s] for s in order])
    ax.set_xlim(0, 1.62)
    ax.set_xlabel("Seconds to run the script, median of 3 runs (thin line: fastest to slowest)")
    ax.xaxis.grid(True, color=GRID, lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    fig.tight_layout()
    fig.savefig(OUT / "time_bars.png", dpi=DPI)
    plt.close(fig)
    return t


# ---------------------------------------------------------------- figure 3: uses split
def uses_split():
    counts = {}
    for s in SOURCES:
        u = uses[s]
        own = sum(o["split"] and (s == "pash-own" or o["source"] == "ours") for o in u)
        filled = sum(o["split"] and s != "pash-own" and o["source"] == "pash-own" for o in u)
        whole = sum(not o["split"] for o in u)
        if own + filled + whole != 9:
            die(f"{s}: segments do not add to 9")
        counts[s] = (own, filled, whole)
    fig, ax = plt.subplots(figsize=(WIDTH, 2.6))
    ys = list(range(len(SOURCES)))[::-1]
    for y, s in zip(ys, SOURCES):
        left = 0
        segs = [(counts[s][0], SOURCE_COLOR[s], ON_COLOR[s], None),
                (counts[s][1], SOURCE_COLOR["pash-own"], "white", "////"),
                (counts[s][2], WHOLE, INK, None)]
        for val, colour, tc, hatch in segs:
            if val == 0:
                continue
            ax.barh(y, val, left=left, height=0.6, color=colour, edgecolor=SURFACE, linewidth=1.5,
                    hatch=hatch, zorder=2)
            ax.text(left + val / 2, y, f"{val} of 9", ha="center", va="center", fontsize=8, color=tc, zorder=3,
                    bbox=dict(boxstyle="round,pad=0.15", fc=colour, ec="none") if hatch else None)
            left += val
    ax.set_yticks(ys, [LABEL[s].replace("\n", " ").replace(" (reference)", "\n(reference)") for s in SOURCES])
    ax.set_xlim(0, 9)
    ax.set_xticks(range(10))
    ax.set_xlabel("The script's 9 command uses")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    handles = [Patch(facecolor=SOURCE_COLOR["naive"], label="Split, with the source's own files (its colour)"),
               Patch(facecolor=SOURCE_COLOR["pash-own"], hatch="////", edgecolor=SURFACE,
                     label="Split, with PaSh's own files filled in"),
               Patch(facecolor=WHOLE, label="Run whole")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0),
               handlelength=1.4, columnspacing=1.2)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(OUT / "uses_split.png", dpi=DPI)
    plt.close(fig)
    return counts


# ================================================================ the full run (86 scripts)

FULL = ["pash-own", "naive", "naive-sed2", "caruca-pash", "caruca-main"]
FLABEL = {"pash-own": "PaSh's own files", "naive": "The naive LLM",
          "naive-sed2": "Naive LLM, second\nsed file (52 scripts)", "caruca-pash": "Caruca's small\ngrammar",
          "caruca-main": "Caruca's full\ngrammar", "pash-own-copy": "PaSh's own files,\nrun twice"}
# one-line panel titles for Figure 1 (the caption says the second sed file ran on 52 scripts)
PANEL = {"naive": "The naive LLM", "naive-sed2": "Second sed file", "caruca-pash": "Caruca's small grammar",
         "caruca-main": "Caruca's full grammar"}


def gz_jsonl(p):
    with gzip.open(p, "rt") as f:
        return [json.loads(x) for x in f if x.strip()]


def load_full():
    """The per-use rows (first instrumented repeat) and the timed rows, with fix-up 2 applied: web-search's
    timed rows without node are left out, and rows that have a redone run are replaced by it (fix-up 1 only
    changes output flags, which no figure uses). The second sed file's own bash rows are not a time reference."""
    occ = [o for o in gz_jsonl(R / "occurrences.jsonl.gz")
           if o["mode"] == "instrumented" and o["repeat"] == 1 and not o["outside_pash"]]
    res = [r for r in gz_jsonl(R / "results.jsonl.gz") if r["mode"] == "plain"]
    res = [r for r in res if not (r["id"] == "web-search/engine" and "node" in (r.get("stderr") or "")
                                  and "No such file" in (r.get("stderr") or ""))]
    redone = {(r["id"], r["repeat"]) for r in res if r["phase"].startswith("redo")}
    res = [r for r in res if r["phase"].startswith("redo") or (r["id"], r["repeat"]) not in redone]
    res = [r for r in res if not (r["phase"] == "sed2" and r["set"] == "bash")]
    per = defaultdict(lambda: defaultdict(list))
    for r in res:
        per[r["set"]][r["id"]].append(r["seconds"])
    for st, d in per.items():
        for i, v in d.items():
            if len(v) != 3:
                die(f"{st} {i}: expected 3 timed runs, got {len(v)}")
    med = {st: {i: statistics.median(v) for i, v in d.items()} for st, d in per.items()}
    return occ, med


def commands_changed(occ):
    sp = defaultdict(lambda: defaultdict(bool))   # (set, script) -> command -> split anywhere
    for o in occ:
        sp[(o["set"], o["id"])][o["command"]] |= o["split"] is True
    out = {}
    for s in FULL[1:]:
        g, l = Counter(), Counter()
        for (st, i), d in sp.items():
            if st != s:
                continue
            ref = sp[("pash-own", i)]
            for c in set(d) | set(ref):
                g[c] += d.get(c, False) and not ref.get(c, False)
                l[c] += ref.get(c, False) and not d.get(c, False)
        out[s] = {c: [g[c], l[c]] for c in set(g) | set(l) if g[c] or l[c]}
    return out


def full_split_map(occ, numbers):
    ch = commands_changed(occ)
    want = numbers["full"]["commands_gained_lost"]
    for s in FULL[1:]:
        if {c: v for c, v in ch[s].items()} != {c: v for c, v in want[s].items()}:
            die(f"{s}: commands gained/lost {ch[s]} differ from the numbers json {want[s]}")
    # PaSh's own count per command: scripts where PaSh's own files had it split, of the scripts using it in a part
    used, own_split = defaultdict(set), defaultdict(set)
    for o in occ:
        if o["set"] == "pash-own":
            used[o["command"]].add(o["id"])
            if o["split"] is True:
                own_split[o["command"]].add(o["id"])
    cmds = sorted({c for d in ch.values() for c in d}, key=lambda c: (-max(sum(d.get(c, [0, 0])) for d in ch.values()), c))
    panels = FULL[1:]
    fig, axes = plt.subplots(1, len(panels), figsize=(WIDTH, 3.3), sharey=True)
    ys = list(range(len(cmds)))[::-1]
    lim = max(max(v) for d in ch.values() for v in d.values())
    for ax, s in zip(axes, panels):
        c = SOURCE_COLOR[s]
        for y, cmd in zip(ys, cmds):
            g, l = ch[s].get(cmd, [0, 0])
            if g:
                ax.barh(y, g, height=0.58, color=c, edgecolor=c, zorder=2)
                ax.text(g + lim * 0.05, y, str(g), va="center", ha="left", fontsize=8.2)
            if l:
                ax.barh(y, -l, height=0.58, color=SURFACE, edgecolor=c, linewidth=1.1, hatch="////", zorder=2)
                ax.text(-l - lim * 0.05, y, str(l), va="center", ha="right", fontsize=8.2)
        ax.axvline(0, color=INK2, lw=0.7, zorder=3)
        ax.set_xlim(-lim * 1.45, lim * 1.45)
        ax.set_xticks([])
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.set_title(PANEL[s], fontsize=7.8, loc="center", pad=6)
        ax.text(-lim * 0.7, -0.95, "lost", ha="center", va="center", fontsize=8, color=INK2)
        ax.text(lim * 0.7, -0.95, "gained", ha="center", va="center", fontsize=8, color=INK2)
    axes[0].set_yticks(ys, [""] * len(cmds))
    for y, cmd in zip(ys, cmds):  # command name, and PaSh's own count in grey beneath it
        axes[0].text(-lim * 1.6, y + 0.13, cmd, ha="right", va="center", fontsize=8.6, family="monospace")
        axes[0].text(-lim * 1.6, y - 0.24, f"PaSh's own: {len(own_split[cmd])} of {len(used[cmd])}",
                     ha="right", va="center", fontsize=7.2, color=INK2)
    axes[0].set_ylim(-1.4, len(cmds) - 0.4)
    handles = [Patch(facecolor=INK2, edgecolor=INK2, label="solid: gained (split with this source, not with PaSh's own)"),
               Patch(facecolor=SURFACE, edgecolor=INK2, hatch="////", label="hatched: lost (the reverse)")]
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.0),
               handlelength=1.6, columnspacing=2.0)
    fig.subplots_adjust(left=0.17, right=0.995, top=0.9, bottom=0.1, wspace=0.16)
    fig.savefig(OUT / "split_map.png", dpi=DPI)
    plt.close(fig)
    return ch


def full_time(med, numbers):
    rows = ["naive", "naive-sed2", "caruca-pash", "caruca-main", "pash-own-copy"]
    ps = numbers["full"]["per_source"]
    own = med["pash-own"]
    ratios = {s: sorted(med[s][i] / own[i] for i in med[s]) for s in rows}
    gm = {s: math.exp(sum(map(math.log, v)) / len(v)) for s, v in ratios.items()}
    for s in rows + ["pash-own"]:
        slow_bash = sum(med[s][i] > med["bash"][i] for i in med[s])
        if slow_bash != ps[s]["slower_than_bash"]["a"]:
            die(f"{s}: {slow_bash} scripts slower than bash, the numbers json says {ps[s]['slower_than_bash']}")
    for s in rows:
        if abs(gm[s] - ps[s]["vs_pash_own_gmean"]) > 1e-9:
            die(f"{s}: geometric mean {gm[s]} differs from the numbers json {ps[s]['vs_pash_own_gmean']}")
        slow = sum(v > 1.1 for v in ratios[s])
        if slow != ps[s]["slower_than_own_10pct"]["a"] or len(ratios[s]) != ps[s]["slower_than_own_10pct"]["b"]:
            die(f"{s}: {slow} of {len(ratios[s])} slower by 10%, the numbers json says {ps[s]['slower_than_own_10pct']}")
    lo, hi = min(ratios["pash-own-copy"]), max(ratios["pash-own-copy"])
    if [round(lo, 2), round(hi, 2)] != [round(x, 2) for x in ps["pash-own-copy"]["noise_band"][:2]]:
        die("noise band differs from the numbers json")
    color = {**SOURCE_COLOR, "pash-own-copy": SOURCE_COLOR["pash-own"]}
    fig, ax = plt.subplots(figsize=(WIDTH, 3.15))
    ax.axvspan(lo, hi, color="#f3f2ee", zorder=0)
    ax.axvline(1, color=INK2, lw=0.7, zorder=1)
    ys = list(range(len(rows)))[::-1]
    for y, s in zip(ys, rows):
        v = ratios[s]
        # spread equal values a little up and down so each script stays visible
        jit = [((k % 5) - 2) * 0.07 for k in range(len(v))]
        ax.scatter(v, [y + j for j in jit], s=9, color=color[s], alpha=0.85, linewidths=0, zorder=3)
        ax.plot([gm[s], gm[s]], [y - 0.32, y + 0.32], color=INK, lw=1.6, zorder=4, solid_capstyle="butt")
        r = ps[s]
        ax.text(2.95, y + 0.17, f"{gm[s]:.2f}  ·  {r['slower_than_own_10pct']['a']} of {r['slower_than_own_10pct']['b']} slower by >10%",
                va="center", ha="left", fontsize=8)
        ax.text(2.95, y - 0.2, f"slower than bash: {r['slower_than_bash']['text']}", va="center", ha="left",
                fontsize=8, color=INK2)
    ax.set_xscale("log")
    ax.set_xlim(0.42, 2.9)
    ticks = [0.5, 0.75, 1, 1.5, 2]
    ax.set_xticks(ticks, [f"{t:g}" for t in ticks])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.set_yticks(ys, [FLABEL[s] for s in rows])
    ax.set_xlabel("Time against PaSh's own files, per script\n(median of 3 runs; below 1 = faster)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    top = len(rows) - 0.45
    ax.text(lo * 0.98, top, "noise band (same files run twice)", ha="right", va="bottom", fontsize=8, color=INK2)
    ax.text(1.02, top + 0.32, f"PaSh's own files = 1; slower than bash: {ps['pash-own']['slower_than_bash']['text']}",
            ha="left", va="bottom", fontsize=8, color=INK2)
    ax.text(2.95, top, "geometric mean", ha="left", va="bottom", fontsize=8, color=INK2)
    ax.set_ylim(-0.6, len(rows) + 0.25)
    fig.subplots_adjust(left=0.2, right=0.69, bottom=0.2, top=0.97)  # tight_layout would count the side text
    fig.savefig(OUT / "time_bars.png", dpi=DPI)
    plt.close(fig)
    return gm


def full_uses_split(occ, numbers):
    t1 = {r["source"]: r["uses_split"] for r in numbers["table1"]}
    part = numbers["full"]["partial"]["naive-sed2"]["uses"]
    counts = {}
    for s in FULL:
        u = [o for o in occ if o["set"] == s]
        own = sum(o["split"] is True and o["source"] in ("ours", "pash-own" if s == "pash-own" else "ours") for o in u)
        filled = sum(o["split"] is True and s != "pash-own" and o["source"] == "pash-own" for o in u)
        whole = len(u) - own - filled
        if s in t1 and (own + filled != t1[s]["a"] or len(u) != t1[s]["b"]):
            die(f"{s}: {own + filled} of {len(u)} uses split, the numbers json says {t1[s]['text']}")
        if s == "naive-sed2" and (len(u), own, filled) != (part["in_parts"], part["split_own"], part["split_filled"]):
            die(f"naive-sed2: uses {len(u)}/{own}/{filled} differ from the numbers json {part}")
        counts[s] = (own, filled, whole, len(u))
    fig, ax = plt.subplots(figsize=(WIDTH, 2.9))
    ys = list(range(len(FULL)))[::-1]
    for y, s in zip(ys, FULL):
        left = 0
        segs = [(counts[s][0], SOURCE_COLOR[s], ON_COLOR[s], None),
                (counts[s][1], SOURCE_COLOR["pash-own"], "white", "////"),
                (counts[s][2], WHOLE, INK, None)]
        for val, colour, tc, hatch in segs:
            if val == 0:
                continue
            ax.barh(y, val, left=left, height=0.6, color=colour, edgecolor=SURFACE, linewidth=1.5,
                    hatch=hatch, zorder=2)
            if val >= 20:
                ax.text(left + val / 2, y, str(val), ha="center", va="center", fontsize=8, color=tc, zorder=3,
                        bbox=dict(boxstyle="round,pad=0.15", fc=colour, ec="none") if hatch else None)
            left += val
        ax.text(left + 6, y, f"{counts[s][0] + counts[s][1]} of {counts[s][3]} split", va="center", ha="left", fontsize=8)
    ax.set_yticks(ys, [FLABEL[s].replace("\n", " ").replace(" (52", "\n(52") for s in FULL])
    ax.set_xlim(0, 760)
    ax.set_xlabel("Command uses inside the parts the scripts send PaSh")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    handles = [Patch(facecolor=SOURCE_COLOR["naive"], label="Split, with the source's own files (its colour)"),
               Patch(facecolor=SOURCE_COLOR["pash-own"], hatch="////", edgecolor=SURFACE,
                     label="Split, with PaSh's own files filled in"),
               Patch(facecolor=WHOLE, label="Not split")]
    fig.legend(handles=handles, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 0.0),
               handlelength=1.4, columnspacing=1.2)
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    fig.savefig(OUT / "uses_split.png", dpi=DPI)
    plt.close(fig)
    return counts


# ---------------------------------------------------------------- Figure 3: the setup, column width
def full_setup():
    """How each script was run, drawn small enough to sit beside the text on page 1 (2.9 in wide), lettered
    in the report's faces. Same content as setup_diagram.excalidraw (the long-form drawing, kept)."""
    W, H = 2.9, 1.62
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    fs = 6.6
    from matplotlib.patches import FancyBboxPatch

    def box(x, y, w, h, fc, ec, text="", tc=INK, fsz=fs, lw=0.7, ls="-", r=0.035, **kw):
        ax.add_patch(FancyBboxPatch((x + r, y + r), w - 2 * r, h - 2 * r, boxstyle=f"round,pad={r}",
                                    facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls))
        if text:
            ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fsz, color=tc, linespacing=1.1, **kw)

    head = H - 0.1
    xs, xw = 0.0, 0.44          # the script
    sx, sw = 0.55, 1.12         # the files handed to PaSh
    rx, rw = 1.76, 0.34         # the run
    ox, ow = 2.19, 0.71         # what was recorded
    for x, w, t in ((sx, sw, "Files handed to PaSh"), (rx, rw, "Run"), (ox, ow, "Recorded")):
        ax.text(x + w / 2, head, t, ha="center", va="center", fontsize=fs, color=INK2)
    rh, gap = 0.215, 0.055
    ys = [head - 0.2 - k * (rh + gap) for k in range(5)]   # top of each row
    rows = [(None, "no files", "bash"), ("pash-own", "PaSh's own files", "PaSh"),
            ("naive", "naive LLM", "PaSh"), ("caruca-pash", "Caruca, small", "PaSh"),
            ("caruca-main", "Caruca, full", "PaSh")]
    mid = (ys[0] + ys[-1] - rh) / 2
    box(xs, mid - 0.24, xw, 0.48, SURFACE, INK, "One\nscript,\none input")
    for (src, label, run), yt in zip(rows, ys):
        yb = yt - rh
        ym = yb + rh / 2
        ax.annotate("", xy=(sx - 0.01, ym), xytext=(xs + xw, mid),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.5, mutation_scale=5))
        if src is None:
            box(sx, yb, sw, rh, SURFACE, INK2, label, tc=INK2, ls=(0, (3, 2)))
        elif src == "pash-own":
            box(sx, yb, sw, rh, SOURCE_COLOR[src], SOURCE_COLOR[src], label, tc="white")
        else:
            cw = 0.74
            box(sx, yb, cw, rh, SOURCE_COLOR[src], SOURCE_COLOR[src], label, tc=ON_COLOR[src])
            box(sx + cw + 0.02, yb, sw - cw - 0.02, rh, SOURCE_COLOR["pash-own"], SOURCE_COLOR["pash-own"],
                "+ PaSh's", tc="white", fsz=fs - 0.6)
        ax.annotate("", xy=(rx - 0.01, ym), xytext=(sx + sw + 0.01, ym),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.5, mutation_scale=5))
        box(rx, yb, rw, rh, "#e4e3df" if run == "bash" else SURFACE, INK2 if run == "bash" else INK, run)
        ax.plot([rx + rw, rx + rw + 0.04], [ym, ym], color=INK2, lw=0.5)
    ax.plot([rx + rw + 0.04] * 2, [ys[0] - rh / 2, ys[-1] - rh / 2], color=INK2, lw=0.5)
    oy = [ys[1] - 0.02, ys[2] - 0.08, ys[3] - 0.14]
    for y, t in zip(oy, ("printed output,\nagainst bash's", "which commands\nPaSh split", "seconds,\n3 timed runs")):
        box(ox, y - 0.25, ow, 0.25, SURFACE, INK, t, fsz=fs - 0.7)
        ax.annotate("", xy=(ox - 0.005, y - 0.125), xytext=(rx + rw + 0.04, y - 0.125),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=0.5, mutation_scale=5))
    fig.savefig(OUT / "setup_diagram.png", dpi=DPI)
    plt.close(fig)


# ---------------------------------------------------------------- A5: every script, one page
GROUPS = [("oneliners", "Classics (one-liners)"), ("unixfun", "Unix50"), ("covid", "COVID transit analytics"),
          ("nlp", "Natural-language processing"), ("weather", "Weather analysis"), ("web-search", "Web indexing"),
          ("analytics", "Log analysis"), ("file-mod", "File conversion and encryption"), ("bio", "Genomics")]


def natural(sid):
    import re
    return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", sid)]


def parts_per_script():
    """(set, script id) -> (distinct parts, distinct parts run in parallel, distinct parts where PaSh's compiler
    stopped), from the instrumented run (the timed runs stopped in exactly the same parts)."""
    seen = defaultdict(dict)
    for r in gz_jsonl(R / "regions.jsonl.gz"):
        if r["set"] in SOURCES:
            seen[(r["set"], r["id"])][r["text_sha"]] = r["outcome"]
    return {k: (len(v), list(v.values()).count("parallelized"), list(v.values()).count("pash crash"))
            for k, v in seen.items()}


def full_a5(numbers):
    rows = {r["script"]: r for r in numbers["A5"]}
    if len(rows) != numbers["N"]:
        die(f"A5: {len(rows)} scripts, the numbers json says {numbers['N']}")
    parts = parts_per_script()
    crash_total = {s: sum(v[2] for (st, _), v in parts.items() if st == s) for s in SOURCES}
    want = {"pash-own": 4, "naive": 4, "caruca-pash": 14, "caruca-main": 4}   # Table 1's crash row
    if crash_total != want:
        die(f"A5: crashed parts {crash_total} differ from Table 1 {want}")
    cols = [GROUPS[:2], GROUPS[2:]]
    FW, FH = 6.9, 5.5
    fig = plt.figure(figsize=(FW, FH))
    off = {"pash-own": 0.27, "naive": 0.09, "caruca-pash": -0.09, "caruca-main": -0.27}
    lo_x, hi_x = 0.15, 260
    for ci, groups in enumerate(cols):
        lines = []
        for g, name in groups:
            ids = sorted((i for i in rows if i.split("/")[0] == g), key=natural)
            lines.append(("head", name, len(ids)))
            lines += [("row", i, None) for i in ids]
        n = len(lines)
        left = ci * 0.5 + 1.47 / FW
        ax = fig.add_axes((left, 0.045, 1.22 / FW, 0.875))
        ax.set_xscale("log")
        ax.set_xlim(lo_x, hi_x)
        ax.set_ylim(48 - 0.4, -0.7)
        ax.axvline(1, color=INK2, lw=0.6, zorder=1)
        for x in (0.25, 4, 16, 64):
            ax.axvline(x, color=GRID, lw=0.5, zorder=0)
        ax.set_xticks([0.25, 1, 4, 16, 64], ["0.25", "1", "4", "16", "64"])
        ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
        ax.tick_params(axis="x", labelsize=7, length=2, pad=1)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_xlabel("time ÷ bash time (lower is better)", fontsize=7.2, labelpad=2)
        for y, (kind, key, cnt) in enumerate(lines):
            if kind == "head":
                ax.text(lo_x, y + 0.15, "", transform=ax.transData)
                ax.annotate(f"{key} ({cnt})", xy=(0, y), xycoords=("axes fraction", "data"), xytext=(-104, 0),
                            textcoords="offset points", ha="left", va="center", fontsize=7.2, fontweight=600)
                continue
            r = rows[key]
            b = r["bash"]
            short = key.split("/", 1)[1]
            if len(short) > 19:
                short = short[:18] + "…"
            ax.annotate(short, xy=(0, y), xycoords=("axes fraction", "data"), xytext=(-104, 0),
                        textcoords="offset points", ha="left", va="center", fontsize=6.2, family="monospace")
            ax.annotate(f"{b['median']:.2f} s", xy=(0, y), xycoords=("axes fraction", "data"), xytext=(-4, 0),
                        textcoords="offset points", ha="right", va="center", fontsize=6.2, color=INK2)
            ax.plot([b["min"] / b["median"], b["max"] / b["median"]], [y, y], color=BASH, lw=2.2, zorder=1,
                    solid_capstyle="butt")
            for k, s in enumerate(SOURCES):
                t = r[s]
                yy = y - off[s]
                ax.plot([t["min"] / b["median"], t["max"] / b["median"]], [yy, yy], color=SOURCE_COLOR[s], lw=0.6,
                        zorder=2)
                n_parts, par, crash = parts.get((s, key), (0, 0, 0))
                ax.scatter([t["median"] / b["median"]], [yy], s=8, zorder=3, linewidths=0.8,
                           facecolors=SURFACE if crash else SOURCE_COLOR[s], edgecolors=SOURCE_COLOR[s])
                txt = str(par) if n_parts else "–"
                ax.annotate(txt, xy=(1, y), xycoords=("axes fraction", "data"), xytext=(5 + 6.5 * k, 0),
                            textcoords="offset points", ha="center", va="center", fontsize=6.3,
                            color=SOURCE_COLOR[s] if s != "caruca-main" else "#c98a2e", fontweight=600)
            n_parts = parts.get(("pash-own", key), (0, 0, 0))[0]
            ax.annotate(f"of {n_parts}" if n_parts else "", xy=(1, y), xycoords=("axes fraction", "data"),
                        xytext=(28, 0), textcoords="offset points", ha="left", va="center", fontsize=6.1, color=INK2)
        ax.annotate("bash", xy=(0, -0.7), xycoords=("axes fraction", "data"), xytext=(-4, 2),
                    textcoords="offset points", ha="right", va="bottom", fontsize=6.4, color=INK2)
        ax.annotate("parts split", xy=(1, -0.7), xycoords=("axes fraction", "data"), xytext=(3, 2),
                    textcoords="offset points", ha="left", va="bottom", fontsize=6.4, color=INK2)
    handles = [plt.Line2D([], [], marker="o", linestyle="-", lw=0.6, color=SOURCE_COLOR[s], markersize=4,
                          label={"pash-own": "PaSh's own files", "naive": "The naive LLM",
                                 "caruca-pash": "Caruca's small grammar", "caruca-main": "Caruca's full grammar"}[s])
               for s in SOURCES]
    handles += [plt.Line2D([], [], marker="o", linestyle="none", markerfacecolor=SURFACE, markeredgecolor=INK2,
                           markersize=4, label="hollow: PaSh's compiler stopped in a part"),
                plt.Line2D([], [], color=BASH, lw=2.2, label="grey bar at 1: bash's own fastest to slowest")]
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.0),
               fontsize=7.2, handlelength=1.8, columnspacing=1.6)
    fig.savefig(OUT / "a5_scripts.png", dpi=DPI)
    plt.close(fig)
    return crash_total


if __name__ == "__main__":
    plt.rcParams["hatch.linewidth"] = 0.6
    nums = json.load(open(ARGS.numbers))
    if nums["N"] > 1:
        occ_f, med_f = load_full()
        print("commands gained/lost:", full_split_map(occ_f, nums))
        print("time against PaSh's own (geometric mean):", full_time(med_f, nums))
        print("uses split (own, filled in, not split, total):", full_uses_split(occ_f, nums))
        full_setup()
        print("A5 chart, crashed parts per source:", full_a5(nums))
    else:
        load_pilot()
        split_map()
        t = time_bars()
        c = uses_split()
        print("times (median, min, max):", t)
        print("uses split (own, filled in, whole):", c)
