from caruca.ir.syntax import *

comm_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-1"),
            Flag("-2"),
            Flag("-3"),
            Flag("--check-order"),
            Flag("--nocheck-order"),
            Separator(flag="--output-delimiter", flag_followed_by_equals=True),
            Flag("--total"),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        # FILE1 FILE2: both required; either one (but not both) may be "-" for stdin
        [
            Path(arity=Arity.EXACTLY_ONE, dash_as_stdin=True),
            Path(arity=Arity.EXACTLY_ONE, dash_as_stdin=True),
        ],
    ]
]
