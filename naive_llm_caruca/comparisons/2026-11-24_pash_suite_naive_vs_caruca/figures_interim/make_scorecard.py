#!/usr/bin/env python3
"""Draw Figure 2 (scorecard.png): one-axis Tufte dot plot answering "how did the naive LLM fare?".

    uv run --offline --with matplotlib --with numpy python figures_interim/make_scorecard.py

Every metric is placed on one log x-axis with one direction: each source's result as a fraction
of PaSh's own files' result (1.0 = vertical black line; right of 1.0 = better, left = worse).
Hand-fed from numbers_full.md and the report's Table 2 (report/report.html).
"""
import os as _os
from pathlib import Path

import matplotlib
import matplotlib.ticker
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager as _fm  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
RUN = HERE.parent
OUT = RUN / "figures_full"
OUT.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT, DPI = 6.3, 3.7, 300   # Draft 2.0: shorter, so Table 3 fits on the same page
INK, INK2, GUIDE, SURFACE = "#1f1f1e", "#5f5e5a", "#e4e3df", "#ffffff"
NOISE_FILL = "#ebeae5"

# Fonts: registered from scripts/md-to-pdf/fonts/academic/ as in make_figures_interim.py
_FONTS = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "..", "..", "scripts", "md-to-pdf", "fonts")
_ACAD = _os.path.join(_FONTS, "academic")
for _f in ("LibertinusSans-Regular.otf", "LibertinusSans-Bold.otf", "LibertinusSans-Italic.otf", "Inconsolata.ttf"):
    _fm.fontManager.addfont(_os.path.join(_ACAD, _f))
plt.rcParams["font.family"] = "Libertinus Sans"
plt.rcParams["font.monospace"] = ["Inconsolata", "DejaVu Sans Mono"]
plt.rcParams.update({
    "font.size": 8.0,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 8.0,
    "ytick.labelsize": 8.0,
    "legend.fontsize": 7.6,
    "axes.edgecolor": INK2,
    "axes.labelcolor": INK,
    "xtick.color": INK2,
    "ytick.color": INK,
    "text.color": INK,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.spines.left": False,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})

# Sources and colours (matching the other figures and brief_scorecard.md)
COLOR = {
    "naive": "#2563EB",
    "naive-sed2": "#93b4f5",
    "caruca-full": "#f0b060",
    "caruca-small": "#e8622b",
    "pash-copy": "#9a9a9a",
}
LEGEND_LABEL = {
    "naive": "Naive LLM",
    "naive-sed2": "Naive LLM, fixed sed",
    "caruca-full": "Caruca, full where traced",
    "caruca-small": "Caruca small",
    "pash-copy": "PaSh's own (2nd copy)",
}

# Hand-fed scorecard rows, top to bottom.
# Each entry: (short plain-word label, dict of source -> x value).
# Provenance: numbers_full.md and report/report.html (Table 1; the old Table 2 was merged into it in Draft 2.3).
ROWS = [
    # Draft 2.0 (2026-11-27): Caruca's values are from the rerun with all converted commands
    # (numbers_caruca_all.md, full_run_caruca_all/); the naive LLM's from the first run (numbers_full.md).
    # Row 1: commands with own files, vs PaSh's own 30: naive 82 (task 024 set), Caruca 53 for both sets
    #        (full_run_caruca_all/manifest.json; the full-grammar set uses its full grammar for 22 of them)
    (
        "Commands covered\nby its own files",
        {"naive": 82 / 30, "caruca-full": 53 / 30, "caruca-small": 53 / 30},
    ),
    # Row 2: uses decided by own files, of 609, vs PaSh's own 485: naive 523 (numbers_full.md Table 2),
    #        Caruca 527 for both (numbers_caruca_all.md Table 2)
    (
        "Command uses decided\nby its own files (of 609)",
        {"naive": 523 / 485, "caruca-full": 527 / 485, "caruca-small": 527 / 485},
    ),
    # Row 3: printed output same as bash, vs PaSh's own 86 of 86: naive 86, Caruca full 76, small 77
    #        (numbers_full.md / numbers_caruca_all.md, "Full run: output")
    (
        "Printed output\nsame as bash",
        {"naive": 86 / 86, "caruca-full": 76 / 86, "caruca-small": 77 / 86},
    ),
    # Row 4: scripts with a part split, vs PaSh's own 41 of 86: naive 43, Caruca full 40, small 29
    (
        "Scripts with a part split",
        {"naive": 43 / 41, "caruca-full": 40 / 41, "caruca-small": 29 / 41},
    ),
    # Row 5: parts split of 177, vs PaSh's own 41: naive 43, Caruca full 40, small 29 (Chart A data)
    (
        "Parts split",
        {"naive": 43 / 41, "caruca-full": 40 / 41, "caruca-small": 29 / 41},
    ),
    # Row 6: compiler stops, plotted inverted as own / source, PaSh's own 4: naive 4, Caruca full 3, small 11
    #        (Appendix A3 "pash crash": naive 2+2; Caruca small 1+10, full 1+2)
    (
        "Compiler stops\n(fewer is better)",
        {"naive": 4 / 4, "caruca-full": 4 / 3, "caruca-small": 4 / 11},
    ),
    # Row 7: files that load without error: naive 80 of 82; Caruca 106 of 106 after the converter repair
    #        (full_run_caruca_all/load_check.jsonl)
    (
        "Files that load\nwithout error",
        {"naive": 80 / 82, "caruca-full": 1.00, "caruca-small": 1.00},
    ),
    # Row 8: same reads and writes as PaSh's own, of 178 lines: naive 172, Caruca full 155, small 147 (Table 4)
    (
        "Agreement with PaSh's own\non reads and writes",
        {"naive": 172 / 178, "caruca-full": 155 / 178, "caruca-small": 147 / 178},
    ),
    # Row 9: own time / source time, geometric means, each against PaSh's own of its own session:
    #        naive 1/1.15, fixed sed 1/1.07, PaSh's own 2nd copy 1/0.99 (first session); Caruca full 1/1.10,
    #        small 1/1.09 (second session; its 2nd copy 1/1.00). Noise band: the first session's.
    (
        "Wall-clock\n(faster is better)",
        {
            "naive": 1 / 1.1483,
            "caruca-full": 1 / 1.0974,
            "naive-sed2": 1 / 1.0682,
            "caruca-small": 1 / 1.0929,
            "pash-copy": 1 / 0.9902,
        },
    ),
]

# Draft 2.4 (2026-11-27): --no-caruca-full drops the full-grammar series; the body shows one Caruca (small grammars).
import sys as _sys
NOFULL = "--no-caruca-full" in _sys.argv
if NOFULL:
    ROWS = [(lbl, {k: v for k, v in vals.items() if k != "caruca-full"}) for lbl, vals in ROWS]
    LEGEND_LABEL["caruca-small"] = "Caruca"

# Noise band on the wall-clock row only (numbers_full.md:1841, brief_scorecard.md)
NOISE_LO, NOISE_HI = 0.87, 1.13


def compute_y_offsets(vals):
    """Return small vertical offsets when sources share (or nearly share) a value on a row."""
    # Group points that fall within 0.015 in log space (~1.5% apart) so overlapping dots separate cleanly.
    items = sorted(vals.items(), key=lambda kv: (kv[1], kv[0]))
    groups = []
    for src, x in items:
        if groups and abs(np.log(x) - np.log(groups[-1][-1][1])) < 0.015:
            groups[-1].append((src, x))
        else:
            groups.append([(src, x)])
    offsets = {}
    # Order inside a tied cluster: deterministic visual order (naive on top, then caruca-full, caruca-small, extras)
    rank = {"naive": 0, "caruca-full": 1, "caruca-small": 2, "naive-sed2": 3, "pash-copy": 4}
    for grp in groups:
        if len(grp) == 1:
            offsets[grp[0][0]] = 0.0
        elif len(grp) == 2:
            ordered = sorted(grp, key=lambda kv: rank[kv[0]])
            offsets[ordered[0][0]] = 0.18
            offsets[ordered[1][0]] = -0.18
        else:
            # 3 points tied or nearly tied (row 3: all 1.00; row 9: 0.94, 0.94, 0.95)
            ordered = sorted(grp, key=lambda kv: rank[kv[0]])
            # Place the distinct-x point (if any) at center, exact ties at +/-0.23
            xs = [x for _, x in ordered]
            if len(set(xs)) == 2:
                # Row 9: 0.94 (caruca-full), 0.94 (naive-sed2), 0.95 (caruca-small)
                uniq = [kv for kv in ordered if xs.count(kv[1]) == 1][0]
                tied = [kv for kv in ordered if kv[0] != uniq[0]]
                offsets[tied[0][0]] = 0.23
                offsets[uniq[0]] = 0.0
                offsets[tied[1][0]] = -0.23
            else:
                step = 0.25
                mid = (len(ordered) - 1) / 2.0
                for idx, (src, _) in enumerate(ordered):
                    offsets[src] = (mid - idx) * step
    return offsets


def draw_scorecard():
    fig, ax = plt.subplots(figsize=(WIDTH, HEIGHT))
    n = len(ROWS)
    ys = list(range(n - 1, -1, -1))  # top row at n-1, bottom row at 0

    ax.set_xscale("log")
    ax.set_xlim(0.24, 3.6)   # Draft 2.3: wide enough that the 2.7x point and its label sit well inside
    ax.set_ylim(-0.62, n - 0.38)

    # Shaded noise band on the wall-clock row (row 9, y = 0) only
    y_time = ys[-1]
    band_h = 0.78
    ax.add_patch(
        Rectangle(
            (NOISE_LO, y_time - band_h / 2),
            NOISE_HI - NOISE_LO,
            band_h,
            facecolor=NOISE_FILL,
            edgecolor="none",
            zorder=0.5,
        )
    )
    ax.text(
        NOISE_HI * 1.03,
        y_time,
        "noise",
        ha="left",
        va="center",
        fontsize=7.5,
        color=INK2,
        zorder=2,
    )

    # Horizontal light grey guide per row (no other grid)
    for y in ys:
        ax.axhline(y, color=GUIDE, lw=0.85, zorder=1)

    # Reference vertical black line at PaSh's own files = 1.0
    ax.axvline(1.0, color="#000000", lw=1.0, zorder=2)

    # Plot dots: 9 pt diameter, thin white edge so overlapping dots stay visible
    draw_order = ["pash-copy", "naive-sed2", "caruca-small", "caruca-full", "naive"]
    for idx, (y, (_, vals)) in enumerate(zip(ys, ROWS)):
        y_off = compute_y_offsets(vals)
        for src in draw_order:
            if src not in vals:
                continue
            x = vals[src]
            ax.plot(
                x,
                y + y_off[src],
                marker="o",
                markersize=9.0,
                markerfacecolor=COLOR[src],
                markeredgecolor=SURFACE,
                markeredgewidth=0.9,
                linestyle="none",
                zorder=4 if src == "naive" else 3,
            )
        # Row 1: label the naive LLM dot with its value (2.7×)
        if idx == 0:
            ax.annotate(
                "2.7×",
                xy=(vals["naive"], y),
                xytext=(-7.5, 0),
                textcoords="offset points",
                ha="right",
                va="center",
                fontsize=7.8,
                color=COLOR["naive"],
                fontweight="bold",
                zorder=5,
            )

    # Axes ticks, labels, spines
    ticks = [0.25, 0.5, 1, 2, 3]
    ax.set_xticks(ticks, ["0.25", "0.5", "1", "2", "3"])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    ax.tick_params(axis="x", labelsize=8.0, length=3.5, pad=3, color=INK2, labelcolor=INK)
    ax.set_yticks(ys, [lbl for lbl, _ in ROWS])
    ax.tick_params(axis="y", length=0, pad=6, labelsize=8.0, labelcolor=INK)
    ax.set_xlabel("Result as a fraction of PaSh's own files (right of the line = better)", fontsize=8.5, labelpad=6)
    ax.spines["bottom"].set_linewidth(0.8)
    ax.spines["bottom"].set_color(INK2)

    # Legend across the top in one line
    legend_order = ["pash-copy", "naive", "naive-sed2", "caruca-small", "caruca-full"]   # one source order everywhere
    if NOFULL:
        legend_order = [x for x in legend_order if x != "caruca-full"]
    handles = [
        plt.Line2D(
            [],
            [],
            marker="o",
            linestyle="none",
            markersize=7.0,
            markerfacecolor=COLOR[s],
            markeredgecolor=SURFACE,
            markeredgewidth=0.6,
            label=LEGEND_LABEL[s],
        )
        for s in legend_order
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        ncol=len(legend_order),
        frameon=False,
        bbox_to_anchor=(0.5, 0.992),
        fontsize=7.8,
        handletextpad=0.32,
        columnspacing=1.05,
        handlelength=1.0,
    )

    fig.subplots_adjust(left=0.255, right=0.985, top=0.915, bottom=0.125)
    out_path = OUT / "scorecard.png"
    fig.savefig(out_path, dpi=DPI)
    plt.close(fig)
    print(f"wrote {out_path} ({WIDTH} x {HEIGHT} in @ {DPI} dpi; smallest font = 7.5 pt)")


if __name__ == "__main__":
    draw_scorecard()
