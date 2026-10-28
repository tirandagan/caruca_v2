from caruca.ir.syntax import *

# dd takes no positional operands: every argument is a KEY=VALUE word (modelled
# here as an option whose value is attached with "="), or one of the two GNU
# long options --help / --version.  A key may be repeated; the last occurrence
# wins, except that conv=, iflag= and oflag= lists accumulate.

# multiplicative suffixes accepted after N (the same ones apply to BYTES);
# "B" makes count=, skip= and seek= count bytes rather than blocks
_DD_NUMBER_SUFFIXES = (
    "c", "w", "b", "B", "kB", "K", "KiB", "MB", "M", "MiB", "xM",
    "GB", "G", "GiB", "TB", "T", "TiB", "PB", "P", "PiB", "EB", "E", "EiB",
    "ZB", "Z", "ZiB", "YB", "Y", "YiB", "RB", "R", "RiB", "QB", "Q", "QiB",
)

_DD_CONV_SYMBOLS = (
    "ascii", "ebcdic", "ibm", "block", "unblock", "lcase", "ucase", "sparse",
    "swab", "sync", "excl", "nocreat", "notrunc", "noerror", "fdatasync", "fsync",
)
# count_bytes, skip_bytes and seek_bytes are undocumented but accepted (GNU
# compatibility spellings); fullblock is accepted for iflag only
_DD_OFLAG_SYMBOLS = (
    "append", "direct", "directory", "dsync", "sync", "nonblock",
    "noatime", "nocache", "noctty", "nofollow",
    "count_bytes", "skip_bytes", "seek_bytes",
)
_DD_IFLAG_SYMBOLS = _DD_OFLAG_SYMBOLS + ("fullblock",)

dd_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Size(flag="bs", flag_followed_by_equals=True),
            Size(flag="cbs", flag_followed_by_equals=True),
            List(
                flag="conv",
                flag_followed_by_equals=True,
                of=Selection(choices=_DD_CONV_SYMBOLS),
                separator=",",
            ),
            Integer(flag="count", flag_followed_by_equals=True, min=0, suffixes=_DD_NUMBER_SUFFIXES),
            Size(flag="ibs", flag_followed_by_equals=True),
            Path(flag="if", flag_followed_by_equals=True),
            List(
                flag="iflag",
                flag_followed_by_equals=True,
                of=Selection(choices=_DD_IFLAG_SYMBOLS),
                separator=",",
            ),
            Size(flag="obs", flag_followed_by_equals=True),
            Path(flag="of", flag_followed_by_equals=True),
            List(
                flag="oflag",
                flag_followed_by_equals=True,
                of=Selection(choices=_DD_OFLAG_SYMBOLS),
                separator=",",
            ),
            Integer(flag="seek", alias=["oseek"], flag_followed_by_equals=True, min=0, suffixes=_DD_NUMBER_SUFFIXES),
            Integer(flag="skip", alias=["iseek"], flag_followed_by_equals=True, min=0, suffixes=_DD_NUMBER_SUFFIXES),
            Selection(
                flag="status",
                flag_followed_by_equals=True,
                choices=("none", "noxfer", "progress"),
            ),
            Flag("--help"),
            Flag("--version"),
        ],
        [],
    ]
]
