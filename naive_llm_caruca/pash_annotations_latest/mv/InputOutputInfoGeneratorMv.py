from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMv(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "--debug", "-f", "-i", "-n", "--no-copy", "--strip-trailing-slashes",
    #                      "-T", "-u", "-v", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "-S", "-t", "--update"]

    # Which ones do affect input/output?
    # -t/--target-directory: the destination is given as an option argument (typed OTHER_OUTPUT via
    #   mv.json) and *all* operands are sources
    # otherwise the last operand is the destination (a file or a directory) and the rest are sources
    # sources are consumed (renamed away or copied and unlinked), i.e. read in a non-streaming way
    # -v/--debug print what is done to stdout
    # -i reads confirmations from stdin, but only when a destination exists; we ignore it
    # --backup/-b additionally create backup files next to the destination; they are not operands

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-v", "--debug"]):
            self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["-t"]):
            self.all_operands_are_other_inputs()
        else:
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
