from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCol(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-f", "-h", "-p", "-x", "-H", "--help", "-V", "--version"]
    # list_of_all_options = ["-l", "--lines"]

    # Which ones do affect input/output?
    # col is a pure filter: it always reads stdin and writes stdout (util-linux 2.39.3).
    # It accepts no operands at all; any operand makes it fail with "bad usage".
    # Only -H/--help and -V/--version change this: they print to stdout and exit without reading stdin.

    def generate_info(self) -> None:
        if self.get_operand_list_length() > 0:
            raise Exception('col does not accept operands')
        if self.does_flag_option_list_contain_at_least_one_of(["-H", "--help", "-V", "--version"]):
            self.set_implicit_use_of_stdout()
        else:
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
