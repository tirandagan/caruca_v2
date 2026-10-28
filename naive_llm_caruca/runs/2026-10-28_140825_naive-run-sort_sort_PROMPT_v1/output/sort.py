from caruca.ir.syntax import *

# GNU coreutils 9.4 sort(1).
#
# Notes on the encoding:
# - `-c`/`--check` and `-C` take no value; the only way to give --check a value is
#   `--check=WORD`, which is encoded as a Selection whose empty choice stands for the
#   bare `--check` (same convention as rm's `--preserve-root` in the samples).
# - `-k`/`--key` and `-T`/`--temporary-directory` may be repeated; `-o` may not
#   (sort rejects "multiple output files specified").
# - `-t` accepts exactly one character, or the two-character spelling `\0` for NUL.
# - `-y` is an undocumented, ignored compatibility option (accepted, takes no separate
#   word; `-y0` is also accepted).  Included so invocations carrying it still parse.
# - Operands are input files; `-` means standard input and may be repeated.
# - The second syntax is the man page's second synopsis line: with --files0-from no
#   file operands are allowed.

_sort_ordering_options = [
    Flag("-b", alias=["--ignore-leading-blanks"]),
    Flag("-d", alias=["--dictionary-order"]),
    Flag("-f", alias=["--ignore-case"]),
    Flag("-g", alias=["--general-numeric-sort"]),
    Flag("-i", alias=["--ignore-nonprinting"]),
    Flag("-M", alias=["--month-sort"]),
    Flag("-h", alias=["--human-numeric-sort"]),
    Flag("-n", alias=["--numeric-sort"]),
    Flag("-R", alias=["--random-sort"]),
    Path(flag="--random-source", flag_followed_by_equals=True),
    Flag("-r", alias=["--reverse"]),
    Selection(
        flag="--sort",
        choices=["general-numeric", "human-numeric", "month", "numeric", "random", "version"],
        flag_followed_by_equals=True,
    ),
    Flag("-V", alias=["--version-sort"]),
]

_sort_other_options = [
    Integer(flag="--batch-size", min=2, flag_followed_by_equals=True),  # NMERGE
    Flag("-c", alias=["--check"]),
    Selection(
        flag="--check",
        choices=["", "diagnose-first", "silent", "quiet"],
        flag_followed_by_equals=True,
    ),
    Flag("-C"),
    Command(flag="--compress-program", flag_followed_by_equals=True),  # PROG
    Flag("--debug"),
    String(flag="-k", alias=["--key"], flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),  # KEYDEF
    Flag("-m", alias=["--merge"]),
    Path(flag="-o", alias=["--output"], flag_followed_by_equals=True),
    Flag("-s", alias=["--stable"]),
    Size(flag="-S", alias=["--buffer-size"], flag_followed_by_equals=True),
    Char(flag="-t", alias=["--field-separator"], flag_followed_by_equals=True),  # SEP
    Path(flag="-T", alias=["--temporary-directory"], flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),  # DIR
    Integer(flag="--parallel", min=1, flag_followed_by_equals=True),  # N
    Flag("-u", alias=["--unique"]),
    Flag("-y"),
    Flag("-z", alias=["--zero-terminated"]),
    Flag("--help"),
    Flag("--version"),
]

sort_syntax_spec: list[SyntaxSpecification] = [
    # sort [OPTION]... [FILE]...
    [
        _sort_ordering_options + _sort_other_options,
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],
    ],
    # sort [OPTION]... --files0-from=F
    [
        _sort_ordering_options
        + _sort_other_options
        + [
            Path(
                flag="--files0-from",
                flag_followed_by_equals=True,
                dash_as_stdin=True,
                arity=Arity.EXACTLY_ONE,
            ),
        ],
        [],
    ],
]
