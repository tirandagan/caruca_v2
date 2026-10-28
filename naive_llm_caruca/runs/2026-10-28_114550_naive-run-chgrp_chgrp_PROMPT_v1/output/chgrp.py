from caruca.ir.syntax import (
    Flag,
    Group,
    Path,
    Arity,
    SyntaxSpecification,
)

# chgrp has two synopses:
#   chgrp [OPTION]... GROUP FILE...
#   chgrp [OPTION]... --reference=RFILE FILE...
# In the second, --reference is mandatory and no GROUP operand is given.
_chgrp_options = [
    Flag("-c", alias=["--changes"]),
    Flag("-f", alias=["--silent", "--quiet"]),
    Flag("-v", alias=["--verbose"]),
    Flag("--dereference"),
    Flag("-h", alias=["--no-dereference"]),
    Flag("--no-preserve-root"),
    Flag("--preserve-root"),
    Flag("-R", alias=["--recursive"]),
    Flag("-H"),
    Flag("-L"),
    Flag("-P"),
    Flag("--help"),
    Flag("--version"),
]

chgrp_syntax_spec: list[SyntaxSpecification] = [
    [
        _chgrp_options,
        [
            Group(arity=Arity.EXACTLY_ONE),  # GROUP (name or numeric gid)
            Path(arity=Arity.AT_LEAST_ONE),  # FILE...
        ],
    ],
    [
        _chgrp_options
        + [
            Path(
                flag="--reference",
                flag_followed_by_equals=True,
                arity=Arity.EXACTLY_ONE,
            ),  # RFILE
        ],
        [
            Path(arity=Arity.AT_LEAST_ONE),  # FILE...
        ],
    ],
]
