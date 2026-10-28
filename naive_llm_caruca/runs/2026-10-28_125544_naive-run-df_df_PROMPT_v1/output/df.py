from caruca.ir.syntax import *

# GNU coreutils 9.4 df.
# Notes from testing the binary:
#   * -m is accepted but undocumented (like --block-size=1M), and -F TYPE is an
#     undocumented synonym for -t TYPE.
#   * -t/--type and -x/--exclude-type take one file system type each and may be
#     repeated; a comma-separated list is not understood.
#   * --output takes an optional, '='-attached, comma-separated field list and
#     may be repeated (the lists accumulate); a bare --output prints all fields.
#   * -B/--block-size accepts an integer with optional unit suffix
#     (K,M,G,T,P,E,Z,Y,R,Q, KB,MB,..., KiB,MiB,...) or a bare unit letter.
#   * Standard input is never read; a lone '-' operand is an ordinary file name.

_output_fields = [
    "source",
    "fstype",
    "itotal",
    "iused",
    "iavail",
    "ipcent",
    "size",
    "used",
    "avail",
    "pcent",
    "file",
    "target",
]

df_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-a", alias=["--all"]),
            Size(flag="-B", alias=["--block-size"]),
            Flag("-h", alias=["--human-readable"]),
            Flag("-H", alias=["--si"]),
            Flag("-i", alias=["--inodes"]),
            Flag("-k"),
            Flag("-m"),
            Flag("-l", alias=["--local"]),
            Flag("--no-sync"),
            Flag("--output"),
            List(
                of=Selection(choices=_output_fields),
                separator=",",
                flag="--output",
                flag_followed_by_equals=True,
                arity=Arity.ZERO_OR_MORE,
            ),
            Flag("-P", alias=["--portability"]),
            Flag("--sync"),
            Flag("--total"),
            Filesystem(flag="-t", alias=["--type", "-F"], arity=Arity.ZERO_OR_MORE),
            Flag("-T", alias=["--print-type"]),
            Filesystem(flag="-x", alias=["--exclude-type"], arity=Arity.ZERO_OR_MORE),
            Flag("-v"),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE)],  # [FILE]...
    ],
]
