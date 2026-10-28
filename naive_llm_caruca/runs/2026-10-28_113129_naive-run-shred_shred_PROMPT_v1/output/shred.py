from caruca.ir.syntax import *

# shred [OPTION]... FILE...
#
# Verified against GNU coreutils 9.4:
#   -n/--iterations takes a plain non-negative integer (no size suffixes).
#   -s/--size takes a byte count with optional suffix (K, KiB, kB, M, G, T, P, E, B, b);
#       the file is extended to that size if it is shorter.
#   --remove's HOW argument is optional and must be attached with "=";
#       a detached word is treated as a FILE operand. -u takes no argument.
#   A FILE operand of "-" means standard output (not standard input).

shred_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-f", alias=["--force"]),
            Integer(flag="-n", alias=["--iterations"], flag_followed_by_equals=True, min=0),
            Path(flag="--random-source", flag_followed_by_equals=True),
            Size(flag="-s", alias=["--size"], flag_followed_by_equals=True),
            Flag("-u"),
            Selection(
                flag="--remove",
                choices=["", "unlink", "wipe", "wipesync"],
                flag_followed_by_equals=True,
            ),
            Flag("-v", alias=["--verbose"]),
            Flag("-x", alias=["--exact"]),
            Flag("-z", alias=["--zero"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.AT_LEAST_ONE)],
    ],
]
