from caruca.ir.syntax import *

expand_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-i", alias=["--initial"]),
            Integer(flag="-t", alias=["--tabs"]),
            List(flag="-t", alias=["--tabs"], separator=","),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE)],
    ]
]

