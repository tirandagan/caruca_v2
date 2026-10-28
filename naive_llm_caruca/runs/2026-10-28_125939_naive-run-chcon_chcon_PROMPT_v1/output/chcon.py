from caruca.ir.syntax import *

# Options shared by all three synopsis forms of chcon.
_chcon_common_options = [
    Flag("--dereference"),
    Flag("-h", alias=["--no-dereference"]),
    Flag("--no-preserve-root"),
    Flag("--preserve-root"),
    Flag("-R", alias=["--recursive"]),
    Flag("-v", alias=["--verbose"]),
    Flag("-H"),
    Flag("-L"),
    Flag("-P"),
    Flag("--help"),
    Flag("--version"),
]

chcon_syntax_spec: list[SyntaxSpecification] = [
    # chcon [OPTION]... CONTEXT FILE...
    [
        list(_chcon_common_options),
        [
            SecurityContext(arity=Arity.EXACTLY_ONE),  # CONTEXT
            Path(arity=Arity.AT_LEAST_ONE),  # FILE...
        ],
    ],
    # chcon [OPTION]... [-u USER] [-r ROLE] [-l RANGE] [-t TYPE] FILE...
    # (at least one of -u/-r/-l/-t must be given, otherwise the first
    # operand is taken as CONTEXT as in the first form)
    [
        list(_chcon_common_options)
        + [
            User(flag="-u", alias=["--user"]),
            SecurityRole(flag="-r", alias=["--role"]),
            SecurityType(flag="-t", alias=["--type"]),
            SecurityRange(flag="-l", alias=["--range"]),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],  # FILE...
    ],
    # chcon [OPTION]... --reference=RFILE FILE...
    [
        list(_chcon_common_options)
        + [
            Path(flag="--reference", arity=Arity.EXACTLY_ONE),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],  # FILE...
    ],
]
