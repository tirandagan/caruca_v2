from caruca.ir.syntax import *

seq_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            PrintfFormat(flag="-f", alias=["--format"]),
            Separator(flag="-s", alias=["--separator"]),
            Flag("-w", alias=["--equal-width"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            [String(arity=Arity.EXACTLY_ONE)],  # LAST
            [String(arity=Arity.EXACTLY_TWO)],  # FIRST LAST
            [String(arity=Arity.EXACTLY_THREE)],  # FIRST INCREMENT LAST
        ],
    ]
]

