from caruca.ir.syntax import *

# Options shared by every form of the command line.
# `--backup`, `--preserve`, `--reflink`, `--update` and `--context` take an
# optional value, which must be attached with `=`; the others that carry a
# value require it.
_cp_options = [
    Flag("-a", alias=["--archive"]),
    Flag("--attributes-only"),
    Selection(
        flag="--backup",
        choices=["none", "off", "numbered", "t", "existing", "nil", "simple", "never"],
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
    List(
        flag="--preserve",
        of=Selection(
            choices=["mode", "ownership", "timestamps", "links", "context", "xattr", "all"]
        ),
        separator=",",
        flag_followed_by_equals=True,
    ),
    List(
        flag="--no-preserve",
        of=Selection(
            choices=["mode", "ownership", "timestamps", "links", "context", "xattr", "all"]
        ),
        separator=",",
        flag_followed_by_equals=True,
    ),
    Flag("--parents"),
    Flag("-R", alias=["-r", "--recursive"]),
    Selection(
        flag="--reflink",
        choices=["always", "auto", "never"],
        flag_followed_by_equals=True,
    ),
    Flag("--remove-destination"),
    Selection(
        flag="--sparse",
        choices=["auto", "always", "never"],
        flag_followed_by_equals=True,
    ),
    Flag("--strip-trailing-slashes"),
    Flag("-s", alias=["--symbolic-link"]),
    String(flag="-S", alias=["--suffix"]),
    Selection(
        flag="--update",
        choices=["all", "none", "older"],
        flag_followed_by_equals=True,
    ),
    Flag("-u"),
    Flag("-v", alias=["--verbose"]),
    Flag("-x", alias=["--one-file-system"]),
    Flag("-Z"),
    SecurityContext(flag="--context", flag_followed_by_equals=True),
    Flag("--help"),
    Flag("--version"),
]

cp_syntax_spec: list[SyntaxSpecification] = [
    # cp [OPTION]... [-T] SOURCE DEST
    # cp [OPTION]... SOURCE... DIRECTORY
    [
        _cp_options + [Flag("-T", alias=["--no-target-directory"])],
        [
            Path(arity=Arity.AT_LEAST_ONE),  # SOURCE...
            Path(arity=Arity.EXACTLY_ONE),  # DEST / DIRECTORY
        ],
    ],
    # cp [OPTION]... -t DIRECTORY SOURCE...
    [
        _cp_options
        + [Path(flag="-t", alias=["--target-directory"], arity=Arity.EXACTLY_ONE)],
        [Path(arity=Arity.AT_LEAST_ONE)],  # SOURCE...
    ],
]
