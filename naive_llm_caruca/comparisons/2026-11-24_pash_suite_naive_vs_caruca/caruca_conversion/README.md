# Converting Caruca's remaining commands to PaSh's current annotation format (2026-11-26)

Why: the first suite run gave Caruca files for only 8 commands (the ones converted on 2026-11-10). Tiran asked for as many
as possible. Every command below was converted by Caruca's own `run_pash_py.sh` on its `pash-python-annotations` branch;
outputs are in `~/dev/stevens/caruca/caruca/save_pash_py/<cmd>/<grammar>_grammar/trace_1/` (three PaSh files, `run.json`
with settings and seconds, `traces.json.gz`). Driver: `trace_batch.sh`; per-command log: `logs/status.tsv`.

Settings, as for the first 8: small (PaSh) grammars at max-count 4; full grammars at max-count 2. One tracing lane per
8-vCPU VM (`caruca`, and a clone `caruca2`), because Caruca's tracer kills each run after 2 s and an overloaded VM
turns good runs into failures; a first start with five lanes in one VM was stopped within two minutes and its outputs
deleted (`logs/aborted_0822/`).

## Small grammars: 45 of 46 remaining commands converted

| Command | Result | Seconds | Traced runs | Runs that hit the 2 s limit |
|---|---|---:|---:|---:|
| `tr` | ok | 5 | 176 | 0 |
| `sed` | ok | 6 | 176 | 0 |
| `awk` | ok | 7 | 198 | 0 |
| `uniq` | ok | 2 | 44 | 0 |
| `head` | ok | 41 | 1364 | 0 |
| `tail` | ok | 37 | 1364 | 0 |
| `seq` | ok | 3 | 33 | 0 |
| `tee` | ok | 22 | 330 | 0 |
| `mkfifo` | ok | 25 | 330 | 0 |
| `col` | ok | 3 | 44 | 0 |
| `fmt` | ok | 3 | 44 | 0 |
| `rev` | ok | 134 | 1364 | 67 |
| `join` | ok | 21 | 1056 | 0 |
| `paste` | ok | 29 | 1023 | 0 |
| `iconv` | ok | 11 | 528 | 0 |
| `ls` | ok | 24 | 682 | 0 |
| `mktemp` | ok | 1 | 22 | 0 |
| `echo` | ok | 3 | 88 | 0 |
| `xargs` | ok | 2 | 33 | 0 |
| `find` | ok | 16 | 341 | 0 |
| `date` | ok | 79 | 4092 | 0 |
| `base64` | ok | 2 | 11 | 0 |
| `bc` | ok | 2 | 22 | 0 |
| `gunzip` | ok | 17 | 341 | 0 |
| `groff` | ok | 34 | 330 | 0 |
| `history` | ok | 2 | 11 | 0 |
| `jq` | ok | 33 | 1364 | 0 |
| `nc` | ok | 2 | 22 | 0 |
| `nl` | ok | 16 | 341 | 0 |
| `pandoc` | ok | 48 | 341 | 23 |
| `pr` | ok | 3 | 88 | 0 |
| `ps` | ok | 1 | 11 | 0 |
| `pwd` | ok | 2 | 11 | 0 |
| `read` | ok | 1 | 11 | 0 |
| `readelf` | ok | 17 | 341 | 0 |
| `sha256sum` | ok | 17 | 341 | 0 |
| `shuf` | ok | 1 | 11 | 0 |
| `gzip` | failed(1) | 1 | – | – |
| `comm` | ok | 1293 | 39600 | 0 |
| `diff` | ok | 1255 | 39600 | 0 |
| `convert` | ok | 1533 | 29700 | 0 |
| `ffmpeg` | ok | 691 | 19800 | 0 |
| `ln` | ok | 745 | 19800 | 4 |
| `mv` | ok | 598 | 9900 | 0 |
| `chmod` | ok | 71 | 2970 | 0 |
| `dd` | ok | 531 | 10571 | 0 |

`gzip` failed: its grammar file in Caruca's repo defines `gunzip_syntax_spec` instead of `gzip_syntax_spec`, so
Caruca cannot load it (`AttributeError`). Not fixed (v1 code is not edited).

## Full grammars: the suite's commands, where tractable

| Command | Result | Seconds | Traced runs | Runs that hit the 2 s limit |
|---|---|---:|---:|---:|
| `awk` | ok | 83 | 2959 | 0 |
| `tr` | ok | 21 | 924 | 0 |
| `col` | ok | 32 | 1540 | 0 |
| `rev` | ok | 650 | 2178 | 273 |
| `echo` | ok | 16 | 660 | 0 |
| `paste` | ok | 112 | 4279 | 0 |
| `mktemp` | ok | 195 | 6688 | 0 |
| `fmt` | ok | 310 | 9834 | 0 |
| `head` | ok | 222 | 8624 | 0 |
| `cat` | ok | 262 | 11088 | 0 |
| `wc` | ok | 335 | 11396 | 0 |
| `tail` | ok | 843 | 20218 | 330 |
| `seq` | ok | 761 | 28314 | 0 |
| `mkfifo` | ok | 1155 | 36630 | 0 |
| `split` | ok | 1037 | 35211 | 0 |
| `iconv` | ok | 857 | 29667 | 0 |
| `uniq` | ok | 1316 | 42669 | 0 |
| `sed` | ok | 1747 | 50171 | 0 |
| `grep` | failed(137) | 7539 | – | – |
| `ls` | failed(137) | 6149 | – | – |

- `grep` and `ls` were killed by the kernel for lack of memory (exit 137) near the end: the tracer held 7.7 GB and
  6.6 GB. `grep` is rerun alone with 16 GB (`vm1-grep-retry`). `ls` is not rerun: the suite calls `ls` only outside
  the parts PaSh compiles, so its full grammar cannot change a result.
- Not attempted, too large at max-count 2: `comm` (1.96 million runs), `join` (8.0 million), `cp` (64.7 million),
  `diff` (271 million). Their small-grammar files are used in both Caruca sets.
- Already converted on 2026-11-10 and reused: small grammar for `cat cp cut grep rm sort split wc`; full grammar for
  `cut rm sort`.

## Runs that hit the 2 s limit

Most commands have none. `rev`, `pandoc` and Caruca's original `grep` file (2026-11-10) do. To rule out load, `rev`'s
small grammar was traced again on an idle VM (`trace_2`): the same 67 of 1,364 runs timed out and the annotation files
are identical apart from the trace checksum in their header, so the timeouts come from the command, not the setup.
## Update 14:13: `grep` full grammar converted

Retraced alone on the `caruca` VM with 16 GB: ok in 4,592 s (`vm1-grep-retry` in `logs/status.tsv`). Full grammars
now exist for 22 commands: `cut rm sort` (2026-11-10) and `awk tr col rev echo paste mktemp fmt head cat wc tail seq
mkfifo split iconv uniq sed grep` (2026-11-26).

## Repair 14:30: three generated files did not compile

`paste` (small and full grammar) and `awk` (full grammar) raised `TabError`: the converter (task 020's
`annotator/pash_py.py`, `_comment()`) copied a traced example holding a literal newline and tab into a comment.
This is a fault in our converter, not in Caruca's method, so it was repaired like the naive LLM's quoting gap: the
example is now escaped (`\n`, `\t`, `\r`), and the three files were regenerated from their existing traces with
`caruca annotate pash-py` (no retrace). Only the comment changed; the converter's 14 unit tests pass. The edit is
uncommitted on the `pash-python-annotations` branch.
