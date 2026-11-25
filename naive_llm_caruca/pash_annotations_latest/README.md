# The naive LLM's PaSh annotation files, latest run per command

One folder per command for which the naive LLM (a fresh Claude Code session given only the binary, its manual and the format descriptions) has written PaSh annotation files. Each folder holds byte-for-byte copies of the PaSh output folder of that command's **latest** run (`output/annotation/`, or `output/pash/` in the October pilot runs); the run's syntax file (`output/<cmd>.py`) is not copied. Nothing here is edited: the run folders under `../runs/` stay the record, and this folder is rebuilt from them by `refresh.py`.

84 commands, from 101 run folders. Cost: "billed" is what the billing service charged (campaign ledger); "Claude Code's figure" is Claude Code's own estimate, used where no bill is available; "run log" is the cost in the run table of `../README.md` (pilot runs, which predate the ledger).

| Command | Files | Run folder | Run date | Prompt | Cost | Note |
|---|---|---|---|---|---|---|
| `awk` | 3: `InputOutputInfoGeneratorAwk.py`, `ParallelizabilityInfoGeneratorAwk.py`, `awk.json` | [2026-11-24_115222…](../runs/2026-11-24_115222_naive-run-awk_awk_PROMPT_v1/) | 2026-11-24 | PROMPT_v1 | $4.32 (Claude Code's figure) |  |
| `b2sum` | 3: `InputOutputInfoGeneratorB2sum.py`, `ParallelizabilityInfoGeneratorB2sum.py`, `b2sum.json` | [2026-10-28_105421…](../runs/2026-10-28_105421_naive-run-b2sum_b2sum_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.32 (billed) |  |
| `basenc` | 3: `InputOutputInfoGeneratorBasenc.py`, `ParallelizabilityInfoGeneratorBasenc.py`, `basenc.json` | [2026-10-28_111031…](../runs/2026-10-28_111031_naive-run-basenc_basenc_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.74 (billed) |  |
| `bc` | 3: `InputOutputInfoGeneratorBc.py`, `ParallelizabilityInfoGeneratorBc.py`, `bc.json` | [2026-10-28_084323…](../runs/2026-10-28_084323_naive-run-bc_bc_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.78 (billed) |  |
| `binwalk` | 3: `InputOutputInfoGeneratorBinwalk.py`, `ParallelizabilityInfoGeneratorBinwalk.py`, `binwalk.json` | [2026-10-20_133813…](../runs/2026-10-20_133813_naive-run-binwalk_binwalk_PROMPT_v1/) | 2026-10-20 | PROMPT_v1 | $2.12 (run log) | older layout `output/pash/` |
| `cat` | 3: `InputOutputInfoGeneratorCat.py`, `ParallelizabilityInfoGeneratorCat.py`, `cat.json` | [2026-10-28_100411…](../runs/2026-10-28_100411_naive-run-cat_cat_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.33 (billed) |  |
| `chcon` | 3: `InputOutputInfoGeneratorChcon.py`, `ParallelizabilityInfoGeneratorChcon.py`, `chcon.json` | [2026-10-28_125939…](../runs/2026-10-28_125939_naive-run-chcon_chcon_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.42 (billed) |  |
| `chgrp` | 3: `InputOutputInfoGeneratorChgrp.py`, `ParallelizabilityInfoGeneratorChgrp.py`, `chgrp.json` | [2026-10-28_114550…](../runs/2026-10-28_114550_naive-run-chgrp_chgrp_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.20 (billed) |  |
| `chmod` | 3: `InputOutputInfoGeneratorChmod.py`, `ParallelizabilityInfoGeneratorChmod.py`, `chmod.json` | [2026-10-28_112202…](../runs/2026-10-28_112202_naive-run-chmod_chmod_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.33 (billed) |  |
| `chown` | 3: `InputOutputInfoGeneratorChown.py`, `ParallelizabilityInfoGeneratorChown.py`, `chown.json` | [2026-10-28_115536…](../runs/2026-10-28_115536_naive-run-chown_chown_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.33 (billed) |  |
| `chroot` | 3: `InputOutputInfoGeneratorChroot.py`, `ParallelizabilityInfoGeneratorChroot.py`, `chroot.json` | [2026-10-28_083453…](../runs/2026-10-28_083453_naive-run-chroot_chroot_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.11 (billed) |  |
| `col` | 3: `InputOutputInfoGeneratorCol.py`, `ParallelizabilityInfoGeneratorCol.py`, `col.json` | [2026-10-28_093614…](../runs/2026-10-28_093614_naive-run-col_col_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.68 (billed) |  |
| `comm` | 3: `InputOutputInfoGeneratorComm.py`, `ParallelizabilityInfoGeneratorComm.py`, `comm.json` | [2026-10-28_111854…](../runs/2026-10-28_111854_naive-run-comm_comm_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.75 (billed) |  |
| `convert` | 3: `InputOutputInfoGeneratorConvert.py`, `ParallelizabilityInfoGeneratorConvert.py`, `convert.json` | [2026-10-27_231631…](../runs/2026-10-27_231631_naive-run-convert_convert_PROMPT_v1/) | 2026-10-27 | PROMPT_v1 | $4.10 (billed) |  |
| `cp` | 3: `InputOutputInfoGeneratorCp.py`, `ParallelizabilityInfoGeneratorCp.py`, `cp.json` | [2026-10-28_153913…](../runs/2026-10-28_153913_naive-run-cp-r3_cp_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.55 (billed) | repeat 3 |
| `csplit` | 3: `InputOutputInfoGeneratorCsplit.py`, `ParallelizabilityInfoGeneratorCsplit.py`, `csplit.json` | [2026-10-28_104909…](../runs/2026-10-28_104909_naive-run-csplit_csplit_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.84 (billed) |  |
| `cut` | 3: `InputOutputInfoGeneratorCut.py`, `ParallelizabilityInfoGeneratorCut.py`, `cut.json` | [2026-10-28_152550…](../runs/2026-10-28_152550_naive-run-cut-r3_cut_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.03 (billed) | repeat 3 |
| `date` | 3: `InputOutputInfoGeneratorDate.py`, `ParallelizabilityInfoGeneratorDate.py`, `date.json` | [2026-10-28_111357…](../runs/2026-10-28_111357_naive-run-date_date_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.17 (billed) |  |
| `dd` | 3: `InputOutputInfoGeneratorDd.py`, `ParallelizabilityInfoGeneratorDd.py`, `dd.json` | [2026-10-28_153005…](../runs/2026-10-28_153005_naive-run-dd-r3_dd_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.96 (billed) | repeat 3 |
| `df` | 3: `InputOutputInfoGeneratorDf.py`, `ParallelizabilityInfoGeneratorDf.py`, `df.json` | [2026-10-28_125544…](../runs/2026-10-28_125544_naive-run-df_df_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.01 (billed) |  |
| `diff` | 3: `InputOutputInfoGeneratorDiff.py`, `ParallelizabilityInfoGeneratorDiff.py`, `diff.json` | [2026-10-28_115007…](../runs/2026-10-28_115007_naive-run-diff_diff_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.65 (billed) |  |
| `dir` | 3: `InputOutputInfoGeneratorDir.py`, `ParallelizabilityInfoGeneratorDir.py`, `dir.json` | [2026-10-28_143025…](../runs/2026-10-28_143025_naive-run-dir_dir_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.13 (billed) |  |
| `dirname` | 3: `InputOutputInfoGeneratorDirname.py`, `ParallelizabilityInfoGeneratorDirname.py`, `dirname.json` | [2026-10-26_191443…](../runs/2026-10-26_191443_naive-run-dirname_dirname_PROMPT_v1/) | 2026-10-26 | PROMPT_v1 | $0.88 (run log) | pilot run (before the campaign ledger); older layout `output/pash/` |
| `du` | 3: `InputOutputInfoGeneratorDu.py`, `ParallelizabilityInfoGeneratorDu.py`, `du.json` | [2026-10-28_141545…](../runs/2026-10-28_141545_naive-run-du_du_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.06 (billed) |  |
| `env` | 3: `InputOutputInfoGeneratorEnv.py`, `ParallelizabilityInfoGeneratorEnv.py`, `env.json` | [2026-10-28_121513…](../runs/2026-10-28_121513_naive-run-env_env_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.96 (billed) |  |
| `expand` | 3: `InputOutputInfoGeneratorExpand.py`, `ParallelizabilityInfoGeneratorExpand.py`, `expand.json` | [2026-10-28_083113…](../runs/2026-10-28_083113_naive-run-expand_expand_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.89 (billed) |  |
| `fmt` | 3: `InputOutputInfoGeneratorFmt.py`, `ParallelizabilityInfoGeneratorFmt.py`, `fmt.json` | [2026-10-28_104147…](../runs/2026-10-28_104147_naive-run-fmt_fmt_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.12 (billed) |  |
| `fold` | 3: `InputOutputInfoGeneratorFold.py`, `ParallelizabilityInfoGeneratorFold.py`, `fold.json` | [2026-10-28_081910…](../runs/2026-10-28_081910_naive-run-fold_fold_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.24 (billed) |  |
| `grep` | 3: `InputOutputInfoGeneratorGrep.py`, `ParallelizabilityInfoGeneratorGrep.py`, `grep.json` | [2026-10-28_135447…](../runs/2026-10-28_135447_naive-run-grep_grep_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.49 (billed) |  |
| `head` | 3: `InputOutputInfoGeneratorHead.py`, `ParallelizabilityInfoGeneratorHead.py`, `head.json` | [2026-10-28_151834…](../runs/2026-10-28_151834_naive-run-head-r3_head_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.21 (billed) | repeat 3 |
| `iconv` | 3: `InputOutputInfoGeneratorIconv.py`, `ParallelizabilityInfoGeneratorIconv.py`, `iconv.json` | [2026-10-28_110404…](../runs/2026-10-28_110404_naive-run-iconv_iconv_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.91 (billed) |  |
| `id` | 3: `InputOutputInfoGeneratorId.py`, `ParallelizabilityInfoGeneratorId.py`, `id.json` | [2026-10-28_093251…](../runs/2026-10-28_093251_naive-run-id_id_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.49 (billed) |  |
| `install` | 3: `InputOutputInfoGeneratorInstall.py`, `ParallelizabilityInfoGeneratorInstall.py`, `install.json` | [2026-10-28_140311…](../runs/2026-10-28_140311_naive-run-install_install_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.42 (billed) |  |
| `join` | 3: `InputOutputInfoGeneratorJoin.py`, `ParallelizabilityInfoGeneratorJoin.py`, `join.json` | [2026-10-28_132048…](../runs/2026-10-28_132048_naive-run-join_join_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.25 (billed) |  |
| `kill` | 3: `InputOutputInfoGeneratorKill.py`, `ParallelizabilityInfoGeneratorKill.py`, `kill.json` | [2026-10-28_120050…](../runs/2026-10-28_120050_naive-run-kill_kill_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.75 (billed) |  |
| `ln` | 3: `InputOutputInfoGeneratorLn.py`, `ParallelizabilityInfoGeneratorLn.py`, `ln.json` | [2026-10-28_130353…](../runs/2026-10-28_130353_naive-run-ln_ln_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.83 (billed) |  |
| `ls` | 3: `InputOutputInfoGeneratorLs.py`, `ParallelizabilityInfoGeneratorLs.py`, `ls.json` | [2026-10-27_225849…](../runs/2026-10-27_225849_naive-run-ls_ls_PROMPT_v1/) | 2026-10-27 | PROMPT_v1 | $2.42 (billed) |  |
| `md5sum` | 3: `InputOutputInfoGeneratorMd5sum.py`, `ParallelizabilityInfoGeneratorMd5sum.py`, `md5sum.json` | [2026-10-28_103723…](../runs/2026-10-28_103723_naive-run-md5sum_md5sum_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.06 (billed) |  |
| `mkdir` | 3: `InputOutputInfoGeneratorMkdir.py`, `ParallelizabilityInfoGeneratorMkdir.py`, `mkdir.json` | [2026-10-28_094955…](../runs/2026-10-28_094955_naive-run-mkdir_mkdir_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.74 (billed) |  |
| `mkfifo` | 3: `InputOutputInfoGeneratorMkfifo.py`, `ParallelizabilityInfoGeneratorMkfifo.py`, `mkfifo.json` | [2026-10-28_082734…](../runs/2026-10-28_082734_naive-run-mkfifo_mkfifo_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.76 (billed) |  |
| `mknod` | 3: `InputOutputInfoGeneratorMknod.py`, `ParallelizabilityInfoGeneratorMknod.py`, `mknod.json` | [2026-10-28_120953…](../runs/2026-10-28_120953_naive-run-mknod_mknod_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.21 (billed) |  |
| `mktemp` | 3: `InputOutputInfoGeneratorMktemp.py`, `ParallelizabilityInfoGeneratorMktemp.py`, `mktemp.json` | [2026-10-28_092028…](../runs/2026-10-28_092028_naive-run-mktemp_mktemp_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.59 (billed) |  |
| `mogrify` | 3: `InputOutputInfoGeneratorMogrify.py`, `ParallelizabilityInfoGeneratorMogrify.py`, `mogrify.json` | [2026-10-28_084707…](../runs/2026-10-28_084707_naive-run-mogrify_mogrify_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $4.97 (billed) |  |
| `mv` | 3: `InputOutputInfoGeneratorMv.py`, `ParallelizabilityInfoGeneratorMv.py`, `mv.json` | [2026-10-28_123450…](../runs/2026-10-28_123450_naive-run-mv_mv_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.03 (billed) |  |
| `nl` | 3: `InputOutputInfoGeneratorNl.py`, `ParallelizabilityInfoGeneratorNl.py`, `nl.json` | [2026-10-28_131454…](../runs/2026-10-28_131454_naive-run-nl_nl_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.40 (billed) |  |
| `numfmt` | 3: `InputOutputInfoGeneratorNumfmt.py`, `ParallelizabilityInfoGeneratorNumfmt.py`, `numfmt.json` | [2026-10-28_135110…](../runs/2026-10-28_135110_naive-run-numfmt_numfmt_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.87 (billed) |  |
| `od` | 3: `InputOutputInfoGeneratorOd.py`, `ParallelizabilityInfoGeneratorOd.py`, `od.json` | [2026-10-28_132554…](../runs/2026-10-28_132554_naive-run-od_od_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.99 (billed) |  |
| `pandoc` | 3: `InputOutputInfoGeneratorPandoc.py`, `ParallelizabilityInfoGeneratorPandoc.py`, `pandoc.json` | [2026-10-28_144226…](../runs/2026-10-28_144226_naive-run-pandoc_pandoc_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.82 (billed) |  |
| `pinky` | 3: `InputOutputInfoGeneratorPinky.py`, `ParallelizabilityInfoGeneratorPinky.py`, `pinky.json` | [2026-10-28_094246…](../runs/2026-10-28_094246_naive-run-pinky_pinky_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.58 (billed) |  |
| `pr` | 3: `InputOutputInfoGeneratorPr.py`, `ParallelizabilityInfoGeneratorPr.py`, `pr.json` | [2026-10-28_142022…](../runs/2026-10-28_142022_naive-run-pr_pr_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.44 (billed) |  |
| `ptx` | 3: `InputOutputInfoGeneratorPtx.py`, `ParallelizabilityInfoGeneratorPtx.py`, `ptx.json` | [2026-10-28_130800…](../runs/2026-10-28_130800_naive-run-ptx_ptx_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.13 (billed) |  |
| `readlink` | 3: `InputOutputInfoGeneratorReadlink.py`, `ParallelizabilityInfoGeneratorReadlink.py`, `readlink.json` | [2026-10-28_101249…](../runs/2026-10-28_101249_naive-run-readlink_readlink_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.12 (billed) |  |
| `rev` | 3: `InputOutputInfoGeneratorRev.py`, `ParallelizabilityInfoGeneratorRev.py`, `rev.json` | [2026-10-28_090550…](../runs/2026-10-28_090550_naive-run-rev_rev_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.58 (billed) |  |
| `rm` | 3: `InputOutputInfoGeneratorRm.py`, `ParallelizabilityInfoGeneratorRm.py`, `rm.json` | [2026-10-28_105951…](../runs/2026-10-28_105951_naive-run-rm_rm_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.97 (billed) |  |
| `runcon` | 3: `InputOutputInfoGeneratorRuncon.py`, `ParallelizabilityInfoGeneratorRuncon.py`, `runcon.json` | [2026-10-28_083856…](../runs/2026-10-28_083856_naive-run-runcon_runcon_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.21 (billed) |  |
| `sed` | 3: `InputOutputInfoGeneratorSed.py`, `ParallelizabilityInfoGeneratorSed.py`, `sed.json` | [2026-11-24_125757…](../runs/2026-11-24_125757_naive-run-sed-r2_sed_PROMPT_v1/) | 2026-11-24 | PROMPT_v1 | $4.64 (Claude Code's figure) | repeat 2, after the format-document repair (PaSh keeps quotes on operands) |
| `seq` | 3: `InputOutputInfoGeneratorSeq.py`, `ParallelizabilityInfoGeneratorSeq.py`, `seq.json` | [2026-10-28_095809…](../runs/2026-10-28_095809_naive-run-seq_seq_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.70 (billed) |  |
| `sha1sum` | 3: `InputOutputInfoGeneratorSha1sum.py`, `ParallelizabilityInfoGeneratorSha1sum.py`, `sha1sum.json` | [2026-10-28_103316…](../runs/2026-10-28_103316_naive-run-sha1sum_sha1sum_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.91 (billed) |  |
| `sha224sum` | 3: `InputOutputInfoGeneratorSha224sum.py`, `ParallelizabilityInfoGeneratorSha224sum.py`, `sha224sum.json` | [2026-10-28_102417…](../runs/2026-10-28_102417_naive-run-sha224sum_sha224sum_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.60 (billed) |  |
| `sha256sum` | 3: `InputOutputInfoGeneratorSha256sum.py`, `ParallelizabilityInfoGeneratorSha256sum.py`, `sha256sum.json` | [2026-10-28_101707…](../runs/2026-10-28_101707_naive-run-sha256sum_sha256sum_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.92 (billed) |  |
| `sha384sum` | 3: `InputOutputInfoGeneratorSha384sum.py`, `ParallelizabilityInfoGeneratorSha384sum.py`, `sha384sum.json` | [2026-10-28_102715…](../runs/2026-10-28_102715_naive-run-sha384sum_sha384sum_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.04 (billed) |  |
| `sha512sum` | 3: `InputOutputInfoGeneratorSha512sum.py`, `ParallelizabilityInfoGeneratorSha512sum.py`, `sha512sum.json` | [2026-10-28_102118…](../runs/2026-10-28_102118_naive-run-sha512sum_sha512sum_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.82 (billed) |  |
| `shred` | 3: `InputOutputInfoGeneratorShred.py`, `ParallelizabilityInfoGeneratorShred.py`, `shred.json` | [2026-10-28_113129…](../runs/2026-10-28_113129_naive-run-shred_shred_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.96 (billed) |  |
| `shuf` | 3: `InputOutputInfoGeneratorShuf.py`, `ParallelizabilityInfoGeneratorShuf.py`, `shuf.json` | [2026-10-28_113528…](../runs/2026-10-28_113528_naive-run-shuf_shuf_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.31 (billed) |  |
| `sort` | 3: `InputOutputInfoGeneratorSort.py`, `ParallelizabilityInfoGeneratorSort.py`, `sort.json` | [2026-10-28_154444…](../runs/2026-10-28_154444_naive-run-sort-r3_sort_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.58 (billed) | repeat 3 |
| `split` | 3: `InputOutputInfoGeneratorSplit.py`, `ParallelizabilityInfoGeneratorSplit.py`, `split.json` | [2026-10-28_134035…](../runs/2026-10-28_134035_naive-run-split_split_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.82 (billed) |  |
| `stat` | 3: `InputOutputInfoGeneratorStat.py`, `ParallelizabilityInfoGeneratorStat.py`, `stat.json` | [2026-10-28_100917…](../runs/2026-10-28_100917_naive-run-stat_stat_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.93 (billed) |  |
| `tail` | 3: `InputOutputInfoGeneratorTail.py`, `ParallelizabilityInfoGeneratorTail.py`, `tail.json` | [2026-10-28_122555…](../runs/2026-10-28_122555_naive-run-tail_tail_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.89 (billed) |  |
| `tee` | 3: `InputOutputInfoGeneratorTee.py`, `ParallelizabilityInfoGeneratorTee.py`, `tee.json` | [2026-10-28_082342…](../runs/2026-10-28_082342_naive-run-tee_tee_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.83 (billed) |  |
| `test` | 3: `InputOutputInfoGeneratorTest.py`, `ParallelizabilityInfoGeneratorTest.py`, `test.json` | [2026-10-27_230951…](../runs/2026-10-27_230951_naive-run-test_test_PROMPT_v1/) | 2026-10-27 | PROMPT_v1 | $1.87 (billed) |  |
| `timeout` | 3: `InputOutputInfoGeneratorTimeout.py`, `ParallelizabilityInfoGeneratorTimeout.py`, `timeout.json` | [2026-10-28_100100…](../runs/2026-10-28_100100_naive-run-timeout_timeout_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.72 (billed) |  |
| `touch` | 3: `InputOutputInfoGeneratorTouch.py`, `ParallelizabilityInfoGeneratorTouch.py`, `touch.json` | [2026-10-28_112717…](../runs/2026-10-28_112717_naive-run-touch_touch_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.86 (billed) |  |
| `tr` | 3: `InputOutputInfoGeneratorTr.py`, `ParallelizabilityInfoGeneratorTr.py`, `tr.json` | [2026-11-24_114025…](../runs/2026-11-24_114025_naive-run-tr_tr_PROMPT_v1/) | 2026-11-24 | PROMPT_v1 | $1.87 (Claude Code's figure) |  |
| `truncate` | 3: `InputOutputInfoGeneratorTruncate.py`, `ParallelizabilityInfoGeneratorTruncate.py`, `truncate.json` | [2026-10-28_094521…](../runs/2026-10-28_094521_naive-run-truncate_truncate_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.26 (billed) |  |
| `uglifyjs` | 3: `InputOutputInfoGeneratorUglifyjs.py`, `ParallelizabilityInfoGeneratorUglifyjs.py`, `uglifyjs.json` | [2026-10-28_133241…](../runs/2026-10-28_133241_naive-run-uglifyjs_uglifyjs_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.00 (billed) |  |
| `uname` | 3: `InputOutputInfoGeneratorUname.py`, `ParallelizabilityInfoGeneratorUname.py`, `uname.json` | [2026-10-28_092528…](../runs/2026-10-28_092528_naive-run-uname_uname_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.00 (billed) |  |
| `unexpand` | 3: `InputOutputInfoGeneratorUnexpand.py`, `ParallelizabilityInfoGeneratorUnexpand.py`, `unexpand.json` | [2026-10-28_091112…](../runs/2026-10-28_091112_naive-run-unexpand_unexpand_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.71 (billed) |  |
| `uniq` | 3: `InputOutputInfoGeneratorUniq.py`, `ParallelizabilityInfoGeneratorUniq.py`, `uniq.json` | [2026-10-28_123910…](../runs/2026-10-28_123910_naive-run-uniq_uniq_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.60 (billed) |  |
| `unzip` | 3: `InputOutputInfoGeneratorUnzip.py`, `ParallelizabilityInfoGeneratorUnzip.py`, `unzip.json` | [2026-10-28_143438…](../runs/2026-10-28_143438_naive-run-unzip_unzip_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $2.99 (billed) |  |
| `vdir` | 3: `InputOutputInfoGeneratorVdir.py`, `ParallelizabilityInfoGeneratorVdir.py`, `vdir.json` | [2026-10-28_142559…](../runs/2026-10-28_142559_naive-run-vdir_vdir_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.16 (billed) |  |
| `wc` | 3: `InputOutputInfoGeneratorWc.py`, `ParallelizabilityInfoGeneratorWc.py`, `wc.json` | [2026-10-28_091448…](../runs/2026-10-28_091448_naive-run-wc_wc_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.13 (billed) |  |
| `who` | 3: `InputOutputInfoGeneratorWho.py`, `ParallelizabilityInfoGeneratorWho.py`, `who.json` | [2026-10-28_122120…](../runs/2026-10-28_122120_naive-run-who_who_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $1.01 (billed) |  |
| `xargs` | 3: `InputOutputInfoGeneratorXargs.py`, `ParallelizabilityInfoGeneratorXargs.py`, `xargs.json` | [2026-11-24_114448…](../runs/2026-11-24_114448_naive-run-xargs_xargs_PROMPT_v1/) | 2026-11-24 | PROMPT_v1 | $3.04 (Claude Code's figure) |  |
| `yes` | 3: `InputOutputInfoGeneratorYes.py`, `ParallelizabilityInfoGeneratorYes.py`, `yes.json` | [2026-10-28_104621…](../runs/2026-10-28_104621_naive-run-yes_yes_PROMPT_v1/) | 2026-10-28 | PROMPT_v1 | $0.64 (billed) |  |

## Runs without PaSh files

None: every run folder has a PaSh output folder with files in it.

## Superseded runs

Older runs of a command that has a later one. Their files are not copied here.

- `convert`: [2026-10-20_135842…](../runs/2026-10-20_135842_naive-run-convert_convert_PROMPT_v1/) (2026-10-20)
- `cp`: [2026-10-28_114133…](../runs/2026-10-28_114133_naive-run-cp_cp_PROMPT_v1/) (2026-10-28)
- `cp`: [2026-10-28_150709…](../runs/2026-10-28_150709_naive-run-cp-r2_cp_PROMPT_v1/) (2026-10-28)
- `cut`: [2026-10-20_135253…](../runs/2026-10-20_135253_naive-run-cut_cut_PROMPT_v1/) (2026-10-20)
- `cut`: [2026-10-27_230555…](../runs/2026-10-27_230555_naive-run-cut_cut_PROMPT_v1/) (2026-10-27)
- `cut`: [2026-10-28_145447…](../runs/2026-10-28_145447_naive-run-cut-r2_cut_PROMPT_v1/) (2026-10-28)
- `dd`: [2026-10-27_225152…](../runs/2026-10-27_225152_naive-run-dd_dd_PROMPT_v1/) (2026-10-27)
- `dd`: [2026-10-28_145937…](../runs/2026-10-28_145937_naive-run-dd-r2_dd_PROMPT_v1/) (2026-10-28)
- `grep`: [2026-10-13_193448…](../runs/2026-10-13_193448_naive-run-grep_grep_PROMPT_v1/) (2026-10-13)
- `grep`: [2026-10-20_112956…](../runs/2026-10-20_112956_naive-run-grep-noweb_grep_PROMPT_v1/) (2026-10-20)
- `head`: [2026-10-28_095255…](../runs/2026-10-28_095255_naive-run-head_head_PROMPT_v1/) (2026-10-28)
- `head`: [2026-10-28_144919…](../runs/2026-10-28_144919_naive-run-head-r2_head_PROMPT_v1/) (2026-10-28)
- `rm`: [2026-10-20_121932…](../runs/2026-10-20_121932_naive-run-rm_rm_PROMPT_v1/) (2026-10-20)
- `sed`: [2026-10-28_124823…](../runs/2026-10-28_124823_naive-run-sed_sed_PROMPT_v1/) (2026-10-28): its file misreads quoted scripts because the format document never said PaSh keeps the quotes (an instrument gap, see [judgment_errors.md](../runs/2026-11-24_pash_koala_naive_vs_pash/orchestration/judgment_errors.md), section 1); re-run as repeat 2
- `sort`: [2026-10-20_160340…](../runs/2026-10-20_160340_naive-run-sort_sort_PROMPT_v1/) (2026-10-20)
- `sort`: [2026-10-28_140825…](../runs/2026-10-28_140825_naive-run-sort_sort_PROMPT_v1/) (2026-10-28)
- `sort`: [2026-10-28_151151…](../runs/2026-10-28_151151_naive-run-sort-r2_sort_PROMPT_v1/) (2026-10-28)

## How to refresh

Run `python3 naive_llm_caruca/pash_annotations_latest/refresh.py` from the repository root (add `--dry-run` to see what it would copy). It scans every `runs/*_naive-run-*_PROMPT_v*` folder, takes the command from `run.env` (checked against the folder name), finds the PaSh folder (`output/annotation/` or `output/pash/`), keeps the run with the newest timestamp per command, deletes and recreates the command folders here, copies the files with their times kept (no `__pycache__`), and rewrites this README. Costs come from `fig7_campaign/ledger.jsonl`, or for pilot runs from `../README.md`. Notes on particular runs (such as why a run was superseded) live in `RUN_NOTES` and `SUPERSEDED_WHY` at the top of the script; add one there when a run is re-done for a reason.
