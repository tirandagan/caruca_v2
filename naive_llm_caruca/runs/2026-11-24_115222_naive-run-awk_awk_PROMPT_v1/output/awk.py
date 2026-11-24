from caruca.ir.syntax import *

# GNU awk (gawk 5.2).  The AWK program may be supplied either through
# -f / -e / -E (then every operand is an input file) or as the first operand
# (then the remaining operands are input files).  The two layouts are the two
# syntaxes below; they share the option list `_common_options`.
#
# Limitations of this description (not expressible in the format):
#   * In syntax 1 at least one of -f, -e, -E must be present.
#   * -d, -D, -o, -p and -L take an *optional* argument that must be attached
#     to the short option (-dFILE, -Lfatal); a following separate word is never
#     consumed.  The bare short forms are given as Flag nodes and the long forms
#     with a value as `--long=VALUE` nodes.
#   * An operand of the form var=val is a variable assignment, not a file.
#   * -W NAME is equivalent to --NAME (e.g. -W posix == --posix).

_common_options = [
    # POSIX / standard options
    Separator(flag="-F", alias=["--field-separator"]),
    String(flag="-v", alias=["--assign"], arity=Arity.ZERO_OR_MORE),  # var=val
    # gawk extensions
    Flag("-b", alias=["--characters-as-bytes"]),
    Flag("-c", alias=["--traditional"]),
    Flag("-C", alias=["--copyright"]),
    Flag("-d", alias=["--dump-variables"]),
    Path(flag="--dump-variables", flag_followed_by_equals=True),
    Flag("-D", alias=["--debug"]),
    Path(flag="--debug", flag_followed_by_equals=True),
    Flag("-g", alias=["--gen-pot"]),
    Flag("-h", alias=["--help"]),
    Path(flag="-i", alias=["--include"], arity=Arity.ZERO_OR_MORE),
    Flag("-I", alias=["--trace"]),
    Path(flag="-l", alias=["--load"], arity=Arity.ZERO_OR_MORE),
    Flag("-L", alias=["--lint"]),
    Selection(
        flag="--lint",
        choices=["fatal", "invalid", "no-ext"],
        flag_followed_by_equals=True,
    ),
    Flag("-M", alias=["--bignum"]),
    Flag("-N", alias=["--use-lc-numeric"]),
    Flag("-n", alias=["--non-decimal-data"]),
    Flag("-o", alias=["--pretty-print"]),
    Path(flag="--pretty-print", flag_followed_by_equals=True),
    Flag("-O", alias=["--optimize"]),
    Flag("-p", alias=["--profile"]),
    Path(flag="--profile", flag_followed_by_equals=True),
    Flag("-P", alias=["--posix"]),
    Flag("-r", alias=["--re-interval"]),
    Flag("-s", alias=["--no-optimize"]),
    Flag("-S", alias=["--sandbox"]),
    Flag("-t", alias=["--lint-old"]),
    Flag("-V", alias=["--version"]),
    String(flag="-W", arity=Arity.ZERO_OR_MORE),  # -W long-option-name
]

awk_syntax_spec: list[SyntaxSpecification] = [
    # awk [options] -f program-file ... [--] [file ...]
    # (program from -f, -e and/or -E; all operands are input files)
    [
        [
            Path(flag="-f", alias=["--file"], arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),
            String(flag="-e", alias=["--source"], arity=Arity.ZERO_OR_MORE),  # program text
            Path(flag="-E", alias=["--exec"]),
        ]
        + _common_options,
        [
            Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),  # [file ...]
        ],
    ],
    # awk [options] [--] 'program-text' [file ...]
    [
        _common_options,
        [
            String(arity=Arity.EXACTLY_ONE),  # program-text
            Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),  # [file ...]
        ],
    ],
]
