from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTr(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-C", "-d", "-s", "-t", "-A", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none: tr always reads stdin and writes stdout, and its operands (STRING1 [STRING2]) are
    # character arrays, never file names (tested: a third word is rejected as "extra operand",
    # so a file name can never be taken as an input file).
    # --help and --version print to stdout without reading stdin.

    def generate_info(self) -> None:
        self.set_all_operands_as_config_arg_type_string()
        self.set_implicit_use_of_stdout()
        if not self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]):
            self.set_implicit_use_of_stdin()
