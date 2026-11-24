import re

from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


# an operand of the form var=val is a variable assignment, not an input file
_ASSIGNMENT_OPERAND = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


def _operand_as_string(operand) -> str:
    if hasattr(operand, "get_name_as_string"):
        return str(operand.get_name_as_string())
    return str(operand)


class InputOutputInfoGeneratorAwk(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "-C", "-d", "-D", "-g", "-h", "-I", "-L", "-M", "-N", "-n", "-o",
    #                      "-O", "-p", "-P", "-r", "-s", "-S", "-t", "-V"]
    # list_of_all_options = ["-f", "-F", "-v", "-e", "-E", "-i", "-l", "-W"]

    # Which ones do affect input/output?
    # -f, -e, -E: the program comes from the option, so the first operand is an input file rather
    #             than the program text (-f - reads the program from stdin; not detected here)
    # -h, -V, -C: print to stdout and exit, nothing is read
    # -g: the program is parsed but not run; a .pot file goes to stdout, no input is read
    # -D: the debugger reads its commands from stdin (unless -Dfile)
    # -d, -o, -p: additionally write awkvars.out / awkprof.out (or the attached file name) in the
    #             current directory; these outputs cannot be expressed through the operands
    # the program itself may read further files (getline < file) and write files (print > file);
    # these are invisible here and over-approximated as not present
    # var=val operands are assignments and not files; they are reported as streaming inputs since
    # the interface cannot mark a single non-first operand as configuration (over-approximation)

    def generate_info(self) -> None:
        # help/version/copyright: immediate exit after writing to stdout
        if self.does_flag_option_list_contain_at_least_one_of(["-h", "--help", "-V", "--version", "-C", "--copyright"]):
            self.set_implicit_use_of_stdout()
            self.set_all_operands_as_config_arg_type_string()
            return

        program_given_by_option = self.does_flag_option_list_contain_at_least_one_of(["-f", "-e", "-E"])

        # --gen-pot: program is only parsed, no input is processed
        if self.does_flag_option_list_contain_at_least_one_of(["-g", "--gen-pot"]):
            self.set_implicit_use_of_stdout()
            self.set_all_operands_as_config_arg_type_string()
            return

        if not program_given_by_option and self.get_operand_list_length() == 0:
            # no program at all: awk prints its usage to stderr and exits
            return

        self.set_implicit_use_of_stdout()

        if program_given_by_option:
            self.all_operands_are_streaming_inputs()
            file_operands = self.cmd_inv.operand_list
        else:
            self.set_first_operand_as_config_arg_type_string()
            self.all_but_first_operand_is_streaming_input()
            file_operands = self.cmd_inv.operand_list[1:]

        # stdin is read when no operand names an input file (assignments do not count)
        if not any(not _ASSIGNMENT_OPERAND.match(_operand_as_string(op)) for op in file_operands):
            self.set_implicit_use_of_stdin()

        # the debugger takes its commands from stdin
        if self.does_flag_option_list_contain_at_least_one_of(["-D", "--debug"]):
            self.set_implicit_use_of_stdin()
