from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorUname(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-s", "-n", "-r", "-v", "-m", "-p", "-i", "-o", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none: uname never reads stdin or any file, takes no operands
    # (an operand is an error), and always writes to stdout.

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
