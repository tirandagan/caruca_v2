from caruca.ir.syntax import (
    Flag,
    Path,
    OwnerGroup,
    Arity,
    SyntaxSpecification,
)

# Options shared by both synopsis forms:
#   chown [OPTION]... [OWNER][:[GROUP]] FILE...
#   chown [OPTION]... --reference=RFILE FILE...
_common_options = [
    Flag("-c", alias=["--changes"]),
    Flag("-f", alias=["--silent", "--quiet"]),
    Flag("-v", alias=["--verbose"]),
    Flag("--dereference"),
    Flag("-h", alias=["--no-dereference"]),
    OwnerGroup(flag="--from", flag_followed_by_equals=True),  # CURRENT_OWNER:CURRENT_GROUP
    Flag("--no-preserve-root"),
    Flag("--preserve-root"),
    Flag("-R", alias=["--recursive"]),
    Flag("-H"),
    Flag("-L"),
    Flag("-P"),
    Flag("--help"),
    Flag("--version"),
]

chown_syntax_spec: list[SyntaxSpecification] = [
    # chown [OPTION]... [OWNER][:[GROUP]] FILE...
    [
        list(_common_options),
        [
            OwnerGroup(arity=Arity.EXACTLY_ONE),  # [OWNER][:[GROUP]], may be empty or a lone ':'
            Path(arity=Arity.AT_LEAST_ONE),  # FILE...
        ],
    ],
    # chown [OPTION]... --reference=RFILE FILE...
    [
        list(_common_options)
        + [
            Path(
                flag="--reference",
                flag_followed_by_equals=True,
                arity=Arity.EXACTLY_ONE,
            ),  # RFILE
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],  # FILE...
    ],
]
