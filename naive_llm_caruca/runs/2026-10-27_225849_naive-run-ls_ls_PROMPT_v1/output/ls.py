from caruca.ir.syntax import *

# GNU coreutils ls 9.4.  Operands are paths; a lone "-" is an ordinary file
# name, not standard input.  Long options with a mandatory argument accept
# both "--opt VALUE" and "--opt=VALUE"; the three with an optional argument
# (--color, --classify, --hyperlink) only accept "--opt" or "--opt=VALUE",
# which is modelled with an empty choice plus flag_followed_by_equals, as
# rm's --preserve-root is.  -F is the argument-less spelling of --classify.

WHEN_CHOICES = [
    "",
    "always", "yes", "force",
    "never", "no", "none",
    "auto", "tty", "if-tty",
]

ls_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-a", alias=["--all"]),
            Flag("-A", alias=["--almost-all"]),
            Flag("--author"),
            Flag("-b", alias=["--escape"]),
            Size(flag="--block-size"),
            Flag("-B", alias=["--ignore-backups"]),
            Flag("-c"),
            Flag("-C"),
            Selection(
                flag="--color", choices=WHEN_CHOICES, flag_followed_by_equals=True
            ),
            Flag("-d", alias=["--directory"]),
            Flag("-D", alias=["--dired"]),
            Flag("-f"),
            Flag("-F"),
            Selection(
                flag="--classify", choices=WHEN_CHOICES, flag_followed_by_equals=True
            ),
            Flag("--file-type"),
            Selection(
                flag="--format",
                choices=[
                    "verbose", "long",
                    "commas",
                    "horizontal", "across",
                    "vertical",
                    "single-column",
                ],
            ),
            Flag("--full-time"),
            Flag("-g"),
            Flag("--group-directories-first"),
            Flag("-G", alias=["--no-group"]),
            Flag("-h", alias=["--human-readable"]),
            Flag("--si"),
            Flag("-H", alias=["--dereference-command-line"]),
            Flag("--dereference-command-line-symlink-to-dir"),
            Glob(flag="--hide", arity=Arity.ZERO_OR_MORE),
            Selection(
                flag="--hyperlink", choices=WHEN_CHOICES, flag_followed_by_equals=True
            ),
            Selection(
                flag="--indicator-style",
                choices=["none", "slash", "file-type", "classify"],
            ),
            Flag("-i", alias=["--inode"]),
            Glob(flag="-I", alias=["--ignore"], arity=Arity.ZERO_OR_MORE),
            Flag("-k", alias=["--kibibytes"]),
            Flag("-l"),
            Flag("-L", alias=["--dereference"]),
            Flag("-m"),
            Flag("-n", alias=["--numeric-uid-gid"]),
            Flag("-N", alias=["--literal"]),
            Flag("-o"),
            Flag("-p"),  # same as --indicator-style=slash
            Flag("-q", alias=["--hide-control-chars"]),
            Flag("--show-control-chars"),
            Flag("-Q", alias=["--quote-name"]),
            Selection(
                flag="--quoting-style",
                choices=[
                    "literal", "shell", "shell-always", "shell-escape",
                    "shell-escape-always", "c", "c-maybe", "escape",
                    "locale", "clocale",
                ],
            ),
            Flag("-r", alias=["--reverse"]),
            Flag("-R", alias=["--recursive"]),
            Flag("-s", alias=["--size"]),
            Flag("-S"),
            Selection(
                flag="--sort",
                choices=["none", "time", "size", "extension", "version", "width"],
            ),
            Selection(
                flag="--time",
                choices=[
                    "atime", "access", "use",
                    "ctime", "status",
                    "mtime", "modification",
                    "birth", "creation",
                ],
            ),
            TimeStyle(flag="--time-style"),
            Flag("-t"),
            Integer(flag="-T", alias=["--tabsize"], min=0),
            Flag("-u"),
            Flag("-U"),
            Flag("-v"),
            Integer(flag="-w", alias=["--width"], min=0),
            Flag("-x"),
            Flag("-X"),
            Flag("-Z", alias=["--context"]),
            Flag("--zero"),
            Flag("-1"),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(arity=Arity.ZERO_OR_MORE),  # [FILE...]; "." when none given
        ],
    ]
]
