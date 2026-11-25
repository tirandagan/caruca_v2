from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorFmt(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-s", "-t", "-u", "--help", "--version"]
    # list_of_all_options = ["-p", "-w", "-g"]

    # Which ones do affect input/output?
    # only the number of operands and the flags --help and --version:
    # fmt reformats every FILE operand (or stdin when there is none, or when FILE is "-")
    # and always writes to stdout; no option names a file.

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]):
            # nothing is read; the help/version text goes to stdout
            self.set_all_operands_as_config_arg_type_string()
            self.set_implicit_use_of_stdout()
        else:
            self.all_operands_are_streaming_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
            self.set_implicit_use_of_stdout()
