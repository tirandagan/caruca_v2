from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorChgrp(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-f", "-v", "--dereference", "-h", "--no-preserve-root", "--preserve-root",
    #                      "-R", "-H", "-L", "-P", "--help", "--version"]
    # list_of_all_options = ["--reference"]

    # Which ones do affect input/output?
    # --reference: the group is taken from RFILE (already typed as CONFIG_INPUT by the parser table)
    #              and there is no GROUP operand, so every operand is a FILE
    # without --reference: the first operand is the GROUP (a name or numeric gid), the rest are FILEs
    # -c and -v write diagnostics to stdout; nothing is ever read from stdin
    # -R only changes which files below the operands are affected, not what the operands are
    # FILEs are modified in-place (metadata only), so they are "other outputs" like for rm/chmod

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-c", "-v"]):
            self.set_implicit_use_of_stdout()
        # FILEs are modified in place; set this first so the GROUP operand can be re-typed afterwards
        self.all_operands_are_other_outputs()
        if not self.does_flag_option_list_contain_at_least_one_of(["--reference"]):
            self.set_first_operand_as_config_arg_type_string()
