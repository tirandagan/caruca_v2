from caruca.ir.syntax import *

# vdir is GNU coreutils' `ls -l -b` (long listing with C-style escapes).
# It takes no stream input: a lone `-` operand is an ordinary file name.
# --color, --classify/-F and --hyperlink take an *optional* WHEN that must be
# attached with `=`; the bare spelling is therefore listed as a Flag and the
# `=WHEN` spelling as a Selection.
WHEN_CHOICES = (
    "always", "yes", "force",
    "never", "no", "none",
    "auto", "tty", "if-tty",
)

vdir_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-a", alias=["--all"]),
            Flag("-A", alias=["--almost-all"]),
            Flag("--author"),
            Flag("-b", alias=["--escape"]),
            Size(flag="--block-size", flag_followed_by_equals=True),
            Flag("-B", alias=["--ignore-backups"]),
            Flag("-c"),
            Flag("-C"),
            Flag("--color"),
            Selection(flag="--color", flag_followed_by_equals=True, choices=WHEN_CHOICES),
            Flag("-d", alias=["--directory"]),
            Flag("-D", alias=["--dired"]),
            Flag("-f"),
            Flag("-F", alias=["--classify"]),
            Selection(flag="--classify", flag_followed_by_equals=True, choices=WHEN_CHOICES),
            Flag("--file-type"),
            Selection(
                flag="--format",
                flag_followed_by_equals=True,
                choices=("across", "commas", "horizontal", "long", "single-column", "verbose", "vertical"),
            ),
            Flag("--full-time"),
            Flag("-g"),
            Flag("--group-directories-first"),
            Flag("-G", alias=["--no-group"]),
            Flag("-h", alias=["--human-readable"]),
            Flag("--si"),
            Flag("-H", alias=["--dereference-command-line"]),
            Flag("--dereference-command-line-symlink-to-dir"),
            Glob(flag="--hide", flag_followed_by_equals=True),
            Flag("--hyperlink"),
            Selection(flag="--hyperlink", flag_followed_by_equals=True, choices=WHEN_CHOICES),
            Selection(
                flag="--indicator-style",
                flag_followed_by_equals=True,
                choices=("none", "slash", "file-type", "classify"),
            ),
            Flag("-i", alias=["--inode"]),
            Glob(flag="-I", alias=["--ignore"], flag_followed_by_equals=True),
            Flag("-k", alias=["--kibibytes"]),
            Flag("-l"),
            Flag("-L", alias=["--dereference"]),
            Flag("-m"),
            Flag("-n", alias=["--numeric-uid-gid"]),
            Flag("-N", alias=["--literal"]),
            Flag("-o"),
            Flag("-p"),
            Flag("-q", alias=["--hide-control-chars"]),
            Flag("--show-control-chars"),
            Flag("-Q", alias=["--quote-name"]),
            Selection(
                flag="--quoting-style",
                flag_followed_by_equals=True,
                choices=("literal", "locale", "shell", "shell-always", "shell-escape", "shell-escape-always", "c", "escape"),
            ),
            Flag("-r", alias=["--reverse"]),
            Flag("-R", alias=["--recursive"]),
            Flag("-s", alias=["--size"]),
            Flag("-S"),
            Selection(
                flag="--sort",
                flag_followed_by_equals=True,
                choices=("none", "size", "time", "version", "extension", "width"),
            ),
            Selection(
                flag="--time",
                flag_followed_by_equals=True,
                choices=("atime", "access", "use", "ctime", "status", "mtime", "modification", "birth", "creation"),
            ),
            TimeStyle(flag="--time-style", flag_followed_by_equals=True),
            Flag("-t"),
            Integer(flag="-T", alias=["--tabsize"], flag_followed_by_equals=True, min=0),
            Flag("-u"),
            Flag("-U"),
            Flag("-v"),
            Integer(flag="-w", alias=["--width"], flag_followed_by_equals=True, min=0),
            Flag("-x"),
            Flag("-X"),
            Flag("-Z", alias=["--context"]),
            Flag("--zero"),
            Flag("-1"),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(arity=Arity.ZERO_OR_MORE),  # [FILE]...  (current directory when absent)
        ],
    ]
]
