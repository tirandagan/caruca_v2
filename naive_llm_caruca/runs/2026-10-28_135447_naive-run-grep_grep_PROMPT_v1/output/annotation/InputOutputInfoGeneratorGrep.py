from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorGrep(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "-V", "-E", "-F", "-G", "-P", "-i", "-y", "--no-ignore-case", "-v", "-w",
    #                      "-x", "-c", "--color", "-L", "-l", "-o", "-q", "-s", "-b", "-u", "-H", "-h", "-n",
    #                      "-T", "-Z", "--no-group-separator", "-a", "-I", "-r", "-R", "--line-buffered",
    #                      "-U", "-z"]
    # list_of_all_options = ["-e", "-f", "-m", "--label", "-A", "-B", "-C", "--group-separator",
    #                        "--binary-files", "-D", "-d", "--include", "--exclude", "--exclude-from",
    #                        "--exclude-dir"]

    # Which ones do affect input/output?  (checked against GNU grep 3.11)
    # -q: nothing is written to stdout
    # -e / -f: the PATTERNS operand disappears, every operand is a FILE
    # -f - : patterns are read from stdin (the parser table already types -f FILE as CONFIG_INPUT)
    # -r / -R / -d recurse: with no FILE operand grep searches "." instead of reading stdin
    # --help / -V print to stdout and read nothing; we assume they are not given
    # --include, --exclude, --exclude-from, --exclude-dir only filter the files already named,
    # so ignoring them over-approximates the inputs
    # -D / -d skip likewise only drop some named files

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-q"]):
            self.set_implicit_use_of_stdout()

        patterns_from_options = self.does_flag_option_list_contain_at_least_one_of(["-e", "-f"])
        if patterns_from_options:
            number_of_file_operands = self.get_operand_list_length()
            self.all_operands_are_streaming_inputs()  # also fine when there are none
        else:
            number_of_file_operands = self.get_operand_list_length() - 1
            if self.get_operand_list_length() >= 1:
                self.set_first_operand_as_config_arg_type_string()
            if number_of_file_operands >= 1:
                self.all_but_first_operand_is_streaming_input()

        if number_of_file_operands <= 0 and not self.is_recursive():
            # no FILE: grep reads stdin ("-"); when recursive it reads "." instead,
            # which we cannot express as an operand, so no input is recorded then
            self.set_implicit_use_of_stdin()

        if "-" in self.option_arguments_of("-f"):
            self.set_implicit_use_of_stdin()

    def is_recursive(self) -> bool:
        if self.does_flag_option_list_contain_at_least_one_of(["-r", "-R"]):
            return True
        return "recurse" in self.option_arguments_of("-d")

    def option_arguments_of(self, option_name: str) -> list:
        """The argument texts of every occurrence of the named option."""
        arguments = []
        for flag_option in self.get_flag_option_list_filtered_with([option_name]):
            argument = getattr(flag_option, "option_arg", None)
            if argument is None and hasattr(flag_option, "get_arg"):
                argument = flag_option.get_arg()
            if argument is None:
                continue  # a bare flag, not an option
            if hasattr(argument, "get_name"):
                argument = argument.get_name()
            arguments.append(str(argument))
        return arguments
