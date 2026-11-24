# Setting up the four Koala groups not yet downloaded

Done 2026-11-24, about 11:25–12:10 (VM time; the VM clock was checked against the Mac's and agreed), in
the Lima VM `pash` (ARM processor, 8 CPUs, 8 GiB memory). Only Koala's own install, fetch, run and check
scripts were used, with the one exception noted under `analytics`. No PaSh runs. Free disk went from
17 GB to 9.3 GB, never below the 5 GB floor. The VM was otherwise idle throughout. Logs are in the VM
under `/tmp/inv_*.log`.

"Matches Koala's hash" means the output files have the same checksums Koala ships as its reference
answers.

## Summary

| Group | Size | Downloaded (on disk after unpacking) | Install | Scripts run under bash | Match Koala's hash |
|---|---|---|---|---|---|
| `analytics` | small | about 735 MB (2.0 GB) in 5 min 28 s | system packages only, 17 s | 3 of 3 planned | 2 of 3 |
| `file-mod` | small | about 1.3 GB (2.3 GB) in 10 min 13 s | source builds, 2 min 15 s | 5 of 5 | 2 of 5 |
| `bio` | min | nothing (1 MB copied from Koala's own folder) | `samtools` built, 35 s; `minimap2` failed | 1 of 1 (`bio.sh`) | 1 of 1 |
| `pkg` | min | skipped | skipped | none | none |

All nine scripts that ran finished without error. For the ones that don't match Koala's hash, a second
run gave byte-identical output, so the output is stable in this VM. The plain-bash output from this VM
can therefore serve as the reference for PaSh runs.

## `analytics` (small)

- **Install.** Koala's installer has two parts: system packages, then a Go toolchain built for Intel
  plus `zannotate`, which only `port-scan` uses. I ran the installer's package step exactly as written
  (5 packages were missing; none of them is used by the three scripts we need) and skipped the Go part,
  as the brief says. I did not run the installer file itself, because it would have gone on to download
  the Intel-only Go toolchain.
- **Fetch.** Koala's fetch script, unchanged. It also downloads the two inputs only `port-scan` uses
  (routing table 79 MB, port-scan logs 78 MB); the script has no way to skip them.
- **Runs.** These times are one run each, not the timed measurements.

| Script | Wall time | Matches Koala's hash |
|---|---|---|
| `nginx` | 1.6 s | yes |
| `pcaps` | 126.5 s | **no**: 35 of 69 output files differ. Stable across two runs |
| `ray-tracing` | 0.2 s | yes |

  `pcaps` is all `tcpdump` output. Koala's reference answers were made on Debian 12, and this VM has
  Ubuntu 24.04 with `tcpdump` 4.99.4. A different `tcpdump` version is the likely reason, but I have not
  tested it.

## `file-mod` (small)

- **Install.** Koala's installer, unchanged. It built libjpeg-turbo 2.1.5, libpng 1.6.39, ImageMagick
  6.9.11-60 and FFmpeg 5.1.9 from source and linked them into `/usr/local/legacy-bin`. It took 2 min 15 s,
  including the system packages.
- **Fetch.** Koala's fetch script, unchanged: images 779 MB, captures 1.3 GB, audio 180 MB.
- **Runs.**

| Script | Wall time | Matches Koala's hash |
|---|---|---|
| `compress_files` | 19.7 s | yes |
| `encrypt_files` | 3.3 s | yes |
| `img_convert` | 35.6 s | **no**: 1 of 508 images differs (`112200.jpg`) |
| `to_mp3` | 9.2 s | **no**: 40 of 40 audio files differ |
| `thumbnail_generation` | 24.7 s | **no**: 460 of 508 thumbnails differ |

  Two separate things go wrong with `to_mp3`'s check. First, Koala's check script looks for `ffmpeg` on
  the system path, which in this VM has none; only Koala's run script adds the folder with its own
  `ffmpeg`. So the check cannot work as shipped. Second, when I re-did the check by hand with Koala's own
  `ffmpeg`, all 40 files still differ. The image and audio differences are most likely caused by building
  the same versions on an ARM processor instead of Intel, but I have not tested that. All three gave the
  same output on a second run.

## `bio` (min)

- **Install.** Koala's installer, run at min size. At that size it installs only the system packages,
  `samtools` and `minimap2`, then stops. `samtools` 1.16.1 built fine in 35 s. **`minimap2` failed to
  build**: Koala's installer compiles it with options for Intel processors (`-msse2`, `-msse4.1`), which
  the ARM compiler rejects. `bio.sh` does not use `minimap2`, so this does not block anything in scope.
- **Fetch.** Koala's fetch script at min size copies Koala's own 1 MB sample file and stops before the
  TERA-Seq part (read in the script, and confirmed: nothing was downloaded).
- **Run.** `bio.sh` finished in 0.2 s and all 11 output files match Koala's hash. It prints a warning
  that the sample has no `chrY` data, but the outputs still match.

## `pkg` (min): skipped

Its installer needs two outside package servers: the `makedeb` package server (proget.makedeb.org),
plus the npm registry, which it uses to install the `mir-sa` analysis tool. While it runs, `pacaur` also
fetches signing keys from key servers and package source code from upstream hosts. By the brief's rule,
both `pkg` scripts are skipped. Nothing was downloaded or installed for it.

## Ready to run under PaSh

- `analytics`: `nginx`, `pcaps`, `ray-tracing`, at small.
- `file-mod`: `compress_files`, `encrypt_files`, `img_convert`, `to_mp3`, `thumbnail_generation`, at
  small.
- `bio`: `bio.sh`, at min.

For `pcaps`, `img_convert`, `to_mp3` and `thumbnail_generation`, compare PaSh's output with this VM's
plain-bash output, not with Koala's hashes.
