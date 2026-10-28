from caruca.ir.syntax import *

# NUM for -n/-c may carry a multiplier suffix (b, kB, K, KiB, MB, M, ... up to Q);
# a leading '-' means "all but the last NUM" rather than "the first NUM".
# The obsolete BSD-style `head -NUM` spelling (e.g. `head -3`, `head -2q`) is also
# accepted by GNU head but has no representation in this vocabulary.
_num_suffixes = (
    "b",
    "kB", "KB", "K", "k", "KiB",
    "MB", "M", "m", "MiB",
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
            Integer(flag="-c", alias=["--bytes"], flag_followed_by_equals=True, suffixes=_num_suffixes),
            Integer(flag="-n", alias=["--lines"], flag_followed_by_equals=True, suffixes=_num_suffixes),
            Flag("-q", alias=["--quiet", "--silent"]),
            Flag("-v", alias=["--verbose"]),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],
    ]
]
