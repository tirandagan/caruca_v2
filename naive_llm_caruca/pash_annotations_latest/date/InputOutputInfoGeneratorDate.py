from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorDate(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--debug", "-I", "--resolution", "-R", "-u", "--help", "--version"]
    # list_of_all_options = ["-d", "-f", "--rfc-3339", "-r", "-s"]

    # Which ones do affect input/output?
    # date never reads a data stream from stdin and never writes to a file: the result always goes to stdout.
    # -f DATEFILE reads one date string per line of DATEFILE (CONFIG_INPUT, typed via date.json);
    #   `-f -` reads those lines from stdin (verified against coreutils 9.4).
    # -r FILE only reads FILE's modification time (OTHER_INPUT, typed via date.json); `-r -` is a literal filename.
    # -s STRING (and the bare MMDDhhmm[[CC]YY][.ss] operand) set the system clock, a side effect
    #   that is not a file input/output and is not modelled here.
    # The operands (+FORMAT, or the MMDDhhmm... string) are values, not files.

    def generate_info(self) -> None:
        # assumption that --help/--version not provided
        self.set_implicit_use_of_stdout()
        self.set_all_operands_as_config_arg_type_string()
        if self.does_file_option_read_stdin():
            self.set_implicit_use_of_stdin()

    def does_file_option_read_stdin(self) -> bool:
        for flag_option in self.get_flag_option_list_filtered_with(["-f", "--file"]):
            if self.option_argument_as_string(flag_option) == "-":
                return True
        return False

    @staticmethod
    def option_argument_as_string(option) -> str:
        arg = option.get_arg() if hasattr(option, "get_arg") else getattr(option, "option_arg", None)
        if arg is None:
            return ""
        if hasattr(arg, "get_name"):
            return str(arg.get_name())
        return str(arg)
