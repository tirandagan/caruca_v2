from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorChroot(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--skip-chdir", "--help", "--version"]
    # list_of_all_options = ["--groups", "--userspec"]

    # chroot NEWROOT [COMMAND [ARG]...]
    # Which ones do affect input/output?
    # None of the flags/options do: they only change the identity and cwd of the process.
    # Operands: NEWROOT is a directory that becomes '/', not a data file; COMMAND and ARG... are
    # an arbitrary command line that is executed with the inherited stdin/stdout (verified: data
    # piped into chroot reaches COMMAND, and COMMAND's output appears on stdout). As the executed
    # command is opaque, we conservatively assume both standard streams are used.
    # With no COMMAND, '"$SHELL" -i' is run, which also reads stdin and writes stdout.
    # --help and --version write to stdout only, but we assume they are not given.

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
        # no operand is a file that is read or written as data
        self.set_all_operands_as_config_arg_type_string()
