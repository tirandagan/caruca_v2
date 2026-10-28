from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorNumfmt(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--debug", "--grouping", "--header", "-z", "--help", "--version"]
    # list_of_all_options = ["-d", "--field", "--format", "--from", "--from-unit", "--invalid",
    #                        "--padding", "--round", "--suffix", "--to", "--to-unit"]

    # Which ones do affect input/output?
    # none of them; only the number of operands matters
    # operands are NUMBERs (values to convert), never files; a lone "-" is rejected as an invalid number
    # (tested: `numfmt -` and `numfmt /some/file` both fail with "invalid number")
    # without operands, the numbers are read from stdin; the result always goes to stdout

    def generate_info(self) -> None:
        # assumption that version/help not provided
        self.set_implicit_use_of_stdout()
        if self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
        else:
            self.set_all_operands_as_config_arg_type_string()
