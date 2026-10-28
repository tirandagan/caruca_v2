from caruca.ir.syntax import (
    Flag,
    List,
    Group,
    OwnerGroup,
    Path,
    Command,
    Other,
    Arity,
    SyntaxSpecification,
)

# chroot [OPTION] NEWROOT [COMMAND [ARG]...]
# chroot OPTION
#
# Options are only recognised before NEWROOT: the first non-option word is
# NEWROOT and every following word, even one starting with '-', is passed to
# COMMAND unchanged (GNU coreutils 9.4, verified against the binary).
chroot_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            # --groups=G_LIST: supplementary groups as g1,g2,..,gN (names or IDs);
            # an empty list is accepted and clears the supplementary groups.
            List(
                flag="--groups",
                of=Group,
                separator=",",
                flag_followed_by_equals=True,
            ),
            # --userspec=USER:GROUP, either half may be a name or a numeric ID
            # and either half may be omitted (e.g. "nobody", ":65534").
            OwnerGroup(flag="--userspec", flag_followed_by_equals=True),
            # Only permitted when NEWROOT is the current '/'.
            Flag("--skip-chdir"),
            Flag("--help"),
            Flag("--version"),
        ],
        [
            Path(arity=Arity.EXACTLY_ONE),  # NEWROOT (a directory)
            Command(arity=Arity.ZERO_OR_ONE),  # [COMMAND], defaults to "$SHELL" -i
            Other(arity=Arity.ZERO_OR_MORE),  # [ARG]...
        ],
    ],
]
