from caruca.ir.syntax import *

# Options shared by both synopsis forms of du:
#   du [OPTION]... [FILE]...
#   du [OPTION]... --files0-from=F
_du_options = [
    Flag("-0", alias=["--null"]),
    Flag("-a", alias=["--all"]),
    Flag("--apparent-size"),
    Size(flag="-B", alias=["--block-size"]),
    Flag("-b", alias=["--bytes"]),
    Flag("-c", alias=["--total"]),
    Flag("-D", alias=["--dereference-args", "-H"]),
    Integer(flag="-d", alias=["--max-depth"], min=0),
    Flag("-h", alias=["--human-readable"]),
    Flag("--inodes"),
    Flag("-k"),
    Flag("-L", alias=["--dereference"]),
    Flag("-l", alias=["--count-links"]),
    Flag("-m"),
    Flag("-P", alias=["--no-dereference"]),
    Flag("-S", alias=["--separate-dirs"]),
    Flag("--si"),
    Flag("-s", alias=["--summarize"]),
    # SIZE may be negative ("-t -1k" excludes entries larger than 1k)
    Size(flag="-t", alias=["--threshold"]),
    # "--time" alone shows mtime; the WORD is only accepted attached with "="
    Flag("--time"),
    Selection(
        flag="--time",
        choices=["atime", "access", "use", "ctime", "status"],
        flag_followed_by_equals=True,
    ),
    TimeStyle(flag="--time-style"),  # full-iso, long-iso, iso, or +FORMAT
    Path(flag="-X", alias=["--exclude-from"], dash_as_stdin=True),
    Glob(flag="--exclude"),
    Flag("-x", alias=["--one-file-system"]),
    Flag("--help"),
    Flag("--version"),
]

du_syntax_spec: list[SyntaxSpecification] = [
    # du [OPTION]... [FILE]...   (no FILE means ".")
    [
        _du_options,
        # a lone "-" is an ordinary file name here, not standard input
        [Path(arity=Arity.ZERO_OR_MORE)],
    ],
    # du [OPTION]... --files0-from=F   (file operands are rejected)
    [
        _du_options
        + [Path(flag="--files0-from", arity=Arity.EXACTLY_ONE, dash_as_stdin=True)],
        [],
    ],
]
