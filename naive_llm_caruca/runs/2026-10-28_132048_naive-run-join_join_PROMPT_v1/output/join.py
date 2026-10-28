from caruca.ir.syntax import *

# join (GNU coreutils 9.4): join [OPTION]... FILE1 FILE2
#
# Not expressed here (obsolete forms the binary still accepts):
#   * "-j1 FIELD" / "-j2 FIELD" as spellings of "-1 FIELD" / "-2 FIELD" when the
#     word after "-j1"/"-j2" starts with a digit; otherwise "-j1" is just "-j 1".
#   * "-o SPEC SPEC ..." where additional blank-separated FILENUM.FIELD words
#     following -o are appended to the format instead of being operands.
join_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            # FILENUM is 1 or 2; may be given for both files (-a 1 -a 2)
            Integer(flag="-a", min=1, max=2, arity=Arity.ZERO_OR_MORE),
            String(flag="-e"),
            Flag("-i", alias=["--ignore-case"]),
            Integer(flag="-j", min=1),
            # one or more comma/blank separated 'FILENUM.FIELD' or '0' specs, or 'auto';
            # repeated -o options are accumulated
            Format(flag="-o", arity=Arity.ZERO_OR_MORE),
            # a single character, or '' for "no separator" (whole line is the field)
            Char(flag="-t"),
            Integer(flag="-v", min=1, max=2, arity=Arity.ZERO_OR_MORE),
            Integer(flag="-1", min=1),
            Integer(flag="-2", min=1),
            Flag("--check-order"),
            Flag("--nocheck-order"),
            Flag("--header"),
            Flag("-z", alias=["--zero-terminated"]),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            # exactly two files; at most one of them may be '-'
            Path(arity=Arity.EXACTLY_ONE, dash_as_stdin=True),  # FILE1
            Path(arity=Arity.EXACTLY_ONE, dash_as_stdin=True),  # FILE2
        ],
    ]
]
