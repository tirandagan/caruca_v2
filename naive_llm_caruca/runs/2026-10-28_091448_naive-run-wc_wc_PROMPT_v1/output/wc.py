from caruca.ir.syntax import *

wc_syntax_spec: list[SyntaxSpecification] = [
    # wc [OPTION]... [FILE]...
    [
        [
            Flag("-c", alias=["--bytes"]),
            Flag("-m", alias=["--chars"]),
            Flag("-l", alias=["--lines"]),
            Flag("-L", alias=["--max-line-length"]),
            Flag("-w", alias=["--words"]),
            Selection(
                flag="--total",
                choices=("auto", "always", "only", "never"),
                flag_followed_by_equals=True,
            ),
            # undocumented in the man page, accepted by coreutils 9.4 wc
            Flag("--debug"),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],
    ],
    # wc [OPTION]... --files0-from=F   (file operands may not be combined with it)
    [
        [
            Flag("-c", alias=["--bytes"]),
            Flag("-m", alias=["--chars"]),
            Flag("-l", alias=["--lines"]),
            Flag("-L", alias=["--max-line-length"]),
            Flag("-w", alias=["--words"]),
            Selection(
                flag="--total",
                choices=("auto", "always", "only", "never"),
                flag_followed_by_equals=True,
            ),
            Flag("--debug"),
            Flag("--help"),
            Flag("--version"),
            Path(
                flag="--files0-from",
                flag_followed_by_equals=True,
                arity=Arity.EXACTLY_ONE,
                dash_as_stdin=True,
            ),
        ],
        [],
    ],
]
