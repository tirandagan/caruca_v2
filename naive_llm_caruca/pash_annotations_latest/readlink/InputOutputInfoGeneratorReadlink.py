from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorReadlink(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-f", "-e", "-m", "-n", "-q", "-s", "-v", "-z", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none: every operand is a path whose link target or canonical name is looked up
    # (lstat/readlink/realpath), never opened and read as a data stream;
    # a lone "-" is an ordinary file name, stdin is never read;
    # the result for each operand is written to stdout (nothing is ever written to a file)

    def generate_info(self) -> None:
        # --help and --version print to stdout without touching operands, but we assume no help/version
        self.set_implicit_use_of_stdout()
        self.all_operands_are_other_inputs()
