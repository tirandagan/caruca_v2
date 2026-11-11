# Decision table: cat

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `naive:2026-10-28_100411`, `pash-own`, `v1-pash`

### 83 line(s) — sides differ; from {'A (benchmark)': 74, 'C-naive': 7, 'C-v1': 2}
Examples: `cat WIKI/ARG0`; `cat data_file`; `cat namelist`; `cat AUX_HEAD1`

- **naive:2026-10-28_100411**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1; writes stdout | no split (no class)
- **v1-pash**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 79 line(s) — sides differ; from {'C-naive': 79}
Examples: `cat -A f`; `cat --show-all f`; `cat -e f`; `cat -E f`

- **naive:2026-10-28_100411**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 13 line(s) — sides differ; from {'C-naive': 13}
Examples: `cat -s f`; `cat --squeeze-blank f`; `cat --squeeze-blank /dev/null`; `cat -s /dev/null`

- **naive:2026-10-28_100411**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → ADJ_LINES_SEQ; ROUND_ROBIN_PLAIN → ADJ_LINES_SEQ
- **pash-own**: reads operand 1; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 13 line(s) — sides differ; from {'C-naive': 11, 'C-v1': 2}
Examples: `cat -n relpath_1`; `cat -n abspath_1`; `cat -n f`; `cat --number f`

- **naive:2026-10-28_100411**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1; writes stdout | no split (no class)
- **v1-pash**: reads operand 1; writes stdout | no split

### 12 line(s) — sides differ; from {'C-naive': 12}
Examples: `cat -b f`; `cat --number-nonblank f`; `cat -n -b f`; `cat --number-nonblank /dev/null`

- **naive:2026-10-28_100411**: reads operand 1; writes stdout | no split
- **pash-own**: reads operand 1; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 7 line(s) — sides differ; from {'C-naive': 7}
Examples: `cat -- -n`; `cat -x f`; `cat f -n`; `cat --num f`

- **naive:2026-10-28_100411**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'A (benchmark)': 1, 'C-naive': 1}
Examples: `cat IN1 temp IN2`; `cat f - g`

- **naive:2026-10-28_100411**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'A (benchmark)': 1}
Examples: `cat a1 b1 c1 d1 e1 f1`

- **naive:2026-10-28_100411**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'A (benchmark)': 1}
Examples: `cat 'M0/*.csv' 'M1/*.csv' 'M2/*.csv' 'M3/*.csv' 'M4/*.csv'`

- **naive:2026-10-28_100411**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `cat -n f g`

- **naive:2026-10-28_100411**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2; writes stdout | no split (no class)
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `cat -s`

- **naive:2026-10-28_100411**: reads stdin; writes stdout | split: CONSEC_CHUNKS → ADJ_LINES_SEQ; ROUND_ROBIN_PLAIN → ADJ_LINES_SEQ
- **pash-own**: reads stdin; writes stdout | no split (no class)
- **v1-pash**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 1 line(s) — sides differ; from {'C-v1': 1}
Examples: `cat -n`

- **naive:2026-10-28_100411**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | no split (no class)
- **v1-pash**: reads stdin; writes stdout | no split

### 1 line(s) — sides differ; from {'A (benchmark)': 1, 'C-naive': 1, 'C-v1': 1}
Examples: `cat`

- **naive:2026-10-28_100411**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; INDIV_FILES → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | no split (no class)
- **v1-pash**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

