from caruca.ir.syntax import *

# date (GNU coreutils 9.4)
#
# Two synopses from the manual:
#   date [OPTION]... [+FORMAT]
#   date [-u|--utc|--universal] [MMDDhhmm[[CC]YY][.ss]]
#
# -I/--iso-8601 takes an *optional* argument that must be attached to the option
# (`-Ihours`, `--iso-8601=hours`); `-I hours` is rejected by the binary.  As in the
# rm sample (`--preserve-root[=all]`), the empty-string choice stands for the bare
# form with no argument.
date_syntax_spec: list[SyntaxSpecification] = [
    # date [OPTION]... [+FORMAT]
    [
        [
            DateTime(flag="-d", alias=["--date"], flag_followed_by_equals=True),
            Flag("--debug"),
            Path(flag="-f", alias=["--file"], flag_followed_by_equals=True, dash_as_stdin=True),
            Selection(
                flag="-I",
                alias=["--iso-8601"],
                choices=["", "date", "hours", "minutes", "seconds", "ns"],
                flag_followed_by_equals=True,
            ),
            Flag("--resolution"),
            Flag("-R", alias=["--rfc-email"]),
            Selection(
                flag="--rfc-3339",
                choices=["date", "seconds", "ns"],
                flag_followed_by_equals=True,
            ),
            Path(flag="-r", alias=["--reference"], flag_followed_by_equals=True),
            DateTime(flag="-s", alias=["--set"], flag_followed_by_equals=True),
            Flag("-u", alias=["--utc", "--universal"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [DateFormat()],  # [+FORMAT], at most one, must start with '+'
    ],
    # date [-u|--utc|--universal] [MMDDhhmm[[CC]YY][.ss]]  (sets the system clock)
    [
        [
            Flag("-u", alias=["--utc", "--universal"]),
        ],
        [DateTime()],  # MMDDhhmm[[CC]YY][.ss]
    ],
]
