from caruca.ir.syntax import *

# GNU findutils xargs 4.9.0: xargs [OPTION]... [COMMAND [INITIAL-ARGS]...]
#
# Option parsing stops at the first non-option word (the command); everything
# after it, including words that look like xargs options, is passed to COMMAND.
#
# -e/--eof, -i/--replace and -l/--max-lines take an *optional* value which must
# be attached (-eSTR, --eof=STR); a separate following word is taken as COMMAND.
# -E, -I and -L are the mandatory-value spellings and accept a separate word.

xargs_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-0", alias=["--null"]),
            Path(flag="-a", alias=["--arg-file"], dash_as_stdin=True),
            Delimiter(flag="-d", alias=["--delimiter"]),  # one char or a \-escape such as \n, \0, \x41
            String(flag="-E"),  # eof-str
            String(flag="-e", alias=["--eof"], flag_followed_by_equals=True),  # [eof-str], attached only
            String(flag="-I"),  # replace-str
            String(flag="-i", alias=["--replace"], flag_followed_by_equals=True),  # [replace-str], attached only; default {}
            Integer(flag="-L", min=1),  # max-lines
            Integer(flag="-l", alias=["--max-lines"], flag_followed_by_equals=True, min=1),  # [max-lines], attached only; default 1
            Integer(flag="-n", alias=["--max-args"], min=1),
            Integer(flag="-P", alias=["--max-procs"], min=0, max=2147483647),
            Flag("-o", alias=["--open-tty"]),
            Flag("-p", alias=["--interactive"]),
            Variable(flag="--process-slot-var"),
            Flag("-r", alias=["--no-run-if-empty"]),
            Integer(flag="-s", alias=["--max-chars"], min=1),
            Flag("--show-limits"),
            Flag("-t", alias=["--verbose"]),
            Flag("-x", alias=["--exit"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Command(),  # COMMAND, defaults to echo
            String(arity=Arity.ZERO_OR_MORE),  # INITIAL-ARGS
        ],
    ]
]
