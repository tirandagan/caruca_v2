from caruca.ir.syntax import *

# GNU diffutils 3.10.  Verified against /usr/bin/diff.
#
# Notes on the binary's behaviour that shape this description:
#   * -C/-U take a mandatory NUM (`-C 1`, `-C1`), while --context/--unified
#     take an optional NUM only in the `=` form (`--context=1`; `--context 1`
#     makes `1` an operand).  Likewise `--color` / `--color=WHEN`.
#   * -c/-u accept an attached count (`-c1`, `-u3`), and the lone digits
#     -0 .. -9 are themselves accepted as the context count (`-c -1`).
#   * --label/-L, -I, -F, -x and -X may be repeated.
#   * -L, -H, -P, --binary, -h, --inhibit-hunk-merge and --sdiff-merge-assist
#     are accepted but undocumented; -h and --inhibit-hunk-merge are no-ops.
#   * Without --from-file/--to-file exactly two operands are required; with
#     one of them, one or more operands are allowed.  A lone `-` operand (or
#     FILE1/FILE2) is standard input.

_diff_options = [
    # output format
    Flag("--normal"),
    Flag("-q", alias=["--brief"]),
    Flag("-s", alias=["--report-identical-files"]),
    Flag("-c"),
    Integer(flag="-C", min=0),
    Integer(flag="--context", flag_followed_by_equals=True, min=0),
    Flag("-u"),
    Integer(flag="-U", min=0),
    Integer(flag="--unified", flag_followed_by_equals=True, min=0),
    Flag("-0"),
    Flag("-1"),
    Flag("-2"),
    Flag("-3"),
    Flag("-4"),
    Flag("-5"),
    Flag("-6"),
    Flag("-7"),
    Flag("-8"),
    Flag("-9"),
    Flag("-e", alias=["--ed"]),
    Flag("-n", alias=["--rcs"]),
    Flag("-y", alias=["--side-by-side"]),
    Integer(flag="-W", alias=["--width"], min=1),
    Flag("--left-column"),
    Flag("--suppress-common-lines"),
    Flag("--sdiff-merge-assist"),
    Flag("-p", alias=["--show-c-function"]),
    Regex(flag="-F", alias=["--show-function-line"], arity=Arity.ZERO_OR_MORE),
    String(flag="-L", alias=["--label"], arity=Arity.ZERO_OR_MORE),
    Flag("-t", alias=["--expand-tabs"]),
    Flag("-T", alias=["--initial-tab"]),
    Integer(flag="--tabsize", min=1),
    Flag("--suppress-blank-empty"),
    Flag("-l", alias=["--paginate"]),
    # directory comparison
    Flag("-r", alias=["--recursive"]),
    Flag("--no-dereference"),
    Flag("-N", alias=["--new-file"]),
    Flag("-P", alias=["--unidirectional-new-file"]),
    Flag("--ignore-file-name-case"),
    Flag("--no-ignore-file-name-case"),
    Glob(flag="-x", alias=["--exclude"], arity=Arity.ZERO_OR_MORE),
    Path(flag="-X", alias=["--exclude-from"], arity=Arity.ZERO_OR_MORE),
    String(flag="-S", alias=["--starting-file"]),  # a file name within the directories, not a path that is read
    # what to ignore
    Flag("-i", alias=["--ignore-case"]),
    Flag("-E", alias=["--ignore-tab-expansion"]),
    Flag("-Z", alias=["--ignore-trailing-space"]),
    Flag("-b", alias=["--ignore-space-change"]),
    Flag("-w", alias=["--ignore-all-space"]),
    Flag("-B", alias=["--ignore-blank-lines"]),
    Regex(flag="-I", alias=["--ignore-matching-lines"], arity=Arity.ZERO_OR_MORE),
    Flag("-a", alias=["--text"]),
    Flag("--binary"),
    Flag("--strip-trailing-cr"),
    # merged / custom formats
    String(flag="-D", alias=["--ifdef"]),
    Format(flag="--old-group-format"),
    Format(flag="--new-group-format"),
    Format(flag="--changed-group-format"),
    Format(flag="--unchanged-group-format"),
    Format(flag="--line-format"),
    Format(flag="--old-line-format"),
    Format(flag="--new-line-format"),
    Format(flag="--unchanged-line-format"),
    # algorithm
    Flag("-d", alias=["--minimal"]),
    Integer(flag="--horizon-lines", min=0),
    Flag("-H", alias=["--speed-large-files"]),
    Flag("--inhibit-hunk-merge"),
    Flag("-h"),
    Selection(
        flag="--color",
        choices=["never", "always", "auto"],
        flag_followed_by_equals=True,
    ),
    List(flag="--palette", of=String, separator=":"),
    Flag("--help"),
    Flag("-v", alias=["--version"]),
]

diff_syntax_spec: list[SyntaxSpecification] = [
    # diff [OPTION]... FILE1 FILE2   (also DIR1 DIR2, DIR FILE, FILE DIR)
    [
        _diff_options,
        [
            Path(arity=Arity.EXACTLY_ONE, dash_as_stdin=True),
            Path(arity=Arity.EXACTLY_ONE, dash_as_stdin=True),
        ],
    ],
    # diff [OPTION]... --from-file=FILE1 FILE...
    [
        _diff_options
        + [Path(flag="--from-file", dash_as_stdin=True, arity=Arity.EXACTLY_ONE)],
        [Path(arity=Arity.AT_LEAST_ONE, dash_as_stdin=True)],
    ],
    # diff [OPTION]... --to-file=FILE2 FILE...
    [
        _diff_options
        + [Path(flag="--to-file", dash_as_stdin=True, arity=Arity.EXACTLY_ONE)],
        [Path(arity=Arity.AT_LEAST_ONE, dash_as_stdin=True)],
    ],
]
