from caruca.ir.syntax import *

# NUM for -c/-n may carry a leading '-' (print all but the last NUM) and a
# multiplier suffix (b, kB, K, MB, M, GB, G, T, P, E, Z, Y, R, Q and the
# KiB/MiB/... binary spellings), so it is described as a Size rather than a
# plain Integer.
head_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Size(flag="-c", alias=["--bytes"], flag_followed_by_equals=True),
            Size(flag="-n", alias=["--lines"], flag_followed_by_equals=True),
            Flag("-q", alias=["--quiet", "--silent"]),
            Flag("-v", alias=["--verbose"]),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE]...
    ]
]
