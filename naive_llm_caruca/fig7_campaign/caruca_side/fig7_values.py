"""Caruca's time per command from the paper's Fig. 7, read from the figure's vector drawing (task 019, 3.3 a).

The paper's PDF draws Fig. 7 (page 12) as vector shapes. Each bar is a filled rectangle whose top edge is
exact; the bottom is clipped, since the axis is logarithmic. The axis scale comes from the figure's three
dashed reference lines (5 hours, 24 hours, 1 week), which fix page height as a straight line in
log10(seconds). Bars run left to right in the figure's order, which is commands.txt's order: 48 black bars
(real time, up to 4 options), then for each of the other 31 commands three overlapping bars (projected at up
to 4, 3 and 2 options; the tallest is 4). Bars that pass the top of the plot are labelled in days on the
figure; those labels, in figure order, are entered below by hand, because the figure's text is drawn as
glyph outlines, not text.

    python3 fig7_values.py "<repo>/ai_docs/refs/caruca white paper.pdf" > fig7_values.tsv
"""
import math
import os
import re
import subprocess
import sys
import tempfile

PDF = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
COMMANDS = [l.split("\t")[:2] for l in open(os.path.join(HERE, "..", "commands.txt")) if not l.startswith("#")]
# the white-boxed labels on the figure, left to right (read from the PNG and the PDF, 2026-10-27)
DAY_LABELS = [7.0, 8.3, 8.6, 14.8, 16.5, 17.3, 17.7, 19.6, 21.1, 21.1, 23.8, 83.6, 123.7, 27533.2]
REF = {"rgb(50.195312%, 50.195312%, 50.195312%)": 5 * 3600, "rgb(100%, 0%, 0%)": 24 * 3600,
       "rgb(0%, 0%, 100%)": 7 * 24 * 3600}
FILLS = {"rgb(0%, 0%, 0%)": "real4", "rgb(16.362%, 47.113037%, 55.813599%)": "proj4",
         "rgb(18.577576%, 70.487976%, 48.526001%)": "proj3", "rgb(74.137878%, 87.34436%, 14.955139%)": "proj2"}

with tempfile.TemporaryDirectory() as t:
    svg = os.path.join(t, "p12.svg")
    subprocess.run(["pdftocairo", "-svg", "-f", "12", "-l", "12", PDF, svg], check=True)
    s = open(svg).read()

paths = re.findall(r"<path[^>]*>", s)
nums = lambda d: list(map(float, re.findall(r"-?[\d.]+", d)))

# axis: page y = c - k * log10(seconds), from the reference lines (local coordinates times their transform)
ref = []
for p in paths:
    st = re.search(r'stroke="([^"]*)"', p)
    tr = re.search(r'transform="matrix\(([^)]*)\)"', p)
    if st and st.group(1) in REF and "dasharray" in p and tr:
        a, b, cc, dd, e, f = map(float, tr.group(1).split(","))
        v = nums(re.search(r' d="([^"]*)"', p).group(1))
        if max(v[0::2]) - min(v[0::2]) < 300:   # the legend's short samples, not the lines across the plot
            continue
        ref.append((math.log10(REF[st.group(1)]), dd * v[1] + f))
assert len(ref) == 3, ref
(l1, y1), (l2, y2) = ref[0], ref[1]
k = (y1 - y2) / (l2 - l1)
c = y1 + k * l1
spread = max(abs(c - k * l - y) for l, y in ref)

bars = []
for p in paths:
    f = re.search(r'fill="([^"]*)"', p)
    if not f or f.group(1) not in FILLS:
        continue
    v = nums(re.search(r' d="([^"]*)"', p).group(1))
    xs, ys = v[0::2], v[1::2]
    if max(ys) < 1000:          # legend swatches are short; real bars run to the clipped bottom
        continue
    bars.append((min(xs), FILLS[f.group(1)], min(ys)))
bars.sort()
# the plot's top edge: the upper of the two solid black horizontal frame lines across the plot
frame = []
for p in paths:
    tr = re.search(r'transform="matrix\(([^)]*)\)"', p)
    if 'stroke="rgb(0%, 0%, 0%)"' in p and "dasharray" not in p and tr:
        v = nums(re.search(r' d="([^"]*)"', p).group(1))
        if max(v[0::2]) - min(v[0::2]) > 300 and max(v[1::2]) - min(v[1::2]) < 0.5:
            a_, b_, c_, d_, e_, f_ = map(float, tr.group(1).split(","))
            frame.append(d_ * v[1] + f_)
plot_top = min(frame)

by_x = []
for x, kind, top in bars:
    if not by_x or abs(by_x[-1]["x"] - x) > 1.0:
        by_x.append({"x": x})
    by_x[-1][kind] = top
assert len(by_x) == len(COMMANDS) == 79, (len(by_x), len(COMMANDS))

labels = iter(DAY_LABELS)
print("# Caruca's time per command from the paper's Fig. 7 (vector drawing, page 12). Seconds.")
print(f"# axis: page_y = {c:.4f} - {k:.4f} * log10(s); reference lines fit within {spread:.4f} page units.")
print("# real4 = measured, up to 4 options (group A); proj4/proj3/proj2 = the paper's projection (group B).")
print("# proj4 clipped = bar passes the plot top; value from the figure's label in days.")
print("command\tgroup\treal4_s\tproj4_s\tproj3_s\tproj2_s\tproj4_source")
used = 0
checks = []
for (cmd, grp), b in zip(COMMANDS, by_x):
    val = {kk: 10 ** ((c - y) / k) for kk, y in b.items() if kk != "x"}
    src = ""
    if "proj4" in b:
        clipped = b["proj4"] < plot_top + 0.01
        if clipped or val["proj4"] >= 6.95 * 86400:     # the figure labels every bar of a week or more
            lab = next(labels) * 86400
            used += 1
            if not clipped:                              # both readings exist: a check on the axis scale
                checks.append((cmd, val["proj4"] / 86400, lab / 86400))
            val["proj4"] = lab
            src = "label" if clipped else "label (bar agrees)"
        else:
            src = "bar"
    row = [cmd, grp] + [f"{val[kk]:.1f}" if kk in val else "" for kk in ("real4", "proj4", "proj3", "proj2")] + [src]
    print("\t".join(row))
assert used == len(DAY_LABELS), f"{used} clipped bars, {len(DAY_LABELS)} labels"
for cmd, bar_days, label_days in checks:
    assert abs(bar_days - label_days) < 0.06, (cmd, bar_days, label_days)
print(f"# label check: " + "; ".join(f"{c} bar {b:.2f} d, label {l:.1f} d" for c, b, l in checks))
