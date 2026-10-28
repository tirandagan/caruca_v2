from caruca.ir.syntax import (
    Flag,
    Selection,
    String,
    Path,
    Arity,
    SyntaxSpecification,
)

# Options shared by every form of the command line.  --backup and --update take
# an *optional* value which must be attached with "=", so a bare "--backup" is
# represented by the empty choice "" (as in rm's --preserve-root).
_mv_options = [
    Selection(
        flag="--backup",
        choices=["", "none", "off", "numbered", "t", "existing", "nil", "simple", "never"],
        flag_followed_by_equals=True,
    ),
    Flag("-b"),
    Flag("--debug"),
    Flag("-f", alias=["--force"]),
    Flag("-i", alias=["--interactive"]),
    Flag("-n", alias=["--no-clobber"]),
    Flag("--no-copy"),
    Flag("--strip-trailing-slashes"),
    String(flag="-S", alias=["--suffix"]),
    Flag("-T", alias=["--no-target-directory"]),
    Selection(
        flag="--update",
        choices=["", "all", "none", "older"],
        flag_followed_by_equals=True,
    ),
    Flag("-u"),
    Flag("-v", alias=["--verbose"]),
    Flag("-Z", alias=["--context"]),
    Flag("--help"),
    Flag("--version"),
]

mv_syntax_spec: list[SyntaxSpecification] = [
    # mv [OPTION]... -t DIRECTORY SOURCE...
    [
        _mv_options
        + [
            Path(
                flag="-t",
                alias=["--target-directory"],
                arity=Arity.EXACTLY_ONE,
            ),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],  # SOURCE...
    ],
    # mv [OPTION]... [-T] SOURCE DEST
    # mv [OPTION]... SOURCE... DIRECTORY
    # (at least two operands; the last one is the destination)
    [
        _mv_options,
        [Path(arity=Arity.AT_LEAST_ONE)],  # SOURCE... DEST
    ],
]
