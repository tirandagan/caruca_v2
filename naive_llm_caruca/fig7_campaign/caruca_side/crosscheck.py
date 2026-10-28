"""Check the paper's Fig. 7 times against exact test-run counts (task 019, 3.3 e).

For each group-A command (real time at up to 4 options), the paper's time divided by the number of test runs
v1 would make at up to 4 options with its curated syntax file (counts.tsv) gives the paper's implied time per
test run. Commands far from the median suggest the paper ran a different syntax file or settings.

    python3 crosscheck.py > crosscheck.txt
"""
import csv
import os
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
f7 = {r[0]: r for r in csv.reader(open(os.path.join(HERE, "fig7_values.tsv")), delimiter="\t")
      if r and not r[0].startswith("#") and r[0] != "command"}
cnt = {(r[0], int(r[1])): (int(r[2]), int(r[3])) for r in csv.reader(open(os.path.join(HERE, "counts.tsv")),
                                                                     delimiter="\t") if r[0] != "command"}
rows = sorted((float(r[2]) / cnt[(c, 4)][1], c, float(r[2]), cnt[(c, 4)][1]) for c, r in f7.items() if r[1] == "A")
med = statistics.median(x[0] for x in rows)
print(f"# group A: paper time / test runs at up to 4 options. Median {med:.4f} s per test run.")
print(f"# within 3x of the median: {sum(med / 3 <= x[0] <= med * 3 for x in rows)} of {len(rows)}")
print("command\tseconds_per_test_run\tfig7_seconds\ttest_runs_up_to_4\tratio_to_median")
for per, c, t, n in rows:
    print(f"{c}\t{per:.6f}\t{t:.1f}\t{n}\t{per / med:.4g}")
