from caruca.ir.syntax import *

pandoc_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            String(flag="-f", alias=["--from", "--read"]),
            String(flag="-t", alias=["--to", "--write"]),
            Path(flag="-o", alias=["--output"]),
            Path(flag="--data-dir"),
            Path(flag="-d", alias=["--defaults"]),
            Flag("--verbose"),
            Flag("--quiet"),
            Flag("--fail-if-warnings"),
            Path(flag="--log"),
            Flag("--list-input-formats"),
            Flag("--list-output-formats"),
            Flag("--list-extensions"),
            Flag("--list-highlight-languages"),
            Flag("--list-highlight-styles"),
            Flag("-v", alias=["--version"]),
            Flag("-h", alias=["--help"]),
            # Additional flags and options can be added here following the same pattern
        ],
        [Path(arity=Arity.ZERO_OR_MORE)],  # Input files
    ]
]

