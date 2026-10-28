from caruca.ir.syntax import *

unzip_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-Z"),
            Flag("-A"),
            Flag("-c"),
            Flag("-f"),
            Flag("-l"),
            Flag("-p"),
            Flag("-t"),
            Flag("-T"),
            Flag("-u"),
            Flag("-v"),
            Flag("-z"),
            Flag("-a"),
            Flag("-b"),
            Flag("-B"),
            Flag("-C"),
            Flag("-D"),
            Flag("-E"),
            Flag("-F"),
            Flag("-i"),
            Flag("-j"),
            Flag("-J"),
            Flag("-K"),
            Flag("-L"),
            Flag("-M"),
            Flag("-n"),
            Flag("-N"),
            Flag("-o"),
            String(flag="-P"),
            Flag("-q"),
            Flag("-s"),
            Flag("-S"),
            Flag("-U"),
            Flag("-V"),
            Flag("-W"),
            Flag("-X"),
            Flag("-Y"),
            Flag("-$"),
            Flag("-/"),
            Flag("-:"),
            Flag("-^"),
            Flag("-2"),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(arity=Arity.EXACTLY_ONE),  # file[.zip]
            Path(arity=Arity.ZERO_OR_MORE),  # [file(s)]
            Path(flag="-x", arity=Arity.ZERO_OR_MORE),  # [-x xfile(s)]
            Path(flag="-d", arity=Arity.EXACTLY_ONE),  # [-d exdir]
        ],
    ]
]

