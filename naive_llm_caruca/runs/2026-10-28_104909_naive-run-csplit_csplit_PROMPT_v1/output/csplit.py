from caruca.ir.syntax import *

csplit_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            SprintfFormat(flag="-b", alias=["--suffix-format"], flag_followed_by_equals=True),
            # PREFIX is a filename prefix (may contain directory components); the
            # output files are PREFIX followed by the formatted piece number
            String(flag="-f", alias=["--prefix"], flag_followed_by_equals=True),
            Flag("-k", alias=["--keep-files"]),
            Flag("--suppress-matched"),
            Integer(flag="-n", alias=["--digits"], flag_followed_by_equals=True, min=0),
            # -q is accepted by the binary as a synonym of -s although undocumented
            Flag("-s", alias=["-q", "--quiet", "--silent"]),
            Flag("-z", alias=["--elide-empty-files"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(arity=Arity.EXACTLY_ONE, dash_as_stdin=True),  # FILE
            # PATTERN...: INTEGER | /REGEXP/[OFFSET] | %REGEXP%[OFFSET] | {INTEGER} | {*}
            String(arity=Arity.AT_LEAST_ONE),
        ],
    ]
]
