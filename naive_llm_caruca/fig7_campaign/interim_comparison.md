# Task 019: agent vs Caruca, commands finished so far (57 of 79)

Made 2026-10-28 12:37 by `compare_table.py`. Agent = Claude Code, Fable 5.1 at medium effort, one run per command. Refused shares on both sides are provisional (messages not yet classed are left out).

| Command | Agent: billed | Agent: wall time | Agent: program runs | Agent: refused share | Caruca: GPT-4o step billed | Caruca: Fig. 7 time | Caruca: test runs (up to 4 options) | Caruca: refused share (2 options) |
|---|---|---|---|---|---|---|---|---|
| `fold` | $1.24 | 3 min | 11,397 | 0.5% | $0.012 | 11 s | 1,552 | 20.2% |
| `tee` | $0.83 | 115 s | 39 | 12.8% | $0.013 | 14 s | 4,800 | 0.0% |
| `mkfifo` | $0.76 | 118 s | 31 | 12.9% | $0.013 | 19 s | 4,200 | 0.0% |
| `expand` | $0.89 | 2 min | 94 | 2.1% | $0.013 | 25 s | 2,908 | 8.8% |
| `chroot` | $1.11 | 2 min | 20 | 20.0% | $0.014 | 28 s | 8,560 | 0.0% |
| `runcon` | $1.21 | 3 min | 60 | 13.3% | $0.013 | 36 s | 5,664 | 0.0% |
| `bc` | $0.78 | 2 min | 53 | 13.2% | $0.033 | 45 s | 3,640 | 0.0% |
| `mogrify` | $4.97 | 17 min | 2,453 | 25.9% | no manual | 54 s | 660 | 22.9% |
| `rev` | $0.58 | 3 min | 21 | 9.5% | $0.011 | 54 s | 88 | 0.0% |
| `unexpand` | $0.71 | 2 min | 78 | 1.3% | $0.014 | 57 s | 4,528 | 8.2% |
| `wc` | $1.13 | 3 min | 46 | 13.0% | $0.015 | 60 s | 7,280 | 0.0% |
| `mktemp` | $1.59 | 4 min | 48 | 27.1% | $0.014 | 62 s | 6,048 | 0.0% |
| `uname` | $0.00 (in `id`'s) | 87 s | 84 | 56.0% | $0.014 | 63 s | 5,280 | 0.0% |
| `id` | $1.49 (incl. `uname`) | 88 s | 92 | 59.8% | $0.014 | 68 s | 5,280 | 0.0% |
| `col` | $0.68 | 2 min | 110 | 42.7% | $0.015 | 76 s | 1,680 | 0.7% |
| `pinky` | $0.58 | 101 s | 69 | 66.7% | $0.014 | 104 s | 7,920 | 6.8% |
| `truncate` | $1.26 | 3 min | 35 | 0.0% | $0.014 | 2 min | 9,736 | 56.2% |
| `mkdir` | $0.74 | 96 s | 31 | 9.7% | $0.013 | 2 min | 21,200 | 0.0% |
| `head` | $1.35 | 4 min | 293 | 12.6% | $0.014 | 3 min | 9,760 | 13.0% |
| `seq` | $0.70 | 117 s | 43 | 9.3% | $0.041 | 3 min | 7,800 | 12.3% |
| `timeout` | $0.72 | 2 min | 103 | 22.3% | $0.016 | 5 min | 13,920 | 38.0% |
| `cat` | $1.33 | 4 min | 176 | 1.7% | $0.013 | 5 min | 27,280 | 0.0% |
| `stat` | $0.93 | 2 min | 60 | 13.3% | $0.016 | 6 min | 36,000 | 0.0% |
| `readlink` | $1.12 | 2 min | 42 | 19.0% | $0.014 | 6 min | 33,600 | 0.0% |
| `sha256sum` | $0.92 | 2 min | 34 | 5.9% | $0.015 | 7 min | 27,280 | 27.5% |
| `sha512sum` | $0.82 | 109 s | 122 | 57.4% | $0.016 | 7 min | 27,280 | 27.5% |
| `sha224sum` | $0.60 | 106 s | 78 | 10.3% | $0.015 | 7 min | 27,280 | 27.5% |
| `sha384sum` | $2.04 | 4 min | 71 | 26.8% | $0.013 | 7 min | 27,280 | 27.5% |
| `sha1sum` | $0.91 | 2 min | 62 | 6.5% | $0.015 | 7 min | 27,280 | 27.5% |
| `md5sum` | $1.06 | 2 min | 107 | 5.6% | $0.015 | 7 min | 27,280 | 27.5% |
| `fmt` | $1.12 | 3 min | 2,675 | 0.7% | $0.015 | 8 min | 17,080 | 11.9% |
| `yes` | $0.64 | 83 s | 31 | 16.1% | $0.011 | 10 min | 8 | n/a |
| `csplit` | $1.84 | 4 min | 30 | 13.3% | $0.015 | 10 min | 41,440 | 8.5% |
| `b2sum` | $1.32 | 3 min | 154 | 1.9% | $0.015 | 11 min | 36,608 | 27.6% |
| `rm` | $0.97 | 3 min | 107 | 3.7% | $0.017 | 13 min | 122,400 | 0.0% |
| `iconv` | $1.91 | 4 min | 2,585 | 0.0% | $0.017 | 26 min | 67,416 | 0.0% |
| `cut` | $0.91 | 2 min | 116 | 3.4% | $0.021 | 27 min | 114,004 | 52.6% |
| `basenc` | $0.74 | 91 s | 47 | 8.5% | $0.016 | 39 min | 45,936 | 47.6% |
| `date` | $1.17 | 3 min | 199 | 13.6% | $0.019 | 45 min | 142,768 | 47.9% |
| `comm` | $0.75 | 117 s | 93 | 66.7% | $0.014 | 68 min | 403,200 | 0.0% |
| `chmod` | $1.33 | 3 min | 335 | 7.8% | $0.032 | 82 min | 515,200 | 0.0% |
| `touch` | $0.86 | 107 s | 61 | 21.3% | $0.035 | 101 min | 381,280 | 20.1% |
| `shred` | $0.96 | 3 min | 116 | 9.5% | $0.016 | 2.5 h | 311,120 | 5.6% |
| `shuf` | $1.31 | 4 min | 123 | 34.1% | $0.014 | 2.6 h | 111,752 | 4.7% |
| `cp` | $1.04 | 3 min | 225 | 25.8% | $0.025 | 2.7 h | 307,764,400 | 1.2% |
| `chgrp` | $1.20 | 2 min | 43 | 9.3% | $0.016 | 2.9 h | 594,880 | 42.0% |
| `diff` | $1.65 | 4 min | 294 | 33.7% | $0.021 | 3.3 h | 2,365,404,900 | 18.9% |
| `chown` | $1.33 | 3 min | 69 | 21.7% | $0.017 | 4.9 h | 919,360 | 43.0% |
| `kill` | $1.75 | 7 min | 1,067 | 3.1% | $0.015 | 6.1 h (projected) | 13,824 | 11.4% |
| `mknod` | $1.21 | 3 min | 44 | 31.8% | $0.014 | 11.4 h (projected) | 188,320 | 63.2% |
| `env` | $1.96 | 4 min | 77 | 3.9% | $0.018 | 16.9 h (projected) | 211,368 | 35.1% |
| `who` | $1.01 | 3 min | 69 | 26.1% | $0.016 | 17.7 h (projected) | 212,800 | 3.9% |
| `tail` | $2.89 | 7 min | 218 | 14.7% | $0.018 | 19.7 h (projected) | 125,496 | 44.5% |
| `dd` | $2.11 | 5 min | 379 | 16.1% | $0.017 | 14.8 days (projected) | 3,345,253 | 69.6% |
| `ls` | $2.42 | 5 min | 983 | 26.1% | $0.023 | 19.6 days (projected) | 32,849,979 | 0.9% |
| `test` | $1.87 | 5 min | 131 | 10.7% | $0.044 | 123.7 days (projected) | 483,653,928 | 100.0% |
| `convert` | $4.10 | 10 min | 18,728 | 17.3% | $0.117 | 27533.2 days (projected) | 229,656,055,750 | 94.8% |

**Totals:** agent $73.43, 3.2 h of wall time, 44,951 program runs; Caruca's model step $1.07, 232,854,043,534 test runs. Fig. 7 time divided by the agent's wall time: median 3x (range 0.1x to 3,781,985x).

`cp` and `diff`: Caruca's current syntax files would make 308 million and 2.4 billion test runs at up to 4 options, which cannot fit the paper's measured 2.7 h and 3.3 h (crosscheck.txt); the paper must have run other syntax files or settings for these two.
