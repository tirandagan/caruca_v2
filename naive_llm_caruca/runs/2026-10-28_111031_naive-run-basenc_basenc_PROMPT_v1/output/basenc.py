from caruca.ir.syntax import *

basenc_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            # encoding selectors: at least one is required by the binary
            # ("missing encoding type" otherwise); when several are given the
            # last one wins
            Flag("--base64"),
            Flag("--base64url"),
            Flag("--base32"),
            Flag("--base32hex"),
            Flag("--base16"),
            Flag("--base2msbf"),
            Flag("--base2lsbf"),
            Flag("--z85"),
            Flag("-d", alias=["--decode"]),
            Flag("-i", alias=["--ignore-garbage"]),
            # wrap width; 0 disables wrapping; ignored when decoding
            Integer(flag="-w", alias=["--wrap"], flag_followed_by_equals=True, min=0),
            Flag("--help"),
            Flag("--version"),
        ],
        # [FILE]: at most one operand; a second one is rejected as "extra operand"
        [Path(arity=Arity.ZERO_OR_ONE, dash_as_stdin=True)],
    ]
]
