from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTee(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-i", "-p", "--help", "--version"]
    # list_of_all_options = ["--output-error"]

    # tee always reads stdin (there is no operand that names an input) and
    # always writes the same data to stdout.  Every FILE operand is an output
    # that receives a copy of the stream; there may be none.  A lone "-" is a
    # regular file called "-", not stdout.  None of the flags change which
    # arguments are inputs or outputs: -a only switches truncate to append,
    # -i / -p / --output-error only affect signal and write-error handling.

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdin()
        # copies to both operands and stdout
        self.set_implicit_use_of_stdout()
        self.all_operands_are_streaming_outputs()
