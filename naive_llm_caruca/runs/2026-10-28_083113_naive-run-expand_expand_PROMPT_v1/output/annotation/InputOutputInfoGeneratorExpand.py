from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorExpand(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-i", "--help", "--version"]
    # list_of_all_options = ["-t"]

    # Which ones do affect input/output?
    # none; only the number of operands matters
    # (--help and --version produce no actual result, we assume they are not given)

    def generate_info(self) -> None:
        # tested with the command: all FILE operands are read in order and the
        # converted text is written to stdout; with no FILE (or FILE being -),
        # stdin is read instead
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
        self.set_implicit_use_of_stdout()
