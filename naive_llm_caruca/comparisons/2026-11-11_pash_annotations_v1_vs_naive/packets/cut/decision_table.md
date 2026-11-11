# Decision table: cut

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `A`, `B`, `C`, `D`, `E`, `F`, `R`

### 997 line(s) — sides differ; from {'test lines of A, C, D, F': 340, 'test lines of B, E': 657}
Examples: `cut`; `cut -s`; `cut -c 1 -s`; `cut -c 1- -s`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 996 line(s) — sides differ; from {'benchmark lines': 9, 'test lines of A, C, D, F': 952, 'test lines of B, E': 35}
Examples: `cut -b-32`; `cut -d '"' -f3`; `cut -d ' ' -f1`; `cut -d ' ' -f2`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 962 line(s) — sides differ; from {'test lines of A, C, D, F': 960, 'test lines of B, E': 2}
Examples: `cut -z relpath_1`; `cut -z abspath_1`; `cut -b 1 -z /tmp/cutcheck/in.txt`; `cut -b 1 -z -`

- **A**: reads operand 1; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | no split
- **D**: reads operand 1; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1; writes stdout | no split
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 785 line(s) — sides differ; from {'test lines of A, C, D, F': 785}
Examples: `cut -d: -f2 c1.txt - c2.txt`; `cut -d: -f1,2 --output-delimiter @ c1.txt`; `cut -d: -s -f1,3 --output-delimiter=@ big2.txt`; `cut -d: -s -f1,3 --output-delimiter=@ cc_aa`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 740 line(s) — sides differ; from {'test lines of A, C, D, F': 740}
Examples: `cut -b1 -n --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 -n --complement --output-delimiter -- /tmp/cutcheck/in.txt`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 725 line(s) — sides differ; from {'benchmark lines': 8, 'test lines of A, C, D, F': 711, 'test lines of B, E': 7}
Examples: `cut -d '' '' -f1`; `cut -d= -f1`; `cut '-d ' -f1`; `cut '-d ' -f2-`

- **A**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 682 line(s) — sides differ; from {'test lines of A, C, D, F': 682}
Examples: `cut -d: -s -f1 c1.txt`; `cut -d: --complement -f2 c1.txt`; `cut -d: -f1,3 --output-delimiter=@ c1.txt`; `cut -d: -f1 -- c1.txt`

- **A**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 560 line(s) — sides differ; from {'test lines of A, C, D, F': 560}
Examples: `cut -b1 -n --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 -n --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1 -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 485 line(s) — sides differ; from {'test lines of A, C, D, F': 485}
Examples: `cut -z -d: -f2`; `cut -z -d: -f1`; `cut -b 1 -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b 1 -n -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **A**: reads operand 1, operand 2; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | no split
- **D**: reads operand 1, operand 2; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes stdout | no split
- **R**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 458 line(s) — sides differ; from {'test lines of A, C, D, F': 450, 'test lines of B, E': 8}
Examples: `cut -z`; `cut -s -z`; `cut -n -z`; `cut --complement -z`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: no answer | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 450 line(s) — sides differ; from {'test lines of A, C, D, F': 448, 'test lines of B, E': 2}
Examples: `cut -w --output-delimiter ,`; `cut -w --output-delimiter '
	'`; `cut --delimiter=: --fields=1-2 c1.txt`; `cut -d: -f-1 c1.txt`

- **A**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 340 line(s) — sides differ; from {'test lines of A, C, D, F': 340}
Examples: `cut -b1 -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b2- -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b-2 -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -b1,3 -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 170 line(s) — sides differ; from {'test lines of A, C, D, F': 170}
Examples: `cut -f1 -d : -s -n --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -s --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -s --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -n --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 104 line(s) — sides differ; from {'test lines of A, C, D, F': 70, 'test lines of B, E': 50}
Examples: `cut -c 1 -n`; `cut -c 1- -n`; `cut -c 1-2 -n`; `cut -c -2 -n`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 102 line(s) — sides differ; from {'benchmark lines': 2, 'test lines of A, C, D, F': 70, 'test lines of B, E': 30}
Examples: `cut -f 2 IN/bio/Gene_locs.txt`; `cut -f 2 ./Gene_locs.txt`; `cut -c 1 relpath_1`; `cut -c 1 abspath_1`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: reads operand 1; writes stdout | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 60 line(s) — sides differ; from {'test lines of A, C, D, F': 60}
Examples: `cut -f1 -d : -s -n --complement --output-delimiter -- /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -s -n --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -s --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1 -d : -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **A**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 10, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 47 line(s) — sides differ; from {'test lines of B, E': 47}
Examples: `cut --help`; `cut -c 1 --help`; `cut -c 1- --help`; `cut -c 1-2 --help`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 33 line(s) — sides differ; from {'test lines of A, C, D, F': 30, 'test lines of B, E': 15}
Examples: `cut -c 1 -z`; `cut -c 1- -z`; `cut -c 1-2 -z`; `cut -c -2 -z`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 33 line(s) — sides differ; from {'test lines of A, C, D, F': 30, 'test lines of B, E': 15}
Examples: `cut -c 1 --complement`; `cut -c 1- --complement`; `cut -c 1-2 --complement`; `cut -c -2 --complement`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 10 line(s) — sides differ; from {'test lines of A, C, D, F': 10}
Examples: `cut -f1 -d : -s -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f2- -d : -s -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f-2 -d : -s -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`; `cut -f1,3 -d : -s -n --complement --output-delimiter -- -z /tmp/cutcheck/in.txt - /tmp/cutcheck/in.txt`

- **A**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: no answer | no split
- **F**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1, operand 10, operand 11, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 4 line(s) — sides differ; from {'test lines of A, C, D, F': 4}
Examples: `cut -z -d: -f1 z.bin`; `cut -sz NOFILE_-d: NOFILE_-f1 NOFILE_in1`; `cut -sz -d: -f1 in1`; `cut -sz -d: -f1 NOFILE_in1`

- **A**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **D**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **R**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `cut --help relpath_1`; `cut --help abspath_1`; `cut --version relpath_1`; `cut --version abspath_1`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: reads nothing; writes stdout | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `cut -z --help`; `cut -z --version`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

### 77 line(s); from {'benchmark lines': 27, 'test lines of A, C, D, F': 41, 'test lines of B, E': 25}
Examples: `cut -c 1-1`; `cut -c 1-12`; `cut -c 1-2`; `cut -c 1-4`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **E**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE

