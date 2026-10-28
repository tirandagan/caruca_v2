from caruca.ir.syntax import *

# who [OPTION]... [ FILE | ARG1 ARG2 ]
#
# Every option is a plain flag; none takes a value (GNU coreutils 9.4 rejects
# e.g. `--lookup=foo` with "doesn't allow an argument").
#
# Operands come in two mutually exclusive shapes, hence two syntaxes:
#   1. zero or one FILE: the utmp/wtmp database to read instead of
#      /var/run/utmp.  A lone `-` is opened as a literal file name, not stdin.
#   2. exactly two words (ARG1 ARG2, conventionally `am i`), which imply -m.
#      They are not files; their text is ignored.
# A third operand is rejected: "who: extra operand".

_who_options = [
    Flag("-a", alias=["--all"]),
    Flag("-b", alias=["--boot"]),
    Flag("-d", alias=["--dead"]),
    Flag("-H", alias=["--heading"]),
    Flag("-l", alias=["--login"]),
    Flag("--lookup"),
    Flag("-m"),
    Flag("-p", alias=["--process"]),
    Flag("-q", alias=["--count"]),
    Flag("-r", alias=["--runlevel"]),
    Flag("-s", alias=["--short"]),
    Flag("-t", alias=["--time"]),
    Flag("-T", alias=["-w", "--mesg", "--message", "--writable"]),
    Flag("-u", alias=["--users"]),
    Flag("--help"),
    Flag("--version"),
]

who_syntax_spec: list[SyntaxSpecification] = [
    [
        list(_who_options),
        [Path(arity=Arity.ZERO_OR_ONE)],  # [FILE]
    ],
    [
        list(_who_options),
        [String(arity=Arity.EXACTLY_TWO)],  # ARG1 ARG2 ('am i')
    ],
]
