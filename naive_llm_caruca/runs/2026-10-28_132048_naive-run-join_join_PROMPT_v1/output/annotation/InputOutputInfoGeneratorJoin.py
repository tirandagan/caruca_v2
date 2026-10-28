from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorJoin(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-i", "--check-order", "--nocheck-order", "--header", "-z", "--help", "--version"]
    # list_of_all_options = ["-a", "-e", "-j", "-o", "-t", "-v", "-1", "-2"]

    # Which ones do affect input/output?
    # none: join always reads exactly two operands (FILE1 FILE2) as streams and writes to stdout;
    # a '-' operand (at most one of the two) means stdin, which the operand handling covers.
    # assumption that version/help not provided

    def generate_info(self) -> None:
        # tested with the binary: fewer or more than two operands is an error
        if self.get_operand_list_length() != 2:
            raise Exception('join requires exactly two operands (FILE1 FILE2)')
        self.all_operands_are_streaming_inputs()
        self.set_implicit_use_of_stdout()
