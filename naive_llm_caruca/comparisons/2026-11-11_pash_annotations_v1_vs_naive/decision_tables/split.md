# Decision table: split

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `naive:2026-10-28_134035`, `v1-pash`

### 49 line(s) — sides differ; from {'C-naive': 49}
Examples: `split -l 4 -d in.txt d_`; `split -l 4 -x in.txt h_`; `split -l 4 --numeric-suffixes 7 in.txt`; `split -l 4 -a 3 in.txt a_`

- **naive:2026-10-28_134035**: reads operand 1; writes operand 2 | no split
- **v1-pash**: no answer | no split

### 27 line(s) — sides differ; from {'C-naive': 3, 'C-v1': 24}
Examples: `split string`; `split relpath_1`; `split abspath_1`; `split -n -1 string`

- **naive:2026-10-28_134035**: reads operand 1; writes nothing | no split
- **v1-pash**: reads operand 1, stdin; writes nothing | no split

### 27 line(s) — sides differ; from {'C-naive': 11, 'C-v1': 16}
Examples: `split relpath_1 string`; `split abspath_1 string`; `split -n -1 relpath_1 string`; `split -n -1 abspath_1 string`

- **naive:2026-10-28_134035**: reads operand 1; writes operand 2 | no split
- **v1-pash**: reads operand 1, stdin; writes nothing | no split

### 22 line(s) — sides differ; from {'A (benchmark)': 1, 'C-naive': 21}
Examples: `split -dn N IN`; `split -3 in.txt p_`; `split -l 4 --numeric-suffixes=7 in.txt n_`; `split -l 4 --additional-suffix=.txt in.txt s_`

- **naive:2026-10-28_134035**: exception | no split
- **v1-pash**: no answer | no split

### 11 line(s) — sides differ; from {'C-naive': 11}
Examples: `split -n 2/3 in.txt`; `split -n l/2/3 in.txt`; `split -n r/1/3 in.txt`; `split -n r/1/3 in.txt zz_`

- **naive:2026-10-28_134035**: reads operand 1; writes stdout | no split
- **v1-pash**: reads operand 1, stdin; writes nothing | no split

### 6 line(s) — sides differ; from {'C-naive': 6}
Examples: `split -l 2 -b 3 in.txt`; `split -l 0 in.txt`; `split -b 0 in.txt`; `split -b 1x in.txt`

- **naive:2026-10-28_134035**: reads operand 1; writes nothing | no split
- **v1-pash**: no answer | no split

### 4 line(s) — sides differ; from {'C-naive': 4}
Examples: `split -l 5 --verbose in.txt v_`; `split --verbose -l 5 in.txt pre_`; `split --verbose -l 5 in.txt v_`; `split --verbose in.txt p_`

- **naive:2026-10-28_134035**: reads operand 1; writes operand 2, stdout | no split
- **v1-pash**: no answer | no split

### 4 line(s) — sides differ; from {'C-naive': 4}
Examples: `split -l 2 -n 1/2 in.txt`; `split --verbose -n 1/2 in.txt`; `split --verbose -n 1/2 in.txt pre_`; `split --verbose -l 5 in.txt`

- **naive:2026-10-28_134035**: reads operand 1; writes stdout | no split
- **v1-pash**: no answer | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `split -n 2 -n 1/2 in.txt pp_`; `split -n 1/2 -n 2 in.txt pp_`

- **naive:2026-10-28_134035**: exception | no split
- **v1-pash**: reads operand 1, stdin; writes nothing | no split

### 2 line(s) — sides differ; from {'C-naive': 2}
Examples: `split -l 5`; `split -l 2`

- **naive:2026-10-28_134035**: reads stdin; writes nothing | no split
- **v1-pash**: reads operand 1, stdin; writes nothing | no split

### 8 line(s); from {'C-v1': 8}
Examples: `split`; `split -n -1`; `split -n 0`; `split -n 1`

- **naive:2026-10-28_134035**: reads stdin; writes nothing | no split
- **v1-pash**: reads stdin; writes nothing | no split

