from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorUnexpand(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "--first-only", "--help", "--version"]
    # list_of_all_options = ["-t"]

    # Which ones do affect input/output?
    # none of them; only the number of operands matters
    # (assumption that --help/--version are not provided)

    def generate_info(self) -> None:
        # unexpand [OPTION]... [FILE]...
        # every FILE operand is read as a stream and concatenated; "-" means stdin
        # with no FILE, stdin is read; output always goes to stdout
        self.all_operands_are_streaming_inputs()
        self.if_no_operands_given_stdin_implicitly_used()
        self.set_implicit_use_of_stdout()
