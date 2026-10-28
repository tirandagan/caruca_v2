from caruca.ir.syntax import (
    Flag,
    Path,
    Permission,
    Arity,
    SyntaxSpecification,
)

# chmod [OPTION]... MODE[,MODE]... FILE...
# chmod [OPTION]... OCTAL-MODE FILE...
# chmod [OPTION]... --reference=RFILE FILE...
#
# The first two synopsis lines are one syntax: a single MODE operand, which may
# be symbolic (possibly comma-separated, e.g. "u+x,g-w"), octal ("0755") or an
# octal change ("=755", "-6000"), followed by at least one file. The third form
# replaces the MODE operand with the --reference option. A MODE operand may
# itself begin with '-' (e.g. "chmod -w FILE"); no mode letter collides with a
# chmod short option, so such a word is an operand, not an option.
_common_options = [
    Flag("-c", alias=["--changes"]),
    Flag("-f", alias=["--silent", "--quiet"]),
    Flag("-v", alias=["--verbose"]),
    Flag("--no-preserve-root"),
    Flag("--preserve-root"),
    Flag("-R", alias=["--recursive"]),
    Flag("--help"),
    Flag("--version"),
]

chmod_syntax_spec: list[SyntaxSpecification] = [
    [
        _common_options,
        [
            Permission(arity=Arity.EXACTLY_ONE),  # MODE[,MODE]... | OCTAL-MODE
            Path(arity=Arity.AT_LEAST_ONE),  # FILE...
        ],
    ],
    [
        _common_options
        + [
            Path(
                flag="--reference",
                flag_followed_by_equals=True,
                arity=Arity.EXACTLY_ONE,
            ),  # RFILE, whose mode is copied
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],  # FILE...
    ],
]
