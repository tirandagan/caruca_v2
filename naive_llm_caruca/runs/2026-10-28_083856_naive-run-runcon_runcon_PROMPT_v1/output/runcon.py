from caruca.ir.syntax import *

# runcon parses its own options with getopt string "+r:t:u:l:c": option
# scanning stops at the first operand (COMMAND), and every word after it,
# option-looking or not, is passed to COMMAND unchanged.
#
# Two alternative layouts:
#   runcon CONTEXT COMMAND [args]
#       (used when none of -c/-t/-u/-r/-l is given; CONTEXT is then mandatory
#        and so is COMMAND)
#   runcon [-c] [-u USER] [-r ROLE] [-t TYPE] [-l RANGE] [COMMAND [args]]
#       (with no COMMAND, the current security context is printed to stdout)
runcon_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("--help"),
            Flag("--version"),
        ],
        [
            SecurityContext(arity=Arity.EXACTLY_ONE),  # CONTEXT
            Command(arity=Arity.EXACTLY_ONE),  # COMMAND
            Other(arity=Arity.ZERO_OR_MORE),  # [args]
        ],
    ],
    [
        [
            Flag("-c", alias=["--compute"]),
            SecurityType(flag="-t", alias=["--type"]),
            User(flag="-u", alias=["--user"]),
            SecurityRole(flag="-r", alias=["--role"]),
            SecurityRange(flag="-l", alias=["--range"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Command(arity=Arity.ZERO_OR_ONE),  # COMMAND
            Other(arity=Arity.ZERO_OR_MORE),  # [args]
        ],
    ],
]
