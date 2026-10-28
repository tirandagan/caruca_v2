from caruca.ir.syntax import *

# cut (GNU coreutils 9.4): cut OPTION... [FILE]...
# Exactly one of -b, -c, -f must be given; the binary rejects an invocation
# with none ("you must specify a list of bytes, characters, or fields") or
# with more than one ("only one list may be specified"). That constraint is
# not expressible here, so each is OPTIONAL. Every LIST is a comma-separated
# list of ranges (N, N-, N-M, -M); DELIM must be a single character.
cut_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            List(flag="-b", alias=["--bytes"], of=Range, separator=",", flag_followed_by_equals=True),
            List(flag="-c", alias=["--characters"], of=Range, separator=",", flag_followed_by_equals=True),
            Char(flag="-d", alias=["--delimiter"], flag_followed_by_equals=True),
            List(flag="-f", alias=["--fields"], of=Range, separator=",", flag_followed_by_equals=True),
            Flag("-n"),
            Flag("--complement"),
            Flag("-s", alias=["--only-delimited"]),
            Separator(flag="--output-delimiter", flag_followed_by_equals=True),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE]...
    ]
]
