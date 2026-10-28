from caruca.ir.syntax import *

nl_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            # STYLE is one of a, t, n, or pBRE (a basic regex prefixed by "p"),
            # so it is not a closed set of choices.
            String(flag="-b", alias=["--body-numbering"], flag_followed_by_equals=True),
            # CC: two delimiter characters; a single character implies ':' as the
            # second one, more than two characters is a GNU extension, and the empty
            # string disables section matching.
            Delimiter(flag="-d", alias=["--section-delimiter"], flag_followed_by_equals=True),
            String(flag="-f", alias=["--footer-numbering"], flag_followed_by_equals=True),
            String(flag="-h", alias=["--header-numbering"], flag_followed_by_equals=True),
            # zero and negative increments are accepted
            Integer(flag="-i", alias=["--line-increment"], flag_followed_by_equals=True),
            Integer(flag="-l", alias=["--join-blank-lines"], flag_followed_by_equals=True, min=1),
            Selection(
                flag="-n",
                alias=["--number-format"],
                choices=("ln", "rn", "rz"),
                flag_followed_by_equals=True,
            ),
            Flag("-p", alias=["--no-renumber"]),
            Separator(flag="-s", alias=["--number-separator"], flag_followed_by_equals=True),
            # zero and negative starting numbers are accepted
            Integer(flag="-v", alias=["--starting-line-number"], flag_followed_by_equals=True),
            Integer(flag="-w", alias=["--number-width"], flag_followed_by_equals=True, min=1),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE]...
    ]
]
