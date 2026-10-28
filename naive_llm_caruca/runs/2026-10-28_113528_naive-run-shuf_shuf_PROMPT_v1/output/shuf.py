from caruca.ir.syntax import *

# shuf has three mutually exclusive input modes (see SYNOPSIS in shuf(1)):
#   shuf [OPTION]... [FILE]        -- permute the lines of FILE (or stdin)
#   shuf -e [OPTION]... [ARG]...   -- permute the ARGs themselves
#   shuf -i LO-HI [OPTION]...      -- permute the integers LO..HI
# -e and -i cannot be combined ("cannot combine -e and -i options"), and
# neither accepts a FILE operand ("extra operand"), so each mode is its own
# syntax below. The remaining options are common to all three.

_shuf_common_options = [
    Integer(flag="-n", alias=["--head-count"], flag_followed_by_equals=True, min=0),
    Path(flag="-o", alias=["--output"], flag_followed_by_equals=True, dash_as_stdin=True),
    Path(flag="--random-source", flag_followed_by_equals=True),
    Flag("-r", alias=["--repeat"]),
    Flag("-z", alias=["--zero-terminated"]),
    Flag("--help"),
    Flag("--version"),
]

shuf_syntax_spec: list[SyntaxSpecification] = [
    # shuf [OPTION]... [FILE]
    [
        [
            *_shuf_common_options,
        ],
        [Path(arity=Arity.ZERO_OR_ONE, dash_as_stdin=True)],
    ],
    # shuf -e [OPTION]... [ARG]...
    [
        [
            Flag("-e", alias=["--echo"], arity=Arity.EXACTLY_ONE),
            *_shuf_common_options,
        ],
        [String(arity=Arity.ZERO_OR_MORE)],
    ],
    # shuf -i LO-HI [OPTION]...
    [
        [
            Range(
                flag="-i",
                alias=["--input-range"],
                flag_followed_by_equals=True,
                arity=Arity.EXACTLY_ONE,
            ),
            *_shuf_common_options,
        ],
        [],
    ],
]
