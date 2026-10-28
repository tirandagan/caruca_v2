from caruca.ir.syntax import *

# fold [OPTION]... [FILE]...
# Note: GNU fold also accepts the obsolete form `-NUM` (e.g. `fold -20`) as a
# synonym for `-w NUM`; that spelling has no representation here.
fold_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-b", alias=["--bytes"]),
            Flag("-s", alias=["--spaces"]),
            Integer(flag="-w", alias=["--width"], flag_followed_by_equals=True, min=1),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],
    ]
]
