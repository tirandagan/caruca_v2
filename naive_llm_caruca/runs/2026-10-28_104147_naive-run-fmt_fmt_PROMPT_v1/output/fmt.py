from caruca.ir.syntax import *

# fmt [-WIDTH] [OPTION]... [FILE]...
#
# Verified against GNU coreutils 9.4:
#  - WIDTH and GOAL are decimal integers; fmt rejects anything outside 0..2500
#    ("Numerical result out of range") and rejects a goal larger than the width.
#  - Short options take their value attached or separated (-w20, -w 20); long
#    options take it with "=" or separated (--width=20, --width 20).
#  - Operands are files read as streams; no operand, or a lone "-", means stdin.
#  - The legacy shorthand "-WIDTH" (e.g. "fmt -20 FILE") is accepted only as the
#    very first option and cannot be expressed as a fixed spelling here; it is
#    equivalent to "-w WIDTH".
fmt_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-c", alias=["--crown-margin"]),
            String(flag="-p", alias=["--prefix"], flag_followed_by_equals=True),
            Flag("-s", alias=["--split-only"]),
            Flag("-t", alias=["--tagged-paragraph"]),
            Flag("-u", alias=["--uniform-spacing"]),
            Integer(flag="-w", alias=["--width"], flag_followed_by_equals=True, min=0, max=2500),
            Integer(flag="-g", alias=["--goal"], flag_followed_by_equals=True, min=0, max=2500),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True)],  # [FILE...]
    ]
]
