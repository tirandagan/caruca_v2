from caruca.ir.syntax import *

# GNU grep 3.11.  The man page gives three synopses, which differ only in how
# the patterns are supplied:
#
#   grep [OPTION...] PATTERNS [FILE...]
#   grep [OPTION...] -e PATTERNS ... [FILE...]
#   grep [OPTION...] -f PATTERN_FILE ... [FILE...]
#
# The option nodes are shared; only the arity of -e / -f and the presence of the
# PATTERNS operand differ, so they are built from one common list below.
#
# Not representable here: the context shorthand -NUM (e.g. `grep -2 foo`), which
# is a numeric option letter rather than a named option.

_grep_common_options = [
    Flag("--help"),
    Flag("-V", alias=["--version"]),
    # pattern syntax
    Flag("-E", alias=["--extended-regexp"]),
    Flag("-F", alias=["--fixed-strings"]),
    Flag("-G", alias=["--basic-regexp"]),
    Flag("-P", alias=["--perl-regexp"]),
    # matching control (-e / -f are added per syntax)
    Flag("-i", alias=["-y", "--ignore-case"]),  # -y is an undocumented synonym
    Flag("--no-ignore-case"),
    Flag("-v", alias=["--invert-match"]),
    Flag("-w", alias=["--word-regexp"]),
    Flag("-x", alias=["--line-regexp"]),
    # general output control
    Flag("-c", alias=["--count"]),
    # the value is only accepted as --color=WHEN; `--color always` makes
    # "always" the PATTERNS operand
    Selection(
        flag="--color",
        alias=["--colour"],
        choices=["never", "always", "auto"],
        flag_followed_by_equals=True,
    ),
    Flag("-L", alias=["--files-without-match"]),
    Flag("-l", alias=["--files-with-matches"]),
    Integer(flag="-m", alias=["--max-count"]),  # negative NUM means no limit
    Flag("-o", alias=["--only-matching"]),
    Flag("-q", alias=["--quiet", "--silent"]),
    Flag("-s", alias=["--no-messages"]),
    # output line prefix control
    Flag("-b", alias=["--byte-offset"]),
    Flag("-u", alias=["--unix-byte-offsets"]),  # obsolete, accepted with a warning
    Flag("-H", alias=["--with-filename"]),
    Flag("-h", alias=["--no-filename"]),
    String(flag="--label"),
    Flag("-n", alias=["--line-number"]),
    Flag("-T", alias=["--initial-tab"]),
    Flag("-Z", alias=["--null"]),
    # context line control
    Integer(flag="-A", alias=["--after-context"], min=0),
    Integer(flag="-B", alias=["--before-context"], min=0),
    Integer(flag="-C", alias=["--context"], min=0),
    Separator(flag="--group-separator"),
    Flag("--no-group-separator"),
    # file and directory selection
    Flag("-a", alias=["--text"]),
    Selection(flag="--binary-files", choices=["binary", "without-match", "text"]),
    Selection(flag="-D", alias=["--devices"], choices=["read", "skip"]),
    Selection(
        flag="-d", alias=["--directories"], choices=["read", "skip", "recurse"]
    ),
    Glob(flag="--exclude", arity=Arity.ZERO_OR_MORE),
    Path(flag="--exclude-from", arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),
    Glob(flag="--exclude-dir", arity=Arity.ZERO_OR_MORE),
    Flag("-I"),
    Glob(flag="--include", arity=Arity.ZERO_OR_MORE),
    Flag("-r", alias=["--recursive"]),
    Flag("-R", alias=["--dereference-recursive"]),
    # other options
    Flag("--line-buffered"),
    Flag("-U", alias=["--binary"]),
    Flag("-z", alias=["--null-data"]),
]

grep_syntax_spec: list[SyntaxSpecification] = [
    # grep [OPTION...] PATTERNS [FILE...]
    [
        _grep_common_options,
        [
            Regex(arity=Arity.EXACTLY_ONE),  # PATTERNS
            Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),  # [FILE...]
        ],
    ],
    # grep [OPTION...] -e PATTERNS ... [FILE...]
    [
        _grep_common_options
        + [
            Regex(flag="-e", alias=["--regexp"], arity=Arity.AT_LEAST_ONE),
            Path(flag="-f", alias=["--file"], arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),
        ],
        [
            Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),  # [FILE...]
        ],
    ],
    # grep [OPTION...] -f PATTERN_FILE ... [FILE...]
    [
        _grep_common_options
        + [
            Path(flag="-f", alias=["--file"], arity=Arity.AT_LEAST_ONE, dash_as_stdin=True),
            Regex(flag="-e", alias=["--regexp"], arity=Arity.ZERO_OR_MORE),
        ],
        [
            Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),  # [FILE...]
        ],
    ],
]
