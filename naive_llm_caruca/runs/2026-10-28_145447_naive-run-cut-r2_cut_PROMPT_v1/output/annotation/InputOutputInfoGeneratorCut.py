from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCut(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter"]

    # Which ones do affect input/output?
    # none: every operand is a file read as a stream (a lone "-" is stdin),
    # with no operands stdin is read, and the result always goes to stdout.
    # -d, -f, -b, -c and --output-delimiter take plain values, not files.

    def generate_info(self) -> None:
        # assumption that version/help not provided
        self.all_operands_are_streaming_inputs()
        self.if_no_operands_given_stdin_implicitly_used()
        self.set_implicit_use_of_stdout()
