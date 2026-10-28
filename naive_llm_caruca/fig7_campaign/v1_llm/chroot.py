from caruca.ir.syntax import *

chroot_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            String(flag="--groups"),
            String(flag="--userspec"),
            Flag("--skip-chdir"),
            Flag("--help"),
            Flag("--version"),
        ],
        [Path(arity=Arity.EXACTLY_ONE), Command(arity=Arity.ZERO_OR_MORE)],
    ]
]

