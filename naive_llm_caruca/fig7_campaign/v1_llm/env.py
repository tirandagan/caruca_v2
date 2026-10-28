from caruca.ir.syntax import *

env_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-i", alias=["--ignore-environment"]),
            Flag("-0", alias=["--null"]),
            Variable(flag="-u", alias=["--unset"]),
            Path(flag="-C", alias=["--chdir"]),
            String(flag="-S", alias=["--split-string"]),
            Signal(flag="--block-signal", flag_followed_by_equals=True, arity=Arity.ZERO_OR_ONE),
            Signal(flag="--default-signal", flag_followed_by_equals=True, arity=Arity.ZERO_OR_ONE),
            Signal(flag="--ignore-signal", flag_followed_by_equals=True, arity=Arity.ZERO_OR_ONE),
            Flag("--list-signal-handling"),
            Flag("-v", alias=["--debug"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Variable(arity=Arity.ZERO_OR_MORE),
            Command(arity=Arity.ZERO_OR_MORE),
        ],
    ]
]

