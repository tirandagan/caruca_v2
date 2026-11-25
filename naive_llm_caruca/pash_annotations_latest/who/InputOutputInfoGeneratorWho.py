from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorWho(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-b", "-d", "-H", "-l", "--lookup", "-m", "-p", "-q", "-r", "-s", "-t",
    #                      "-T", "-u", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # only the number of operands and -m
    #
    # who [OPTION]... [ FILE | ARG1 ARG2 ]
    # - no operand:   reads the utmp database /var/run/utmp, writes to stdout
    # - one operand:  FILE is a utmp/wtmp database read whole (binary records, not a line stream);
    #                 a lone '-' is opened as a literal file name, not stdin (checked with strace)
    # - two operands: 'am i' style; the words are ignored and -m is presumed, /var/run/utmp is read
    # - three or more operands: "who: extra operand", exit 1
    #
    # who never reads data from stdin.  With -m (or two operands) it calls ttyname() on fd 0 to find
    # the current terminal, so its output does depend on what stdin is connected to; we record that
    # as an implicit use of stdin so stdin is not re-routed from under it.

    def generate_info(self) -> None:
        # assumption that version/help not provided
        if self.get_operand_list_length() == 0:
            pass
        elif self.get_operand_list_length() == 1:
            self.all_operands_are_other_inputs()
        elif self.get_operand_list_length() == 2:
            self.set_all_operands_as_config_arg_type_string()
        else:
            raise Exception('extra operand for who, the 3rd one')
        if self.get_operand_list_length() == 2 or self.does_flag_option_list_contain_at_least_one_of(["-m"]):
            self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
