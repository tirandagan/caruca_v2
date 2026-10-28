from caruca.ir.syntax import *

# GNU coreutils tee 9.4:  tee [OPTION]... [FILE]...
#
# Verified against /usr/bin/tee:
#   * FILE operands are optional; with none, tee just copies stdin to stdout.
#   * A lone "-" operand is an ordinary file named "-" (no dash_as_stdin).
#   * --output-error's MODE is only taken when attached with "=";
#     "tee --output-error exit f" treats "exit" as a FILE operand.
#   * -p takes no argument (it implies --output-error=warn-nopipe).
#   * Short flags bundle (-aip) and options may follow operands.
tee_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-a", alias=["--append"]),
            Flag("-i", alias=["--ignore-interrupts"]),
            Flag("-p"),
            Selection(
                flag="--output-error",
                flag_followed_by_equals=True,
                choices=("warn", "warn-nopipe", "exit", "exit-nopipe"),
            ),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE)],
    ]
]
