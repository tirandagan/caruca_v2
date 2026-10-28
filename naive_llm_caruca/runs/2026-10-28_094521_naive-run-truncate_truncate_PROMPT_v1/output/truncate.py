from caruca.ir.syntax import *

truncate_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-c", alias=["--no-create"]),
            Flag("-o", alias=["--io-blocks"]),
            Path(flag="-r", alias=["--reference"], flag_followed_by_equals=True),
            # SIZE is an integer with an optional unit (K, M, G, ..., KB, MB, ..., KiB, MiB, ...)
            # and may carry a leading modifier: '+' '-' '<' '>' '/' '%'.
            Size(flag="-s", alias=["--size"], flag_followed_by_equals=True),
            Flag("--help"),
            Flag("--version"),
        ],
        # a lone '-' is an ordinary file name here, not standard input
        [Path(arity=Arity.AT_LEAST_ONE)],
    ]
]
