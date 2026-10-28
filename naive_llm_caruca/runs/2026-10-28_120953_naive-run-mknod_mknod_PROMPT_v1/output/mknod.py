from caruca.ir.syntax import (
    Flag,
    Permission,
    SecurityContext,
    Selection,
    Path,
    Integer,
    Arity,
    SyntaxSpecification,
)

# mknod [OPTION]... NAME TYPE [MAJOR MINOR]
#
# Two alternative syntaxes: a FIFO (TYPE p) takes no device numbers, while a
# block or character special file (TYPE b, c or u) requires both MAJOR and
# MINOR. MAJOR and MINOR may be written in decimal, octal (leading 0) or
# hexadecimal (leading 0x).
_mknod_options = [
    Permission(flag="-m", alias=["--mode"]),
    Flag("-Z"),
    # the value is optional: a bare --context behaves like -Z
    SecurityContext(flag="--context", flag_followed_by_equals=True),
    Flag("--help"),
    Flag("--version"),
]

mknod_syntax_spec: list[SyntaxSpecification] = [
    [
        _mknod_options,
        [
            Path(arity=Arity.EXACTLY_ONE),  # NAME
            Selection(choices=["p"], arity=Arity.EXACTLY_ONE),  # TYPE
        ],
    ],
    [
        _mknod_options,
        [
            Path(arity=Arity.EXACTLY_ONE),  # NAME
            Selection(choices=["b", "c", "u"], arity=Arity.EXACTLY_ONE),  # TYPE
            Integer(min=0, arity=Arity.EXACTLY_ONE),  # MAJOR
            Integer(min=0, arity=Arity.EXACTLY_ONE),  # MINOR
        ],
    ],
]
