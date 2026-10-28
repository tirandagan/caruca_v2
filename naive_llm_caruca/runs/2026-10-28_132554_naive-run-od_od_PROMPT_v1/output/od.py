from caruca.ir.syntax import *

# Shared option list for all three call forms of GNU od (coreutils 9.4):
#   od [OPTION]... [FILE]...
#   od [-abcdfilosx]... [FILE] [[+]OFFSET[.][b]]
#   od --traditional [OPTION]... [FILE] [[+]OFFSET[.][b] [+][LABEL][.][b]]
#
# -w/--width and --strings take an *optional* argument (attached: -w16, --width=16,
# --strings=3); the bare spelling is therefore listed as a Flag alongside the value node.
# -S always requires its argument (-S 3 / -S3). -t/--format may be repeated and accumulates.
_od_options = [
    Selection(flag="-A", alias=["--address-radix"], choices=("d", "o", "x", "n"), flag_followed_by_equals=True),
    Selection(flag="--endian", choices=("big", "little"), flag_followed_by_equals=True),
    Size(flag="-j", alias=["--skip-bytes"], flag_followed_by_equals=True),
    Size(flag="-N", alias=["--read-bytes"], flag_followed_by_equals=True),
    Flag("--strings"),
    Size(flag="-S", alias=["--strings"], flag_followed_by_equals=True),
    Format(flag="-t", alias=["--format"], flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
    Flag("-v", alias=["--output-duplicates"]),
    Flag("-w", alias=["--width"]),
    Integer(flag="-w", alias=["--width"], flag_followed_by_equals=True, min=1),
    Flag("--traditional"),
    Flag("--help"),
    Flag("--version"),
    # traditional format specifications; they accumulate like repeated -t
    Flag("-a"),
    Flag("-b"),
    Flag("-c"),
    Flag("-d"),
    Flag("-f"),
    Flag("-i"),
    Flag("-l"),
    Flag("-o"),
    Flag("-s"),
    Flag("-x"),
]

od_syntax_spec: list[SyntaxSpecification] = [
    # od [OPTION]... [FILE]...
    [
        _od_options,
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],
    ],
    # od [-abcdfilosx]... [FILE] [+]OFFSET[b]
    # chosen when the last operand begins with '+' or (with two operands) a digit;
    # OFFSET is octal, hex with 0x/0X prefix, and 'b' multiplies by 512
    [
        _od_options,
        [
            Path(dash_as_stdin=True),
            Integer(arity=Arity.EXACTLY_ONE, suffixes=("b",)),
        ],
    ],
    # od --traditional [OPTION]... [FILE] [+]OFFSET[b] [+]LABEL[b]   (--traditional required)
    [
        _od_options,
        [
            Path(dash_as_stdin=True),
            Integer(suffixes=("b",)),
            Integer(suffixes=("b",)),
        ],
    ],
]
