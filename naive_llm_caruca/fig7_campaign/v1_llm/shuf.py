from caruca.ir.syntax import *

shuf_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-e", alias=["--echo"]),
            Range(flag="-i", alias=["--input-range"]),
            Integer(flag="-n", alias=["--head-count"]),
            Path(flag="-o", alias=["--output"]),
            Path(flag="--random-source"),
            Flag("-r", alias=["--repeat"]),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(arity=Arity.ZERO_OR_ONE),  # For the FILE argument
            Other(arity=Arity.ZERO_OR_MORE),  # For the ARG arguments when using -e
        ],
    ]
]

