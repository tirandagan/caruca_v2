from caruca.ir.syntax import *

# Multiplier suffixes accepted by NUM arguments of -c/--bytes and -n/--lines
# (b 512, kB 1000, K 1024, MB 1000*1000, M 1024*1024, ... and the KiB/MiB/... spellings).
# GNU tail also accepts the lowercase "k" and "m". NUM may be prefixed with "+"
# (output starting *from* byte/line NUM instead of the last NUM); the prefix is
# not representable in the type vocabulary and is handled in the annotation.
_NUM_SUFFIXES = (
    "b",
    "kB", "K", "k", "KB", "KiB",
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

tail_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Integer(flag="-c", alias=["--bytes"], flag_followed_by_equals=True, suffixes=_NUM_SUFFIXES),
            # -f never takes an argument; --follow takes an *optional* one, attached with "=" only
            # (an absent argument means "descriptor"), so the two are modelled separately as in rm's
            # --preserve-root sample where "" stands for the bare option.
            Flag("-f"),
            Selection(
                flag="--follow",
                choices=["", "descriptor", "name"],
                flag_followed_by_equals=True,
            ),
            Flag("-F"),  # same as --follow=name --retry
            Integer(flag="-n", alias=["--lines"], flag_followed_by_equals=True, suffixes=_NUM_SUFFIXES),
            Integer(flag="--max-unchanged-stats", flag_followed_by_equals=True),
            Pid(flag="--pid", flag_followed_by_equals=True),
            Flag("-q", alias=["--quiet", "--silent"]),
            Flag("--retry"),
            # seconds; GNU tail accepts fractional values such as 0.5
            Duration(flag="-s", alias=["--sleep-interval"], flag_followed_by_equals=True),
            Flag("-v", alias=["--verbose"]),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE]...
    ]
]
