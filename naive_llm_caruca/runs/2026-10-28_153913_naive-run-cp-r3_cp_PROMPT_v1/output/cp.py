from caruca.ir.syntax import *

# cp (GNU coreutils 9.4)
#
#   cp [OPTION]... [-T] SOURCE DEST
#   cp [OPTION]... SOURCE... DIRECTORY
#   cp [OPTION]... -t DIRECTORY SOURCE...
#
# The first two forms share one syntax (SOURCE... followed by a final DEST/DIRECTORY
# operand); the third is listed as a separate syntax because -t removes the trailing
# destination operand.  A lone "-" operand is an ordinary file name for cp, not stdin.
#
# --backup, --preserve, --reflink, --update and --context take an *optional* value, which
# must be attached with "=" (a following word is taken as an operand).  As in the rm
# sample, an empty string in `choices` stands for the bare, value-less spelling.
# --no-preserve, --sparse, -S/--suffix and -t/--target-directory require their value.

_ATTRS = ["mode", "ownership", "timestamps", "links", "context", "xattr", "all"]


def _options(with_target_directory: bool) -> list:
    opts = [
        Flag("-a", alias=["--archive"]),
        Flag("--attributes-only"),
        Selection(
            flag="--backup",
            choices=["", "none", "off", "numbered", "t", "existing", "nil", "simple", "never"],
            flag_followed_by_equals=True,
        ),
        Flag("-b"),
        Flag("--copy-contents"),
        Flag("-d"),
        Flag("--debug"),
        Flag("-f", alias=["--force"]),
        Flag("-i", alias=["--interactive"]),
        Flag("-H"),
        Flag("-l", alias=["--link"]),
        Flag("-L", alias=["--dereference"]),
        Flag("-n", alias=["--no-clobber"]),
        Flag("-P", alias=["--no-dereference"]),
        Flag("-p"),
        # --preserve may be given bare (same as --preserve=mode,ownership,timestamps)
        List(
            flag="--preserve",
            of=Selection(choices=_ATTRS),
            separator=",",
            flag_followed_by_equals=True,
        ),
        List(
            flag="--no-preserve",
            of=Selection(choices=_ATTRS),
            separator=",",
            flag_followed_by_equals=True,
        ),
        Flag("--parents"),
        Flag("-R", alias=["-r", "--recursive"]),
        Selection(
            flag="--reflink",
            choices=["", "auto", "always", "never"],
            flag_followed_by_equals=True,
        ),
        Flag("--remove-destination"),
        Selection(
            flag="--sparse",
            choices=["never", "auto", "always"],
            flag_followed_by_equals=True,
        ),
        Flag("--strip-trailing-slashes"),
        Flag("-s", alias=["--symbolic-link"]),
        String(flag="-S", alias=["--suffix"]),
        Flag("-T", alias=["--no-target-directory"]),
        Selection(
            flag="--update",
            choices=["", "all", "none", "older"],
            flag_followed_by_equals=True,
        ),
        Flag("-u"),
        Flag("-v", alias=["--verbose"]),
        Flag("-x", alias=["--one-file-system"]),
        Flag("-Z"),
        # --context may be given bare (same as -Z)
        SecurityContext(flag="--context", flag_followed_by_equals=True),
        Flag("--help"),
        Flag("--version"),
    ]
    if with_target_directory:
        opts.append(
            Path(flag="-t", alias=["--target-directory"], arity=Arity.EXACTLY_ONE)
        )
    return opts


cp_syntax_spec: list[SyntaxSpecification] = [
    # cp [OPTION]... [-T] SOURCE DEST
    # cp [OPTION]... SOURCE... DIRECTORY
    [
        _options(with_target_directory=False),
        [
            Path(arity=Arity.AT_LEAST_ONE),  # SOURCE...
            Path(arity=Arity.EXACTLY_ONE),  # DEST / DIRECTORY
        ],
    ],
    # cp [OPTION]... -t DIRECTORY SOURCE...
    [
        _options(with_target_directory=True),
        [
            Path(arity=Arity.AT_LEAST_ONE),  # SOURCE...
        ],
    ],
]
