from caruca.ir.syntax import *

# yes [STRING]...   -- repeatedly prints the STRINGs (joined by spaces) or 'y'
# yes OPTION        -- OPTION is --help or --version; anything else starting
#                      with '-' is rejected ("invalid option"), except '-' and
#                      operands after '--', which are plain strings.
yes_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("--help"),
            Flag("--version"),
        ],
        [String(arity=Arity.ZERO_OR_MORE)],
    ]
]
