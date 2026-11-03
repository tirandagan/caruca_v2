#!/usr/bin/env python3
"""Task 019 figures: the paper's Fig. 7 redrawn with the naive agent's times, and a Caruca-vs-agent comparison.

    uv run --no-project --with matplotlib==3.9.2 python naive_llm_caruca/fig7_campaign/make_figures.py

Writes figures/fig7_agent.{png,pdf}, figures/fig7_compare.{png,pdf} and figures/fig7_data.csv (every plotted
value) beside this file. Sources: caruca_side/fig7_values.tsv (Caruca's Fig. 7 bars, read from the paper's
vector drawing), caruca_side/counts.tsv (Caruca's test runs at up to 4 options per line, counted from its
curated syntax files) and ledger.jsonl (the agent's runs, main arm; repeats 2 and 3 where they exist).
"""
import csv, json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

HERE = Path(__file__).resolve().parent
SIDE = HERE / "caruca_side"
OUT = HERE / "figures"

# the dataviz skill's reference palette (light mode): slot 1 blue = agent, slot 2 orange = Caruca
AGENT, CARUCA = "#2a78d6", "#eb6834"
AGENT_LIGHT = "#86b6ef"  # blue step 250, the lightest that still clears 2:1 on the surface
INK, INK2, MUTED, GRID, BASE, SURFACE, SHADE = ("#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7",
                                                "#fcfcfb", "#f0efec")
plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                     "font.size": 9, "axes.edgecolor": BASE, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                     "savefig.facecolor": SURFACE})

MIN, HOUR, DAY = 60, 3600, 86400
# opaque legend box so the dashed lines do not run through its text
LEGEND = {"frameon": True, "facecolor": SURFACE, "edgecolor": "none", "framealpha": 1}
REFS = [(MIN, "1 minute"), (HOUR, "1 hour"), (5 * HOUR, "5 hours (the paper's time limit)"),
        (DAY, "1 day"), (7 * DAY, "1 week"), (365 * DAY, "1 year")]


def rows(path):
    return list(csv.DictReader((l for l in open(path) if not l.startswith("#")), delimiter="\t"))


def load():
    runs4 = {r["command"]: int(r["traced_configurations"]) for r in rows(SIDE / "counts.tsv") if r["k"] == "4"}
    agent = {}
    for l in open(HERE / "ledger.jsonl"):
        d = json.loads(l)
        if d.get("arm", "main") == "main" and d.get("status") == "ok":
            agent.setdefault(d["command"], {})[d.get("repeat", 1)] = d
    data = []
    for f in rows(SIDE / "fig7_values.tsv"):
        c = f["command"]
        a = agent.get(c, {})
        measured = f["group"] == "A"
        data.append({"command": c, "caruca_measured": measured,
                     "caruca_s": float(f["real4_s"] if measured else f["proj4_s"]),
                     "caruca_test_runs": runs4[c],
                     "agent_s": a[1]["wall_s"] if 1 in a else None,
                     "agent_runs": a[1]["tries"]["tries"] if 1 in a else None,
                     "agent_repeat_s": [a[r]["wall_s"] for r in sorted(a) if r > 1],
                     "agent_repeat_runs": [a[r]["tries"]["tries"] for r in sorted(a) if r > 1]})
    return data


def refs(ax, lo, hi):
    """Dashed time lines, labelled in the right margin so the labels never sit on a mark."""
    for v, name in REFS:
        if lo < v < hi:
            ax.axhline(v, color=MUTED, lw=0.8, ls=(0, (4, 3)), zorder=1)
            ax.text(1.004, v, name.replace(" (", "\n("), color=INK2, fontsize=7.5, ha="left", va="center",
                    transform=ax.get_yaxis_transform())


def shade_unfinished(ax, data, label_y, label="Caruca did not finish these within 5 hours;\n"
                                              "its times here are the paper's projections"):
    b = [i for i, d in enumerate(data) if not d["caruca_measured"]]
    if b:
        ax.axvspan(b[0] - 0.5, b[-1] + 0.5, color=SHADE, zorder=0, lw=0)
        ax.text((b[0] + b[-1]) / 2, label_y, label, ha="center", va="top", color=INK2, fontsize=7.5)


def axes_common(ax, data):
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels([d["command"] for d in data], rotation=90, fontsize=7.5)
    ax.set_xlim(-1, len(data))
    ax.set_yscale("log")
    ax.grid(axis="y", which="major", color=GRID, lw=0.5, zorder=0)
    ax.tick_params(axis="x", length=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)


def spearman(x, y):
    rank = lambda v: {i: r for r, i in enumerate(sorted(range(len(v)), key=v.__getitem__))}  # noqa: E731
    rx, ry = rank(x), rank(y)
    n = len(x)
    return 1 - 6 * sum((rx[i] - ry[i]) ** 2 for i in range(n)) / (n * (n * n - 1))


def fig_agent(data):
    """Fig. 7's form (log axis, limit lines), the agent's time as the bars, sorted by that time as the paper
    sorted by Caruca's; a lighter bar marks a command Caruca did not finish within 5 hours."""
    data = sorted(data, key=lambda d: d["agent_s"])
    fig, ax = plt.subplots(figsize=(14, 4.6))
    xs = range(len(data))
    ax.bar(xs, [d["agent_s"] for d in data], width=0.72, zorder=2,
           color=[AGENT if d["caruca_measured"] else AGENT_LIGHT for d in data])
    for i, d in enumerate(data):
        if d["agent_repeat_s"]:
            ax.scatter([i] * len(d["agent_repeat_s"]), d["agent_repeat_s"], s=14, facecolor=SURFACE,
                       edgecolor=INK, lw=0.9, zorder=3)
    axes_common(ax, data)
    lo, hi = 5, 1.5e6
    ax.set_ylim(lo, hi)
    refs(ax, lo, hi)
    ax.set_ylabel("Time per command (seconds, log scale)")
    t = [d["agent_s"] for d in data]
    rho = spearman(t, [d["caruca_s"] for d in data])
    fig.suptitle("Fig. 7 redrawn with the naive agent's times: every command took between "
                 f"{min(t):.0f} seconds and {max(t) / 60:.0f} minutes", x=0.06, ha="left", fontsize=11, color=INK)
    ax.set_title("The paper's 79 commands on its axis and limit lines, sorted by the agent's time as Fig. 7 is sorted "
                 "by Caruca's. One Claude Code session per command (Fable 5.1, medium effort) in a Lima VM on an Apple "
                 f"M5 Pro Mac, 2026-10-28; the time is the whole session. Rank agreement with Caruca's order: {rho:.2f} "
                 "(1 = same order).", loc="left", fontsize=8, color=INK2, wrap=True)
    nb = sum(not d["caruca_measured"] for d in data)
    ax.legend(handles=[Patch(color=AGENT, label=f"agent; Caruca finished this command ({len(data) - nb})"),
                       Patch(color=AGENT_LIGHT, label=f"agent; Caruca did not finish it within 5 hours ({nb})"),
                       Line2D([], [], ls="", marker="o", markersize=4.5, markerfacecolor=SURFACE,
                              markeredgecolor=INK, label="agent, repeat runs (head, cut, dd, cp, sort)")],
              loc="upper left", fontsize=8, bbox_to_anchor=(0.0, 0.93), **LEGEND)
    fig.tight_layout()
    return fig


def dumbbell(ax, data, ck, ak, rk):
    for i, d in enumerate(data):
        ax.plot([i, i], [d[ck], d[ak]], color=BASE, lw=1, zorder=1)
        ax.scatter(i, d[ck], s=26, zorder=3, lw=1.2, edgecolor=CARUCA,
                   facecolor=CARUCA if d["caruca_measured"] or ck != "caruca_s" else SURFACE)
        ax.scatter(i, d[ak], s=26, color=AGENT, zorder=3, lw=0)
        if d[rk]:
            ax.scatter([i] * len(d[rk]), d[rk], s=12, facecolor=SURFACE, edgecolor=AGENT, lw=0.9, zorder=4)
    axes_common(ax, data)


def fig_compare(data):
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(14, 8.6), sharex=True)
    dumbbell(a1, data, "caruca_s", "agent_s", "agent_repeat_s")
    lo, hi = 5, 2e10
    a1.set_ylim(lo, hi)
    shade_unfinished(a1, data, hi / 2)
    refs(a1, lo, hi)
    a1.set_ylabel("Time per command (seconds, log scale)")
    faster = sum(d["agent_s"] < d["caruca_s"] for d in data)
    faster_m = sum(d["agent_s"] < d["caruca_s"] for d in data if d["caruca_measured"])
    nm = sum(d["caruca_measured"] for d in data)
    a1.set_title(f"Time: the agent took less time than Caruca on {faster} of the 79 commands ({faster_m} of the "
                 f"{nm} Caruca finished; all {len(data) - nm} it did not)", loc="left", fontsize=10, color=INK)
    a1.legend(handles=[
        Line2D([], [], ls="", marker="o", markersize=6, color=CARUCA, label="Caruca, measured (paper, up to 4 options)"),
        Line2D([], [], ls="", marker="o", markersize=6, markerfacecolor=SURFACE, markeredgecolor=CARUCA,
               label="Caruca, the paper's projection (an upper bound)"),
        Line2D([], [], ls="", marker="o", markersize=6, color=AGENT, label="agent, first run (whole session)"),
        Line2D([], [], ls="", marker="o", markersize=4.5, markerfacecolor=SURFACE, markeredgecolor=AGENT,
               label="agent, repeat runs")], loc="upper left", fontsize=8, ncol=2,
        bbox_to_anchor=(0.0, 1.0), **LEGEND)

    dumbbell(a2, data, "caruca_test_runs", "agent_runs", "agent_repeat_runs")
    a2.set_ylim(3, 1e12)
    shade_unfinished(a2, data, 1e12 / 2, "Caruca did not finish these within 5 hours")
    more = sum(d["agent_runs"] > d["caruca_test_runs"] for d in data)
    a2.set_ylabel("Runs of the program (log scale)")
    a2.set_title(f"Program runs: the agent ran the program fewer times than Caruca would on {len(data) - more} of "
                 f"the 79 commands", loc="left", fontsize=10, color=INK)
    a2.legend(handles=[
        Line2D([], [], ls="", marker="o", markersize=6, color=CARUCA,
               label="Caruca, test runs at up to 4 options (counted from its syntax files)"),
        Line2D([], [], ls="", marker="o", markersize=6, color=AGENT, label="agent, every start of the program")],
        loc="upper left", fontsize=8, ncol=2, bbox_to_anchor=(0.0, 1.0), **LEGEND)
    fig.suptitle("Caruca and the naive agent on the 79 commands of the paper's Fig. 7", x=0.06, ha="left",
                 fontsize=12, color=INK)
    fig.text(0.06, 0.005,
             "Caruca's times are from the paper (Xeon E5-2667 v2, all cores); the agent's from one Claude Code session "
             "per command (Fable 5.1, medium effort, Lima VM on an Apple M5 Pro Mac, 2026-10-28). Caruca's counts for "
             "cp and diff (308 million and 2.4 billion) cannot fit its measured 2.7 and 3.3 hours, so the paper ran "
             "other syntax files or settings for those two. The agent's output has not yet been checked for quality.",
             fontsize=7.5, color=INK2, ha="left", va="bottom", wrap=True)
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    return fig


def main():
    data = load()
    missing = [d["command"] for d in data if d["agent_s"] is None]
    if missing:
        raise SystemExit(f"no agent run yet for: {' '.join(missing)}")
    OUT.mkdir(exist_ok=True)
    with open(OUT / "fig7_data.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["command", "caruca_seconds", "caruca_seconds_kind", "caruca_test_runs_up_to_4_options",
                    "agent_seconds_run1", "agent_program_runs_run1", "agent_seconds_repeats", "agent_runs_repeats"])
        for d in data:
            w.writerow([d["command"], d["caruca_s"], "measured" if d["caruca_measured"] else "projected",
                        d["caruca_test_runs"], d["agent_s"], d["agent_runs"],
                        " ".join(f"{x:g}" for x in d["agent_repeat_s"]), " ".join(map(str, d["agent_repeat_runs"]))])
    for name, fig in (("fig7_agent", fig_agent(data)), ("fig7_compare", fig_compare(data))):
        fig.savefig(OUT / f"{name}.png", dpi=200)
        fig.savefig(OUT / f"{name}.pdf")
        plt.close(fig)
    print("wrote", ", ".join(sorted(p.name for p in OUT.iterdir())))


if __name__ == "__main__":
    main()
