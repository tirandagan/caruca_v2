# Decision table: rm

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `A`, `B`, `C`, `D`, `R`

### 96 line(s) — sides differ; from {'benchmark lines': 32, 'test lines of A, B': 22, 'test lines of C, D': 42}
Examples: `rm -f input.txt`; `rm -f a`; `rm -f nginx.zip`; `rm -f oneliners.zip`

- **A**: reads nothing; writes operand 1 | no split
- **B**: reads nothing; writes operand 1 | no split
- **C**: reads nothing; writes operand 1 | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1 | no split (no class)

### 80 line(s) — sides differ; from {'benchmark lines': 5, 'test lines of A, B': 1, 'test lines of C, D': 74}
Examples: `rm -f OUT/input.words OUT/input.nextwords OUT/input.nextwords2`; `rm -f '*.bz2' in.csv in_small.csv`; `rm -f access.log apache.log shutdown.log`; `rm -rf genesis exodus pg`

- **A**: reads nothing; writes operand 1, operand 2, operand 3 | no split
- **B**: reads nothing; writes operand 1, operand 2, operand 3 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1, operand 2, operand 3 | no split (no class)

### 72 line(s) — sides differ; from {'benchmark lines': 7, 'test lines of A, B': 17, 'test lines of C, D': 48}
Examples: `rm s2 s3`; `rm -f a b`; `rm -rf ../1-grams.txt ../2-grams.txt`; `rm -rf full web-index.full.zip`

- **A**: reads nothing; writes operand 1, operand 2 | no split
- **B**: reads nothing; writes operand 1, operand 2 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1, operand 2 | no split (no class)

### 38 line(s) — sides differ; from {'test lines of C, D': 38}
Examples: `rm --help relpath_1`; `rm --help abspath_1`; `rm -i --help relpath_1`; `rm -i --help abspath_1`

- **A**: reads nothing; writes operand 1, stdout | no split
- **B**: reads nothing; writes operand 1 | no split
- **C**: reads nothing; writes stdout | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1 | no split (no class)

### 20 line(s) — sides differ; from {'benchmark lines': 15, 'test lines of A, B': 4, 'test lines of C, D': 2}
Examples: `rm aux1`; `rm aux2`; `rm aux3`; `rm s2`

- **A**: reads nothing; writes operand 1 | no split
- **B**: reads nothing; writes operand 1 | no split
- **C**: reads nothing; writes operand 1 | no split
- **D**: reads nothing; writes operand 1 | no split
- **R**: reads nothing; writes operand 1 | no split (no class)

### 18 line(s) — sides differ; from {'test lines of A, B': 4, 'test lines of C, D': 14}
Examples: `rm -i relpath_1`; `rm -i abspath_1`; `rm -i -r relpath_1`; `rm -i -r abspath_1`

- **A**: reads nothing; writes operand 1 | no split
- **B**: reads nothing; writes operand 1 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1 | no split (no class)

### 18 line(s) — sides differ; from {'test lines of A, B': 4, 'test lines of C, D': 14}
Examples: `rm -v relpath_1`; `rm -v abspath_1`; `rm -r -v relpath_1`; `rm -r -v abspath_1`

- **A**: reads nothing; writes operand 1, stdout | no split
- **B**: reads nothing; writes operand 1 | no split
- **C**: reads nothing; writes operand 1, stdout | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1 | no split (no class)

### 5 line(s) — sides differ; from {'test lines of A, B': 5}
Examples: `rm`; `rm --interactive a`; `rm --preserve-root a`; `rm --interactive /tmp/tmp66m8n4b_/a`

- **A**: reads nothing; writes nothing | no split
- **B**: reads nothing; writes nothing | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes nothing | no split (no class)

### 5 line(s) — sides differ; from {'benchmark lines': 5}
Examples: `rm -f OUT/a OUT/sort_IN OUT/sort_dict OUT/bad`; `rm -f A B A+B.sgsh.ft2 A-B.sgsh.ft2`; `rm -f a b A B`; `rm -f a b c d`

- **A**: reads nothing; writes operand 1, operand 2, operand 3, operand 4 | no split
- **B**: reads nothing; writes operand 1, operand 2, operand 3, operand 4 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1, operand 2, operand 3, operand 4 | no split (no class)

### 3 line(s) — sides differ; from {'test lines of A, B': 3}
Examples: `rm -rf a b c d -`; `rm -I a b c d -r`; `rm --interactive=once a b c d`

- **A**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5 | no split
- **B**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5 | no split (no class)

### 3 line(s) — sides differ; from {'benchmark lines': 3}
Examples: `rm -f a b c d a1 b1 c1 d1`; `rm -f sed_a sed_b a b a_ch1 a_ch2 b_ch1 b_ch2`; `rm a b c d a1 b1 c1 d1`

- **A**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8 | no split
- **B**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8 | no split (no class)

### 3 line(s) — sides differ; from {'test lines of A, B': 3}
Examples: `rm -v a b`; `rm -rfv d a`; `rm -v -- -`

- **A**: reads nothing; writes operand 1, operand 2, stdout | no split
- **B**: reads nothing; writes operand 1, operand 2 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1, operand 2 | no split (no class)

### 2 line(s) — sides differ; from {'benchmark lines': 2}
Examples: `rm -f a b c d e f g digram.txt trigram.txt words.txt teea_res teeb_res teea teeb`; `rm a b c e f g d trigram.txt words.txt digram.txt teea teeb teea_res teeb_res`

- **A**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 13, operand 14, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split
- **B**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 13, operand 14, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 13, operand 14, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split (no class)

### 2 line(s) — sides differ; from {'benchmark lines': 2}
Examples: `rm -f a b c d e f a1 b1 c1 d1 e1 f1`; `rm a1 b1 c1 d1 e1 f1 a b c d e f`

- **A**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split
- **B**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1, operand 10, operand 11, operand 12, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9 | no split (no class)

### 2 line(s) — sides differ; from {'test lines of C, D': 2}
Examples: `rm -i -v relpath_1`; `rm -i -v abspath_1`

- **A**: reads nothing; writes operand 1, stdout | no split
- **B**: reads nothing; writes operand 1 | no split
- **C**: no answer | no split
- **D**: no answer | no split
- **R**: reads nothing; writes operand 1 | no split (no class)

### 1 line(s) — sides differ; from {'test lines of A, B': 1}
Examples: `rm -f`

- **A**: reads nothing; writes nothing | no split
- **B**: reads nothing; writes nothing | no split
- **C**: no answer | no split
- **D**: reads nothing; writes operand 1 | no split
- **R**: reads nothing; writes nothing | no split (no class)

