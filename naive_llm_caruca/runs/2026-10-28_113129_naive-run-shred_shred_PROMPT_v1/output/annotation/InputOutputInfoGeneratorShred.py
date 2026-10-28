from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorShred(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-f", "-u", "-v", "-x", "-z", "--help", "--version"]
    # list_of_all_options = ["-n", "--random-source", "-s", "--remove"]

    # Which ones do affect input/output?
    # shred never reads its operands as data; it overwrites them in place (and with -u/--remove
    # also unlinks them), so every operand is an "other" output.
    # --random-source=FILE is a configuration input and is already typed by the parser table.
    # An operand of "-" means standard output is overwritten (not standard input read).
    # -v writes progress to stderr only, which does not affect stdout.

    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()
        for operand in self.cmd_inv.operand_list:
            if getattr(operand, "name", str(operand)) == "-":
                self.set_implicit_use_of_stdout()
                break
