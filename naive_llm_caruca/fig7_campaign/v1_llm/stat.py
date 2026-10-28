from caruca.ir.syntax import *

stat_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-L", alias=["--dereference"]),
            Flag("-f", alias=["--file-system"]),
            Selection(flag="--cached", choices=("always", "never", "default"), flag_followed_by_equals=True),
            String(flag="-c", alias=["--format"]),
            String(flag="--printf"),
            Flag("-t", alias=["--terse"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE)],
    ]
]

