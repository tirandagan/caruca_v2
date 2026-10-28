from caruca.ir.syntax import *

col_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-b", alias=["--no-backspaces"]),
            Flag("-f", alias=["--fine"]),
            Flag("-h", alias=["--tabs"]),
            # -l accepts 0 .. UINT32_MAX (util-linux strtou32_or_err); -h and -x are mutually exclusive
            Integer(flag="-l", alias=["--lines"], flag_followed_by_equals=True, min=0, max=4294967295),
            Flag("-p", alias=["--pass"]),
            Flag("-x", alias=["--spaces"]),
            Flag("-H", alias=["--help"]),
            Flag("-V", alias=["--version"]),
        ],
        # col takes no operands: any operand is rejected with "bad usage"
        [],
    ]
]
