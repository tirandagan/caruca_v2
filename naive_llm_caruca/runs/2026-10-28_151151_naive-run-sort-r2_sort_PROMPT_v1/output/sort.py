from caruca.ir.syntax import *

# GNU coreutils 9.4 sort.
#
# Two syntaxes, mirroring the SYNOPSIS:
#   sort [OPTION]... [FILE]...
#   sort [OPTION]... --files0-from=F        (no FILE operands allowed)
#
# Constraints the binary enforces that this format cannot express:
#   * -c / -C / --check accept at most one FILE operand and are incompatible with -o.
#   * -o may be given at most once ("multiple output files specified").
#   * only one of -g -h -M -n -R -V (or --sort) may be in effect globally.
#   * -t accepts a single character, or the two-character string '\0' meaning NUL.
#   * the obsolete, undocumented -y[N] and +POS[-POS] key syntax are accepted but omitted here.

_sort_options = [
    # ordering options
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
        choices=("general-numeric", "human-numeric", "month", "numeric", "random", "version"),
        flag_followed_by_equals=True,
    ),
    Flag("-V", alias=["--version-sort"]),
    # other options
    Integer(flag="--batch-size", flag_followed_by_equals=True, min=2),
    Flag("-c"),
    Flag("-C"),
    # bare --check is -c; --check=diagnose-first is -c; --check=quiet / --check=silent is -C
    Selection(
        flag="--check",
        choices=("", "diagnose-first", "quiet", "silent"),
        flag_followed_by_equals=True,
    ),
    Command(flag="--compress-program", flag_followed_by_equals=True),
    Flag("--debug"),
    String(flag="-k", alias=["--key"], flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),  # KEYDEF
    Flag("-m", alias=["--merge"]),
    Path(flag="-o", alias=["--output"], flag_followed_by_equals=True),
    Flag("-s", alias=["--stable"]),
    Size(flag="-S", alias=["--buffer-size"], flag_followed_by_equals=True),
    Char(flag="-t", alias=["--field-separator"], flag_followed_by_equals=True),
    Path(flag="-T", alias=["--temporary-directory"], flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
    Integer(flag="--parallel", flag_followed_by_equals=True, min=1),
    Flag("-u", alias=["--unique"]),
    Flag("-z", alias=["--zero-terminated"]),
    Flag("--help"),
    Flag("--version"),
]

sort_syntax_spec: list[SyntaxSpecification] = [
    # sort [OPTION]... [FILE]...
    [
        _sort_options,
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE]...
    ],
    # sort [OPTION]... --files0-from=F
    [
        _sort_options
        + [Path(flag="--files0-from", flag_followed_by_equals=True, dash_as_stdin=True, arity=Arity.EXACTLY_ONE)],
        [],
    ],
]
