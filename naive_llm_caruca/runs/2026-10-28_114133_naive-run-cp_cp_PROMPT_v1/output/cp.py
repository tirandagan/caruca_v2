from caruca.ir.syntax import *

# Options shared by every form of the command line.  The three usage forms
#
#   cp [OPTION]... [-T] SOURCE DEST
#   cp [OPTION]... SOURCE... DIRECTORY
#   cp [OPTION]... -t DIRECTORY SOURCE...
#
# are expressed as two syntaxes below: one where the destination is the last
# operand (-T allowed, -t not), and one where -t names the destination and all
# operands are sources.  cp rejects -t together with -T.
#
# Verified against GNU coreutils 9.4: --backup, --preserve, --reflink, --update
# and --context take their value only when attached with "=" (a separate word is
# an operand); --no-preserve, --sparse, -S/--suffix and -t/--target-directory
# accept either form.  A lone "-" operand is an ordinary file name, not stdin.

_PRESERVE_ATTRS = ["mode", "ownership", "timestamps", "links", "context", "xattr", "all"]

_common_options = [
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
    List(
        flag="--preserve",
        of=Selection(choices=_PRESERVE_ATTRS),
        separator=",",
        flag_followed_by_equals=True,
    ),
    List(
        flag="--no-preserve",
        of=Selection(choices=_PRESERVE_ATTRS),
        separator=",",
    ),
    Flag("--parents"),
    Flag("-R", alias=["-r", "--recursive"]),
    Selection(
        flag="--reflink",
        choices=["", "always", "auto", "never"],
        flag_followed_by_equals=True,
    ),
    Flag("--remove-destination"),
    Selection(flag="--sparse", choices=["always", "auto", "never"]),
    Flag("--strip-trailing-slashes"),
    Flag("-s", alias=["--symbolic-link"]),
    String(flag="-S", alias=["--suffix"]),
    Selection(
        flag="--update",
        choices=["", "all", "none", "older"],
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
    # cp [OPTION]... [-T] SOURCE DEST   /   cp [OPTION]... SOURCE... DIRECTORY
    [
        _common_options + [Flag("-T", alias=["--no-target-directory"])],
        [
            Path(arity=Arity.AT_LEAST_ONE),  # SOURCE...
            Path(arity=Arity.EXACTLY_ONE),  # DEST or DIRECTORY
        ],
    ],
    # cp [OPTION]... -t DIRECTORY SOURCE...
    [
        _common_options
        + [Path(flag="-t", alias=["--target-directory"], arity=Arity.EXACTLY_ONE)],
        [Path(arity=Arity.AT_LEAST_ONE)],  # SOURCE...
    ],
]
