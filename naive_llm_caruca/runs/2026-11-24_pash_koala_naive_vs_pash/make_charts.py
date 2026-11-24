#!/usr/bin/env python3
"""Draw charts A, B and C of the PaSh-suite report from numbers.json (written by count_report.py).

    uv run --with matplotlib==3.9.2 python make_charts.py --numbers <folder>/numbers.json

Writes <folder>/figures/chartA.png, chartB.png, chartC.png: portrait page width (6.5 in), text 8 pt or
larger, 300 dpi. Draws only what numbers.json holds; it counts nothing itself.
"""
import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

WIDTH = 6.5
DPI = 300
INK, INK2, GRID, SURFACE = "#1f1f1e", "#5f5e5a", "#e4e3df", "#ffffff"
# one colour per source, the same in every chart (report plan section 2). PaSh's own files: dark grey.
# Caruca's main grammar: a lighter orange than the plan's first idea, so it stays apart from the PaSh-grammar
# orange for readers with full colour vision (dataviz validator, 2026-11-24); both are always labelled.
SOURCE_COLOR = {"pash-own": "#4a4a48", "naive": "#2a78d6", "caruca-pash": "#eb6834", "caruca-main": "#f0b060"}
# chart A's four outcomes (plan section 2): validated together with the dataviz validator
SEG = {"both": "#2a78d6", "only_this": "#1baf7a", "neither": "#d9d8d3", "only_pash_own": "#eb6834"}
WRONG = "#e34948"

plt.rcParams.update({
    "font.size": 8.5, "axes.titlesize": 9, "axes.labelsize": 8.5, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK, "xtick.color": INK2,
    "ytick.color": INK2, "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
})


def chart_a(n, out):
    ref, rows = n["chartA_reference"], n["chartA"]
    P = ref["P"]
    labels = [ref["label"] + " (reference)"] + [r["label"] for r in rows]
    fig_h = 0.5 + 0.42 * len(labels) + 0.9
    fig, ax = plt.subplots(figsize=(WIDTH, fig_h))
    ys = list(range(len(labels)))[::-1]

    def segs(ax, y, parts, h):
        left = 0
        for key, val, colour, text_colour in parts:
            if val == 0:
                continue
            w = val / P
            ax.barh(y, w, left=left, height=h, color=colour, edgecolor=SURFACE, linewidth=1.5)
            label = f"{val} of {P}"
            # leave a segment unlabelled only when it is too narrow for its number
            if w * WIDTH * 0.72 > 0.075 * len(label):
                ax.text(left + w / 2, y, label, ha="center", va="center", fontsize=8, color=text_colour)
            left += w

    segs(ax, ys[0], [("p", ref["parallel"], SOURCE_COLOR["pash-own"], "white"),
                     ("n", ref["not_parallel"], SEG["neither"], INK)], 0.38)
    for y, r in zip(ys[1:], rows):
        segs(ax, y, [("both", r["both"], SEG["both"], "white"), ("only_this", r["only_this"], SEG["only_this"], INK),
                     ("neither", r["neither"], SEG["neither"], INK),
                     ("only_pash_own", r["only_pash_own"], SEG["only_pash_own"], INK)], 0.62)
    ax.set_yticks(ys, labels)
    ax.set_xlim(0, 1)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1], ["0%", "25%", "50%", "75%", "100%"])
    ax.set_xlabel(f"Share of the {P} distinct parts of the scripts that PaSh was asked to compile")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    handles = [Patch(color=SEG["both"], label="Run in parallel with both"),
               Patch(color=SEG["only_this"], label="Only with this source"),
               Patch(color=SEG["only_pash_own"], label="Only with PaSh's own files"),
               Patch(color=SEG["neither"], label="With neither (top bar: not run in parallel)"),
               Patch(color=SOURCE_COLOR["pash-own"], label="Top bar: run in parallel with PaSh's own files")]
    fig.legend(handles=handles, loc="lower left", ncol=2, frameon=False, bbox_to_anchor=(0.01, 0.0),
               handlelength=1.2, columnspacing=1.5)
    fig.tight_layout(rect=(0, 0.24, 1, 1))
    fig.savefig(out / "chartA.png", dpi=DPI)
    plt.close(fig)


def chart_b(n, out):
    b = n["chartB"]
    panels = b["panels"]
    allv = [p[k] for pan in panels for p in pan["points"] for k in ("x", "y")] + \
           [p[k] for p in b["noise"] for k in ("x", "y")]
    lo, hi = min(allv) / 1.4, max(allv) * 1.4
    fig, axes = plt.subplots(1, len(panels), figsize=(WIDTH, 3.3), sharex=True, sharey=True)
    if len(panels) == 1:
        axes = [axes]
    for ax, pan in zip(axes, panels):
        ax.plot([lo, hi], [lo, hi], color=INK2, linewidth=0.8, linestyle="--", zorder=1)
        if b["noise"]:
            ax.scatter([p["x"] for p in b["noise"]], [p["y"] for p in b["noise"]], s=18, color="#a8a7a2",
                       zorder=2, linewidths=0)
        colour = SOURCE_COLOR.get(pan["source"], INK)
        for p in pan["points"]:
            size = 46 if p["split_differs"] else 20
            if p["output_ok"]:
                ax.scatter(p["x"], p["y"], s=size, color=colour, edgecolor=SURFACE, linewidth=0.8, zorder=3)
            else:
                ax.scatter(p["x"], p["y"], s=size, marker="x", color=WRONG, linewidth=1.4, zorder=4)
        # label only the 2-3 points farthest from the diagonal
        far = sorted(pan["points"], key=lambda p: -abs((p["y"] / p["x"]) - 1))[:3]
        for i, p in enumerate(far):
            if abs(p["y"] / p["x"] - 1) > 0.05:
                ax.annotate(p["script"].split("/")[-1], (p["x"], p["y"]), xytext=(-4, (3, -10, 12)[i]),
                            ha="right",
                            textcoords="offset points", fontsize=8, color=INK)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(lo, hi)
        ax.set_ylim(lo, hi)
        ax.set_title(pan["label"], loc="left", fontsize=8.5, pad=6)
        fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}")
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_locator(matplotlib.ticker.LogLocator(subs=(1.0, 2.0, 5.0)))
            axis.set_major_formatter(fmt)
            axis.set_minor_formatter(matplotlib.ticker.NullFormatter())
        ax.grid(True, color=GRID, linewidth=0.6, which="major")
        ax.set_aspect("equal")
    axes[0].set_ylabel("Median seconds,\nthis source's files")
    fig.supxlabel("Median seconds, PaSh's own files (both axes on a log scale)", fontsize=8.5, y=0.2)
    handles = [plt.Line2D([], [], marker="o", linestyle="", color=INK2, label="Script, output same as bash"),
               plt.Line2D([], [], marker="x", linestyle="", color=WRONG, label="Output not the same as bash"),
               plt.Line2D([], [], marker="o", linestyle="", color="#a8a7a2",
                          label=(b["noise_label"] or "second copy") + " against the first (noise)"),
               plt.Line2D([], [], marker="o", markersize=9, linestyle="", color=INK2,
                          label="Larger: split choices differ from PaSh's own")]
    fig.tight_layout(rect=(0, 0.22, 1, 0.97))
    fig.legend(handles=handles, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, 0.0))
    fig.savefig(out / "chartB.png", dpi=DPI)
    plt.close(fig)


def chart_c(n, out):
    c = n["chartC"]
    cmds = c["commands"]
    rows = c["rows"]
    ncol = len(cmds)
    LEFT, TOP, BAR, GAP, BOTTOM = 2.25, 0.12, 0.5, 0.08, 0.8   # inches
    cell = min(0.26, (WIDTH - LEFT - 0.1) / max(ncol, 1))
    grid_h = cell * len(rows)
    fig_h = TOP + BAR + GAP + grid_h + BOTTOM
    fig = plt.figure(figsize=(WIDTH, fig_h))
    gw = cell * ncol / WIDTH
    bar_ax = fig.add_axes([LEFT / WIDTH, (BOTTOM + grid_h + GAP) / fig_h, gw, BAR / fig_h])
    grid_ax = fig.add_axes([LEFT / WIDTH, BOTTOM / fig_h, gw, grid_h / fig_h])
    xs = range(ncol)
    bar_ax.bar(xs, [x["scripts"] for x in cmds], width=0.7, color="#a8a7a2")
    bar_ax.set_xlim(-0.5, ncol - 0.5)
    bar_ax.set_xticks([])
    bar_ax.set_ylabel(f"Scripts using the command (of {c['N']})", fontsize=8, rotation=0, ha="right", va="center")
    bar_ax.set_yticks([0, max(x["scripts"] for x in cmds)])
    bar_ax.spines["bottom"].set_visible(False)
    for i, r in enumerate(rows):
        y = len(rows) - 1 - i
        colour = SOURCE_COLOR.get(r["source"], INK)
        has = set(r["has"])
        for j, x in enumerate(cmds):
            filled = x["command"] in has
            grid_ax.add_patch(plt.Rectangle((j - 0.4, y - 0.4), 0.8, 0.8, facecolor=colour if filled else SURFACE,
                                            edgecolor=colour if filled else GRID, linewidth=0.8))
    grid_ax.set_xlim(-0.5, ncol - 0.5)
    grid_ax.set_ylim(-0.5, len(rows) - 0.5)
    grid_ax.set_yticks(range(len(rows)), [f"{r['label']} ({len(r['has'])})" for r in rows][::-1])
    grid_ax.set_xticks(list(xs), [x["command"] for x in cmds], rotation=90, fontsize=8)
    for s in ("left", "bottom"):
        grid_ax.spines[s].set_visible(False)
    grid_ax.tick_params(length=0)
    fig.savefig(out / "chartC.png", dpi=DPI)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--numbers", type=Path, default=Path(__file__).resolve().parent / "numbers.json")
    ap.add_argument("--out", type=Path, default=None, help="default: figures/ beside numbers.json")
    a = ap.parse_args()
    n = json.loads(a.numbers.read_text())
    # numbers_pilot.json -> figures_pilot/ ; numbers.json -> figures/
    out = a.out or a.numbers.parent / ("figures" + a.numbers.stem[len("numbers"):])
    out.mkdir(parents=True, exist_ok=True)
    chart_a(n, out)
    chart_b(n, out)
    chart_c(n, out)
    print(f"wrote {out}/chartA.png, chartB.png, chartC.png")


if __name__ == "__main__":
    main()
