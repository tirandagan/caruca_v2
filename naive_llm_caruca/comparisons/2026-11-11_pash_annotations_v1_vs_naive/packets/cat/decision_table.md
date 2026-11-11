# Decision table: cat

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `A`, `B`, `R`

### 83 line(s) — sides differ; from {'benchmark lines': 74, 'test lines of A': 2, 'test lines of B': 7}
Examples: `cat WIKI/ARG0`; `cat data_file`; `cat namelist`; `cat AUX_HEAD1`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1; writes stdout | no split (no class)

### 79 line(s) — sides differ; from {'test lines of B': 79}
Examples: `cat -A f`; `cat --show-all f`; `cat -e f`; `cat -E f`

- **A**: no answer | no split
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1; writes stdout | no split (no class)

### 13 line(s) — sides differ; from {'test lines of B': 13}
Examples: `cat -s f`; `cat --squeeze-blank f`; `cat --squeeze-blank /dev/null`; `cat -s /dev/null`

- **A**: no answer | no split
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → ADJ_LINES_SEQ; ROUND_ROBIN_PLAIN → ADJ_LINES_SEQ
- **R**: reads operand 1; writes stdout | no split (no class)

### 13 line(s) — sides differ; from {'test lines of A': 2, 'test lines of B': 11}
Examples: `cat -n relpath_1`; `cat -n abspath_1`; `cat -n f`; `cat --number f`

- **A**: reads operand 1; writes stdout | no split
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1; writes stdout | no split (no class)

### 12 line(s) — sides differ; from {'test lines of B': 12}
Examples: `cat -b f`; `cat --number-nonblank f`; `cat -n -b f`; `cat --number-nonblank /dev/null`

- **A**: no answer | no split
- **B**: reads operand 1; writes stdout | no split
- **R**: reads operand 1; writes stdout | no split (no class)

### 7 line(s) — sides differ; from {'test lines of B': 7}
Examples: `cat -- -n`; `cat -x f`; `cat f -n`; `cat --num f`

- **A**: no answer | no split
- **B**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2; writes stdout | no split (no class)

### 2 line(s) — sides differ; from {'benchmark lines': 1, 'test lines of B': 1}
Examples: `cat IN1 temp IN2`; `cat f - g`

- **A**: no answer | no split
- **B**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'benchmark lines': 1}
Examples: `cat a1 b1 c1 d1 e1 f1`

- **A**: no answer | no split
- **B**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'benchmark lines': 1}
Examples: `cat 'M0/*.csv' 'M1/*.csv' 'M2/*.csv' 'M3/*.csv' 'M4/*.csv'`

- **A**: no answer | no split
- **B**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'test lines of B': 1}
Examples: `cat -n f g`

- **A**: no answer | no split
- **B**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'test lines of B': 1}
Examples: `cat -s`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → ADJ_LINES_SEQ; ROUND_ROBIN_PLAIN → ADJ_LINES_SEQ
- **R**: reads stdin; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'test lines of A': 1}
Examples: `cat -n`

- **A**: reads stdin; writes stdout | no split
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads stdin; writes stdout | no split (no class)

### 1 line(s) — sides differ; from {'benchmark lines': 1, 'test lines of A': 1, 'test lines of B': 1}
Examples: `cat`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads stdin; writes stdout | no split (no class)

