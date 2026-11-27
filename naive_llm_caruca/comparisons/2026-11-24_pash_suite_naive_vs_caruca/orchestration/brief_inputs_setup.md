# Brief: set up the four Koala groups not yet downloaded

For the `pash-inventory` agent, which wrote `coverage.md`. Tiran decided (2026-11-24) that the full run
covers the six ready groups plus `analytics` (without `port-scan`) and `file-mod`, with `bio.sh` at min
size only and the two `pkg` scripts run once at min size if they can run without outside servers.

## Do

In the Lima VM `pash`, using only Koala's own `install.sh` and `fetch.sh` for each group:

1. `analytics` at small: fetch and install; skip anything only `port-scan` needs (`zannotate`, the Go
   toolchain).
2. `file-mod` at small: fetch and install (the source builds of ImageMagick, libjpeg, libpng, FFmpeg).
3. `bio` at min: install `samtools` and `minimap2`; do **not** let its fetch pull the TERA-Seq data
   (stop if the fetch script would; say what you did instead).
4. `pkg` at min: only if the installer needs no outside package server at run time; otherwise record
   why it was skipped.

Keep at least 5 GB of free disk in the VM at all times; stop and report before any step that would
break that. Then run each group's scripts **once under plain bash** with Koala's own runner and its
hash check (`./execute.sh --small` or `--min`, then `./validate.sh`), to show they run; record wall
time per script. **Do not run PaSh.** Write `orchestration/inputs_setup.md`: per group, what was
downloaded (size), what was installed and how long it took, which scripts ran and matched Koala's hash,
and what failed. Plain words, short.

Do not change the Koala or PaSh checkouts other than through those scripts; do not touch other
workers' folders in the VM (`~/t024*`). Do not commit or push.

## When done

Reply with: the path of `inputs_setup.md`; which scripts are ready to run; what could not be set up.
