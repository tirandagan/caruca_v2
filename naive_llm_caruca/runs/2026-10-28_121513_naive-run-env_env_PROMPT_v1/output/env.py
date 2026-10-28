from caruca.ir.syntax import *

# env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]   (GNU coreutils 9.4)
#
# Observed on the binary:
#   * -u/--unset may be repeated; -u NAME, -uNAME and --unset=NAME all work.
#   * --block-signal, --default-signal and --ignore-signal take an *optional*
#     argument that must be attached with '=' ("--block-signal PIPE" runs PIPE
#     as the command). SIG is a comma-separated list of signal names/numbers;
#     without SIG all known signals are meant. The format has no way to mark a
#     value as optional, so they are described the same way tee's
#     --output-error[=MODE] is in the samples.
#   * A lone '-' right after the options is a synonym for -i; anywhere later it
#     is taken as the COMMAND. It is listed with the options for that reason.
#   * The first operand without '=' is the COMMAND; everything after it is an ARG
#     and is never interpreted by env. -0/--null is rejected when a COMMAND is given.

env_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-i", alias=["--ignore-environment"]),
            Flag("-"),
            Flag("-0", alias=["--null"]),
            Variable(flag="-u", alias=["--unset"], arity=Arity.ZERO_OR_MORE),
            Path(flag="-C", alias=["--chdir"]),
            String(flag="-S", alias=["--split-string"]),
            List(
                of=Signal,
                separator=",",
                flag="--block-signal",
                flag_followed_by_equals=True,
                arity=Arity.ZERO_OR_MORE,
            ),
            List(
                of=Signal,
                separator=",",
                flag="--default-signal",
                flag_followed_by_equals=True,
                arity=Arity.ZERO_OR_MORE,
            ),
            List(
                of=Signal,
                separator=",",
                flag="--ignore-signal",
                flag_followed_by_equals=True,
                arity=Arity.ZERO_OR_MORE,
            ),
            Flag("--list-signal-handling"),
            Flag("-v", alias=["--debug"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            String(arity=Arity.ZERO_OR_MORE),  # NAME=VALUE assignments
            Command(arity=Arity.ZERO_OR_ONE),  # COMMAND
            Other(arity=Arity.ZERO_OR_MORE),  # ARG... passed through to COMMAND
        ],
    ]
]
