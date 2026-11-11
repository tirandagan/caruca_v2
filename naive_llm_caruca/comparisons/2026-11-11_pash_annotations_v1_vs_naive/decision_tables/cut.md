# Decision table: cut

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `naive:2026-10-20_135253`, `naive:2026-10-27_230555`, `naive:2026-10-28_145447`, `naive:2026-10-28_152550`, `pash-own`, `v1-main`, `v1-pash`

### 997 line(s) — sides differ; from {'C-naive': 340, 'C-v1': 657}
Examples: `cut`; `cut -s`; `cut -c 1 -s`; `cut -c 1- -s`

- **naive:2026-10-20_135253**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 996 line(s) — sides differ; from {'A (benchmark)': 9, 'C-naive': 952, 'C-v1': 35}
Examples: `cut -b-32`; `cut -d '"' -f3`; `cut -d ' ' -f1`; `cut -d ' ' -f2`

- **naive:2026-10-20_135253**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 962 line(s) — sides differ; from {'C-naive': 960, 'C-v1': 2}
Examples: `cut -z relpath_1`; `cut -z abspath_1`; `cut -b 1 -z /tmp/cutcheck/in.txt`; `cut -b 1 -z -`

- **naive:2026-10-20_135253**: reads operand 1; writes stdout | no split
- **naive:2026-10-27_230555**: reads operand 1; writes stdout | no split
- **naive:2026-10-28_145447**: reads operand 1; writes stdout | no split
- **naive:2026-10-28_152550**: reads operand 1; writes stdout | no split
- **pash-own**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 785 line(s) — sides differ; from {'C-naive': 785}
Examples: `cut -d: -f2 c1.txt - c2.txt`; `cut -d: -f1,2 --output-delimiter @ c1.txt`; `cut -d: -s -f1,3 --output-delimiter=@ big2.txt`; `cut -d: -s -f1,3 --output-delimiter=@ cc_aa`

- **naive:2026-10-20_135253**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 740 line(s) — sides differ; from {'C-naive': 740}
Examples: `cut -b1 -n --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 -n --complement --output-delimiter -- /tmp/cutcheck/in.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 725 line(s) — sides differ; from {'A (benchmark)': 8, 'C-naive': 711, 'C-v1': 7}
Examples: `cut -d '' '' -f1`; `cut -d= -f1`; `cut '-d ' -f1`; `cut '-d ' -f2-`

- **naive:2026-10-20_135253**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 682 line(s) — sides differ; from {'C-naive': 682}
Examples: `cut -d: -s -f1 c1.txt`; `cut -d: --complement -f2 c1.txt`; `cut -d: -f1,3 --output-delimiter=@ c1.txt`; `cut -d: -f1 -- c1.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 560 line(s) — sides differ; from {'C-naive': 560}
Examples: `cut -b1 -n --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 -n --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 485 line(s) — sides differ; from {'C-naive': 485}
Examples: `cut -z -d: -f2`; `cut -z -d: -f1`; `cut -b 1 -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b 1 -n -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 2; writes stdout | no split
- **naive:2026-10-27_230555**: reads operand 1, operand 2; writes stdout | no split
- **naive:2026-10-28_145447**: reads operand 1, operand 2; writes stdout | no split
- **naive:2026-10-28_152550**: reads operand 1, operand 2; writes stdout | no split
- **pash-own**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 458 line(s) — sides differ; from {'C-naive': 450, 'C-v1': 8}
Examples: `cut -z`; `cut -s -z`; `cut -n -z`; `cut --complement -z`

- **naive:2026-10-20_135253**: reads stdin; writes stdout | no split
- **naive:2026-10-27_230555**: reads stdin; writes stdout | no split
- **naive:2026-10-28_145447**: reads stdin; writes stdout | no split
- **naive:2026-10-28_152550**: reads stdin; writes stdout | no split
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 450 line(s) — sides differ; from {'C-naive': 448, 'C-v1': 2}
Examples: `cut -w --output-delimiter ,`; `cut -w --output-delimiter '
	'`; `cut --delimiter=: --fields=1-2 c1.txt`; `cut -d: -f-1 c1.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 340 line(s) — sides differ; from {'C-naive': 340}
Examples: `cut -b1 -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b2- -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b-2 -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1,3 -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 170 line(s) — sides differ; from {'C-naive': 170}
Examples: `cut -f1 -d : -s -n --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -s --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -s --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -n --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 104 line(s) — sides differ; from {'C-naive': 70, 'C-v1': 50}
Examples: `cut -c 1 -n`; `cut -c 1- -n`; `cut -c 1-2 -n`; `cut -c -2 -n`

- **naive:2026-10-20_135253**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: no answer | no split

### 102 line(s) — sides differ; from {'A (benchmark)': 2, 'C-naive': 70, 'C-v1': 30}
Examples: `cut -f 2 IN/bio/Gene_locs.txt`; `cut -f 2 ./Gene_locs.txt`; `cut -c 1 relpath_1`; `cut -c 1 abspath_1`

- **naive:2026-10-20_135253**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: reads operand 1; writes stdout | no split
- **v1-pash**: no answer | no split

### 60 line(s) — sides differ; from {'C-naive': 60}
Examples: `cut -f1 -d : -s -n --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -s -n --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -s --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 47 line(s) — sides differ; from {'C-v1': 47}
Examples: `cut --help`; `cut -c 1 --help`; `cut -c 1- --help`; `cut -c 1-2 --help`

- **naive:2026-10-20_135253**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: reads nothing; writes stdout | no split
- **v1-pash**: no answer | no split

### 33 line(s) — sides differ; from {'C-naive': 30, 'C-v1': 15}
Examples: `cut -c 1 -z`; `cut -c 1- -z`; `cut -c 1-2 -z`; `cut -c -2 -z`

- **naive:2026-10-20_135253**: reads stdin; writes stdout | no split
- **naive:2026-10-27_230555**: reads stdin; writes stdout | no split
- **naive:2026-10-28_145447**: reads stdin; writes stdout | no split
- **naive:2026-10-28_152550**: reads stdin; writes stdout | no split
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: reads stdin; writes stdout | no split
- **v1-pash**: no answer | no split

### 33 line(s) — sides differ; from {'C-naive': 30, 'C-v1': 15}
Examples: `cut -c 1 --complement`; `cut -c 1- --complement`; `cut -c 1-2 --complement`; `cut -c -2 --complement`

- **naive:2026-10-20_135253**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: reads stdin; writes stdout | no split
- **v1-pash**: no answer | no split

### 10 line(s) — sides differ; from {'C-naive': 10}
Examples: `cut -f1 -d : -s -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f2- -d : -s -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f-2 -d : -s -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1,3 -d : -s -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **naive:2026-10-20_135253**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 4 line(s) — sides differ; from {'C-naive': 4}
Examples: `cut -z -d: -f1 z.bin`; `cut -sz NOFILE_-d: NOFILE_-f1 NOFILE_in1`; `cut -sz -d: -f1 in1`; `cut -sz -d: -f1 NOFILE_in1`

- **naive:2026-10-20_135253**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **naive:2026-10-27_230555**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **naive:2026-10-28_145447**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **naive:2026-10-28_152550**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **pash-own**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: no answer | no split
- **v1-pash**: no answer | no split

### 4 line(s) — sides differ; from {'C-v1': 4}
Examples: `cut --help relpath_1`; `cut --help abspath_1`; `cut --version relpath_1`; `cut --version abspath_1`

- **naive:2026-10-20_135253**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: reads nothing; writes stdout | no split
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-v1': 2}
Examples: `cut -z --help`; `cut -z --version`

- **naive:2026-10-20_135253**: reads stdin; writes stdout | no split
- **naive:2026-10-27_230555**: reads stdin; writes stdout | no split
- **naive:2026-10-28_145447**: reads stdin; writes stdout | no split
- **naive:2026-10-28_152550**: reads stdin; writes stdout | no split
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: reads nothing; writes stdout | no split
- **v1-pash**: no answer | no split

### 77 line(s); from {'A (benchmark)': 27, 'C-naive': 41, 'C-v1': 25}
Examples: `cut -c 1-1`; `cut -c 1-12`; `cut -c 1-2`; `cut -c 1-4`

- **naive:2026-10-20_135253**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-27_230555**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_145447**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **naive:2026-10-28_152550**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **pash-own**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-main**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **v1-pash**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

