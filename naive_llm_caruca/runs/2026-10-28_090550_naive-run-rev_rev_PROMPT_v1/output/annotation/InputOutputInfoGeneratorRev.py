from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorRev(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-0", "-h", "-V"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # only the number of operands; -h and -V print to stdout and read nothing
    # (assumption, as in the other annotations: help/version not provided)

    def generate_info(self) -> None:
        # rev copies the operand files (or stdin if none) to stdout, reversing each line.
        # Tested: a lone "-" operand is NOT stdin, rev tries to open a file named "-".
        self.all_operands_are_streaming_inputs()
        self.if_no_operands_given_stdin_implicitly_used()
        self.set_implicit_use_of_stdout()
