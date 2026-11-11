# Decision table: cp

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `naive:2026-10-28_114133`, `naive:2026-10-28_150709`, `naive:2026-10-28_153913`, `v1-pash`

### 187 line(s) — sides differ; from {'C-naive': 187}
Examples: `cp --backup=numbered a d`; `cp --backup=bogus a d`; `cp --preserve=mode,timestamps a d`; `cp --preserve=bogus a d`

- **naive:2026-10-28_114133**: reads operand 1, operand 2; writes operand 3 | no split
- **naive:2026-10-28_150709**: reads operand 1, operand 2; writes operand 3 | no split
- **naive:2026-10-28_153913**: reads operand 1, operand 2; writes operand 3 | no split
- **v1-pash**: no answer | no split

### 141 line(s) — sides differ; from {'C-naive': 141}
Examples: `cp --backup numbered a d`; `cp --no-preserve mode a d`; `cp --sparse always a d`; `cp -S .bak a d`

- **naive:2026-10-28_114133**: reads operand 1; writes operand 2 | no split
- **naive:2026-10-28_150709**: reads operand 1; writes operand 2 | no split
- **naive:2026-10-28_153913**: reads operand 1; writes operand 2 | no split
- **v1-pash**: no answer | no split

### 28 line(s) — sides differ; from {'C-naive': 28}
Examples: `cp --backup a d`; `cp --preserve a d`; `cp --reflink a d`; `cp --sparse a d`

- **naive:2026-10-28_114133**: reads nothing; writes operand 1 | no split
- **naive:2026-10-28_150709**: exception | no split
- **naive:2026-10-28_153913**: reads nothing; writes operand 1 | no split
- **v1-pash**: no answer | no split

### 17 line(s) — sides differ; from {'A (benchmark)': 4, 'C-naive': 9, 'C-v1': 4}
Examples: `cp f fi.wav`; `cp R1.fastq Sample1.R1.fq`; `cp R2.fastq Sample1.R2.fq`; `cp sample.rtf i.rtf`

- **naive:2026-10-28_114133**: reads operand 1; writes operand 2 | no split
- **naive:2026-10-28_150709**: reads operand 1; writes operand 2 | no split
- **naive:2026-10-28_153913**: reads operand 1; writes operand 2 | no split
- **v1-pash**: reads nothing; writes operand 1, operand 2 | no split

### 16 line(s) — sides differ; from {'C-naive': 16}
Examples: `cp -dR --parents --copy-contents --attributes-only --debug a d`; `cp --debug /tmp/tmp1yckkyxo/a out`; `cp --verbose /tmp/tmp1yckkyxo/a out`; `cp -v /tmp/tmp1yckkyxo/a out`

- **naive:2026-10-28_114133**: reads operand 1; writes operand 2 | no split
- **naive:2026-10-28_150709**: reads operand 1; writes operand 2, stdout | no split
- **naive:2026-10-28_153913**: reads operand 1; writes operand 2, stdout | no split
- **v1-pash**: no answer | no split

### 10 line(s) — sides differ; from {'C-naive': 10}
Examples: `cp --interactive /tmp/tmp1yckkyxo/a out`; `cp -i /tmp/tmp1yckkyxo/a out`; `cp -H -L -P -l -s -x -p -d -a -f -i -n a d`; `cp -i a b`

- **naive:2026-10-28_114133**: reads operand 1; writes operand 2 | no split
- **naive:2026-10-28_150709**: reads operand 1, stdin; writes operand 2 | no split
- **naive:2026-10-28_153913**: reads operand 1, stdin; writes operand 2 | no split
- **v1-pash**: no answer | no split

### 6 line(s) — sides differ; from {'C-naive': 6}
Examples: `cp -t d -T a`; `cp -t /tmp/tmp1yckkyxo/a out`; `cp -t d a`; `cp --target-directory d a`

- **naive:2026-10-28_114133**: reads operand 1; writes value of -t | no split
- **naive:2026-10-28_150709**: reads operand 1; writes value of -t | no split
- **naive:2026-10-28_153913**: reads operand 1; writes value of -t | no split
- **v1-pash**: no answer | no split

### 4 line(s) — sides differ; from {'C-naive': 4}
Examples: `cp --sparse=auto --sparse=never a d`; `cp --suffix=.bak -b a d/`; `cp -S.bak -b a dir/`; `cp --suffix=.bak -b a dir/`

- **naive:2026-10-28_114133**: reads operand 1, operand 2, operand 3; writes operand 4 | no split
- **naive:2026-10-28_150709**: reads operand 1, operand 2, operand 3; writes operand 4 | no split
- **naive:2026-10-28_153913**: reads operand 1, operand 2, operand 3; writes operand 4 | no split
- **v1-pash**: no answer | no split

### 4 line(s) — sides differ; from {'C-naive': 4}
Examples: `cp -t d a b`; `cp --target-directory d a b`; `cp --target-directory . /tmp/tmp1yckkyxo/a out`; `cp -t . /tmp/tmp1yckkyxo/a out`

- **naive:2026-10-28_114133**: reads operand 1, operand 2; writes value of -t | no split
- **naive:2026-10-28_150709**: reads operand 1, operand 2; writes value of -t | no split
- **naive:2026-10-28_153913**: reads operand 1, operand 2; writes value of -t | no split
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `cp`

- **naive:2026-10-28_114133**: exception | no split
- **naive:2026-10-28_150709**: exception | no split
- **naive:2026-10-28_153913**: exception | no split
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `cp -t d -- a b`

- **naive:2026-10-28_114133**: reads operand 1, operand 2, operand 3; writes value of -t | no split
- **naive:2026-10-28_150709**: reads operand 1, operand 2, operand 3; writes value of -t | no split
- **naive:2026-10-28_153913**: reads operand 1, operand 2, operand 3; writes value of -t | no split
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `cp -t d a d`

- **naive:2026-10-28_114133**: reads operand 1, operand 2; writes operand 2 | no split
- **naive:2026-10-28_150709**: reads operand 1, operand 2; writes operand 2 | no split
- **naive:2026-10-28_153913**: reads operand 1, operand 2; writes operand 2 | no split
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `cp -abfHilLnPpRrsuvx a d`

- **naive:2026-10-28_114133**: reads operand 1; writes operand 2 | no split
- **naive:2026-10-28_150709**: reads operand 1, stdin; writes operand 2, stdout | no split
- **naive:2026-10-28_153913**: reads operand 1, stdin; writes operand 2, stdout | no split
- **v1-pash**: no answer | no split

### 1 line(s) — sides differ; from {'C-naive': 1}
Examples: `cp -t d`

- **naive:2026-10-28_114133**: reads nothing; writes value of -t | no split
- **naive:2026-10-28_150709**: reads nothing; writes value of -t | no split
- **naive:2026-10-28_153913**: reads nothing; writes value of -t | no split
- **v1-pash**: reads nothing; writes operand 1, operand 2 | no split

