from caruca.ir.syntax import *

# dd takes no dash-style options apart from --help and --version. Everything
# else is a KEY=VALUE operand, modelled here as an option whose value is
# attached with "=". Any operand may be repeated; the last occurrence wins.
# A value of "-" for if= or of= names a file literally called "-", not stdin
# or stdout (verified against coreutils 9.4).

_DD_SIZE_SUFFIXES = (
    "c", "w", "b",
    "kB", "K", "KiB", "MB", "M", "MiB", "xM", "GB", "G", "GiB",
    "TB", "T", "TiB", "PB", "P", "PiB", "EB", "E", "EiB",
    "ZB", "Z", "ZiB", "YB", "Y", "YiB", "RB", "R", "RiB", "QB", "Q", "QiB",
)

# N for count=, skip= and seek= accepts the same multipliers; a trailing "B"
# makes it a byte count rather than a block count.
_DD_COUNT_SUFFIXES = _DD_SIZE_SUFFIXES + ("B",)

_DD_CONV_SYMBOLS = (
    "ascii", "ebcdic", "ibm", "block", "unblock", "lcase", "ucase", "sparse",
    "swab", "sync", "excl", "nocreat", "notrunc", "noerror", "fdatasync", "fsync",
)

# count_bytes, skip_bytes and seek_bytes are accepted but absent from --help.
_DD_IFLAG_SYMBOLS = (
    "append", "direct", "directory", "dsync", "sync", "fullblock", "nonblock",
    "noatime", "nocache", "noctty", "nofollow",
    "count_bytes", "skip_bytes", "seek_bytes",
)

# oflag= rejects fullblock, otherwise the same set as iflag=.
_DD_OFLAG_SYMBOLS = tuple(s for s in _DD_IFLAG_SYMBOLS if s != "fullblock")

dd_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Size(flag="bs", flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
            Size(flag="cbs", flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
            List(
                flag="conv",
                flag_followed_by_equals=True,
                of=Selection(choices=_DD_CONV_SYMBOLS),
                separator=",",
                arity=Arity.ZERO_OR_MORE,
            ),
            Integer(flag="count", flag_followed_by_equals=True, min=0, suffixes=_DD_COUNT_SUFFIXES, arity=Arity.ZERO_OR_MORE),
            Size(flag="ibs", flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
            Path(flag="if", flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
            List(
                flag="iflag",
                flag_followed_by_equals=True,
                of=Selection(choices=_DD_IFLAG_SYMBOLS),
                separator=",",
                arity=Arity.ZERO_OR_MORE,
            ),
            Size(flag="obs", flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
            Path(flag="of", flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
            List(
                flag="oflag",
                flag_followed_by_equals=True,
                of=Selection(choices=_DD_OFLAG_SYMBOLS),
                separator=",",
                arity=Arity.ZERO_OR_MORE,
            ),
            Integer(flag="seek", alias=["oseek"], flag_followed_by_equals=True, min=0, suffixes=_DD_COUNT_SUFFIXES, arity=Arity.ZERO_OR_MORE),
            Integer(flag="skip", alias=["iseek"], flag_followed_by_equals=True, min=0, suffixes=_DD_COUNT_SUFFIXES, arity=Arity.ZERO_OR_MORE),
            Selection(
                flag="status",
                flag_followed_by_equals=True,
                choices=("none", "noxfer", "progress"),
                arity=Arity.ZERO_OR_MORE,
            ),
            Flag("--help"),
            Flag("--version"),
        ],
        [],
    ]
]
