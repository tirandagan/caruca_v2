from caruca.ir.syntax import *

sort_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            # Ordering options
            Flag("-b", alias=["--ignore-leading-blanks"]),
            Flag("-d", alias=["--dictionary-order"]),
            Flag("-f", alias=["--ignore-case"]),
            Flag("-g", alias=["--general-numeric-sort"]),
            Flag("-i", alias=["--ignore-nonprinting"]),
            Flag("-M", alias=["--month-sort"]),
            Flag("-h", alias=["--human-numeric-sort"]),
            Flag("-n", alias=["--numeric-sort"]),
            Flag("-R", alias=["--random-sort"]),
            Path(flag="--random-source", flag_followed_by_equals=True),
            Flag("-r", alias=["--reverse"]),
            Selection(
                flag="--sort",
                choices=("general-numeric", "human-numeric", "month", "numeric", "random", "version"),
                flag_followed_by_equals=True,
            ),
            Flag("-V", alias=["--version-sort"]),
            # Other options
            Integer(flag="--batch-size", min=2, flag_followed_by_equals=True),  # NMERGE
            Flag("-c"),
            Flag("-C"),
            # bare --check is the same as -c; --check=quiet / --check=silent are the same as -C
            Selection(
                flag="--check",
                choices=("", "diagnose-first", "quiet", "silent"),
                flag_followed_by_equals=True,
            ),
            Command(flag="--compress-program", flag_followed_by_equals=True),
            Flag("--debug"),
            Path(flag="--files0-from", flag_followed_by_equals=True, dash_as_stdin=True),
            String(flag="-k", alias=["--key"], flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),  # KEYDEF
            Flag("-m", alias=["--merge"]),
            Path(flag="-o", alias=["--output"], flag_followed_by_equals=True),
            Flag("-s", alias=["--stable"]),
            Size(flag="-S", alias=["--buffer-size"], flag_followed_by_equals=True),
            Char(flag="-t", alias=["--field-separator"], flag_followed_by_equals=True),
            Path(flag="-T", alias=["--temporary-directory"], flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE),
            Integer(flag="--parallel", min=1, flag_followed_by_equals=True),
            Flag("-u", alias=["--unique"]),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
            # undocumented, accepted and ignored for compatibility with old System V sort
            Flag("-y"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE]...
    ]
]
