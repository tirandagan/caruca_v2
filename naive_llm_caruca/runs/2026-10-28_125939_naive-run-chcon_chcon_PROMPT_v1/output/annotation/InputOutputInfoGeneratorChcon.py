from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorChcon(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--dereference", "-h", "--no-preserve-root", "--preserve-root", "-R", "-v",
    #                      "-H", "-L", "-P", "--help", "--version"]
    # list_of_all_options = ["-u", "-r", "-t", "-l", "--reference"]

    # chcon never reads stdin and never writes a data stream; it changes the SELinux
    # context (metadata) of every FILE operand, so all FILE operands are "other outputs".
    # Which ones do affect input/output?
    # -u/-r/-t/-l/--reference decide how the operands are interpreted:
    #   without any of them, the first operand is the CONTEXT string and the rest are FILEs;
    #   with at least one of them, every operand is a FILE.
    # --reference=RFILE reads RFILE's context (typed as OTHER_INPUT via chcon.json).
    # -v prints a diagnostic per processed file to stdout; nothing else is written to stdout
    #   (--help/--version also write to stdout but we assume they are not used).
    # -R/-H/-L/-P/-h/--dereference only change which files below the operands are affected;
    #   we over-approximate by reporting the operands themselves as outputs.

    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()
        if not self.does_flag_option_list_contain_at_least_one_of(["-u", "-r", "-t", "-l", "--reference"]):
            # first form: chcon [OPTION]... CONTEXT FILE...
            self.set_first_operand_as_config_arg_type_string()
        if self.does_flag_option_list_contain_at_least_one_of(["-v"]):
            self.set_implicit_use_of_stdout()
