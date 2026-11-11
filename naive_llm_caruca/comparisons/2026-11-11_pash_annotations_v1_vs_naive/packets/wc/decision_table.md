# Decision table: wc

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `A`, `B`, `R`

### 15 line(s) — sides differ; from {'test lines of A': 15}
Examples: `wc -clmwL f1`; `wc --files0-from=names`; `wc --files0-from=-`; `wc -c f1`

- **A**: reads operand 1; writes stdout | exception
- **B**: no answer | no split
- **R**: reads operand 1; writes stdout | no split (no class)

### 13 line(s) — sides differ; from {'test lines of A': 13}
Examples: `wc f1 f2`; `wc f2 -`; `wc --total=always f1`; `wc --total=foo f1`

- **A**: reads operand 1, operand 2; writes stdout | no split
- **B**: no answer | no split
- **R**: reads operand 1, operand 2; writes stdout | no split (no class)

### 5 line(s) — sides differ; from {'benchmark lines': 3, 'test lines of A': 1, 'test lines of B': 4}
Examples: `wc -c`; `wc -l`; `wc -lc`; `wc`

- **A**: reads stdin; writes stdout | exception
- **B**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split (no class)

### 2 line(s) — sides differ; from {'test lines of A': 2}
Examples: `wc --total=only f1 f2`; `wc --total=never f1 f2`

- **A**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **B**: no answer | no split
- **R**: reads operand 1, operand 2, operand 3; writes stdout | no split (no class)

### 2 line(s) — sides differ; from {'test lines of A': 2}
Examples: `wc -lwmcL`; `wc -lwcL`

- **A**: reads stdin; writes stdout | exception
- **B**: no answer | no split
- **R**: reads stdin; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'test lines of A': 1}
Examples: `wc --total only f1`

- **A**: reads operand 1; writes stdout | exception
- **B**: no answer | no split
- **R**: reads operand 1, operand 2, operand 3; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'test lines of A': 1}
Examples: `wc --debug f1`

- **A**: reads operand 1; writes stdout | exception
- **B**: no answer | no split
- **R**: reads operand 1, operand 2; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'test lines of A': 1}
Examples: `wc --files0-from names`

- **A**: reads value of --files0-from; writes stdout | no split
- **B**: no answer | no split
- **R**: exception | no split (no class)

