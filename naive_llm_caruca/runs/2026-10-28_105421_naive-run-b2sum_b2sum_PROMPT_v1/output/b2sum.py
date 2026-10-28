from caruca.ir.syntax import *

b2sum_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-b", alias=["--binary"]),
            Flag("-c", alias=["--check"]),
            # digest length in bits: 0 means the default (512), otherwise 8..512 and a multiple of 8
            Integer(flag="-l", alias=["--length"], flag_followed_by_equals=True, min=0, max=512),
            Flag("--tag"),
            Flag("-t", alias=["--text"]),
            Flag("-z", alias=["--zero"]),
            # the following five are accepted only together with -c/--check
            Flag("--ignore-missing"),
            Flag("--quiet"),
            Flag("--status"),
            Flag("--strict"),
            Flag("-w", alias=["--warn"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE]...
    ]
]
