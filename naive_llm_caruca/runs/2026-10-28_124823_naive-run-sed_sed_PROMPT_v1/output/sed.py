from caruca.ir.syntax import *

# sed [OPTION]... {script-only-if-no-other-script} [input-file]...
#
# The script comes either from the first operand (when no -e/-f is given) or
# from any number of -e/-f options (then every operand is an input file).
# These are three alternative syntaxes below so that a parser does not take
# an input file for a script when -e or -f is present.

_common_options = [
    Flag("-n", alias=["--quiet", "--silent"]),
    Flag("--debug"),
    Flag("--follow-symlinks"),
    # -i takes an optional backup suffix only when attached (-i.bak); a
    # separate word is never consumed. --in-place optionally takes =SUFFIX.
    Flag("-i", alias=["--in-place"]),
    String(flag="--in-place", flag_followed_by_equals=True),  # [=SUFFIX]
    Integer(flag="-l", alias=["--line-length"]),
    Flag("--posix"),
    Flag("-E", alias=["-r", "--regexp-extended"]),
    Flag("-s", alias=["--separate"]),
    Flag("--sandbox"),
    Flag("-u", alias=["--unbuffered"]),
    Flag("-z", alias=["--null-data"]),
    # accepted by GNU sed 4.9 on Linux (a no-op there), but not documented
    Flag("-b", alias=["--binary"]),
    Flag("--help"),
    Flag("--version"),
]

_input_files = Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)  # [input-file]...

sed_syntax_spec: list[SyntaxSpecification] = [
    # 1. script given as the first operand
    [
        _common_options,
        [
            String(arity=Arity.EXACTLY_ONE),  # script
            _input_files,
        ],
    ],
    # 2. script given with at least one -e (and possibly -f)
    [
        _common_options
        + [
            String(flag="-e", alias=["--expression"], arity=Arity.AT_LEAST_ONE),
            Path(flag="-f", alias=["--file"], arity=Arity.ZERO_OR_MORE),
        ],
        [_input_files],
    ],
    # 3. script given with at least one -f (and possibly -e)
    [
        _common_options
        + [
            String(flag="-e", alias=["--expression"], arity=Arity.ZERO_OR_MORE),
            Path(flag="-f", alias=["--file"], arity=Arity.AT_LEAST_ONE),
        ],
        [_input_files],
    ],
]
