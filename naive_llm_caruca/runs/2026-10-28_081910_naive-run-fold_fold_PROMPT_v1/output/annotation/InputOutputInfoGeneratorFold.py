from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorFold(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-s", "--help", "--version"]
    # list_of_all_options = ["-w"]

    # Which ones do affect input/output?
    # none; only the number of operands matters:
    # fold reads every FILE operand (or stdin if none / "-") and always writes to stdout
    # assumption that --help/--version not provided

    def generate_info(self) -> None:
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
        self.set_implicit_use_of_stdout()
