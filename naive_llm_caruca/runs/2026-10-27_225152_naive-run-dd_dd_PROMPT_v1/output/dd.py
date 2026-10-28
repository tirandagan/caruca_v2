from caruca.ir.syntax import *

# dd takes no dash-prefixed options apart from --help and --version. Every
# other argument is a KEY=VALUE operand, so each one is modelled as an option
# whose "flag" is the bare key and whose value is attached with "=".
#
# Observed on GNU coreutils 9.4 (/usr/bin/dd):
#   * `if=-` opens a file literally named "-"; it does not mean stdin, hence no
#     dash_as_stdin on the Path nodes.
#   * `seek`/`oseek` and `skip`/`iseek` are spellings of the same operand.
#   * bs/ibs/obs/cbs reject 0; count/skip/seek accept 0.
#   * N and BYTES accept the multiplicative suffixes below, may be chained with
#     `x` (e.g. `bs=2x3`), and N may end in `B` to count bytes instead of blocks.
#   * conv/iflag/oflag are comma-separated symbol lists; the empty symbol is
#     rejected. `count_bytes`, `skip_bytes` and `seek_bytes` are accepted by both
#     iflag and oflag even though the manual page does not list them; `fullblock`
#     is iflag-only.

_DD_NUMBER_SUFFIXES = (
    "c", "w", "b", "B",
    "kB", "K", "KB", "KiB", "k",
    "MB", "M", "MiB", "xM",
    "GB", "G", "GiB",
    "TB", "T", "TiB",
    "PB", "P", "PiB",
    "EB", "E", "EiB",
    "ZB", "Z", "ZiB",
    "YB", "Y", "YiB",
    "RB", "R", "RiB",
    "QB", "Q", "QiB",
)

_DD_CONV_SYMBOLS = (
    "ascii", "ebcdic", "ibm",
    "block", "unblock",
    "lcase", "ucase",
    "sparse", "swab", "sync",
    "excl", "nocreat", "notrunc", "noerror",
    "fdatasync", "fsync",
)

_DD_IFLAG_SYMBOLS = (
    "append", "direct", "directory", "dsync", "sync", "fullblock", "nonblock",
    "noatime", "nocache", "noctty", "nofollow",
    "count_bytes", "skip_bytes", "seek_bytes",
)

_DD_OFLAG_SYMBOLS = (
    "append", "direct", "directory", "dsync", "sync", "nonblock",
    "noatime", "nocache", "noctty", "nofollow",
    "count_bytes", "skip_bytes", "seek_bytes",
)

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
            Integer(
                flag="count",
                flag_followed_by_equals=True,
                min=0,
                suffixes=_DD_NUMBER_SUFFIXES,
            ),
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
            Integer(
                flag="seek",
                alias=["oseek"],
                flag_followed_by_equals=True,
                min=0,
                suffixes=_DD_NUMBER_SUFFIXES,
            ),
            Integer(
                flag="skip",
                alias=["iseek"],
                flag_followed_by_equals=True,
                min=0,
                suffixes=_DD_NUMBER_SUFFIXES,
            ),
            Selection(
                flag="status",
                flag_followed_by_equals=True,
                choices=("none", "noxfer", "progress"),
            ),
            Flag("--help"),
            Flag("--version"),
        ],
        [],  # dd has no positional operands; input and output come from if=/of=
    ]
]
