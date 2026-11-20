#!/bin/bash
# Reproducers for the PaSh behaviours listed in pash_bugs_for_review.md (task 022).
# Run inside the Lima VM `pash`:   bash -l pash_bug_repros.sh < /dev/null
# Uses PaSh exactly as installed: no annotation folder is passed, nothing in PaSh is changed.
# For each case: the script, bash's result, PaSh's result, and the last error in PaSh's log.
set -u
D=$(mktemp -d); trap 'rm -rf "$D"' EXIT; cd "$D" || exit 1
PA="$PASH_TOP/pa.sh"
echo "PaSh $(cd "$PASH_TOP" && git rev-parse --short HEAD), pash-annotations $("$PASH_TOP/../../python_pkgs/bin/pip" show pash-annotations 2>/dev/null | sed -n 2p), $(sort --version | head -1)"

# input: 200,000 lines, about 6 MB, so PaSh hands out several 1 MB pieces
awk 'BEGIN{srand(7); for(i=1;i<=200000;i++) printf "%d line%d ab,cd:%d\tfield2\n", int(rand()*1000), i, i%97}' > in.txt
cp in.txt in2.txt; mkdir -p d/sub; cp in.txt d/part1.txt; head -3 in.txt > d/sub/part2.txt; echo ab > pats

case_() {  # id, title, script text
  local id=$1 title=$2; shift 2
  printf '%s\n' "$1" > "$id.sh"
  # standard input is closed on purpose: in case W5 PaSh makes grep read it
  bash "$id.sh" > "$id.bash.out" 2> "$id.bash.err" < /dev/null; local brc=$?
  "$PA" -w 8 -d 2 --log_file "$id.log" "$id.sh" > "$id.pash.out" 2> "$id.pash.err" < /dev/null; local prc=$?
  local same="SAME"; cmp -s "$id.bash.out" "$id.pash.out" || same="DIFFERENT"
  local split="no"; [ "$(grep -c 'runtime/r_split \|runtime/split ' "$id.log" 2>/dev/null)" -gt 0 ] && split="yes"
  local err; err=$(grep -E '^[A-Za-z]+Error|^NotImplementedError|^AssertionError' "$id.log" 2>/dev/null | tail -1)
  local where; where=$(grep -E '^  File ' "$id.log" 2>/dev/null | tail -1 | sed -E 's/.*\/([^/"]+)", line ([0-9]+), in (.*)/\1:\2 \3/')
  echo
  echo "[$id] $title"
  echo "    script : $1"
  echo "    bash   : exit $brc, $(wc -l < "$id.bash.out") lines, $(wc -c < "$id.bash.out") bytes"
  echo "    PaSh   : exit $prc, $(wc -l < "$id.pash.out") lines, $(wc -c < "$id.pash.out") bytes  -> output $same, split steps in log: $split"
  [ -n "$err" ] && echo "    PaSh log: $err  ($where)"
  [ -s "$id.log" ] || echo "    PaSh log: none written; stderr: $(tail -c 200 "$id.pash.err" | tr '\n' ' ')"
}

echo; echo "===== wrong output ====="
case_ W1 "grep -m is split, though PaSh's own comment says it must not be" "cat in.txt | grep -m 5 ab"
case_ W2 "grep -A is split, same cause"                                      "cat in.txt | grep -A 1 ':96'"
case_ W3 "cut -z is split on newlines"                                       "cat in.txt | cut -z -c 1-3"
case_ W4 "recursive grep on a folder returns nothing"                        "grep -r 'line7 ' d"
case_ W5 "grep --color swallows the pattern"                                 "grep --color 'line7 ' in.txt"
case_ W6 "a line asking for --help is split, help printed once per worker"   "cat in.txt | sort -k 1 --help"
case_ W7 "double-quoted pattern (seen 2026-10-05)"                           'cat in.txt | grep "\(.\).*\1\(.\).*\2\(.\).*\3" | wc -l'
case_ W7b "same pattern, single quotes"                                      "cat in.txt | grep '\(.\).*\1\(.\).*\2\(.\).*\3' | wc -l"

echo; echo "===== PaSh's compiler raises an exception and the script runs as plain bash ====="
case_ E1 "name used but never imported (option value typed as a file)"       "grep -f pats in.txt"
case_ E2 "value attached to its option is read as a file name"               "cat in.txt | cut -d, -f1"
case_ E2b "same line with the values separated: splits"                      "cat in.txt | cut -d , -f 1"
case_ E3 "head -5 (old-style count)"                                         "cat in.txt | sort -n | head -5"
case_ E3b "head -n 5: splits"                                                "cat in.txt | sort -n | head -n 5"
case_ E4 "two input files"                                                   "grep 'line7 ' in.txt in2.txt"
case_ E5 "input redirection"                                                 "cut -d , -f 1 < in.txt"
case_ E6 "tail -n 1 at the end of a pipeline"                                "cat in.txt | sort -r | tail -n 1"
case_ E6b "the same pipeline without tail: splits"                           "cat in.txt | sort -r"
# PaSh's own benchmark script, unchanged, reading this input
B="$PASH_TOP/../../evaluation/benchmarks/oneliners"; cp "$B/bi-gram.aux.sh" .; export IN="$D/in.txt"
case_ E7 "PaSh's own benchmark oneliners/bi-grams.sh"                        "$(cat "$B/bi-grams.sh")"

echo; echo "===== other ====="
"$PA" -w 8 does_not_exist.sh > /dev/null 2> missing.err < /dev/null; echo "[O1] script file that does not exist: exit $?, stderr: $(tail -c 160 missing.err | tr '\n' ' ')"
