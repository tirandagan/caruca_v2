from caruca.ir.syntax import *

numfmt_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("--debug"),
            Char(flag="-d", alias=["--delimiter"], flag_followed_by_equals=True),
            # cut(1)-style field list: N, N-, N-M, -M, -, joined by commas
            List(flag="--field", of=Range, separator=",", flag_followed_by_equals=True),
            PrintfFormat(flag="--format", flag_followed_by_equals=True),
            Selection(
                flag="--from",
                choices=("none", "auto", "si", "iec", "iec-i"),
                flag_followed_by_equals=True,
            ),
            # unit sizes accept a suffix, e.g. --from-unit=1K
            Size(flag="--from-unit", flag_followed_by_equals=True),
            Flag("--grouping"),
            # --header alone means 1; a count can only be given as --header=N
            # (a separate word after --header is taken as an operand)
            Flag("--header"),
            Integer(flag="--header", flag_followed_by_equals=True, min=1),
            Selection(
                flag="--invalid",
                choices=("abort", "fail", "warn", "ignore"),
                flag_followed_by_equals=True,
            ),
            # negative N left-aligns
            Integer(flag="--padding", flag_followed_by_equals=True),
            Selection(
                flag="--round",
                choices=("up", "down", "from-zero", "towards-zero", "nearest"),
                flag_followed_by_equals=True,
            ),
            String(flag="--suffix", flag_followed_by_equals=True),
            Selection(
                flag="--to",
                choices=("none", "auto", "si", "iec", "iec-i"),
                flag_followed_by_equals=True,
            ),
            Size(flag="--to-unit", flag_followed_by_equals=True),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            # NUMBER...: numbers with optional unit suffix ("1.5K"); with -d/--field
            # an operand is a whole delimited record, so it is free text, not a path.
            # A lone "-" is not stdin (it is rejected as an invalid number).
            String(arity=Arity.ZERO_OR_MORE),
        ],
    ]
]
