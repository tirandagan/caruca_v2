from caruca.ir.syntax import *

# `test` evaluates an EXPRESSION and reports the result only through its exit
# status (0 true, 1 false, 2 error). It prints nothing on stdout and never reads
# stdin. Unlike `[`, `test` does NOT honour --help/--version: it treats both as
# ordinary non-empty strings (exit 0), so they are deliberately absent here.
#
# The expression language is recursive (parentheses, `!`, `-a`, `-o`), which a
# flat option/operand syntax cannot capture exactly. The syntaxes below list the
# common primary forms precisely (each optionally negated with `!`) and end with
# a loose catch-all for compound expressions.

_UNARY_FILE_TESTS = [
    "-b", "-c", "-d", "-e", "-f", "-g", "-G", "-h", "-k", "-L",
    "-N", "-O", "-p", "-r", "-s", "-S", "-u", "-w", "-x",
]

test_syntax_spec: list[SyntaxSpecification] = [
    # test            -> false
    # test STRING     -> true iff STRING is non-empty (also `! STRING`)
    [
        [Flag("!")],
        [String()],
    ],
    # test -n STRING / test -z STRING
    [
        [Flag("!")],
        [
            Selection(choices=["-n", "-z"], arity=Arity.EXACTLY_ONE),
            String(arity=Arity.EXACTLY_ONE),
        ],
    ],
    # test -e FILE and the other unary file tests. `-` is a literal file name,
    # not stdin. Only the file's metadata is examined (-N also consults atime).
    [
        [Flag("!")],
        [
            Selection(choices=_UNARY_FILE_TESTS, arity=Arity.EXACTLY_ONE),
            Path(arity=Arity.EXACTLY_ONE),
        ],
    ],
    # test -t FD   (FD is an integer file descriptor)
    [
        [Flag("!")],
        [
            Selection(choices=["-t"], arity=Arity.EXACTLY_ONE),
            Integer(arity=Arity.EXACTLY_ONE, min=0),
        ],
    ],
    # test STRING1 = STRING2 / test STRING1 != STRING2
    [
        [Flag("!")],
        [
            String(arity=Arity.EXACTLY_ONE),
            Selection(choices=["=", "!="], arity=Arity.EXACTLY_ONE),
            String(arity=Arity.EXACTLY_ONE),
        ],
    ],
    # test INTEGER1 -eq INTEGER2 (and -ge -gt -le -lt -ne). Either INTEGER may
    # also be written `-l STRING` (the length of STRING); that two-word form is
    # covered by the catch-all syntax below.
    [
        [Flag("!")],
        [
            Integer(arity=Arity.EXACTLY_ONE),
            Selection(
                choices=["-eq", "-ge", "-gt", "-le", "-lt", "-ne"],
                arity=Arity.EXACTLY_ONE,
            ),
            Integer(arity=Arity.EXACTLY_ONE),
        ],
    ],
    # test FILE1 -ef FILE2 / -nt / -ot
    [
        [Flag("!")],
        [
            Path(arity=Arity.EXACTLY_ONE),
            Selection(choices=["-ef", "-nt", "-ot"], arity=Arity.EXACTLY_ONE),
            Path(arity=Arity.EXACTLY_ONE),
        ],
    ],
    # Catch-all for compound expressions:
    #   ( EXPR ), ! EXPR, EXPR1 -a EXPR2, EXPR1 -o EXPR2
    # Unary operators are given option-style with the type of their argument;
    # whatever remains (strings, integers, binary operators and their operands)
    # is left as free-text operands.
    [
        [
            Flag("!"),
            Flag("("),
            Flag(")"),
            Flag("-a"),
            Flag("-o"),
            String(flag="-n", arity=Arity.ZERO_OR_MORE),
            String(flag="-z", arity=Arity.ZERO_OR_MORE),
            String(flag="-l", arity=Arity.ZERO_OR_MORE),  # length of STRING, used as an INTEGER
            Integer(flag="-t", arity=Arity.ZERO_OR_MORE, min=0),
            Path(flag="-b", arity=Arity.ZERO_OR_MORE),
            Path(flag="-c", arity=Arity.ZERO_OR_MORE),
            Path(flag="-d", arity=Arity.ZERO_OR_MORE),
            Path(flag="-e", arity=Arity.ZERO_OR_MORE),
            Path(flag="-f", arity=Arity.ZERO_OR_MORE),
            Path(flag="-g", arity=Arity.ZERO_OR_MORE),
            Path(flag="-G", arity=Arity.ZERO_OR_MORE),
            Path(flag="-h", arity=Arity.ZERO_OR_MORE, alias=["-L"]),
            Path(flag="-k", arity=Arity.ZERO_OR_MORE),
            Path(flag="-N", arity=Arity.ZERO_OR_MORE),
            Path(flag="-O", arity=Arity.ZERO_OR_MORE),
            Path(flag="-p", arity=Arity.ZERO_OR_MORE),
            Path(flag="-r", arity=Arity.ZERO_OR_MORE),
            Path(flag="-s", arity=Arity.ZERO_OR_MORE),
            Path(flag="-S", arity=Arity.ZERO_OR_MORE),
            Path(flag="-u", arity=Arity.ZERO_OR_MORE),
            Path(flag="-w", arity=Arity.ZERO_OR_MORE),
            Path(flag="-x", arity=Arity.ZERO_OR_MORE),
        ],
        [Other(arity=Arity.ZERO_OR_MORE)],
    ],
]
