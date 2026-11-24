from caruca.ir.syntax import *

# GNU sed 4.9.  The man page synopsis still lists a short `-V`, but the binary
# rejects it ("option requires an argument -- 'V'"), so only `--version` is kept.
#
# `-i[SUFFIX]` / `--in-place[=SUFFIX]`: the suffix is optional and, for the short
# form, can only be attached (`-i.bak`); `-i .bak` makes `.bak` the script.  The
# bare form is described as a flag and the long `=SUFFIX` form as a value node.

_common_options = [
    Flag("-n", alias=["--quiet", "--silent"]),
    Flag("--debug"),
    Flag("--follow-symlinks"),
    Flag("-i", alias=["--in-place"]),
    String(flag="--in-place", flag_followed_by_equals=True),  # [=SUFFIX]
    Integer(flag="-l", alias=["--line-length"], flag_followed_by_equals=True, min=0),
    Flag("--posix"),
    Flag("-E", alias=["-r", "--regexp-extended"]),
    Flag("-s", alias=["--separate"]),
    Flag("--sandbox"),
    Flag("-u", alias=["--unbuffered"]),
    Flag("-z", alias=["--null-data"]),
    Flag("--help"),
    Flag("--version"),
]

_expression = String(
    flag="-e", alias=["--expression"], flag_followed_by_equals=True, arity=Arity.AT_LEAST_ONE
)
_expression_optional = String(
    flag="-e", alias=["--expression"], flag_followed_by_equals=True, arity=Arity.ZERO_OR_MORE
)
_script_file = Path(
    flag="-f", alias=["--file"], flag_followed_by_equals=True, dash_as_stdin=True, arity=Arity.AT_LEAST_ONE
)
_script_file_optional = Path(
    flag="-f", alias=["--file"], flag_followed_by_equals=True, dash_as_stdin=True, arity=Arity.ZERO_OR_MORE
)

_input_files = Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)  # [input-file]...

sed_syntax_spec: list[SyntaxSpecification] = [
    # 1. No -e/-f given: the first operand is the script, the rest are input files.
    [
        _common_options,
        [
            String(arity=Arity.EXACTLY_ONE),  # script-only-if-no-other-script
            _input_files,
        ],
    ],
    # 2. At least one -e (any number of -f): every operand is an input file.
    [
        _common_options + [_expression, _script_file_optional],
        [_input_files],
    ],
    # 3. At least one -f and no -e: every operand is an input file.
    [
        _common_options + [_script_file],
        [_input_files],
    ],
]
