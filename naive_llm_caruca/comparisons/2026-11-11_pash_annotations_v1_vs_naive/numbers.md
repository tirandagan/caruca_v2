# Numbers: v1 vs the naive LLM vs PaSh's own (task 021, scorer output)

Made by `score_pash.py`. Counts only. Each rate is out of the lines that side was asked about.

## Completeness: what each side gives PaSh

| Command | Side | Lines | Input/output answered | No answer | Exception | No class | Parse failed | Split allowed |
|---|---|---|---|---|---|---|---|---|
| cat | v1-pash | 215 | 99/215 (46%) | 116 | 0 | 0 | 0 | 85/215 (40%) |
| cat | naive:2026-10-28_100411 | 215 | 215/215 (100%) | 0 | 0 | 0 | 0 | 203/215 (94%) |
| cat | pash-own | 215 | 215/215 (100%) | 0 | 0 | 0 | 0 | 0/215 (0%) |
| cp | v1-pash | 418 | 18/418 (4%) | 400 | 0 | 0 | 0 | 0/418 (0%) |
| cp | naive:2026-10-28_114133 | 418 | 417/418 (100%) | 0 | 1 | 0 | 0 | 0/418 (0%) |
| cp | naive:2026-10-28_150709 | 418 | 389/418 (93%) | 0 | 29 | 0 | 0 | 0/418 (0%) |
| cp | naive:2026-10-28_153913 | 418 | 417/418 (100%) | 0 | 1 | 0 | 0 | 0/418 (0%) |
| cut | v1-pash | 8826 | 77/8826 (1%) | 8749 | 0 | 0 | 0 | 77/8826 (1%) |
| cut | v1-main | 8826 | 402/8826 (5%) | 8424 | 0 | 0 | 0 | 181/8826 (2%) |
| cut | naive:2026-10-20_135253 | 8826 | 8826/8826 (100%) | 0 | 0 | 0 | 0 | 6882/8826 (78%) |
| cut | naive:2026-10-27_230555 | 8826 | 8826/8826 (100%) | 0 | 0 | 0 | 0 | 6882/8826 (78%) |
| cut | naive:2026-10-28_145447 | 8826 | 8826/8826 (100%) | 0 | 0 | 0 | 0 | 6882/8826 (78%) |
| cut | naive:2026-10-28_152550 | 8826 | 8826/8826 (100%) | 0 | 0 | 0 | 0 | 6882/8826 (78%) |
| cut | pash-own | 8826 | 8826/8826 (100%) | 0 | 0 | 0 | 0 | 8826/8826 (100%) |
| grep | v1-pash | 279 | 72/279 (26%) | 207 | 0 | 0 | 0 | 5/279 (2%) |
| grep | naive:2026-10-13_193448 | 279 | 228/279 (82%) | 0 | 51 | 0 | 0 | 103/279 (37%) |
| grep | naive:2026-10-20_112956 | 279 | 278/279 (100%) | 0 | 1 | 0 | 0 | 189/279 (68%) |
| grep | naive:2026-10-28_135447 | 279 | 279/279 (100%) | 0 | 0 | 0 | 0 | 189/279 (68%) |
| grep | pash-own | 279 | 278/279 (100%) | 0 | 1 | 0 | 0 | 229/279 (82%) |
| rm | v1-pash | 368 | 21/368 (6%) | 347 | 0 | 0 | 0 | 0/368 (0%) |
| rm | v1-main | 368 | 172/368 (47%) | 196 | 0 | 0 | 0 | 0/368 (0%) |
| rm | naive:2026-10-20_121932 | 368 | 368/368 (100%) | 0 | 0 | 0 | 0 | 0/368 (0%) |
| rm | naive:2026-10-28_105951 | 368 | 368/368 (100%) | 0 | 0 | 0 | 0 | 0/368 (0%) |
| rm | pash-own | 368 | 368/368 (100%) | 0 | 0 | 0 | 0 | 0/368 (0%) |
| sort | v1-pash | 2345 | 84/2345 (4%) | 2261 | 0 | 0 | 0 | 18/2345 (1%) |
| sort | v1-main | 2345 | 1145/2345 (49%) | 1200 | 0 | 0 | 0 | 64/2345 (3%) |
| sort | naive:2026-10-20_160340 | 2345 | 2345/2345 (100%) | 0 | 0 | 0 | 0 | 151/2345 (6%) |
| sort | naive:2026-10-28_140825 | 2345 | 2329/2345 (99%) | 0 | 16 | 0 | 0 | 1561/2345 (67%) |
| sort | naive:2026-10-28_151151 | 2345 | 2345/2345 (100%) | 0 | 0 | 0 | 0 | 159/2345 (7%) |
| sort | naive:2026-10-28_154444 | 2345 | 2345/2345 (100%) | 0 | 0 | 0 | 0 | 153/2345 (7%) |
| sort | pash-own | 2345 | 2345/2345 (100%) | 0 | 0 | 0 | 0 | 1485/2345 (63%) |
| split | v1-pash | 162 | 77/162 (48%) | 85 | 0 | 0 | 0 | 0/162 (0%) |
| split | naive:2026-10-28_134035 | 162 | 138/162 (85%) | 0 | 24 | 0 | 0 | 0/162 (0%) |
| wc | v1-pash | 40 | 5/40 (12%) | 35 | 0 | 0 | 0 | 0/40 (0%) |
| wc | naive:2026-10-28_091448 | 40 | 40/40 (100%) | 0 | 0 | 0 | 0 | 0/40 (0%) |
| wc | pash-own | 40 | 39/40 (98%) | 0 | 1 | 0 | 0 | 0/40 (0%) |

## Input/output sets: v1 against each naive run (Greenberg's question)

Per line, the set of (file or stream, read/written) each side gives PaSh. "v1 larger" means v1's set contains the agent's and more.

| Command | v1 | Naive run | Lines | Identical | v1 larger | Agent larger | Overlapping | Disjoint | v1 no answer | Agent no answer | Both none |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cat | v1-pash | naive:2026-10-28_100411 | 215 | 98/215 (46%) | 0 | 0 | 1 | 0 | 116 | 0 | 0 |
| cp | v1-pash | naive:2026-10-28_114133 | 418 | 0/418 (0%) | 1 | 0 | 17 | 0 | 399 | 0 | 1 |
| cp | v1-pash | naive:2026-10-28_150709 | 418 | 0/418 (0%) | 1 | 0 | 17 | 0 | 371 | 0 | 29 |
| cp | v1-pash | naive:2026-10-28_153913 | 418 | 0/418 (0%) | 1 | 0 | 17 | 0 | 399 | 0 | 1 |
| cut | v1-main | naive:2026-10-20_135253 | 8826 | 349/8826 (4%) | 0 | 53 | 0 | 0 | 8424 | 0 | 0 |
| cut | v1-main | naive:2026-10-27_230555 | 8826 | 349/8826 (4%) | 0 | 53 | 0 | 0 | 8424 | 0 | 0 |
| cut | v1-main | naive:2026-10-28_145447 | 8826 | 349/8826 (4%) | 0 | 53 | 0 | 0 | 8424 | 0 | 0 |
| cut | v1-main | naive:2026-10-28_152550 | 8826 | 349/8826 (4%) | 0 | 53 | 0 | 0 | 8424 | 0 | 0 |
| cut | v1-pash | naive:2026-10-20_135253 | 8826 | 77/8826 (1%) | 0 | 0 | 0 | 0 | 8749 | 0 | 0 |
| cut | v1-pash | naive:2026-10-27_230555 | 8826 | 77/8826 (1%) | 0 | 0 | 0 | 0 | 8749 | 0 | 0 |
| cut | v1-pash | naive:2026-10-28_145447 | 8826 | 77/8826 (1%) | 0 | 0 | 0 | 0 | 8749 | 0 | 0 |
| cut | v1-pash | naive:2026-10-28_152550 | 8826 | 77/8826 (1%) | 0 | 0 | 0 | 0 | 8749 | 0 | 0 |
| grep | v1-pash | naive:2026-10-13_193448 | 279 | 51/279 (18%) | 0 | 2 | 13 | 1 | 161 | 5 | 46 |
| grep | v1-pash | naive:2026-10-20_112956 | 279 | 56/279 (20%) | 1 | 2 | 12 | 1 | 206 | 0 | 1 |
| grep | v1-pash | naive:2026-10-28_135447 | 279 | 56/279 (20%) | 1 | 2 | 12 | 1 | 207 | 0 | 0 |
| rm | v1-main | naive:2026-10-20_121932 | 368 | 134/368 (36%) | 0 | 38 | 0 | 0 | 196 | 0 | 0 |
| rm | v1-main | naive:2026-10-28_105951 | 368 | 116/368 (32%) | 18 | 0 | 0 | 38 | 196 | 0 | 0 |
| rm | v1-pash | naive:2026-10-20_121932 | 368 | 20/368 (5%) | 1 | 0 | 0 | 0 | 347 | 0 | 0 |
| rm | v1-pash | naive:2026-10-28_105951 | 368 | 20/368 (5%) | 1 | 0 | 0 | 0 | 347 | 0 | 0 |
| sort | v1-main | naive:2026-10-20_160340 | 2345 | 890/2345 (38%) | 89 | 152 | 8 | 6 | 1200 | 0 | 0 |
| sort | v1-main | naive:2026-10-28_140825 | 2345 | 898/2345 (38%) | 89 | 146 | 8 | 4 | 1184 | 0 | 16 |
| sort | v1-main | naive:2026-10-28_151151 | 2345 | 892/2345 (38%) | 89 | 152 | 8 | 4 | 1200 | 0 | 0 |
| sort | v1-main | naive:2026-10-28_154444 | 2345 | 892/2345 (38%) | 89 | 152 | 8 | 4 | 1200 | 0 | 0 |
| sort | v1-pash | naive:2026-10-20_160340 | 2345 | 57/2345 (2%) | 0 | 0 | 24 | 3 | 2261 | 0 | 0 |
| sort | v1-pash | naive:2026-10-28_140825 | 2345 | 57/2345 (2%) | 0 | 0 | 24 | 3 | 2245 | 0 | 16 |
| sort | v1-pash | naive:2026-10-28_151151 | 2345 | 57/2345 (2%) | 0 | 0 | 24 | 3 | 2261 | 0 | 0 |
| sort | v1-pash | naive:2026-10-28_154444 | 2345 | 57/2345 (2%) | 0 | 0 | 24 | 3 | 2261 | 0 | 0 |
| split | v1-pash | naive:2026-10-28_134035 | 162 | 8/162 (5%) | 28 | 0 | 38 | 1 | 63 | 2 | 22 |
| wc | v1-pash | naive:2026-10-28_091448 | 40 | 5/40 (12%) | 0 | 0 | 0 | 0 | 35 | 0 | 0 |

## Input/output differences by type (v1 vs naive, lines where both answer)

| Command | Type | Elements | Lines | Example (line: word, v1 → agent) |
|---|---|---|---|---|
| cat | operand used by one side only | 1 | 1 | `cat -s`: -s, ['read'] → ['—'] |
| cat | standard input differs | 1 | 1 | `cat -s`: <stdin>, ['—'] → ['read'] |
| cp | operand direction differs | 51 | 17 | `cp f fi.wav`: f, ['written'] → ['read'] |
| cp | operand used by one side only | 3 | 1 | `cp -t d`: -t, ['written'] → ['—'] |
| cut | standard input differs | 196 | 49 | `cut --help`: <stdin>, ['—'] → ['read'] |
| cut | operand used by one side only | 16 | 4 | `cut --help relpath_1`: relpath_1, ['—'] → ['read'] |
| grep | standard input differs | 46 | 16 | `grep -vE '^_[^_]'`: <stdin>, ['—'] → ['read'] |
| grep | operand used by one side only | 42 | 14 | `grep -vE '^_[^_]'`: ^_[^_], ['read'] → ['—'] |
| grep | kind only | 33 | 29 | `grep -R a relpath_1`: relpath_1, ['STREAM_INPUT'] → ['OTHER_INPUT'] |
| grep | standard output differs | 3 | 1 | `grep -q foo`: <stdout>, ['written'] → ['—'] |
| rm | operand used by one side only | 78 | 39 | `rm --help relpath_1`: relpath_1, ['—'] → ['written'] |
| rm | standard output differs | 56 | 56 | `rm --help relpath_1`: <stdout>, ['written'] → ['—'] |
| sort | standard output differs | 434 | 110 | `sort -c`: <stdout>, ['written'] → ['—'] |
| sort | kind only | 400 | 100 | `sort --random-source relpath_1`: relpath_1, ['STREAM_INPUT'] → ['CONFIG_INPUT'] |
| sort | standard input differs | 394 | 96 | `sort -rn`: <stdin>, ['—'] → ['read'] |
| sort | option value typed differently | 356 | 87 | `sort -T relpath_1`: relpath_1, ['—'] → ['written'] |
| sort | operand used by one side only | 144 | 39 | `sort -rn`: -rn, ['read'] → ['—'] |
| split | standard input differs | 65 | 65 | `split string`: <stdin>, ['read'] → ['—'] |
| split | operand used by one side only | 31 | 30 | `split relpath_1 string`: string, ['—'] → ['written'] |
| split | standard output differs | 11 | 11 | `split -n 2/3 in.txt`: <stdout>, ['—'] → ['written'] |

## Splitting: v1 against each naive run

| Command | v1 | Naive run | Lines both answer | Both split | Only v1 splits | Only agent splits | Neither | Same recipes when both split | Agent's recipes include v1's |
|---|---|---|---|---|---|---|---|---|---|
| cat | v1-pash | naive:2026-10-28_100411 | 215 | 85 | 0 | 118 | 12 | 0/85 (0%) | 84/85 (99%) |
| cp | v1-pash | naive:2026-10-28_114133 | 418 | 0 | 0 | 0 | 418 | 0/0 | 0/0 |
| cp | v1-pash | naive:2026-10-28_150709 | 418 | 0 | 0 | 0 | 418 | 0/0 | 0/0 |
| cp | v1-pash | naive:2026-10-28_153913 | 418 | 0 | 0 | 0 | 418 | 0/0 | 0/0 |
| cut | v1-main | naive:2026-10-20_135253 | 8826 | 181 | 0 | 6701 | 1944 | 181/181 (100%) | 181/181 (100%) |
| cut | v1-main | naive:2026-10-27_230555 | 8826 | 181 | 0 | 6701 | 1944 | 181/181 (100%) | 181/181 (100%) |
| cut | v1-main | naive:2026-10-28_145447 | 8826 | 181 | 0 | 6701 | 1944 | 181/181 (100%) | 181/181 (100%) |
| cut | v1-main | naive:2026-10-28_152550 | 8826 | 181 | 0 | 6701 | 1944 | 181/181 (100%) | 181/181 (100%) |
| cut | v1-pash | naive:2026-10-20_135253 | 8826 | 77 | 0 | 6805 | 1944 | 77/77 (100%) | 77/77 (100%) |
| cut | v1-pash | naive:2026-10-27_230555 | 8826 | 77 | 0 | 6805 | 1944 | 77/77 (100%) | 77/77 (100%) |
| cut | v1-pash | naive:2026-10-28_145447 | 8826 | 77 | 0 | 6805 | 1944 | 77/77 (100%) | 77/77 (100%) |
| cut | v1-pash | naive:2026-10-28_152550 | 8826 | 77 | 0 | 6805 | 1944 | 77/77 (100%) | 77/77 (100%) |
| grep | v1-pash | naive:2026-10-13_193448 | 279 | 5 | 0 | 98 | 176 | 5/5 (100%) | 5/5 (100%) |
| grep | v1-pash | naive:2026-10-20_112956 | 279 | 5 | 0 | 184 | 90 | 5/5 (100%) | 5/5 (100%) |
| grep | v1-pash | naive:2026-10-28_135447 | 279 | 5 | 0 | 184 | 90 | 5/5 (100%) | 5/5 (100%) |
| rm | v1-main | naive:2026-10-20_121932 | 368 | 0 | 0 | 0 | 368 | 0/0 | 0/0 |
| rm | v1-main | naive:2026-10-28_105951 | 368 | 0 | 0 | 0 | 368 | 0/0 | 0/0 |
| rm | v1-pash | naive:2026-10-20_121932 | 368 | 0 | 0 | 0 | 368 | 0/0 | 0/0 |
| rm | v1-pash | naive:2026-10-28_105951 | 368 | 0 | 0 | 0 | 368 | 0/0 | 0/0 |
| sort | v1-main | naive:2026-10-20_160340 | 987 | 20 | 40 | 131 | 796 | 0/20 (0%) | 0/20 (0%) |
| sort | v1-main | naive:2026-10-28_140825 | 2345 | 24 | 40 | 1537 | 744 | 0/24 (0%) | 0/24 (0%) |
| sort | v1-main | naive:2026-10-28_151151 | 843 | 20 | 40 | 139 | 644 | 0/20 (0%) | 0/20 (0%) |
| sort | v1-main | naive:2026-10-28_154444 | 959 | 20 | 44 | 133 | 762 | 0/20 (0%) | 0/20 (0%) |
| sort | v1-pash | naive:2026-10-20_160340 | 987 | 0 | 18 | 151 | 818 | 0/0 | 0/0 |
| sort | v1-pash | naive:2026-10-28_140825 | 2345 | 0 | 18 | 1561 | 766 | 0/0 | 0/0 |
| sort | v1-pash | naive:2026-10-28_151151 | 843 | 0 | 18 | 159 | 666 | 0/0 | 0/0 |
| sort | v1-pash | naive:2026-10-28_154444 | 959 | 0 | 18 | 153 | 788 | 0/0 | 0/0 |
| split | v1-pash | naive:2026-10-28_134035 | 162 | 0 | 0 | 0 | 162 | 0/0 | 0/0 |
| wc | v1-pash | naive:2026-10-28_091448 | 16 | 0 | 0 | 0 | 16 | 0/0 | 0/0 |

## Consistency: naive runs of the same command against each other

| Command | Pair | Lines | Same input/output set | Same splitting |
|---|---|---|---|---|
| cp | naive:2026-10-28_114133 / naive:2026-10-28_150709 | 418 | 362/418 (87%) | 418/418 (100%) |
| cp | naive:2026-10-28_114133 / naive:2026-10-28_153913 | 418 | 390/418 (93%) | 418/418 (100%) |
| cp | naive:2026-10-28_150709 / naive:2026-10-28_153913 | 418 | 389/418 (93%) | 418/418 (100%) |
| cut | naive:2026-10-20_135253 / naive:2026-10-27_230555 | 8826 | 8826/8826 (100%) | 8826/8826 (100%) |
| cut | naive:2026-10-20_135253 / naive:2026-10-28_145447 | 8826 | 8826/8826 (100%) | 8826/8826 (100%) |
| cut | naive:2026-10-20_135253 / naive:2026-10-28_152550 | 8826 | 8826/8826 (100%) | 8826/8826 (100%) |
| cut | naive:2026-10-27_230555 / naive:2026-10-28_145447 | 8826 | 8826/8826 (100%) | 8826/8826 (100%) |
| cut | naive:2026-10-27_230555 / naive:2026-10-28_152550 | 8826 | 8826/8826 (100%) | 8826/8826 (100%) |
| cut | naive:2026-10-28_145447 / naive:2026-10-28_152550 | 8826 | 8826/8826 (100%) | 8826/8826 (100%) |
| grep | naive:2026-10-13_193448 / naive:2026-10-20_112956 | 279 | 202/279 (72%) | 193/279 (69%) |
| grep | naive:2026-10-13_193448 / naive:2026-10-28_135447 | 279 | 204/279 (73%) | 193/279 (69%) |
| grep | naive:2026-10-20_112956 / naive:2026-10-28_135447 | 279 | 272/279 (97%) | 279/279 (100%) |
| rm | naive:2026-10-20_121932 / naive:2026-10-28_105951 | 368 | 307/368 (83%) | 368/368 (100%) |
| sort | naive:2026-10-20_160340 / naive:2026-10-28_140825 | 2345 | 2314/2345 (99%) | 926/2345 (39%) |
| sort | naive:2026-10-20_160340 / naive:2026-10-28_151151 | 2345 | 2329/2345 (99%) | 2193/2345 (94%) |
| sort | naive:2026-10-20_160340 / naive:2026-10-28_154444 | 2345 | 2339/2345 (100%) | 1996/2345 (85%) |
| sort | naive:2026-10-28_140825 / naive:2026-10-28_151151 | 2345 | 2310/2345 (99%) | 839/2345 (36%) |
| sort | naive:2026-10-28_140825 / naive:2026-10-28_154444 | 2345 | 2320/2345 (99%) | 659/2345 (28%) |
| sort | naive:2026-10-28_151151 / naive:2026-10-28_154444 | 2345 | 2335/2345 (100%) | 2006/2345 (86%) |

## Exceptions raised by a side's classes

An input/output exception means PaSh gets no answer and treats the command as side-effectful; a parallelizability exception means PaSh does not split it.

| Command | Side | Class | Lines | Exception |
|---|---|---|---|---|
| cp | naive:2026-10-28_114133 | input/output | 1 | `IndexError: list index out of range` |
| cp | naive:2026-10-28_150709 | input/output | 29 | `Exception: cp needs at least a SOURCE and a DEST operand unless -t is given` |
| cp | naive:2026-10-28_153913 | input/output | 1 | `IndexError: list index out of range` |
| grep | naive:2026-10-13_193448 | input/output | 51 | `Exception: grep option not recognised by the parser table` |
| grep | naive:2026-10-20_112956 | input/output | 1 | `IndexError: list assignment index out of range` |
| grep | pash-own | input/output | 1 | `IndexError: list assignment index out of range` |
| sort | naive:2026-10-20_160340 | parallelizability | 1358 | `AssertionError: ` |
| sort | naive:2026-10-28_140825 | input/output | 16 | `Exception: file operands cannot be combined with --files0-from` |
| sort | naive:2026-10-28_151151 | parallelizability | 1502 | `AssertionError: ` |
| sort | naive:2026-10-28_154444 | parallelizability | 1386 | `AssertionError: ` |
| split | naive:2026-10-28_134035 | input/output | 22 | `Exception: extra operand for split, the 3rd one` |
| split | naive:2026-10-28_134035 | input/output | 2 | `Exception: multiple -n options defined for split` |
| wc | naive:2026-10-28_091448 | parallelizability | 24 | `AssertionError: ` |
| wc | pash-own | input/output | 1 | `Exception: wc with --files0-from is considered side-effectful for now` |

