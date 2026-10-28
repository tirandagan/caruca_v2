from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCat(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "-n", "-s", "-t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none: every flag only changes how the lines are rendered on stdout;
    # only the number of operands matters (no FILE, or FILE being -, means stdin)
    # assumption that version/help not provided

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
