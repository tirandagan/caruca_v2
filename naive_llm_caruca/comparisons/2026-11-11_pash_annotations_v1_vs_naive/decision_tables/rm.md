# Decision table: rm

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `naive:2026-10-20_121932`, `naive:2026-10-28_105951`, `pash-own`, `v1-main`, `v1-pash`

### 96 line(s) — sides differ; from {'A (benchmark)': 32, 'C-naive': 22, 'C-v1': 42}
Examples: `rm -f input.txt`; `rm -f a`; `rm -f nginx.zip`; `rm -f oneliners.zip`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1 | no split
- **pash-own**: reads nothing; writes operand 1 | no split (no class)
- **v1-main**: reads nothing; writes operand 1 | no split
- **v1-pash**: no answer | no split

### 80 line(s) — sides differ; from {'A (benchmark)': 5, 'C-naive': 1, 'C-v1': 74}
Examples: `rm -f OUT/input.words OUT/input.nextwords OUT/input.nextwords2`; `rm -f '*.bz2' in.csv in_small.csv`; `rm -f access.log apache.log shutdown.log`; `rm -rf genesis exodus pg`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, operand 2, operand 3 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1, operand 2, operand 3 | no split
- **pash-own**: reads nothing; writes operand 1, operand 2, operand 3 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 72 line(s) — sides differ; from {'A (benchmark)': 7, 'C-naive': 17, 'C-v1': 48}
Examples: `rm s2 s3`; `rm -f a b`; `rm -rf ../1-grams.txt ../2-grams.txt`; `rm -rf full web-index.full.zip`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, operand 2 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1, operand 2 | no split
- **pash-own**: reads nothing; writes operand 1, operand 2 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 38 line(s) — sides differ; from {'C-v1': 38}
Examples: `rm --help relpath_1`; `rm --help abspath_1`; `rm -i --help relpath_1`; `rm -i --help abspath_1`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, stdout | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1 | no split
- **pash-own**: reads nothing; writes operand 1 | no split (no class)
- **v1-main**: reads nothing; writes stdout | no split
- **v1-pash**: no answer | no split

### 20 line(s) — sides differ; from {'A (benchmark)': 15, 'C-naive': 4, 'C-v1': 2}
Examples: `rm aux1`; `rm aux2`; `rm aux3`; `rm s2`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1 | no split
- **pash-own**: reads nothing; writes operand 1 | no split (no class)
- **v1-main**: reads nothing; writes operand 1 | no split
- **v1-pash**: reads nothing; writes operand 1 | no split

### 18 line(s) — sides differ; from {'C-naive': 4, 'C-v1': 14}
Examples: `rm -i relpath_1`; `rm -i abspath_1`; `rm -i -r relpath_1`; `rm -i -r abspath_1`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1 | no split
- **pash-own**: reads nothing; writes operand 1 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 18 line(s) — sides differ; from {'C-naive': 4, 'C-v1': 14}
Examples: `rm -v relpath_1`; `rm -v abspath_1`; `rm -r -v relpath_1`; `rm -r -v abspath_1`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, stdout | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1 | no split
- **pash-own**: reads nothing; writes operand 1 | no split (no class)
- **v1-main**: reads nothing; writes operand 1, stdout | no split
- **v1-pash**: no answer | no split

### 5 line(s) — sides differ; from {'C-naive': 5}
Examples: `rm`; `rm --interactive a`; `rm --preserve-root a`; `rm --interactive /tmp/tmp66m8n4b_/a`

- **naive:2026-10-20_121932**: reads nothing; writes nothing | no split
- **naive:2026-10-28_105951**: reads nothing; writes nothing | no split
- **pash-own**: reads nothing; writes nothing | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 5 line(s) — sides differ; from {'A (benchmark)': 5}
Examples: `rm -f OUT/a OUT/sort_IN OUT/sort_dict OUT/bad`; `rm -f A B A+B.sgsh.ft2 A-B.sgsh.ft2`; `rm -f a b A B`; `rm -f a b c d`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, operand 2, operand 3, operand 4 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1, operand 2, operand 3, operand 4 | no split
- **pash-own**: reads nothing; writes operand 1, operand 2, operand 3, operand 4 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 3 line(s) — sides differ; from {'C-naive': 3}
Examples: `rm -rf a b c d -`; `rm -I a b c d -r`; `rm --interactive=once a b c d`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5 | no split
- **pash-own**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 3 line(s) — sides differ; from {'A (benchmark)': 3}
Examples: `rm -f a b c d a1 b1 c1 d1`; `rm -f sed_a sed_b a b a_ch1 a_ch2 b_ch1 b_ch2`; `rm a b c d a1 b1 c1 d1`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8 | no split
- **pash-own**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 3 line(s) — sides differ; from {'C-naive': 3}
Examples: `rm -v a b`; `rm -rfv d a`; `rm -v -- -`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, operand 2, stdout | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1, operand 2 | no split
- **pash-own**: reads nothing; writes operand 1, operand 2 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'A (benchmark)': 2}
Examples: `rm -f a b c d e f g digram.txt trigram.txt words.txt teea_res teeb_res teea teeb`; `rm a b c e f g d trigram.txt words.txt digram.txt teea teeb teea_res teeb_res`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 13, operand 14, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 13, operand 14, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split
- **pash-own**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 13, operand 14, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'A (benchmark)': 2}
Examples: `rm -f a b c d e f a1 b1 c1 d1 e1 f1`; `rm a1 b1 c1 d1 e1 f1 a b c d e f`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split
- **pash-own**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-v1': 2}
Examples: `rm -i -v relpath_1`; `rm -i -v abspath_1`

- **naive:2026-10-20_121932**: reads nothing; writes operand 1, stdout | no split
- **naive:2026-10-28_105951**: reads nothing; writes operand 1 | no split
- **pash-own**: reads nothing; writes operand 1 | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `rm -f`

- **naive:2026-10-20_121932**: reads nothing; writes nothing | no split
- **naive:2026-10-28_105951**: reads nothing; writes nothing | no split
- **pash-own**: reads nothing; writes nothing | no split (no class)
- **v1-main**: no answer | no split
- **v1-pash**: reads nothing; writes operand 1 | no split

