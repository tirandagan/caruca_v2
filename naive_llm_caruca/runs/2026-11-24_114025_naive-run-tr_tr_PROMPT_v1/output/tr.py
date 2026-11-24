from caruca.ir.syntax import *

# tr [OPTION]... STRING1 [STRING2]
#
# The number of operands tr accepts depends on the flags (verified against GNU coreutils 9.4):
#   translating (no -d):              exactly two operands
#   -d without -s:                    exactly one operand
#   -d together with -s:              exactly two operands
#   -s alone:                         one or two operands
# This cannot be expressed in a single syntax, so STRING1 is required and STRING2 optional here.
# Operands are character arrays, never file names; tr always reads stdin and writes stdout.
tr_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-c", alias=["-C", "--complement"]),
            Flag("-d", alias=["--delete"]),
            Flag("-s", alias=["--squeeze-repeats"]),
            Flag("-t", alias=["--truncate-set1"]),
            Flag("-A"),  # undocumented; accepted and ignored by GNU tr for compatibility
            Flag("--help"),
            Flag("--version"),
        ],
        [
            String(arity=Arity.EXACTLY_ONE),  # STRING1
            String(arity=Arity.OPTIONAL),  # STRING2
        ],
    ]
]
