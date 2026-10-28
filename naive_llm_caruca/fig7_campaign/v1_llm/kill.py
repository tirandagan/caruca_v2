from caruca.ir.syntax import *

kill_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Signal(flag="-", flag_followed_by_equals=False),
            Signal(flag="-s", alias=["--signal"]),
            Integer(flag="-q", alias=["--queue"]),
            Signal(flag="-l", alias=["--list"], arity=Arity.ZERO_OR_ONE),
            Flag("-L", alias=["--table"]),
        ],
        [Pid(arity=Arity.ONE_OR_MORE)],
    ]
]

