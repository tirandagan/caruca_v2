from caruca.ir.syntax import *

mkdir_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Permission(flag="-m", alias=["--mode"]),
            Flag("-p", alias=["--parents"]),
            Flag("-v", alias=["--verbose"]),
            Flag("-Z"),
            # `--context` alone behaves like -Z; a context may only be attached
            # with `=` (`--context CTX` treats CTX as a DIRECTORY operand).
            Flag("--context"),
            SecurityContext(flag="--context", flag_followed_by_equals=True),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],
    ],
]
