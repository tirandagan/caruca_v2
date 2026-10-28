from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCut(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter"]

    # Which ones do affect input/output?
    # none: every operand is a file read as a stream (a lone "-" is stdin),
    # stdin is read only when no operand is given, and the result always goes to stdout.
    # --help and --version print to stdout without reading anything; as in the other
    # annotations we assume they are not given.

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
