from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTouch(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-c", "-f", "-h", "-m", "--help", "--version"]
    # list_of_all_options = ["-d", "-r", "-t", "--time"]

    # Which ones do affect input/output?
    # -r FILE is read (its timestamps are copied) and is already typed as OTHER_INPUT by the parser table
    # none of the flags change what is read or written: every FILE operand is created or has its
    # timestamps changed, nothing is read from and no data is streamed to any operand
    # a FILE operand of "-" means the file behind standard output

    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()
        for operand in self.cmd_inv.operand_list:
            name = operand.get_name() if hasattr(operand, "get_name") else str(operand)
            if name == "-":
                self.set_implicit_use_of_stdout()
                break
