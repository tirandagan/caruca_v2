# PaSh's overhead and time without it

Fitted on 44 first-run scripts where PaSh's own files split nothing: start-up about 0.11 s per script (median, scripts with at most 2 parts compiled); about 6.5 ms per part compiled (median over scripts with 1,000 or more parts). Used: 0.11 s + 6 ms per part. Split copies' cost is not removed.

Scripts: those with bash median over 0.05 s. One-pass: at most 3 parts compiled and bash at least 1 s.

| Set (run) | Scripts | Time / bash, measured | Time / bash, overhead removed | One-pass scripts | Their time / bash, overhead removed |
|---|---:|---:|---:|---:|---:|
| group A: pash-own | 29 | 0.77 | 0.74 | 28 | 0.71 |
| group A: naive-sed2 | 29 | 1.03 | 0.99 | 28 | 0.96 |
| group A: caruca-pash-all | 29 | 1.17 | 1.14 | 28 | 1.11 |
| group A: pash-own-copy | 29 | 0.79 | 0.76 | 28 | 0.74 |
| group B: pash-own | 0 | nan | nan | 0 | nan |
| group B: naive-sed2 | 0 | nan | nan | 0 | nan |
| group B: caruca-pash-all | 0 | nan | nan | 0 | nan |
| group B: pash-own-copy | 0 | nan | nan | 0 | nan |
