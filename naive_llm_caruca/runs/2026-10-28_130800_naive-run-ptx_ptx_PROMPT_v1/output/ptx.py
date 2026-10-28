from caruca.ir.syntax import *

# Options shared by both syntaxes (GNU coreutils 9.4 ptx).
# -O and -T are flag spellings of --format=roff and --format=tex.
_ptx_common_options = [
    Flag("-A", alias=["--auto-reference"]),
    String(flag="-F", alias=["--flag-truncation"], flag_followed_by_equals=True),
    String(flag="-M", alias=["--macro-name"], flag_followed_by_equals=True),
    Flag("-O"),
    Flag("-T"),
    Selection(flag="--format", choices=["roff", "tex"], flag_followed_by_equals=True),
    Flag("-R", alias=["--right-side-refs"]),
    Regex(flag="-S", alias=["--sentence-regexp"], flag_followed_by_equals=True),
    Regex(flag="-W", alias=["--word-regexp"], flag_followed_by_equals=True),
    Path(flag="-b", alias=["--break-file"], flag_followed_by_equals=True),
    Flag("-f", alias=["--ignore-case"]),
    Integer(flag="-g", alias=["--gap-size"], min=1, flag_followed_by_equals=True),
    Path(flag="-i", alias=["--ignore-file"], flag_followed_by_equals=True),
    Path(flag="-o", alias=["--only-file"], flag_followed_by_equals=True),
    Flag("-r", alias=["--references"]),
    Flag("-t", alias=["--typeset-mode"]),
    Integer(flag="-w", alias=["--width"], min=1, flag_followed_by_equals=True),
    Flag("--help"),
    Flag("--version"),
]

ptx_syntax_spec: list[SyntaxSpecification] = [
    # ptx [OPTION]... [INPUT]...   (without -G): every operand is an input, output goes to stdout
    [
        _ptx_common_options,
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [INPUT]...
    ],
    # ptx -G [OPTION]... [INPUT [OUTPUT]]: System V style, second operand is the output file
    [
        _ptx_common_options
        + [Flag("-G", alias=["--traditional"], arity=Arity.EXACTLY_ONE)],
        [
            Path(dash_as_stdin=True),  # [INPUT]
            Path(),  # [OUTPUT]; a lone "-" here is a literal file name, not stdout
        ],
    ],
]
