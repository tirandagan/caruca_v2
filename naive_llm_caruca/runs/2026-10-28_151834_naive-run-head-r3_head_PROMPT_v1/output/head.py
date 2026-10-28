from caruca.ir.syntax import *

# NUM accepts an optional leading '-' (meaning "all but the last NUM") and a
# multiplier suffix; GNU head also accepts the obsolete form `head -NUM`, which
# this syntax cannot express.
_NUM_SUFFIXES = (
    "b",
    "kB", "K", "KiB", "k", "KB", "kiB",
    "MB", "M", "MiB",
    "GB", "G", "GiB",
    "TB", "T", "TiB",
    "PB", "P", "PiB",
    "EB", "E", "EiB",
    "ZB", "Z", "ZiB",
    "YB", "Y", "YiB",
    "RB", "R", "RiB",
    "QB", "Q", "QiB",
)

head_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Integer(flag="-c", alias=["--bytes"], flag_followed_by_equals=True, suffixes=_NUM_SUFFIXES),
            Integer(flag="-n", alias=["--lines"], flag_followed_by_equals=True, suffixes=_NUM_SUFFIXES),
            Flag("-q", alias=["--quiet", "--silent"]),
            Flag("-v", alias=["--verbose"]),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],
    ]
]
