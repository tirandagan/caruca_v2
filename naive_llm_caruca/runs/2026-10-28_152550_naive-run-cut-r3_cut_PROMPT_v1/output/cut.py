from caruca.ir.syntax import *

# cut requires exactly one of -b, -c or -f. The field delimiter (-d) and the
# suppression of non-delimited lines (-s) are only accepted together with -f,
# so each mode is given as its own alternative syntax.

_common_options = [
    Flag("-n"),  # ignored by GNU cut, accepted for POSIX compatibility
    Flag("--complement"),
    Separator(flag="--output-delimiter", flag_followed_by_equals=True),
    Flag("-z", alias=["--zero-terminated"]),
    Flag("--help"),
    Flag("--version"),
]

_operands = [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)]  # [FILE]...

cut_syntax_spec: list[SyntaxSpecification] = [
    # byte mode: cut -b LIST [FILE]...
    [
        [
            Range(flag="-b", alias=["--bytes"], flag_followed_by_equals=True, arity=Arity.EXACTLY_ONE),
        ]
        + _common_options,
        _operands,
    ],
    # character mode: cut -c LIST [FILE]...
    [
        [
            Range(flag="-c", alias=["--characters"], flag_followed_by_equals=True, arity=Arity.EXACTLY_ONE),
        ]
        + _common_options,
        _operands,
    ],
    # field mode: cut -f LIST [-d DELIM] [-s] [FILE]...
    [
        [
            Range(flag="-f", alias=["--fields"], flag_followed_by_equals=True, arity=Arity.EXACTLY_ONE),
            Char(flag="-d", alias=["--delimiter"], flag_followed_by_equals=True),
            Flag("-s", alias=["--only-delimited"]),
        ]
        + _common_options,
        _operands,
    ],
]
