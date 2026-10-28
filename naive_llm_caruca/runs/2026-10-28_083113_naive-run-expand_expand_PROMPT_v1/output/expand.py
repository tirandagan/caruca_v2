from caruca.ir.syntax import *

# expand [OPTION]... [FILE]...   (GNU coreutils 9.4)
#
# -t/--tabs takes either a single number N or a comma- (or blank-) separated
# list of tab positions; the last list element may carry a '/' or '+' prefix
# (e.g. "2,/4", "3,+4"), so the elements are described as String rather than
# Integer. The option may be repeated; the lists accumulate.
# The obsolete forms "-N" and "-N,M" (e.g. "expand -4") are also accepted by
# the binary but are undocumented and cannot be expressed here.
expand_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-i", alias=["--initial"]),
            List(
                flag="-t",
                alias=["--tabs"],
                of=String(),
                separator=",",
                flag_followed_by_equals=True,
                arity=Arity.ZERO_OR_MORE,
            ),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE...]
    ]
]
