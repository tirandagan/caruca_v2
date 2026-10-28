from caruca.ir.syntax import *

# ln [OPTION]... [-T] TARGET LINK_NAME
# ln [OPTION]... TARGET
# ln [OPTION]... TARGET... DIRECTORY
# ln [OPTION]... -t DIRECTORY TARGET...
#
# All four forms take one or more path operands; which operand is the
# destination depends on -t / -T and on the operand count, so a single
# syntax with Path(AT_LEAST_ONE) covers them.  A lone "-" is an ordinary
# file name for ln, never standard input.
ln_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            # --backup takes its CONTROL value only as --backup=CONTROL;
            # "" stands for the bare --backup form.
            Selection(
                flag="--backup",
                choices=[
                    "",
                    "none",
                    "off",
                    "numbered",
                    "t",
                    "existing",
                    "nil",
                    "simple",
                    "never",
                ],
                flag_followed_by_equals=True,
            ),
            Flag("-b"),
            Flag("-d", alias=["-F", "--directory"]),
            Flag("-f", alias=["--force"]),
            Flag("-i", alias=["--interactive"]),
            Flag("-L", alias=["--logical"]),
            Flag("-n", alias=["--no-dereference"]),
            Flag("-P", alias=["--physical"]),
            Flag("-r", alias=["--relative"]),
            Flag("-s", alias=["--symbolic"]),
            String(flag="-S", alias=["--suffix"]),
            Path(flag="-t", alias=["--target-directory"]),
            Flag("-T", alias=["--no-target-directory"]),
            Flag("-v", alias=["--verbose"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],
    ],
]
