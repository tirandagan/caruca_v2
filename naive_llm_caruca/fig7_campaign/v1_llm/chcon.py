from caruca.ir.syntax import *

chcon_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("--dereference"),
            Flag("-h", alias=["--no-dereference"]),
            SecurityContext(flag="-u", alias=["--user"]),
            SecurityContext(flag="-r", alias=["--role"]),
            SecurityContext(flag="-t", alias=["--type"]),
            SecurityContext(flag="-l", alias=["--range"]),
            Flag("--no-preserve-root"),
            Flag("--preserve-root"),
            Path(flag="--reference"),
            Flag("-R", alias=["--recursive"]),
            Flag("-v", alias=["--verbose"]),
            Flag("-H"),
            Flag("-L"),
            Flag("-P"),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],
    ]
]

