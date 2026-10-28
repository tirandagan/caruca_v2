from caruca.ir.syntax import *

# GNU bc 1.07.1: `bc [ -hilwsqv ] [long-options] [ file ... ]`
# Every operand is a file of bc source code, executed in order; afterwards bc
# reads further source from standard input.  A lone "-" is NOT standard input
# ("File - is unavailable."), and the long options take no "=value".
bc_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-h", alias=["--help"]),
            Flag("-i", alias=["--interactive"]),
            Flag("-l", alias=["--mathlib"]),
            Flag("-q", alias=["--quiet"]),
            Flag("-s", alias=["--standard"]),
            Flag("-w", alias=["--warn"]),
            Flag("-v", alias=["--version"]),
        ],
        [Path(arity=Arity.ZERO_OR_MORE)],
    ]
]
