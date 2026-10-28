from caruca.ir.syntax import *

# pr (GNU coreutils 9.4): pr [OPTION]... [FILE]...
#
# Parsing quirks verified against /usr/bin/pr:
#   * -e, -i, -n, -s and -S take an OPTIONAL value that must be attached to the
#     option (-e8, -s,, -n:3); a separate word is treated as a FILE operand.
#     The long forms take the value only with "=" (--expand-tabs=8).  They are
#     therefore listed below as Flags (the bare, most common form) and the
#     long forms additionally as value nodes with flag_followed_by_equals.
#   * -COLUMN is a run of digits (-2, -12); digits accumulate across options
#     (-1 -2 is the same as -12).  It is modelled by Flag("-1")..Flag("-9")
#     for the single-digit case plus the --columns=COLUMN option.
#   * +FIRST_PAGE[:LAST_PAGE] is a "+"-prefixed operand-looking option; only the
#     --pages=FIRST[:LAST] form is modelled as an option node.

pr_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Range(flag="--pages", flag_followed_by_equals=True),  # +FIRST_PAGE[:LAST_PAGE]
            Integer(flag="--columns", flag_followed_by_equals=True, min=1),  # -COLUMN
            Flag("-1"),
            Flag("-2"),
            Flag("-3"),
            Flag("-4"),
            Flag("-5"),
            Flag("-6"),
            Flag("-7"),
            Flag("-8"),
            Flag("-9"),
            Flag("-a", alias=["--across"]),
            Flag("-c", alias=["--show-control-chars"]),
            Flag("-d", alias=["--double-space"]),
            DateFormat(flag="-D", alias=["--date-format"], flag_followed_by_equals=True),
            Flag("-e", alias=["--expand-tabs"]),
            String(flag="--expand-tabs", flag_followed_by_equals=True),  # [CHAR[WIDTH]]
            Flag("-F", alias=["-f", "--form-feed"]),
            String(flag="-h", alias=["--header"], flag_followed_by_equals=True),
            Flag("-i", alias=["--output-tabs"]),
            String(flag="--output-tabs", flag_followed_by_equals=True),  # [CHAR[WIDTH]]
            Flag("-J", alias=["--join-lines"]),
            Integer(flag="-l", alias=["--length"], flag_followed_by_equals=True, min=1),
            Flag("-m", alias=["--merge"]),
            Flag("-n", alias=["--number-lines"]),
            String(flag="--number-lines", flag_followed_by_equals=True),  # [SEP[DIGITS]]
            Integer(flag="-N", alias=["--first-line-number"], flag_followed_by_equals=True),
            Integer(flag="-o", alias=["--indent"], flag_followed_by_equals=True, min=0),
            Flag("-r", alias=["--no-file-warnings"]),
            Flag("-s", alias=["--separator"]),
            Char(flag="--separator", flag_followed_by_equals=True),  # [CHAR]
            Flag("-S", alias=["--sep-string"]),
            Separator(flag="--sep-string", flag_followed_by_equals=True),  # [STRING]
            Flag("-t", alias=["--omit-header"]),
            Flag("-T", alias=["--omit-pagination"]),
            Flag("-v", alias=["--show-nonprinting"]),
            Integer(flag="-w", alias=["--width"], flag_followed_by_equals=True, min=1),
            Integer(flag="-W", alias=["--page-width"], flag_followed_by_equals=True, min=1),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),  # [FILE]...
        ],
    ]
]
