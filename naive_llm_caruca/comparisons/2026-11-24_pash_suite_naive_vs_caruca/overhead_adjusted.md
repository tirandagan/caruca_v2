# PaSh's overhead and time without it

Fitted on 44 first-run scripts where PaSh's own files split nothing: start-up about 0.11 s per script (median, scripts with at most 2 parts compiled); about 6.5 ms per part compiled (median over scripts with 1,000 or more parts). Used: 0.11 s + 6 ms per part. Split copies' cost is not removed.

Scripts: those with bash median over 0.05 s (72 of 86). One-pass: at most 3 parts compiled and bash at least 1 s.

| Set (run) | Scripts | Time / bash, measured | Time / bash, overhead removed | One-pass scripts | Their time / bash, overhead removed |
|---|---:|---:|---:|---:|---:|
| pash-own | 72 | 1.69 | 1.03 | 11 | 0.62 |
| naive | 72 | 1.95 | 1.26 | 11 | 0.88 |
| pash-own-copy | 72 | 1.70 | 1.04 | 11 | 0.62 |
| 2:pash-own | 72 | 1.62 | 0.92 | 10 | 0.64 |
| 2:caruca-pash-all | 72 | 1.76 | 1.05 | 10 | 0.85 |
| 2:caruca-main-all | 72 | 1.77 | 1.09 | 10 | 0.73 |
