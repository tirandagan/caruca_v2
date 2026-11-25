from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorDirname(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-z", "--zero", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none: dirname is a pure string transformation of its operands.
    # Tested with the binary (coreutils 9.4):
    #   - operands are never opened; nonexistent paths and "-" are processed as plain text
    #   - stdin is never read (with no operands it fails with "missing operand", even if stdin has data)
    #   - one line (or NUL-terminated record with -z) per operand is written to stdout
    # assumption that --help/--version are not provided

    def generate_info(self) -> None:
        self.set_all_operands_as_config_arg_type_string()
        self.set_implicit_use_of_stdout()
