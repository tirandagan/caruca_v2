from caruca.ir.syntax import *

# cut OPTION... [FILE]...
# Exactly one of -b, -c or -f must be given (GNU cut rejects repeats and
# mixtures with "only one list may be specified"); -d and -s are only
# accepted together with -f.  Each LIST is a comma-separated list of ranges
# of the form N, N-, N-M or -M.
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
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],
    ]
]
