from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorHead(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect input/output?
    # only the number of operands; the options merely change how much of each
    # input is printed and whether file-name headers are emitted
    # (tested: `head a b` reads both, `head` and `head -` read stdin,
    #  output always goes to stdout)

    def generate_info(self) -> None:
        # assumption that version/help not provided
        self.set_implicit_use_of_stdout()
        if self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
        else:
            # a '-' operand is standard input; the operand handling of the
            # framework treats it as a standard descriptor
            self.all_operands_are_streaming_inputs()
