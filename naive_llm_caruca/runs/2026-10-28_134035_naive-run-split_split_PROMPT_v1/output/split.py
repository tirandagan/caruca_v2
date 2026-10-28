from caruca.ir.syntax import *

# split [OPTION]... [FILE [PREFIX]]   (GNU coreutils 9.4)
#
# Not expressible in this vocabulary and therefore omitted:
#   - the obsolete `-NUMBER` form (`split -5 FILE` == `split -l 5 FILE`)
#   - the optional-value spelling of --numeric-suffixes[=FROM] and --hex-suffixes[=FROM]
#     is modelled twice: bare, as an alias of the -d / -x flag, and with `=FROM`,
#     as a value node.  `--numeric-suffixes FROM` (separate word) is NOT accepted by
#     the binary; FROM would be taken as the FILE operand.
split_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Integer(flag="-a", alias=["--suffix-length"], flag_followed_by_equals=True, min=0),
            String(flag="--additional-suffix", flag_followed_by_equals=True),
            Size(flag="-b", alias=["--bytes"], flag_followed_by_equals=True),
            Size(flag="-C", alias=["--line-bytes"], flag_followed_by_equals=True),
            Flag("-d", alias=["--numeric-suffixes"]),
            Integer(flag="--numeric-suffixes", flag_followed_by_equals=True, min=0),
            Flag("-x", alias=["--hex-suffixes"]),
            # FROM is a hexadecimal number here ("a", "ff"), so not an Integer
            String(flag="--hex-suffixes", flag_followed_by_equals=True),
            Flag("-e", alias=["--elide-empty-files"]),
            Command(flag="--filter", flag_followed_by_equals=True),
            Integer(flag="-l", alias=["--lines"], flag_followed_by_equals=True, min=1),
            # CHUNKS: N | K/N | l/N | l/K/N | r/N | r/K/N
            String(flag="-n", alias=["--number"], flag_followed_by_equals=True),
            # a single character; '\0' spells NUL
            Separator(flag="-t", alias=["--separator"], flag_followed_by_equals=True),
            Flag("-u", alias=["--unbuffered"]),
            Flag("--verbose"),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(dash_as_stdin=True),  # FILE: input, default stdin
            Path(),                    # PREFIX: output files are PREFIXaa, PREFIXab, ...; default 'x'
        ],
    ]
]
