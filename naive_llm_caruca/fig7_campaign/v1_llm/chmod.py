from caruca.ir.syntax import *

chmod_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-c", alias=["--changes"]),
            Flag("-f", alias=["--silent", "--quiet"]),
            Flag("-v", alias=["--verbose"]),
            Flag("--no-preserve-root"),
            Flag("--preserve-root"),
            Path(flag="--reference"),
            Flag("-R", alias=["--recursive"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            String(arity=Arity.EXACTLY_ONE),  # MODE
            Path(arity=Arity.AT_LEAST_ONE),   # FILE
        ],
    ]
]

