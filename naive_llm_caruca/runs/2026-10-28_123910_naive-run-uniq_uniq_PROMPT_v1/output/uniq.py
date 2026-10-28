from caruca.ir.syntax import *

# uniq (GNU coreutils 9.4): uniq [OPTION]... [INPUT [OUTPUT]]
uniq_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-c", alias=["--count"]),
            Flag("-d", alias=["--repeated"]),
            Flag("-D"),
            # the METHOD of --all-repeated and --group is optional and, when given,
            # must be attached with "=" (a following separate word is an operand)
            Selection(
                flag="--all-repeated",
                choices=("none", "prepend", "separate"),
                flag_followed_by_equals=True,
            ),
            Integer(flag="-f", alias=["--skip-fields"], min=0, flag_followed_by_equals=True),
            Selection(
                flag="--group",
                choices=("separate", "prepend", "append", "both"),
                flag_followed_by_equals=True,
            ),
            Flag("-i", alias=["--ignore-case"]),
            Integer(flag="-s", alias=["--skip-chars"], min=0, flag_followed_by_equals=True),
            Flag("-u", alias=["--unique"]),
            Flag("-z", alias=["--zero-terminated"]),
            Integer(flag="-w", alias=["--check-chars"], min=0, flag_followed_by_equals=True),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(dash_as_stdin=True),  # [INPUT]  ("-" or absent: standard input)
            Path(),                    # [OUTPUT] ("-" or absent: standard output)
        ],
    ]
]
