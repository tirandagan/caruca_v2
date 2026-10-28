from caruca.ir.syntax import *

unexpand_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-a", alias=["--all"]),
            Flag("--first-only"),
            # -t accepts either a single tab width (N) or a comma- or blank-separated
            # list of tab stops; the last entry may carry a '/' or '+' prefix.
            # The option may be repeated, and the lists accumulate.
            List(
                flag="-t",
                alias=["--tabs"],
                flag_followed_by_equals=True,
                of=String,
                separator=",",
                arity=Arity.ZERO_OR_MORE,
            ),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE]...
    ]
]
