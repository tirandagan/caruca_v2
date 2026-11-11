# Decision table: cp

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `A`, `B`, `C`, `D`

### 187 line(s) — sides differ; from {'test lines of A, B, C': 187}
Examples: `cp --backup=numbered a d`; `cp --backup=bogus a d`; `cp --preserve=mode,timestamps a d`; `cp --preserve=bogus a d`

- **A**: reads operand 1, operand 2; writes operand 3 | no split
- **B**: reads operand 1, operand 2; writes operand 3 | no split
- **C**: reads operand 1, operand 2; writes operand 3 | no split
- **D**: no answer | no split

### 141 line(s) — sides differ; from {'test lines of A, B, C': 141}
Examples: `cp --backup numbered a d`; `cp --no-preserve mode a d`; `cp --sparse always a d`; `cp -S .bak a d`

- **A**: reads operand 1; writes operand 2 | no split
- **B**: reads operand 1; writes operand 2 | no split
- **C**: reads operand 1; writes operand 2 | no split
- **D**: no answer | no split

### 28 line(s) — sides differ; from {'test lines of A, B, C': 28}
Examples: `cp --backup a d`; `cp --preserve a d`; `cp --reflink a d`; `cp --sparse a d`

- **A**: reads nothing; writes operand 1 | no split
- **B**: exception | no split
- **C**: reads nothing; writes operand 1 | no split
- **D**: no answer | no split

### 17 line(s) — sides differ; from {'benchmark lines': 4, 'test lines of A, B, C': 9, 'test lines of D': 4}
Examples: `cp f fi.wav`; `cp R1.fastq Sample1.R1.fq`; `cp R2.fastq Sample1.R2.fq`; `cp sample.rtf i.rtf`

- **A**: reads operand 1; writes operand 2 | no split
- **B**: reads operand 1; writes operand 2 | no split
- **C**: reads operand 1; writes operand 2 | no split
- **D**: reads nothing; writes operand 1, operand 2 | no split

### 16 line(s) — sides differ; from {'test lines of A, B, C': 16}
Examples: `cp -dR --parents --copy-contents --attributes-only --debug a d`; `cp --debug /tmp/tmp1yckkyxo/a out`; `cp --verbose /tmp/tmp1yckkyxo/a out`; `cp -v /tmp/tmp1yckkyxo/a out`

- **A**: reads operand 1; writes operand 2 | no split
- **B**: reads operand 1; writes operand 2, stdout | no split
- **C**: reads operand 1; writes operand 2, stdout | no split
- **D**: no answer | no split

### 10 line(s) — sides differ; from {'test lines of A, B, C': 10}
Examples: `cp --interactive /tmp/tmp1yckkyxo/a out`; `cp -i /tmp/tmp1yckkyxo/a out`; `cp -H -L -P -l -s -x -p -d -a -f -i -n a d`; `cp -i a b`

- **A**: reads operand 1; writes operand 2 | no split
- **B**: reads operand 1, stdin; writes operand 2 | no split
- **C**: reads operand 1, stdin; writes operand 2 | no split
- **D**: no answer | no split

### 6 line(s) — sides differ; from {'test lines of A, B, C': 6}
Examples: `cp -t d -T a`; `cp -t /tmp/tmp1yckkyxo/a out`; `cp -t d a`; `cp --target-directory d a`

- **A**: reads operand 1; writes value of -t | no split
- **B**: reads operand 1; writes value of -t | no split
- **C**: reads operand 1; writes value of -t | no split
- **D**: no answer | no split

### 4 line(s) — sides differ; from {'test lines of A, B, C': 4}
Examples: `cp --sparse=auto --sparse=never a d`; `cp --suffix=.bak -b a d/`; `cp -S.bak -b a dir/`; `cp --suffix=.bak -b a dir/`

- **A**: reads operand 1, operand 2, operand 3; writes operand 4 | no split
- **B**: reads operand 1, operand 2, operand 3; writes operand 4 | no split
- **C**: reads operand 1, operand 2, operand 3; writes operand 4 | no split
- **D**: no answer | no split

### 4 line(s) — sides differ; from {'test lines of A, B, C': 4}
Examples: `cp -t d a b`; `cp --target-directory d a b`; `cp --target-directory . /tmp/tmp1yckkyxo/a out`; `cp -t . /tmp/tmp1yckkyxo/a out`

- **A**: reads operand 1, operand 2; writes value of -t | no split
- **B**: reads operand 1, operand 2; writes value of -t | no split
- **C**: reads operand 1, operand 2; writes value of -t | no split
- **D**: no answer | no split

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `cp`

- **A**: exception | no split
- **B**: exception | no split
- **C**: exception | no split
- **D**: no answer | no split

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `cp -t d -- a b`

- **A**: reads operand 1, operand 2, operand 3; writes value of -t | no split
- **B**: reads operand 1, operand 2, operand 3; writes value of -t | no split
- **C**: reads operand 1, operand 2, operand 3; writes value of -t | no split
- **D**: no answer | no split

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `cp -t d a d`

- **A**: reads operand 1, operand 2; writes operand 2 | no split
- **B**: reads operand 1, operand 2; writes operand 2 | no split
- **C**: reads operand 1, operand 2; writes operand 2 | no split
- **D**: no answer | no split

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `cp -abfHilLnPpRrsuvx a d`

- **A**: reads operand 1; writes operand 2 | no split
- **B**: reads operand 1, stdin; writes operand 2, stdout | no split
- **C**: reads operand 1, stdin; writes operand 2, stdout | no split
- **D**: no answer | no split

### 1 line(s) — sides differ; from {'test lines of A, B, C': 1}
Examples: `cp -t d`

- **A**: reads nothing; writes value of -t | no split
- **B**: reads nothing; writes value of -t | no split
- **C**: reads nothing; writes value of -t | no split
- **D**: reads nothing; writes operand 1, operand 2 | no split

