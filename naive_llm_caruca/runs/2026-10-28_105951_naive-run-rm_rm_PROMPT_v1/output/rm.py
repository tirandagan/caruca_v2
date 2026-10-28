from caruca.ir.syntax import (
    Flag,
    Selection,
    Path,
    Arity,
    SyntaxSpecification,
)

# rm (GNU coreutils 9.4): rm [OPTION]... [FILE]...
# Operands are plain paths; a lone "-" is an ordinary file name, not stdin.
# Without -f at least one operand is required ("missing operand"); with -f,
# `rm -f` alone exits 0.
rm_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-f", alias=["--force"]),
            Flag("-i"),
            Flag("-I"),
            # --interactive[=WHEN]: the value must be attached with "=";
            # a bare --interactive (empty choice) means "always".
            Selection(
                flag="--interactive",
                choices=["", "never", "no", "none", "once", "always", "yes"],
                flag_followed_by_equals=True,
            ),
            Flag("--one-file-system"),
            Flag("--no-preserve-root"),
            # --preserve-root[=all]: bare form (empty choice) or "=all".
            Selection(
                flag="--preserve-root",
                choices=["", "all"],
                flag_followed_by_equals=True,
            ),
            Flag("-r", alias=["-R", "--recursive"]),
            Flag("-d", alias=["--dir"]),
            Flag("-v", alias=["--verbose"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],
    ],
]
