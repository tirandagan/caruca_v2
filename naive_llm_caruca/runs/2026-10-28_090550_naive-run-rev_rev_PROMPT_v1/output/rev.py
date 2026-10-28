from caruca.ir.syntax import *

rev_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-0", alias=["--zero"]),
            Flag("-h", alias=["--help"]),
            Flag("-V", alias=["--version"]),
        ],
        # A lone "-" is not treated as standard input by rev (util-linux 2.39.3):
        # it tries to open a file literally named "-".
        [Path(arity=Arity.ZERO_OR_MORE)],
    ]
]
