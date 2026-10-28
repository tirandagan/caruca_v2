from caruca.ir.syntax import *

# seq [OPTION]... LAST
# seq [OPTION]... FIRST LAST
# seq [OPTION]... FIRST INCREMENT LAST
#
# FIRST, INCREMENT and LAST are floating-point values (0.5, 1e2, 0x10 and
# negative numbers such as -3 are all accepted). -w and -f are mutually
# exclusive: seq rejects an invocation that gives both.
seq_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            PrintfFormat(flag="-f", alias=["--format"], flag_followed_by_equals=True),
            Separator(flag="-s", alias=["--separator"], flag_followed_by_equals=True),
            Flag("-w", alias=["--equal-width"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Number(arity=Arity.EXACTLY_ONE),  # LAST
        ],
    ],
    [
        [
            PrintfFormat(flag="-f", alias=["--format"], flag_followed_by_equals=True),
            Separator(flag="-s", alias=["--separator"], flag_followed_by_equals=True),
            Flag("-w", alias=["--equal-width"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Number(arity=Arity.EXACTLY_ONE),  # FIRST
            Number(arity=Arity.EXACTLY_ONE),  # LAST
        ],
    ],
    [
        [
            PrintfFormat(flag="-f", alias=["--format"], flag_followed_by_equals=True),
            Separator(flag="-s", alias=["--separator"], flag_followed_by_equals=True),
            Flag("-w", alias=["--equal-width"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Number(arity=Arity.EXACTLY_ONE),  # FIRST
            Number(arity=Arity.EXACTLY_ONE),  # INCREMENT
            Number(arity=Arity.EXACTLY_ONE),  # LAST
        ],
    ],
]
