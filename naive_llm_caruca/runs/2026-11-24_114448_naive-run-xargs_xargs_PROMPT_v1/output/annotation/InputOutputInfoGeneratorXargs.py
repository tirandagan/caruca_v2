from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorXargs(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-0", "-e", "-i", "-l", "-o", "-p", "-r", "--show-limits", "-t", "-x",
    #                      "--help", "--version"]
    # list_of_all_options = ["-a", "-d", "-E", "-I", "-L", "-n", "-P", "--process-slot-var", "-s"]

    # Which ones do affect input/output?
    # the operands are COMMAND and INITIAL-ARGS, never files xargs itself reads or writes
    # -a FILE: items are read from FILE (typed STREAM_INPUT in the parser table) instead of stdin;
    #          stdin is then left untouched and inherited by the child processes
    # otherwise: items are read from stdin and the children get stdin redirected from /dev/null
    # stdout is only written by the executed command (and by --help/--version/--show-limits);
    # since the command is arbitrary, we over-approximate and always claim stdout is used
    # -t and -p write to stderr/tty only; -o reopens the child's stdin as /dev/tty

    def generate_info(self) -> None:
        # command and initial-arguments are values, not files
        self.set_all_operands_as_config_arg_type_string()
        if not self.does_flag_option_list_contain_at_least_one_of(["-a", "--arg-file"]):
            self.set_implicit_use_of_stdin()
        # assumption: the executed command (default echo) writes its result to stdout
        self.set_implicit_use_of_stdout()
