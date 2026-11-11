# Decision table: sort

Each group is a set of lines on which every side answers the same way. Files are named by position (operand 1, value of -o). Groups where the sides differ come first.

Answer format: what the side says is read and written | how PaSh may split it.

Sides: `A`, `B`, `C`, `D`, `E`, `F`, `R`

### 348 line(s) — sides differ; from {'benchmark lines': 3, 'test lines of A, C, D, F': 129, 'test lines of B, E': 216}
Examples: `sort OUT/input1.types OUT/input2.types OUT/input2.types`; `sort OUT/input.types OUT/input.types.rev`; `sort -nrk 1`; `sort -S=-1 --version`

- **A**: reads operand 1, operand 2; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | exception
- **D**: reads operand 1, operand 2; writes stdout | exception
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 341 line(s) — sides differ; from {'test lines of A, C, D, F': 97, 'test lines of B, E': 244}
Examples: `sort -f relpath_1`; `sort -f abspath_1`; `sort -f -S=-1`; `sort -f -S=0`

- **A**: reads operand 1; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | exception
- **D**: reads operand 1; writes stdout | exception
- **E**: reads operand 1; writes stdout | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 226 line(s) — sides differ; from {'benchmark lines': 1, 'test lines of A, C, D, F': 69, 'test lines of B, E': 156}
Examples: `sort '-t' -k 2`; `sort -S=-1 -T relpath_1`; `sort -S=-1 -T abspath_1`; `sort -S=0 -T relpath_1`

- **A**: reads operand 1, operand 2, operand 3; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3; writes stdout | exception
- **D**: reads operand 1, operand 2, operand 3; writes stdout | exception
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 169 line(s) — sides differ; from {'benchmark lines': 1, 'test lines of A, C, D, F': 3, 'test lines of B, E': 165}
Examples: `sort -k 2n`; `sort --compress-program ls`; `sort --compress-program pwd`; `sort -k 1`

- **A**: reads stdin; writes stdout | exception
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | exception
- **D**: reads stdin; writes stdout | exception
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 95 line(s) — sides differ; from {'test lines of A, C, D, F': 95}
Examples: `sort -m s1 in2`; `sort -R --random-source=/dev/zero in1`; `sort -m ma mb`; `sort -m -r ma mb`

- **A**: reads operand 1, operand 2; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | no split
- **D**: reads operand 1, operand 2; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes stdout | no split
- **R**: reads operand 1, operand 2; writes stdout | no split

### 60 line(s) — sides differ; from {'test lines of A, C, D, F': 60}
Examples: `sort -m -s -k1,1 m1 m2`; `sort -m -k1,1 m1 m2`; `sort -m -u -k1,1 m1 m2`; `sort -m -k2n ma mb`

- **A**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **D**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **R**: reads operand 1, operand 2, operand 3; writes stdout | no split

### 58 line(s) — sides differ; from {'test lines of A, C, D, F': 2, 'test lines of B, E': 56}
Examples: `sort --files0-from relpath_1`; `sort --files0-from abspath_1`; `sort -f --files0-from relpath_1`; `sort -f --files0-from abspath_1`

- **A**: reads value of --files0-from; writes stdout | no split
- **B**: no answer | no split
- **C**: reads value of --files0-from; writes stdout | no split
- **D**: reads value of --files0-from; writes stdout | no split
- **E**: no answer | no split
- **F**: reads value of --files0-from; writes stdout | no split
- **R**: reads value of --files0-from; writes stdout | no split

### 51 line(s) — sides differ; from {'test lines of A, C, D, F': 1, 'test lines of B, E': 51}
Examples: `sort -f -c`; `sort -f -C`; `sort -M -c`; `sort -M -C`

- **A**: reads stdin; writes nothing | no split
- **B**: no answer | no split
- **C**: reads stdin; writes nothing | no split
- **D**: reads stdin; writes nothing | no split
- **E**: no answer | no split
- **F**: reads stdin; writes nothing | no split
- **R**: reads stdin; writes stdout | no split

### 50 line(s) — sides differ; from {'test lines of A, C, D, F': 50}
Examples: `sort -m -k2,2n -k1,1r ma mb`; `sort -m --sort=numeric -k2 ma mb`; `sort -m -R -k1,1 --random-source=/dev/zero a b`; `sort -m -R -k1,1 --random-source=/dev/zero c d`

- **A**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | no split
- **D**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | no split
- **R**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | no split

### 45 line(s) — sides differ; from {'test lines of A, C, D, F': 1, 'test lines of B, E': 44}
Examples: `sort -o relpath_1`; `sort -o abspath_1`; `sort -f -o relpath_1`; `sort -f -o abspath_1`

- **A**: reads stdin; writes value of -o | exception
- **B**: no answer | no split
- **C**: reads stdin; writes value of -o | exception
- **D**: reads stdin; writes value of -o | no split
- **E**: reads stdin; writes stdout, value of -o | no split
- **F**: reads stdin; writes value of -o | no split
- **R**: reads stdin; writes value of -o | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 44 line(s) — sides differ; from {'test lines of A, C, D, F': 34, 'test lines of B, E': 10}
Examples: `sort -s relpath_1`; `sort -s abspath_1`; `sort -u relpath_1`; `sort -u abspath_1`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **E**: reads operand 1; writes stdout | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1; writes stdout | no split

### 44 line(s) — sides differ; from {'test lines of B, E': 44}
Examples: `sort -T relpath_1`; `sort -T abspath_1`; `sort -f -T relpath_1`; `sort -f -T abspath_1`

- **A**: reads stdin; writes stdout, value of -T | exception
- **B**: no answer | no split
- **C**: reads stdin; writes stdout, value of -T | exception
- **D**: reads stdin; writes stdout, value of -T | exception
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 43 line(s) — sides differ; from {'benchmark lines': 3, 'test lines of A, C, D, F': 22, 'test lines of B, E': 19}
Examples: `sort -k1n`; `sort -k2`; `sort /usr/share/dict/words`; `sort relpath_1`

- **A**: reads operand 1; writes stdout | exception
- **B**: reads operand 1; writes stdout | no split
- **C**: reads operand 1; writes stdout | exception
- **D**: reads operand 1; writes stdout | exception
- **E**: reads operand 1; writes stdout | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 42 line(s) — sides differ; from {'test lines of B, E': 42}
Examples: `sort --random-source relpath_1`; `sort --random-source abspath_1`; `sort -f --random-source relpath_1`; `sort -f --random-source abspath_1`

- **A**: reads stdin, value of --random-source; writes stdout | exception
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes stdout | no split
- **D**: reads stdin, value of --random-source; writes stdout | exception
- **E**: reads stdin, value of --random-source; writes stdout | no split
- **F**: reads stdin, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin, value of --random-source; writes stdout | no split

### 41 line(s) — sides differ; from {'test lines of B, E': 41}
Examples: `sort -f --version`; `sort -M --version`; `sort -V --version`; `sort --help --version`

- **A**: reads stdin; writes stdout | exception
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 37 line(s) — sides differ; from {'test lines of A, C, D, F': 20, 'test lines of B, E': 17}
Examples: `sort -R relpath_1`; `sort -R abspath_1`; `sort -R -S=-1`; `sort -R -S=0`

- **A**: reads operand 1; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | no split
- **D**: reads operand 1; writes stdout | no split
- **E**: reads operand 1; writes stdout | no split
- **F**: reads operand 1; writes stdout | no split
- **R**: reads operand 1; writes stdout | no split

### 36 line(s) — sides differ; from {'test lines of A, C, D, F': 2, 'test lines of B, E': 34}
Examples: `sort --random-source relpath_1 relpath_2`; `sort --random-source relpath_1 abspath_2`; `sort --random-source abspath_1 relpath_2`; `sort --random-source abspath_1 abspath_2`

- **A**: reads operand 1, value of --random-source; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1, value of --random-source; writes stdout | no split
- **D**: reads operand 1, value of --random-source; writes stdout | exception
- **E**: reads operand 1, value of --random-source; writes stdout | no split
- **F**: reads operand 1, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1, value of --random-source; writes stdout | no split

### 33 line(s) — sides differ; from {'test lines of A, C, D, F': 33}
Examples: `sort -S 1M in1`; `sort -S 10% in1`; `sort -S 1b in1`; `sort -S 1Q in1`

- **A**: reads operand 1; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | exception
- **D**: reads operand 1; writes stdout | exception
- **E**: no answer | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 33 line(s) — sides differ; from {'test lines of A, C, D, F': 25, 'test lines of B, E': 8}
Examples: `sort --debug relpath_1`; `sort --debug abspath_1`; `sort --debug -S=-1`; `sort --debug -S=0`

- **A**: reads operand 1; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | no split
- **D**: reads operand 1; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1; writes stdout | no split
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 30 line(s) — sides differ; from {'test lines of A, C, D, F': 30}
Examples: `sort -nru in1`; `sort -f -u big`; `sort -f -u part0`; `sort -f -u part1`

- **A**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **E**: no answer | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1; writes stdout | no split

### 30 line(s) — sides differ; from {'test lines of A, C, D, F': 10, 'test lines of B, E': 20}
Examples: `sort -f --debug`; `sort -M --debug`; `sort -V --debug`; `sort -d --debug`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: no answer | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 25 line(s) — sides differ; from {'test lines of A, C, D, F': 25}
Examples: `sort -s -k1,1 big`; `sort -s -k1,1 part0`; `sort -s -k1,1 part1`; `sort -s -k1,1 part2`

- **A**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1, operand 2; writes stdout | no split

### 25 line(s) — sides differ; from {'test lines of A, C, D, F': 9, 'test lines of B, E': 16}
Examples: `sort -o relpath_1 relpath_2`; `sort -o relpath_1 abspath_2`; `sort -o abspath_1 relpath_2`; `sort -o abspath_1 abspath_2`

- **A**: reads operand 1; writes value of -o | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes value of -o | exception
- **D**: reads operand 1; writes value of -o | no split
- **E**: reads operand 1; writes stdout, value of -o | no split
- **F**: reads operand 1; writes value of -o | no split
- **R**: reads operand 1; writes value of -o | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 24 line(s) — sides differ; from {'test lines of A, C, D, F': 24}
Examples: `sort -m f2 f2`; `sort -bdfgiMhnRrVsuz f1`; `sort --debug --merge /dev/null`; `sort --debug --random-sort /dev/null`

- **A**: reads operand 1; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | no split
- **D**: reads operand 1; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1; writes stdout | no split
- **R**: reads operand 1; writes stdout | no split

### 23 line(s) — sides differ; from {'test lines of A, C, D, F': 7, 'test lines of B, E': 16}
Examples: `sort -c relpath_1`; `sort -c abspath_1`; `sort -C relpath_1`; `sort -C abspath_1`

- **A**: reads operand 1; writes nothing | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes nothing | no split
- **D**: reads operand 1; writes nothing | no split
- **E**: reads operand 1; writes nothing | no split
- **F**: reads operand 1; writes nothing | no split
- **R**: reads operand 1; writes stdout | no split

### 22 line(s) — sides differ; from {'test lines of A, C, D, F': 1, 'test lines of B, E': 22}
Examples: `sort -f -s`; `sort -f -u`; `sort -M -u`; `sort -V -s`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | no split

### 21 line(s) — sides differ; from {'benchmark lines': 1, 'test lines of A, C, D, F': 2, 'test lines of B, E': 18}
Examples: `sort -S 512M`; `sort -M -V`; `sort -d -M`; `sort -M -n`

- **A**: reads stdin; writes stdout | exception
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | exception
- **D**: reads stdin; writes stdout | exception
- **E**: no answer | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 21 line(s) — sides differ; from {'test lines of B, E': 21}
Examples: `sort -f -m`; `sort -M -m`; `sort -R -m`; `sort -V -m`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 20 line(s) — sides differ; from {'test lines of B, E': 20}
Examples: `sort -f -z`; `sort -M -z`; `sort -V -z`; `sort -d -z`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | exception
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 20 line(s) — sides differ; from {'test lines of A, C, D, F': 1, 'test lines of B, E': 19}
Examples: `sort -M -s`; `sort -n -s`; `sort -n -u`; `sort -k 1 -s`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **E**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | no split

### 19 line(s) — sides differ; from {'test lines of B, E': 19}
Examples: `sort -f -R`; `sort -R -V`; `sort -d -R`; `sort -i -R`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 16 line(s) — sides differ; from {'test lines of B, E': 16}
Examples: `sort --files0-from relpath_1 relpath_2`; `sort --files0-from relpath_1 abspath_2`; `sort --files0-from abspath_1 relpath_2`; `sort --files0-from abspath_1 abspath_2`

- **A**: reads operand 1, value of --files0-from; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, value of --files0-from; writes stdout | no split
- **D**: reads operand 1, value of --files0-from; writes stdout | no split
- **E**: no answer | no split
- **F**: exception | no split
- **R**: reads operand 1, value of --files0-from; writes stdout | no split

### 15 line(s) — sides differ; from {'test lines of A, C, D, F': 5, 'test lines of B, E': 10}
Examples: `sort -T relpath_1 relpath_2`; `sort -T relpath_1 abspath_2`; `sort -T abspath_1 relpath_2`; `sort -T abspath_1 abspath_2`

- **A**: reads operand 1; writes stdout, value of -T | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout, value of -T | exception
- **D**: reads operand 1; writes stdout, value of -T | exception
- **E**: reads operand 1; writes stdout | no split
- **F**: reads operand 1; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 12 line(s) — sides differ; from {'benchmark lines': 5, 'test lines of A, C, D, F': 10, 'test lines of B, E': 10}
Examples: `sort -rn`; `sort -f`; `sort -n`; `sort -nr`

- **A**: reads stdin; writes stdout | exception
- **B**: reads operand 1; writes stdout | no split
- **C**: reads stdin; writes stdout | exception
- **D**: reads stdin; writes stdout | exception
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 12 line(s) — sides differ; from {'test lines of A, C, D, F': 4, 'test lines of B, E': 8}
Examples: `sort -m relpath_1`; `sort -m abspath_1`; `sort -m -S=-1`; `sort -m -S=0`

- **A**: reads operand 1; writes stdout | no split
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads operand 1; writes stdout | no split
- **D**: reads operand 1; writes stdout | no split
- **E**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads operand 1; writes stdout | no split
- **R**: reads operand 1; writes stdout | no split

### 10 line(s) — sides differ; from {'test lines of A, C, D, F': 10}
Examples: `sort -m -k1,1 -s sp0 sp1 sp2 sp3`; `sort -m -k1,1 -u sp0 sp1 sp2 sp3`; `sort -m -k1,1 -s sp00 sp01 sp02 sp03`; `sort -m -k2,2 -k1,1 sp00 sp01 sp02 sp03`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | no split
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | no split
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | no split

### 9 line(s) — sides differ; from {'test lines of B, E': 9}
Examples: `sort -M -R`; `sort -R --debug`; `sort -n -R`; `sort -g -R`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: no answer | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 8 line(s) — sides differ; from {'test lines of A, C, D, F': 8}
Examples: `sort -y in1`; `sort -y big`; `sort -y part0`; `sort -y part1`

- **A**: reads operand 1, operand 2; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | exception
- **D**: reads operand 1; writes stdout | exception
- **E**: no answer | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 6 line(s) — sides differ; from {'test lines of A, C, D, F': 6}
Examples: `sort --check=silent in1`; `sort --check=quiet in1`; `sort --check=quiet s1`; `sort --check=silent s1`

- **A**: reads operand 1, operand 2; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | exception
- **D**: reads operand 1, operand 2; writes stdout | exception
- **E**: reads operand 1; writes nothing | no split
- **F**: reads operand 1; writes nothing | no split
- **R**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 6 line(s) — sides differ; from {'test lines of A, C, D, F': 4, 'test lines of B, E': 2}
Examples: `sort -z relpath_1`; `sort -z abspath_1`; `sort -z s1`; `sort --zero-terminated s1`

- **A**: reads operand 1; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | exception
- **D**: reads operand 1; writes stdout | no split
- **E**: reads operand 1; writes stdout | no split
- **F**: reads operand 1; writes stdout | no split
- **R**: reads operand 1; writes stdout | no split

### 5 line(s) — sides differ; from {'test lines of A, C, D, F': 1, 'test lines of B, E': 4}
Examples: `sort -c -o relpath_1`; `sort -c -o abspath_1`; `sort -C -o relpath_1`; `sort -C -o abspath_1`

- **A**: reads stdin; writes value of -o | no split
- **B**: no answer | no split
- **C**: reads stdin; writes value of -o | no split
- **D**: reads stdin; writes value of -o | no split
- **E**: no answer | no split
- **F**: reads stdin; writes value of -o | no split
- **R**: reads stdin; writes value of -o | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --random-source relpath_1 -c`; `sort --random-source abspath_1 -c`; `sort --random-source relpath_1 -C`; `sort --random-source abspath_1 -C`

- **A**: reads stdin, value of --random-source; writes nothing | no split
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes nothing | no split
- **D**: reads stdin, value of --random-source; writes nothing | no split
- **E**: no answer | no split
- **F**: reads stdin, value of --random-source; writes nothing | no split
- **R**: reads stdin, value of --random-source; writes stdout | no split

### 4 line(s) — sides differ; from {'test lines of A, C, D, F': 2, 'test lines of B, E': 2}
Examples: `sort --debug -T relpath_1`; `sort --debug -T abspath_1`; `sort --debug --temporary-directory /dev/null`; `sort --debug -T /dev/null`

- **A**: reads stdin; writes stdout, value of -T | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout, value of -T | no split
- **D**: reads stdin; writes stdout, value of -T | no split
- **E**: no answer | no split
- **F**: reads stdin; writes stdout, value of -T | no split
- **R**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -c -T relpath_1`; `sort -c -T abspath_1`; `sort -C -T relpath_1`; `sort -C -T abspath_1`

- **A**: reads stdin; writes value of -T | no split
- **B**: no answer | no split
- **C**: reads stdin; writes value of -T | no split
- **D**: reads stdin; writes value of -T | no split
- **E**: no answer | no split
- **F**: reads stdin; writes value of -T | no split
- **R**: reads stdin; writes stdout, value of -T | no split

### 4 line(s) — sides differ; from {'test lines of A, C, D, F': 2, 'test lines of B, E': 2}
Examples: `sort --debug -o relpath_1`; `sort --debug -o abspath_1`; `sort --debug --output /dev/null`; `sort --debug -o /dev/null`

- **A**: reads stdin; writes value of -o | no split
- **B**: no answer | no split
- **C**: reads stdin; writes value of -o | no split
- **D**: reads stdin; writes value of -o | no split
- **E**: no answer | no split
- **F**: reads stdin; writes value of -o | no split
- **R**: reads stdin; writes value of -o | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --random-source relpath_1 --files0-from relpath_2`; `sort --random-source relpath_1 --files0-from abspath_2`; `sort --random-source abspath_1 --files0-from relpath_2`; `sort --random-source abspath_1 --files0-from abspath_2`

- **A**: reads value of --files0-from, value of --random-source; writes stdout | no split
- **B**: no answer | no split
- **C**: reads value of --files0-from, value of --random-source; writes stdout | no split
- **D**: reads value of --files0-from, value of --random-source; writes stdout | no split
- **E**: no answer | no split
- **F**: reads value of --files0-from, value of --random-source; writes stdout | no split
- **R**: reads value of --files0-from, value of --random-source; writes stdout | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -c --files0-from relpath_1`; `sort -c --files0-from abspath_1`; `sort -C --files0-from relpath_1`; `sort -C --files0-from abspath_1`

- **A**: reads value of --files0-from; writes nothing | no split
- **B**: no answer | no split
- **C**: reads value of --files0-from; writes nothing | no split
- **D**: reads value of --files0-from; writes nothing | no split
- **E**: no answer | no split
- **F**: reads value of --files0-from; writes nothing | no split
- **R**: reads value of --files0-from; writes stdout | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --files0-from relpath_1 -T relpath_2`; `sort --files0-from relpath_1 -T abspath_2`; `sort --files0-from abspath_1 -T relpath_2`; `sort --files0-from abspath_1 -T abspath_2`

- **A**: reads value of --files0-from; writes stdout, value of -T | no split
- **B**: no answer | no split
- **C**: reads value of --files0-from; writes stdout, value of -T | no split
- **D**: reads value of --files0-from; writes stdout, value of -T | no split
- **E**: no answer | no split
- **F**: reads value of --files0-from; writes stdout, value of -T | no split
- **R**: reads value of --files0-from; writes stdout, value of -T | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --files0-from relpath_1 -o relpath_2`; `sort --files0-from relpath_1 -o abspath_2`; `sort --files0-from abspath_1 -o relpath_2`; `sort --files0-from abspath_1 -o abspath_2`

- **A**: reads value of --files0-from; writes value of -o | no split
- **B**: no answer | no split
- **C**: reads value of --files0-from; writes value of -o | no split
- **D**: reads value of --files0-from; writes value of -o | no split
- **E**: no answer | no split
- **F**: reads value of --files0-from; writes value of -o | no split
- **R**: reads value of --files0-from; writes value of -o | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --version relpath_1`; `sort --version abspath_1`; `sort --help relpath_1`; `sort --help abspath_1`

- **A**: reads operand 1; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout | no split
- **D**: reads operand 1; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -c --version`; `sort -C --version`; `sort -c --help`; `sort -C --help`

- **A**: reads stdin; writes nothing | no split
- **B**: no answer | no split
- **C**: reads stdin; writes nothing | no split
- **D**: reads stdin; writes nothing | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes nothing | no split
- **R**: reads stdin; writes stdout | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -R --version`; `sort -z --version`; `sort -R --help`; `sort -z --help`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -s --version`; `sort -u --version`; `sort -s --help`; `sort -u --help`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -T relpath_1 --version`; `sort -T abspath_1 --version`; `sort -T relpath_1 --help`; `sort -T abspath_1 --help`

- **A**: reads stdin; writes stdout, value of -T | exception
- **B**: no answer | no split
- **C**: reads stdin; writes stdout, value of -T | no split
- **D**: reads stdin; writes stdout, value of -T | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --files0-from relpath_1 --version`; `sort --files0-from abspath_1 --version`; `sort --files0-from relpath_1 --help`; `sort --files0-from abspath_1 --help`

- **A**: reads value of --files0-from; writes stdout | no split
- **B**: no answer | no split
- **C**: reads value of --files0-from; writes stdout | no split
- **D**: reads value of --files0-from; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads value of --files0-from; writes stdout | no split
- **R**: reads value of --files0-from; writes stdout | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -o relpath_1 --version`; `sort -o abspath_1 --version`; `sort -o relpath_1 --help`; `sort -o abspath_1 --help`

- **A**: reads stdin; writes value of -o | exception
- **B**: no answer | no split
- **C**: reads stdin; writes value of -o | no split
- **D**: reads stdin; writes value of -o | no split
- **E**: reads nothing; writes stdout, value of -o | no split
- **F**: reads stdin; writes value of -o | no split
- **R**: reads stdin; writes value of -o | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --random-source relpath_1 -s`; `sort --random-source abspath_1 -s`; `sort --random-source relpath_1 -u`; `sort --random-source abspath_1 -u`

- **A**: reads stdin, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes stdout | no split
- **D**: reads stdin, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **E**: reads stdin, value of --random-source; writes stdout | no split
- **F**: reads stdin, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin, value of --random-source; writes stdout | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --random-source relpath_1 -T relpath_2`; `sort --random-source relpath_1 -T abspath_2`; `sort --random-source abspath_1 -T relpath_2`; `sort --random-source abspath_1 -T abspath_2`

- **A**: reads stdin, value of --random-source; writes stdout, value of -T | exception
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes stdout, value of -T | no split
- **D**: reads stdin, value of --random-source; writes stdout, value of -T | exception
- **E**: reads stdin, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin, value of --random-source; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin, value of --random-source; writes stdout, value of -T | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --random-source relpath_1 -o relpath_2`; `sort --random-source relpath_1 -o abspath_2`; `sort --random-source abspath_1 -o relpath_2`; `sort --random-source abspath_1 -o abspath_2`

- **A**: reads stdin, value of --random-source; writes value of -o | exception
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes value of -o | no split
- **D**: reads stdin, value of --random-source; writes value of -o | no split
- **E**: reads stdin, value of --random-source; writes stdout, value of -o | no split
- **F**: reads stdin, value of --random-source; writes value of -o | no split
- **R**: reads stdin, value of --random-source; writes value of -o | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -s -T relpath_1`; `sort -s -T abspath_1`; `sort -T relpath_1 -u`; `sort -T abspath_1 -u`

- **A**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout, value of -T | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -o relpath_1 -T relpath_2`; `sort -o relpath_1 -T abspath_2`; `sort -o abspath_1 -T relpath_2`; `sort -o abspath_1 -T abspath_2`

- **A**: reads stdin; writes value of -T, value of -o | exception
- **B**: no answer | no split
- **C**: reads stdin; writes value of -T, value of -o | exception
- **D**: reads stdin; writes value of -T, value of -o | no split
- **E**: reads stdin; writes stdout, value of -o | no split
- **F**: reads stdin; writes value of -T, value of -o | no split
- **R**: reads stdin; writes value of -T, value of -o | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -R -o relpath_1`; `sort -R -o abspath_1`; `sort -m -o relpath_1`; `sort -m -o abspath_1`

- **A**: reads stdin; writes value of -o | no split
- **B**: no answer | no split
- **C**: reads stdin; writes value of -o | no split
- **D**: reads stdin; writes value of -o | no split
- **E**: reads stdin; writes stdout, value of -o | no split
- **F**: reads stdin; writes value of -o | no split
- **R**: reads stdin; writes value of -o | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort -o relpath_1 -s`; `sort -o abspath_1 -s`; `sort -o relpath_1 -u`; `sort -o abspath_1 -u`

- **A**: reads stdin; writes value of -o | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: no answer | no split
- **C**: reads stdin; writes value of -o | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads stdin; writes value of -o | no split
- **E**: reads stdin; writes stdout, value of -o | no split
- **F**: reads stdin; writes value of -o | no split
- **R**: reads stdin; writes value of -o | no split

### 4 line(s) — sides differ; from {'test lines of B, E': 4}
Examples: `sort --random-source relpath_1 --version`; `sort --random-source abspath_1 --version`; `sort --random-source relpath_1 --help`; `sort --random-source abspath_1 --help`

- **A**: reads stdin, value of --random-source; writes stdout | exception
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes stdout | no split
- **D**: reads stdin, value of --random-source; writes stdout | no split
- **E**: reads value of --random-source; writes stdout | no split
- **F**: reads stdin, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin, value of --random-source; writes stdout | no split

### 3 line(s) — sides differ; from {'test lines of A, C, D, F': 3}
Examples: `sort -m -k1,1 -s sp00 sp01 sp02 sp03 sp1 sp2 sp3`; `sort -m -k1,1 -u sp00 sp01 sp02 sp03 sp1 sp2 sp3`; `sort -m -k2,2 -k1,1 sp00 sp01 sp02 sp03 sp1 sp2 sp3`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | no split
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | no split
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7, operand 8, operand 9; writes stdout | no split

### 3 line(s) — sides differ; from {'test lines of A, C, D, F': 3}
Examples: `sort -m -t ' ' '' -k 3n sorted0 sorted1 sorted2 sorted3`; `sort -m -f -u sp00 sp01 sp02 sp03 sp1 sp2 sp3`; `sort -m -R sp00 sp01 sp02 sp03 sp1 sp2 sp3`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | no split
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | no split
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6, operand 7; writes stdout | no split

### 3 line(s) — sides differ; from {'test lines of A, C, D, F': 3}
Examples: `sort -m --key 2 --field-separator ' ' '' sorted0 sorted1 sorted2 sorted3`; `sort -m -k1,1 sp0 sp1 sp2 sp3`; `sort -m -k1,1 parts/p0.sorted parts/p1.sorted parts/p2.sorted parts/p3.sorted`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | no split
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | no split
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5; writes stdout | no split

### 3 line(s) — sides differ; from {'test lines of A, C, D, F': 3}
Examples: `sort --check=diagnose-first in1`; `sort --check=diagnose-first s1`; `sort --check=diagnose-first f1`

- **A**: reads operand 1, operand 2; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | exception
- **D**: reads operand 1, operand 2; writes stdout | exception
- **E**: no answer | no split
- **F**: reads operand 1; writes nothing | no split
- **R**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 3 line(s) — sides differ; from {'test lines of A, C, D, F': 3}
Examples: `sort --check quiet in1`; `sort --check diagnose-first f1`; `sort --check quiet f1`

- **A**: reads operand 1, operand 2; writes nothing | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes nothing | no split
- **D**: reads operand 1; writes nothing | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes nothing | no split
- **R**: reads operand 1, operand 2; writes stdout | no split

### 3 line(s) — sides differ; from {'test lines of A, C, D, F': 1, 'test lines of B, E': 2}
Examples: `sort --random-source relpath_1 --debug`; `sort --random-source abspath_1 --debug`; `sort --debug --random-source /dev/null`

- **A**: reads stdin, value of --random-source; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes stdout | no split
- **D**: reads stdin, value of --random-source; writes stdout | no split
- **E**: no answer | no split
- **F**: reads stdin, value of --random-source; writes stdout | no split
- **R**: reads stdin, value of --random-source; writes stdout | no split

### 3 line(s) — sides differ; from {'test lines of A, C, D, F': 3}
Examples: `sort -o o1 -o o2 in1`; `sort -o a.txt -o b.txt f2`; `sort -o out5 -o out6 f1`

- **A**: reads operand 1; writes value of -o, value of -o | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes value of -o, value of -o | exception
- **D**: reads operand 1; writes value of -o, value of -o | no split
- **E**: reads operand 1; writes stdout, value of -o, value of -o | no split
- **F**: reads operand 1; writes value of -o, value of -o | no split
- **R**: reads operand 1; writes value of -o, value of -o | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 3 line(s) — sides differ; from {'test lines of A, C, D, F': 2, 'test lines of B, E': 2}
Examples: `sort -c`; `sort -C`; `sort -cu`

- **A**: reads stdin; writes nothing | no split
- **B**: reads operand 1; writes stdout | no split
- **C**: reads stdin; writes nothing | no split
- **D**: reads stdin; writes nothing | no split
- **E**: no answer | no split
- **F**: reads stdin; writes nothing | no split
- **R**: reads stdin; writes stdout | no split

### 2 line(s) — sides differ; from {'benchmark lines': 1, 'test lines of A, C, D, F': 1}
Examples: `sort -k2 -n -t, -r`; `sort --key=1 --field-separator=, --output=out3 f1`

- **A**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | exception
- **D**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | exception
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1, operand 2, operand 3, operand 4; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 2 line(s) — sides differ; from {'test lines of A, C, D, F': 2}
Examples: `sort -c in1 in2`; `sort -c f1 f2`

- **A**: reads operand 1, operand 2; writes nothing | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes nothing | no split
- **D**: reads operand 1, operand 2; writes nothing | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes nothing | no split
- **R**: reads operand 1, operand 2; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of A, C, D, F': 2}
Examples: `sort --debug -C /dev/null`; `sort --debug -c /dev/null`

- **A**: reads operand 1; writes nothing | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes nothing | no split
- **D**: reads operand 1; writes nothing | no split
- **E**: no answer | no split
- **F**: reads operand 1; writes nothing | no split
- **R**: reads operand 1; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of A, C, D, F': 2}
Examples: `sort -c -o out2 s1`; `sort -c -o x f2`

- **A**: reads operand 1; writes value of -o | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes value of -o | no split
- **D**: reads operand 1; writes value of -o | no split
- **E**: no answer | no split
- **F**: reads operand 1; writes value of -o | no split
- **R**: reads operand 1; writes value of -o | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort --debug --version`; `sort --debug --help`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 2 line(s) — sides differ; from {'test lines of A, C, D, F': 2}
Examples: `sort --check s1`; `sort --check f1`

- **A**: reads operand 1; writes nothing | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes nothing | no split
- **D**: reads stdin; writes nothing | no split
- **E**: reads operand 1; writes nothing | no split
- **F**: reads operand 1; writes nothing | no split
- **R**: reads operand 1; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of A, C, D, F': 2}
Examples: `sort -o in1 in1`; `sort -o f1 f1`

- **A**: reads operand 1; writes operand 1 | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes operand 1 | exception
- **D**: reads operand 1; writes operand 1 | no split
- **E**: reads operand 1; writes operand 1, stdout | no split
- **F**: reads operand 1; writes operand 1 | no split
- **R**: reads operand 1; writes operand 1 | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 2 line(s) — sides differ; from {'test lines of A, C, D, F': 2}
Examples: `sort -T /tmp -T /var/tmp in1`; `sort -T /tmp -T /var/tmp f1`

- **A**: reads operand 1; writes stdout, value of -T, value of -T | exception
- **B**: no answer | no split
- **C**: reads operand 1; writes stdout, value of -T, value of -T | exception
- **D**: reads operand 1; writes stdout, value of -T, value of -T | exception
- **E**: reads operand 1; writes stdout | no split
- **F**: reads operand 1; writes stdout, value of -T, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1; writes stdout, value of -T, value of -T | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort --random-source relpath_1 -z`; `sort --random-source abspath_1 -z`

- **A**: reads stdin, value of --random-source; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes stdout | no split
- **D**: reads stdin, value of --random-source; writes stdout | no split
- **E**: reads stdin, value of --random-source; writes stdout | no split
- **F**: reads stdin, value of --random-source; writes stdout | no split
- **R**: reads stdin, value of --random-source; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -R --random-source relpath_1`; `sort -R --random-source abspath_1`

- **A**: reads stdin, value of --random-source; writes stdout | exception
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes stdout | no split
- **D**: reads stdin, value of --random-source; writes stdout | no split
- **E**: reads stdin, value of --random-source; writes stdout | no split
- **F**: reads stdin, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin, value of --random-source; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort --random-source relpath_1 -m`; `sort --random-source abspath_1 -m`

- **A**: reads stdin, value of --random-source; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin, value of --random-source; writes stdout | no split
- **D**: reads stdin, value of --random-source; writes stdout | no split
- **E**: reads stdin, value of --random-source; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin, value of --random-source; writes stdout | no split
- **R**: reads stdin, value of --random-source; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -c -z`; `sort -C -z`

- **A**: reads stdin; writes nothing | no split
- **B**: no answer | no split
- **C**: reads stdin; writes nothing | no split
- **D**: reads stdin; writes nothing | no split
- **E**: reads stdin; writes nothing | no split
- **F**: reads stdin; writes nothing | no split
- **R**: reads stdin; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -s -z`; `sort -u -z`

- **A**: reads stdin; writes stdout | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -T relpath_1 -z`; `sort -T abspath_1 -z`

- **A**: reads stdin; writes stdout, value of -T | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout, value of -T | exception
- **D**: reads stdin; writes stdout, value of -T | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout, value of -T | no split
- **R**: reads stdin; writes stdout, value of -T | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -R -T relpath_1`; `sort -R -T abspath_1`

- **A**: reads stdin; writes stdout, value of -T | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout, value of -T | no split
- **D**: reads stdin; writes stdout, value of -T | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout, value of -T | no split
- **R**: reads stdin; writes stdout, value of -T | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -m -T relpath_1`; `sort -m -T abspath_1`

- **A**: reads stdin; writes stdout, value of -T | no split
- **B**: no answer | no split
- **C**: reads stdin; writes stdout, value of -T | no split
- **D**: reads stdin; writes stdout, value of -T | no split
- **E**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin; writes stdout, value of -T | no split
- **R**: reads stdin; writes stdout, value of -T | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -o relpath_1 -z`; `sort -o abspath_1 -z`

- **A**: reads stdin; writes value of -o | no split
- **B**: no answer | no split
- **C**: reads stdin; writes value of -o | exception
- **D**: reads stdin; writes value of -o | no split
- **E**: reads stdin; writes stdout, value of -o | no split
- **F**: reads stdin; writes value of -o | no split
- **R**: reads stdin; writes value of -o | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort --version`; `sort --help`

- **A**: reads stdin; writes stdout | exception
- **B**: reads operand 1; writes stdout | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 2 line(s) — sides differ; from {'benchmark lines': 1, 'test lines of A, C, D, F': 2, 'test lines of B, E': 2}
Examples: `sort -u`; `sort -s`

- **A**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **B**: reads operand 1; writes stdout | no split
- **C**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_N_ARY
- **D**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -m --version`; `sort -m --help`

- **A**: reads stdin; writes stdout | no split
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads nothing; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 2 line(s) — sides differ; from {'test lines of B, E': 2}
Examples: `sort -m -s`; `sort -m -u`

- **A**: reads stdin; writes stdout | no split
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 1 line(s) — sides differ; from {'test lines of A, C, D, F': 1}
Examples: `sort -k1 -t, -oout4 -S1M -T/tmp f1`

- **A**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | exception
- **D**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | exception
- **E**: no answer | no split
- **F**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1, operand 2, operand 3, operand 4, operand 5, operand 6; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 1 line(s) — sides differ; from {'test lines of A, C, D, F': 1}
Examples: `sort -y 5 f1`

- **A**: reads operand 1, operand 2, operand 3; writes stdout | exception
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | exception
- **D**: reads operand 1, operand 2; writes stdout | exception
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads operand 1, operand 2, operand 3; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 1 line(s) — sides differ; from {'test lines of A, C, D, F': 1}
Examples: `sort -m -y ma mb`

- **A**: reads operand 1, operand 2, operand 3; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | no split
- **D**: reads operand 1, operand 2; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes stdout | no split
- **R**: reads operand 1, operand 2, operand 3; writes stdout | no split

### 1 line(s) — sides differ; from {'test lines of A, C, D, F': 1}
Examples: `sort --debug -k2n part0`

- **A**: reads operand 1, operand 2; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, operand 2; writes stdout | no split
- **D**: reads operand 1, operand 2; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, operand 2; writes stdout | no split
- **R**: reads operand 1, operand 2; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 1 line(s) — sides differ; from {'test lines of A, C, D, F': 1}
Examples: `sort -m -R --random-source /dev/zero f2 f2`

- **A**: reads operand 1, value of --random-source; writes stdout | no split
- **B**: no answer | no split
- **C**: reads operand 1, value of --random-source; writes stdout | no split
- **D**: reads operand 1, value of --random-source; writes stdout | no split
- **E**: no answer | no split
- **F**: reads operand 1, value of --random-source; writes stdout | no split
- **R**: reads operand 1, value of --random-source; writes stdout | no split

### 1 line(s) — sides differ; from {'test lines of A, C, D, F': 1}
Examples: `sort --debug --check /dev/null`

- **A**: reads operand 1; writes nothing | no split
- **B**: no answer | no split
- **C**: reads operand 1; writes nothing | no split
- **D**: reads stdin; writes nothing | no split
- **E**: no answer | no split
- **F**: reads operand 1; writes nothing | no split
- **R**: reads operand 1; writes stdout | no split

### 1 line(s) — sides differ; from {'test lines of B, E': 1}
Examples: `sort --debug`

- **A**: reads stdin; writes stdout | no split
- **B**: reads operand 1; writes stdout | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: no answer | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 1 line(s) — sides differ; from {'test lines of A, C, D, F': 1, 'test lines of B, E': 1}
Examples: `sort -z`

- **A**: reads stdin; writes stdout | no split
- **B**: reads operand 1; writes stdout | no split
- **C**: reads stdin; writes stdout | exception
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 1 line(s) — sides differ; from {'test lines of A, C, D, F': 1, 'test lines of B, E': 1}
Examples: `sort -R`

- **A**: reads stdin; writes stdout | no split
- **B**: reads operand 1; writes stdout | no split
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 1 line(s) — sides differ; from {'test lines of B, E': 1}
Examples: `sort -m -z`

- **A**: reads stdin; writes stdout | no split
- **B**: reads operand 1; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

### 1 line(s) — sides differ; from {'benchmark lines': 1, 'test lines of A, C, D, F': 1, 'test lines of B, E': 1}
Examples: `sort`

- **A**: reads stdin; writes stdout | exception
- **B**: reads stdin; writes stdout | no split
- **C**: reads stdin; writes stdout | exception
- **D**: reads stdin; writes stdout | exception
- **E**: reads stdin; writes stdout | no split
- **F**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY
- **R**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CUSTOM_2_ARY

### 1 line(s) — sides differ; from {'test lines of B, E': 1}
Examples: `sort -m`

- **A**: reads stdin; writes stdout | no split
- **B**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **C**: reads stdin; writes stdout | no split
- **D**: reads stdin; writes stdout | no split
- **E**: reads stdin; writes stdout | split: CONSEC_CHUNKS → CONCATENATE; ROUND_ROBIN_PLAIN → CONCATENATE
- **F**: reads stdin; writes stdout | no split
- **R**: reads stdin; writes stdout | no split

