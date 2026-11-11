# Decision table: wc

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `naive:2026-10-28_091448`, `pash-own`, `v1-pash`

### 15 line(s) — sides differ; from {'C-naive': 15}
Examples: `wc -clmwL f1`; `wc --files0-from=names`; `wc --files0-from=-`; `wc -c f1`

- **naive:2026-10-28_091448**: reads operand 1; writes stdout | exception
- **pash-own**: reads operand 1; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 13 line(s) — sides differ; from {'C-naive': 13}
Examples: `wc f1 f2`; `wc f2 -`; `wc --total=always f1`; `wc --total=foo f1`

- **naive:2026-10-28_091448**: reads operand 1, operand 2; writes stdout | no split
- **pash-own**: reads operand 1, operand 2; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 5 line(s) — sides differ; from {'A (benchmark)': 3, 'C-naive': 1, 'C-v1': 4}
Examples: `wc -c`; `wc -l`; `wc -lc`; `wc`

- **naive:2026-10-28_091448**: reads stdin; writes stdout | exception
- **pash-own**: reads stdin; writes stdout | no split (no class)
- **v1-pash**: reads stdin; writes stdout | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `wc --total=only f1 f2`; `wc --total=never f1 f2`

- **naive:2026-10-28_091448**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **pash-own**: reads operand 1, operand 2, operand 3; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `wc -lwmcL`; `wc -lwcL`

- **naive:2026-10-28_091448**: reads stdin; writes stdout | exception
- **pash-own**: reads stdin; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `wc --total only f1`

- **naive:2026-10-28_091448**: reads operand 1; writes stdout | exception
- **pash-own**: reads operand 1, operand 2, operand 3; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `wc --debug f1`

- **naive:2026-10-28_091448**: reads operand 1; writes stdout | exception
- **pash-own**: reads operand 1, operand 2; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `wc --files0-from names`

- **naive:2026-10-28_091448**: reads value of --files0-from; writes stdout | no split
- **pash-own**: exception | no split (no class)
- **v1-pash**: no answer | no split

