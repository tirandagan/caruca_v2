# Decision table: grep

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `A`, `B`, `C`, `D`, `R`

### 59 line(s) — sides differ; from {'test lines of A, B, C': 59}
Examples: `grep -y FOO a.txt`; `grep -u foo a.txt`; `grep -d x o a.txt`; `grep -D x o a.txt`

- **A**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 43 line(s) — sides differ; from {'test lines of A, B, C': 43}
Examples: `grep --binary-files=x o a.txt`; `grep --color=x o a.txt`; `grep --ext fo+ a.txt`; `grep --no-group-separator=x foo a.txt`

- **A**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: exception | no split
- **D**: no answer | no split
- **R**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 36 line(s) — sides differ; from {'test lines of A, B, C': 36}
Examples: `grep -m -1 o a.txt`; `grep -m x o a.txt`; `grep -A -1 o a.txt`; `grep -C x o a.txt`

- **A**: reads operand 2; writes stdout | no split
- **B**: reads operand 2; writes stdout | no split
- **C**: reads operand 2; writes stdout | no split
- **D**: no answer | no split
- **R**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 17 line(s) — sides differ; from {'test lines of A, B, C': 5, 'test lines of D': 12}
Examples: `grep -R a relpath_1`; `grep -R a abspath_1`; `grep -v -R a relpath_1`; `grep -v -R a abspath_1`

- **A**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2; writes stdout | no split
- **D**: reads operand 2; writes stdout | no split
- **R**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 9 line(s) — sides differ; from {'test lines of A, B, C': 9}
Examples: `grep -nT foo a.txt`; `grep --byte-offset foo a.txt`; `grep --files-with-matches foo a.txt`; `grep --files-without-match foo a.txt`

- **A**: reads operand 2; writes stdout | no split
- **B**: reads operand 2; writes stdout | no split
- **C**: reads operand 2; writes stdout | no split
- **D**: no answer | no split
- **R**: reads operand 2; writes stdout | no split

### 9 line(s) — sides differ; from {'test lines of A, B, C': 5, 'test lines of D': 4}
Examples: `grep a relpath_1`; `grep a abspath_1`; `grep -v a relpath_1`; `grep -v a abspath_1`

- **A**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 2; writes stdout | no split
- **R**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 7 line(s) — sides differ; from {'test lines of A, B, C': 1, 'test lines of D': 6}
Examples: `grep -R a`; `grep -v -R a`; `grep -r a`; `grep -v -r a`

- **A**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | no split
- **D**: no answer | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 6 line(s) — sides differ; from {'test lines of A, B, C': 6}
Examples: `grep --color=always foo a.txt`; `grep --color=never foo a.txt`; `grep --color=auto foo a.txt`; `grep --colour=never foo a.txt`

- **A**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 6 line(s) — sides differ; from {'test lines of D': 6}
Examples: `grep -c -R a`; `grep -c -v -R a`; `grep -c -r a`; `grep -c -v -r a`

- **A**: reads nothing; writes stdout | no split
- **B**: reads nothing; writes stdout | no split
- **C**: reads stdin; writes stdout | no split
- **D**: no answer | no split
- **R**: reads stdin; writes stdout | no split

### 6 line(s) — sides differ; from {'test lines of A, B, C': 6}
Examples: `grep -in foo`; `grep -n foo`; `grep -b foo`; `grep -nb foo`

- **A**: reads stdin; writes stdout | no split
- **B**: reads stdin; writes stdout | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads operand 2; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 5 line(s) — sides differ; from {'test lines of A, B, C': 5}
Examples: `grep -lZ foo a.txt b.txt`; `grep -L zzz a.txt b.txt`; `grep -c foo a.txt b.txt`; `grep -c -l foo a.txt b.txt`

- **A**: reads operand 2, operand 3; writes stdout | no split
- **B**: reads operand 2, operand 3; writes stdout | no split
- **C**: reads operand 2, operand 3; writes stdout | no split
- **D**: no answer | no split
- **R**: reads operand 2, operand 3; writes stdout | no split

### 5 line(s) — sides differ; from {'test lines of A, B, C': 5}
Examples: `grep --label lbl -H foo`; `grep -i -E 'caruca|pash'`; `grep -E -w -x foo`; `grep -e foo -e bar`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 5 line(s) — sides differ; from {'test lines of A, B, C': 5}
Examples: `grep --file=a.txt a.txt`; `grep --regexp=foo a.txt`; `grep -efoo a.txt`; `grep -fa.txt a.txt`

- **A**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: exception | no split
- **D**: reads operand 2; writes stdout | no split
- **R**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 5 line(s) — sides differ; from {'test lines of A, B, C': 5}
Examples: `grep -vE '^_[^_]'`; `grep -e foo`; `grep -i foo`; `grep -o 'fo*'`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 2; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 3 line(s) — sides differ; from {'test lines of A, B, C': 3}
Examples: `grep -q foo a.txt`; `grep --quiet foo a.txt`; `grep --silent foo a.txt`

- **A**: reads operand 2; writes nothing | no split
- **B**: reads operand 2; writes nothing | no split
- **C**: reads operand 2; writes nothing | no split
- **D**: no answer | no split
- **R**: reads operand 2; writes nothing | no split

### 3 line(s) — sides differ; from {'test lines of A, B, C': 3}
Examples: `grep -r --include '*.txt' foo .`; `grep --directories recurse foo a.txt`; `grep -d recurse foo a.txt`

- **A**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2; writes stdout | no split
- **D**: no answer | no split
- **R**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 3 line(s) — sides differ; from {'test lines of A, B, C': 3}
Examples: `grep --color foo a.txt`; `grep --colour foo a.txt`; `grep --color always a.txt`

- **A**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 3 line(s) — sides differ; from {'test lines of A, B, C': 3}
Examples: `grep -m 1 foo`; `grep -C 1 foo`; `grep -m 3 foo`

- **A**: reads stdin; writes stdout | no split
- **B**: reads stdin; writes stdout | no split
- **C**: reads stdin; writes stdout | no split
- **D**: no answer | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 2 line(s) — sides differ; from {'test lines of A, B, C': 2}
Examples: `grep --file a.txt a.txt`; `grep -f a.txt a.txt`

- **A**: reads operand 1, operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 1, operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 1, operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads operand 1, operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 2 line(s) — sides differ; from {'test lines of A, B, C': 2}
Examples: `grep -e foo a.txt b.txt`; `grep -e foo -e bar a.txt b.txt`

- **A**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 1, operand 2; writes stdout | no split
- **D**: no answer | no split
- **R**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 2 line(s) — sides differ; from {'test lines of A, B, C': 2}
Examples: `grep -f nope a.txt`; `grep -f pats a.txt`

- **A**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 2 line(s) — sides differ; from {'test lines of A, B, C': 2}
Examples: `grep -e foo -e bar a.txt`; `grep -e foo a.txt`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 2 line(s) — sides differ; from {'test lines of A, B, C': 2}
Examples: `grep -f pats`; `grep -f -`

- **A**: reads stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 2; writes stdout | no split
- **R**: reads stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -A0 --group-separator XX o a.txt`

- **A**: reads operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: exception | no split
- **D**: no answer | no split
- **R**: reads operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -r '--include=*.txt' '--include=*.c' foo .`

- **A**: reads operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: exception | no split
- **D**: no answer | no split
- **R**: reads operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -H --label=x foo`

- **A**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: exception | no split
- **D**: no answer | no split
- **R**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: exception | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads nothing; writes stdout | no split
- **D**: no answer | no split
- **R**: exception | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -f - a.txt`

- **A**: reads operand 1, stdin, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads operand 1, value of -f; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep --regexp foo a.txt`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep --exclude-from a.txt foo a.txt`

- **A**: reads operand 2, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: no answer | no split
- **R**: reads operand 2, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep foo a.txt b.txt`

- **A**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2, operand 3; writes stdout | no split
- **D**: no answer | no split
- **R**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep --color always foo a.txt`

- **A**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2, operand 3; writes stdout | no split
- **D**: no answer | no split
- **R**: reads operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -2 bar a.txt`

- **A**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 2; writes stdout | no split
- **D**: no answer | no split
- **R**: reads operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -d recurse foo`

- **A**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | no split
- **D**: no answer | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -q foo`

- **A**: reads stdin; writes nothing | no split
- **B**: reads stdin; writes nothing | no split
- **C**: reads stdin; writes nothing | no split
- **D**: reads operand 2; writes stdout | no split
- **R**: reads stdin; writes nothing | no split

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -R -e foo`

- **A**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads nothing; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | no split
- **D**: reads operand 2; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `grep -z foo`

- **A**: reads stdin; writes stdout | no split
- **B**: reads stdin; writes stdout | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads operand 2; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 17 line(s); from {'test lines of A, B, C': 3, 'test lines of D': 14}
Examples: `grep -c a relpath_1`; `grep -c a abspath_1`; `grep -c -R a relpath_1`; `grep -c -R a abspath_1`

- **A**: reads operand 2; writes stdout | no split
- **B**: reads operand 2; writes stdout | no split
- **C**: reads operand 2; writes stdout | no split
- **D**: reads operand 2; writes stdout | no split
- **R**: reads operand 2; writes stdout | no split

### 5 line(s); from {'test lines of A, B, C': 3, 'test lines of D': 2}
Examples: `grep a`; `grep -v a`; `grep on`; `grep foo`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 3 line(s); from {'test lines of A, B, C': 1, 'test lines of D': 2}
Examples: `grep -c a`; `grep -c -v a`; `grep -c foo`

- **A**: reads stdin; writes stdout | no split
- **B**: reads stdin; writes stdout | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

