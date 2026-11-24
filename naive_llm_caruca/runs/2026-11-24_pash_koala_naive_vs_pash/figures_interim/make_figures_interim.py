#!/usr/bin/env python3
"""Draw the three evidence figures of the interim report (report_draft.md) from the `spell` records.

    uv run --with matplotlib==3.9.2 python figures_interim/make_figures_interim.py

Reads validation_2026-11-24/occurrences.jsonl, results.jsonl and regions.jsonl (the records the
report's numbers come from, as numbers_pilot.json names them) and writes split_map.png, time_bars.png
and uses_split.png next to this script: portrait page width (6.5 in), text 8 pt or larger, 300 dpi.
Counts only what the records hold; checks its counts against numbers_pilot.json and stops on a mismatch.
"""
import json
import statistics
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
R = RUN / "validation_2026-11-24"
OUT = HERE

WIDTH, DPI = 6.5, 300
INK, INK2, GRID, SURFACE = "#1f1f1e", "#5f5e5a", "#e4e3df", "#ffffff"
# the same colours as make_charts.py (report plan section 2)
SOURCE_COLOR = {"pash-own": "#4a4a4a", "naive": "#2563EB", "caruca-pash": "#e8622b", "caruca-main": "#f0b060"}
ON_COLOR = {"pash-own": "white", "naive": "white", "caruca-pash": INK, "caruca-main": INK}
BASH = "#a8a7a2"
WHOLE = "#e4e3df"
SOURCES = ["pash-own", "naive", "caruca-pash", "caruca-main"]
LABEL = {"pash-own": "PaSh's own files\n(reference)", "naive": "Naive LLM's files",
         "caruca-pash": "Caruca's files,\nPaSh grammar", "caruca-main": "Caruca's files,\nmain grammar"}

from matplotlib import font_manager as _fm
import os as _os
_FONTS=_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'..','..','..','..','scripts','md-to-pdf','fonts')
for _f in ('LexendDeca-Regular.ttf','LexendDeca-SemiBold.ttf','LexendDeca-Bold.ttf'):
    _fm.fontManager.addfont(_os.path.join(_FONTS,_f))
_fm.fontManager.addfont(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),'fonts','JetBrainsMono-Regular.ttf'))
plt.rcParams['font.family']='Lexend Deca'
plt.rcParams['font.monospace']=['JetBrains Mono','DejaVu Sans Mono']
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

numbers = json.load(open(RUN / "numbers_pilot.json"))
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


if __name__ == "__main__":
    plt.rcParams["hatch.linewidth"] = 0.6
    split_map()
    t = time_bars()
    c = uses_split()
    print("times (median, min, max):", t)
    print("uses split (own, filled in, whole):", c)
