from caruca.ir.syntax import *

numfmt_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("--debug"),
            Delimiter(flag="-d", alias=["--delimiter"]),
            Range(flag="--field"),
            PrintfFormat(flag="--format"),
            String(flag="--from"),
            Integer(flag="--from-unit"),
            Flag("--grouping"),
            Integer(flag="--header", arity=Arity.OPTIONAL),
            Selection(flag="--invalid", choices=("abort", "fail", "warn", "ignore"), flag_followed_by_equals=True),
            Integer(flag="--padding"),
            Selection(flag="--round", choices=("up", "down", "from-zero", "towards-zero", "nearest"), flag_followed_by_equals=True),
            String(flag="--suffix"),
            String(flag="--to"),
            Integer(flag="--to-unit"),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [String(arity=Arity.ZERO_OR_MORE)],
    ]
]

