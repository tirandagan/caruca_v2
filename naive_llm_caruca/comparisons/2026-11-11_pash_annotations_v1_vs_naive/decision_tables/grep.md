# Decision table: grep

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `naive:2026-10-13_193448`, `naive:2026-10-20_112956`, `naive:2026-10-28_135447`, `pash-own`, `v1-pash`

### 59 line(s) — sides differ; from {'C-naive': 59}
Examples: `grep -y FOO a.txt`; `grep -u foo a.txt`; `grep -d x o a.txt`; `grep -D x o a.txt`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 43 line(s) — sides differ; from {'C-naive': 43}
Examples: `grep --binary-files=x o a.txt`; `grep --color=x o a.txt`; `grep --ext fo+ a.txt`; `grep --no-group-separator=x foo a.txt`

- **naive:2026-10-13_193448**: exception | no split
- **naive:2026-10-20_112956**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 36 line(s) — sides differ; from {'C-naive': 36}
Examples: `grep -m -1 o a.txt`; `grep -m x o a.txt`; `grep -A -1 o a.txt`; `grep -C x o a.txt`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | no split
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | no split
- **pash-own**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 17 line(s) — sides differ; from {'C-naive': 5, 'C-v1': 12}
Examples: `grep -R a relpath_1`; `grep -R a abspath_1`; `grep -v -R a relpath_1`; `grep -v -R a abspath_1`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads operand 2; writes stdout | no split

### 9 line(s) — sides differ; from {'C-naive': 9}
Examples: `grep -nT foo a.txt`; `grep --byte-offset foo a.txt`; `grep --files-with-matches foo a.txt`; `grep --files-without-match foo a.txt`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | no split
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | no split
- **pash-own**: reads operand 2; writes stdout | no split
- **v1-pash**: no answer | no split

### 9 line(s) — sides differ; from {'C-naive': 5, 'C-v1': 4}
Examples: `grep a relpath_1`; `grep a abspath_1`; `grep -v a relpath_1`; `grep -v a abspath_1`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads operand 2; writes stdout | no split

### 7 line(s) — sides differ; from {'C-naive': 1, 'C-v1': 6}
Examples: `grep -R a`; `grep -v -R a`; `grep -r a`; `grep -v -r a`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | no split
- **naive:2026-10-20_112956**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 6 line(s) — sides differ; from {'C-naive': 6}
Examples: `grep --color=always foo a.txt`; `grep --color=never foo a.txt`; `grep --color=auto foo a.txt`; `grep --colour=never foo a.txt`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 6 line(s) — sides differ; from {'C-v1': 6}
Examples: `grep -c -R a`; `grep -c -v -R a`; `grep -c -r a`; `grep -c -v -r a`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | no split
- **naive:2026-10-20_112956**: reads nothing; writes stdout | no split
- **naive:2026-10-28_135447**: reads nothing; writes stdout | no split
- **pash-own**: reads stdin; writes stdout | no split
- **v1-pash**: no answer | no split

### 6 line(s) — sides differ; from {'C-naive': 6}
Examples: `grep -in foo`; `grep -n foo`; `grep -b foo`; `grep -nb foo`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | no split
- **naive:2026-10-20_112956**: reads stdin; writes stdout | no split
- **naive:2026-10-28_135447**: reads stdin; writes stdout | no split
- **pash-own**: reads stdin; writes stdout | no split
- **v1-pash**: reads operand 2; writes stdout | no split

### 5 line(s) — sides differ; from {'C-naive': 5}
Examples: `grep -lZ foo a.txt b.txt`; `grep -L zzz a.txt b.txt`; `grep -c foo a.txt b.txt`; `grep -c -l foo a.txt b.txt`

- **naive:2026-10-13_193448**: reads operand 2, operand 3; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2, operand 3; writes stdout | no split
- **naive:2026-10-28_135447**: reads operand 2, operand 3; writes stdout | no split
- **pash-own**: reads operand 2, operand 3; writes stdout | no split
- **v1-pash**: no answer | no split

### 5 line(s) — sides differ; from {'C-naive': 5}
Examples: `grep --label lbl -H foo`; `grep -i -E 'caruca|pash'`; `grep -E -w -x foo`; `grep -e foo -e bar`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 5 line(s) — sides differ; from {'C-naive': 5}
Examples: `grep --file=a.txt a.txt`; `grep --regexp=foo a.txt`; `grep -efoo a.txt`; `grep -fa.txt a.txt`

- **naive:2026-10-13_193448**: exception | no split
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads operand 2; writes stdout | no split

### 5 line(s) — sides differ; from {'C-naive': 5}
Examples: `grep -vE '^_[^_]'`; `grep -e foo`; `grep -i foo`; `grep -o 'fo*'`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads operand 2; writes stdout | no split

### 3 line(s) — sides differ; from {'C-naive': 3}
Examples: `grep -q foo a.txt`; `grep --quiet foo a.txt`; `grep --silent foo a.txt`

- **naive:2026-10-13_193448**: reads operand 2; writes nothing | no split
- **naive:2026-10-20_112956**: reads operand 2; writes nothing | no split
- **naive:2026-10-28_135447**: reads operand 2; writes nothing | no split
- **pash-own**: reads operand 2; writes nothing | no split
- **v1-pash**: no answer | no split

### 3 line(s) — sides differ; from {'C-naive': 3}
Examples: `grep -r --include '*.txt' foo .`; `grep --directories recurse foo a.txt`; `grep -d recurse foo a.txt`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 3 line(s) — sides differ; from {'C-naive': 3}
Examples: `grep --color foo a.txt`; `grep --colour foo a.txt`; `grep --color always a.txt`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 3 line(s) — sides differ; from {'C-naive': 3}
Examples: `grep -m 1 foo`; `grep -C 1 foo`; `grep -m 3 foo`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | no split
- **naive:2026-10-20_112956**: reads stdin; writes stdout | no split
- **naive:2026-10-28_135447**: reads stdin; writes stdout | no split
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `grep --file a.txt a.txt`; `grep -f a.txt a.txt`

- **naive:2026-10-13_193448**: reads operand 1, operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 1, operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 1, operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `grep -e foo a.txt b.txt`; `grep -e foo -e bar a.txt b.txt`

- **naive:2026-10-13_193448**: reads operand 1, operand 2; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `grep -f nope a.txt`; `grep -f pats a.txt`

- **naive:2026-10-13_193448**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `grep -e foo -e bar a.txt`; `grep -e foo a.txt`

- **naive:2026-10-13_193448**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `grep -f pats`; `grep -f -`

- **naive:2026-10-13_193448**: reads stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads operand 2; writes stdout | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -A0 --group-separator XX o a.txt`

- **naive:2026-10-13_193448**: exception | no split
- **naive:2026-10-20_112956**: reads operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -r '--include=*.txt' '--include=*.c' foo .`

- **naive:2026-10-13_193448**: exception | no split
- **naive:2026-10-20_112956**: reads operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -H --label=x foo`

- **naive:2026-10-13_193448**: exception | no split
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep`

- **naive:2026-10-13_193448**: reads nothing; writes stdout | no split
- **naive:2026-10-20_112956**: exception | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: exception | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -f - a.txt`

- **naive:2026-10-13_193448**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 1, stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep --regexp foo a.txt`

- **naive:2026-10-13_193448**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep --exclude-from a.txt foo a.txt`

- **naive:2026-10-13_193448**: reads operand 2, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads operand 2, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep foo a.txt b.txt`

- **naive:2026-10-13_193448**: reads operand 2, operand 3; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep --color always foo a.txt`

- **naive:2026-10-13_193448**: reads operand 2, operand 3; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -2 bar a.txt`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -d recurse foo`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | no split
- **naive:2026-10-20_112956**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -q foo`

- **naive:2026-10-13_193448**: reads stdin; writes nothing | no split
- **naive:2026-10-20_112956**: reads stdin; writes nothing | no split
- **naive:2026-10-28_135447**: reads stdin; writes nothing | no split
- **pash-own**: reads stdin; writes nothing | no split
- **v1-pash**: reads operand 2; writes stdout | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -R -e foo`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | no split
- **naive:2026-10-20_112956**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads operand 2; writes stdout | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `grep -z foo`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | no split
- **naive:2026-10-20_112956**: reads stdin; writes stdout | no split
- **naive:2026-10-28_135447**: reads stdin; writes stdout | no split
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads operand 2; writes stdout | no split

### 17 line(s); from {'C-naive': 3, 'C-v1': 14}
Examples: `grep -c a relpath_1`; `grep -c a abspath_1`; `grep -c -R a relpath_1`; `grep -c -R a abspath_1`

- **naive:2026-10-13_193448**: reads operand 2; writes stdout | no split
- **naive:2026-10-20_112956**: reads operand 2; writes stdout | no split
- **naive:2026-10-28_135447**: reads operand 2; writes stdout | no split
- **pash-own**: reads operand 2; writes stdout | no split
- **v1-pash**: reads operand 2; writes stdout | no split

### 5 line(s); from {'C-naive': 3, 'C-v1': 2}
Examples: `grep a`; `grep -v a`; `grep on`; `grep foo`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-20_112956**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_135447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 3 line(s); from {'C-naive': 1, 'C-v1': 2}
Examples: `grep -c a`; `grep -c -v a`; `grep -c foo`

- **naive:2026-10-13_193448**: reads stdin; writes stdout | no split
- **naive:2026-10-20_112956**: reads stdin; writes stdout | no split
- **naive:2026-10-28_135447**: reads stdin; writes stdout | no split
- **pash-own**: reads stdin; writes stdout | no split
- **v1-pash**: reads stdin; writes stdout | no split

