from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorYes(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "--version"]
    # list_of_all_options = []

    # yes never reads stdin (tested: `echo hi | yes` and `yes < /dev/null`
    # both print 'y' forever) and never opens a file: its operands are the
    # text to repeat, not paths. It only ever writes to stdout.
    # With --help/--version it prints once to stdout and exits; the operands,
    # if any, are ignored.

    def generate_info(self) -> None:
        self.set_all_operands_as_config_arg_type_string()
        self.set_implicit_use_of_stdout()
