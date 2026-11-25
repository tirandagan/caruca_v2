from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorIconv(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-l", "-c", "-s", "--verbose", "-?", "--usage", "-V"]
    # list_of_all_options = ["-f", "-t", "-o"]

    # Which ones do affect input/output?
    # -l, -?/--help, --usage, -V: print information to stdout, operands are ignored (verified: `iconv -l FILE`
    #   does not touch FILE)
    # -o FILE: output goes to FILE instead of stdout (typed STREAM_OUTPUT in the parser table);
    #   `-o -` means stdout, which we cannot distinguish here and therefore over-approximate as a file
    # -c, -s, --verbose, -f, -t: do not change which files are read or written
    #   (--verbose prints file names to stderr only)
    # operands: every FILE is read in sequence as the data stream; `-` is stdin; no operands means stdin

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-l", "--list", "-?", "--help", "--usage", "-V", "--version"]):
            # informational modes: nothing is read, operands are ignored
            self.set_all_operands_as_config_arg_type_string()
            self.set_implicit_use_of_stdout()
            return
        if not self.does_flag_option_list_contain_at_least_one_of(["-o", "--output"]):
            self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
