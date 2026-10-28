from caruca.ir.syntax import *

stat_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-L", alias=["--dereference"]),
            Flag("-f", alias=["--file-system"]),
            Selection(
                flag="--cached",
                choices=["default", "never", "always"],
                flag_followed_by_equals=True,
            ),
            PrintfFormat(flag="-c", alias=["--format"], flag_followed_by_equals=True),
            PrintfFormat(flag="--printf", flag_followed_by_equals=True),
            Flag("-t", alias=["--terse"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.AT_LEAST_ONE, dash_as_stdin=True)],  # FILE...
    ]
]
