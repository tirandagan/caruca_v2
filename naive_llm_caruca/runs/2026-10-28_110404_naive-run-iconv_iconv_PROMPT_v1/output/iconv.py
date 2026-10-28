from caruca.ir.syntax import *

# iconv (GNU libc 2.39): iconv [OPTION...] [FILE...]
# Encoding names are free text (see `iconv -l`); the target may carry the
# suffixes //TRANSLIT and //IGNORE, so they are modelled as String.
iconv_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            String(flag="-f", alias=["--from-code"], flag_followed_by_equals=True),
            String(flag="-t", alias=["--to-code"], flag_followed_by_equals=True),
            Flag("-l", alias=["--list"]),
            Flag("-c"),
            # a lone `-` given to -o means standard output
            Path(flag="-o", alias=["--output"], flag_followed_by_equals=True),
            Flag("-s", alias=["--silent"]),
            Flag("--verbose"),
            Flag("-?", alias=["--help"]),
            Flag("--usage"),
            Flag("-V", alias=["--version"]),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE...]
    ]
]
