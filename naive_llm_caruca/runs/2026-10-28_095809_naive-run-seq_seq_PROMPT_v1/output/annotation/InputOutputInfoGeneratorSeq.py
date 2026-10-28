from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSeq(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-w", "--help", "--version"]
    # list_of_all_options = ["-f", "-s"]

    # Which ones do affect input/output?
    # none: seq never reads standard input or any file, and always writes
    # its sequence to standard output (assuming no --help/--version)

    def generate_info(self) -> None:
        # operands are the numbers LAST / FIRST LAST / FIRST INCREMENT LAST,
        # i.e. configuration values rather than files
        self.set_all_operands_as_config_arg_type_string()
        self.set_implicit_use_of_stdout()
