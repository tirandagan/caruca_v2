from caruca.ir.syntax import *

# timeout [OPTION] DURATION COMMAND [ARG]...
#
# GNU timeout parses its options with POSIXLY_CORRECT-style ordering ("+" in
# the getopt string): option processing stops at the first non-option word,
# which is DURATION. Every word after DURATION belongs to COMMAND, so e.g.
# `timeout 1 -v true` tries to run a program called `-v`.
#
# DURATION is a non-negative floating point number ("0.5", "1e-1", "inf") with
# an optional suffix: 's' seconds (default), 'm' minutes, 'h' hours, 'd' days.
# A duration of 0 disables the associated timeout.
timeout_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("--preserve-status"),
            Flag("--foreground"),
            Duration(
                flag="-k",
                alias=["--kill-after"],
                flag_followed_by_equals=True,
                min=0,
                suffixes=("s", "m", "h", "d"),
            ),
            Signal(flag="-s", alias=["--signal"], flag_followed_by_equals=True),
            Flag("-v", alias=["--verbose"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Duration(arity=Arity.EXACTLY_ONE, min=0, suffixes=("s", "m", "h", "d")),  # DURATION
            Command(arity=Arity.EXACTLY_ONE),  # COMMAND
            Other(arity=Arity.ZERO_OR_MORE),  # [ARG]...
        ],
    ]
]
