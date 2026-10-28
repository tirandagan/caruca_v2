from caruca.ir.syntax import *

# UnZip 6.00 (Unix build).  Only the option letters this build actually accepts are listed; the
# platform-specific ones (-A, -E, -i, -J, -N, -s, -S, -Y, -$, -/, -2 in normal mode) are rejected
# with the usage screen.  Repeated letters (-qq, -aa, -DD, -LL, -UU) are the same flag given twice.
#
#   unzip [-Z] [-cflptTuvz[abjnoqsCDKLMUVWX$/:^]] file[.zip] [file(s) ...] [-x xfile(s) ...] [-d exdir]
#
# The exclude list (-x) and the extraction directory (-d) are written *after* the archive and the member
# patterns, so they get a position of their own; -d is also accepted before the archive.  -x before the
# archive is not accepted (unzip then takes the next word as the archive name).

unzip_syntax_spec: list[SyntaxSpecification] = [
    # normal mode
    [
        [
            # actions
            Flag("-c"),
            Flag("-f"),
            Flag("-l"),
            Flag("-p"),
            Flag("-t"),
            Flag("-T"),
            Flag("-u"),
            Flag("-v"),
            Flag("-z"),
            Flag("-h"),
            Flag("-hh"),
            # modifiers
            Flag("-a"),
            Flag("-b"),
            Flag("-B"),
            Flag("-C"),
            Flag("-D"),
            Flag("-F"),
            Flag("-j"),
            Flag("-K"),
            Flag("-L"),
            Flag("-M"),
            Flag("-n"),
            Flag("-o"),
            Flag("-q"),
            Flag("-U"),
            Flag("-V"),
            Flag("-W"),
            Flag("-X"),
            Flag("-:"),
            Flag("-^"),
            String(flag="-I"),  # CHARSET for UNIX and other archives
            String(flag="-O"),  # CHARSET for DOS, Windows and OS/2 archives
            String(flag="-P"),  # password
            Path(flag="-d"),  # exdir, when given before the archive
        ],
        [
            Path(arity=Arity.EXACTLY_ONE),  # file[.zip] (may be a wildcard; "-" is not stdin)
            Glob(arity=Arity.ZERO_OR_MORE),  # [file(s) ...] archive members to process
        ],
        [
            Glob(flag="-x", arity=Arity.ZERO_OR_MORE),  # [-x xfile(s) ...] members to exclude
            Path(flag="-d"),  # [-d exdir]
        ],
    ],
    # zipinfo mode: -Z must be the first option, the remaining options are zipinfo(1) options
    [
        [
            Flag("-Z"),
            Flag("-1"),
            Flag("-2"),
            Flag("-s"),
            Flag("-m"),
            Flag("-l"),
            Flag("-v"),
            Flag("-h"),
            Flag("-M"),
            Flag("-t"),
            Flag("-T"),
            Flag("-U"),
            Flag("-z"),
            Flag("-C"),
            String(flag="-I"),
            String(flag="-O"),
        ],
        [
            Path(arity=Arity.EXACTLY_ONE),  # file[.zip]
            Glob(arity=Arity.ZERO_OR_MORE),  # [file(s) ...]
        ],
        [
            Glob(flag="-x", arity=Arity.ZERO_OR_MORE),  # [-x xfile(s) ...]
        ],
    ],
]
