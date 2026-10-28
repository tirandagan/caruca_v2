from caruca.ir.syntax import *

# Options shared by all four forms of the command:
#   install [OPTION]... [-T] SOURCE DEST
#   install [OPTION]... SOURCE... DIRECTORY
#   install [OPTION]... -t DIRECTORY SOURCE...
#   install [OPTION]... -d DIRECTORY...
_install_common_options = [
    Selection(
        flag="--backup",
        choices=["", "none", "off", "numbered", "t", "existing", "nil", "simple", "never"],
        flag_followed_by_equals=True,
    ),
    Flag("-b"),
    Flag("-c"),
    Flag("-C", alias=["--compare"]),
    Flag("-D"),
    Flag("--debug"),
    Group(flag="-g", alias=["--group"], flag_followed_by_equals=True),
    Permission(flag="-m", alias=["--mode"], flag_followed_by_equals=True),
    User(flag="-o", alias=["--owner"], flag_followed_by_equals=True),
    Flag("-p", alias=["--preserve-timestamps"]),
    String(flag="-S", alias=["--suffix"], flag_followed_by_equals=True),
    Flag("-v", alias=["--verbose"]),
    Flag("--preserve-context"),
    Flag("-Z"),
    SecurityContext(flag="--context", flag_followed_by_equals=True),
    Flag("--help"),
    Flag("--version"),
]

# Stripping applies to copied files only; "install -d" rejects -s.
_install_strip_options = [
    Flag("-s", alias=["--strip"]),
    Command(flag="--strip-program", flag_followed_by_equals=True),
]

install_syntax_spec: list[SyntaxSpecification] = [
    # install [OPTION]... [-T] SOURCE DEST
    # install [OPTION]... SOURCE... DIRECTORY
    [
        [
            *_install_common_options,
            *_install_strip_options,
            Flag("-T", alias=["--no-target-directory"]),
        ],
        [
            Path(arity=Arity.AT_LEAST_ONE),  # SOURCE...
            Path(arity=Arity.EXACTLY_ONE),  # DEST or DIRECTORY
        ],
    ],
    # install [OPTION]... -t DIRECTORY SOURCE...
    [
        [
            *_install_common_options,
            *_install_strip_options,
            Path(
                flag="-t",
                alias=["--target-directory"],
                flag_followed_by_equals=True,
                arity=Arity.EXACTLY_ONE,
            ),
        ],
        [
            Path(arity=Arity.AT_LEAST_ONE),  # SOURCE...
        ],
    ],
    # install [OPTION]... -d DIRECTORY...
    [
        [
            *_install_common_options,
            Flag("-d", alias=["--directory"]),
        ],
        [
            Path(arity=Arity.AT_LEAST_ONE),  # DIRECTORY...
        ],
    ],
]
