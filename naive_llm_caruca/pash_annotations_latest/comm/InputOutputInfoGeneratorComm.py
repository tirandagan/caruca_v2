from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorComm(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-1", "-2", "-3", "--check-order", "--nocheck-order", "--total", "-z", "--help", "--version"]
    # list_of_all_options = ["--output-delimiter"]

    # Which ones do affect input/output?
    # none of the flags/options; only the operands matter.
    # comm always takes exactly two operands, FILE1 and FILE2, both read as
    # sorted line streams; the result always goes to stdout.
    # Either operand (but not both) may be "-" meaning stdin; tested with
    # coreutils 9.4: "comm - -" fails with "Bad file descriptor".
    # 0, 1 or 3+ operands are an error ("missing operand" / "extra operand").

    def generate_info(self) -> None:
        # assumption that version/help not provided
        if self.get_operand_list_length() == 2:
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
        else:
            raise Exception('comm requires exactly two operands (FILE1 FILE2)')
