from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCut(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter"]

    # Which ones do affect input/output?
    # none: the option arguments are lists of ranges or delimiter strings, never files;
    # exactly one of -b/-c/-f is required, otherwise cut exits with an error
    # (assumption that --help/--version are not provided)

    def generate_info(self) -> None:
        # tested with the binary: every operand is read as a stream, "-" is stdin,
        # no operands means stdin, output always goes to stdout
        self.all_operands_are_streaming_inputs()
        self.if_no_operands_given_stdin_implicitly_used()
        self.set_implicit_use_of_stdout()
