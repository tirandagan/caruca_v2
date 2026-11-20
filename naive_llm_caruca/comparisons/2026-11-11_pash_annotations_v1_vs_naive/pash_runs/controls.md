# Checks that PaSh is really running, and really reading the files it is given

Run inside the virtual machine `pash` before the batch (2026-11-19 16:46:15 -0500) and again after it (2026-11-19 17:28:20 -0500).

Installed: PaSh commit `42a8b87c`, pash-annotations 0.2.4, sort (GNU coreutils) 9.4, 8 cores, Linux 6.8.0-147-generic aarch64.

"Copies started" is the stand-in program's count of how many copies of the watched command ran.

| Check | Script | Command watched | Expected | Before the batch | After the batch | PaSh's reason or error |
|---|---|---|---|---|---|---|
| A script known to split, with PaSh's installed files | `cat in.txt \| grep '\(.\).*\1\(.\).*\2' \| wc -l` | grep | split | split; copies started: 8; output same as bash: yes | same |  |
| The same script, with an untouched copy of those files given as a folder | `cat in.txt \| grep '\(.\).*\1\(.\).*\2' \| wc -l` | grep | split | split; copies started: 8; output same as bash: yes | same |  |
| The same script, with grep's files removed from the folder copy | `cat in.txt \| grep '\(.\).*\1\(.\).*\2' \| wc -l` | grep | not split | not split; copies started: 1; output same as bash: yes | same | Daemon:  WARNING: Exception caught because some region(s) are unparallelizable: InputOutputInformation for grep not provided so considered side-effect |
| `sort -n -u` with v1's main-grammar sort files (they allow the split) | `cat in.txt \| sort -n -u` | sort | split, output differs from bash | split; copies started: 8; output same as bash: **no** | same |  |
| `sort -n -u` with PaSh's own sort files | `cat in.txt \| sort -n -u` | sort | output same as bash | not split; copies started: 1; output same as bash: yes | same |  |
| This morning's script, ending in `head -5` | `cat in.txt \| sort -n \| uniq -c \| sort -rn \| head -5` | sort | PaSh error (ran as plain bash) | PaSh error; copies started: 2; output same as bash: yes | same | AssertionError @ ir.py:596 pipe_append |
| The same script, ending in `head -n 5` | `cat in.txt \| sort -n \| uniq -c \| sort -rn \| head -n 5` | sort | split | split; copies started: 30; output same as bash: yes | same |  |
| Input given with `< file` | `cut -d ' ' -f 1 < in.txt` | cut | PaSh error | PaSh error; copies started: 1; output same as bash: yes | same | NotImplementedError @ dfg_node.py:210 apply_redirections |

## Each side's folder gives the answers we expect

Every line of task 021's comparison was put to every side's files inside the virtual machine, through the same folder PaSh is pointed at. **84,193 of 84,193 answers are identical** to the ones recorded on the Mac on 2026-11-11.

## During the batch

- Runs where a side's files did not allow a split and PaSh split anyway: **0 of 2,377**.
- Runs with no log, or whose two signals disagreed: **0**.
- Runs with the "no annotation" control that split: **0 of 382**.
