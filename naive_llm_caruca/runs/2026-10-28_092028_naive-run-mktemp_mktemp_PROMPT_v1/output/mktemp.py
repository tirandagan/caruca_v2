from caruca.ir.syntax import *

# mktemp [OPTION]... [TEMPLATE]   (GNU coreutils 9.4)
mktemp_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-d", alias=["--directory"]),
            Flag("-u", alias=["--dry-run"]),
            Flag("-q", alias=["--quiet"]),
            # SUFF must not contain a slash; accepted as --suffix=SUFF and --suffix SUFF
            String(flag="--suffix"),
            # -p DIR takes its argument as the next word; --tmpdir only takes one
            # attached with '=' (a following word is treated as the TEMPLATE)
            Path(flag="-p"),
            Path(flag="--tmpdir", flag_followed_by_equals=True),
            # bare --tmpdir: use $TMPDIR if set, else /tmp
            Flag("--tmpdir"),
            Flag("-t"),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            # TEMPLATE: at most one; defaults to tmp.XXXXXXXXXX under --tmpdir
            Path(arity=Arity.OPTIONAL),
        ],
    ]
]
