from caruca.ir.syntax import *

runcon_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            SecurityContext(arity=Arity.ZERO_OR_ONE),
            Flag("-c", alias=["--compute"]),
            SecurityContext(flag="-t", alias=["--type"]),
            User(flag="-u", alias=["--user"]),
            SecurityContext(flag="-r", alias=["--role"]),
            Range(flag="-l", alias=["--range"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Command(), String(arity=Arity.ZERO_OR_MORE)],
    ]
]

