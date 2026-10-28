from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorShuf(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-e", "-r", "-z", "--help", "--version"]
    # list_of_all_options = ["-i", "-n", "-o", "--random-source"]

    # Which ones do affect input/output?
    # -e: the operands are literal strings (the lines to permute), not files; stdin is not read
    # -i: the input is a numeric range; no operands are allowed and stdin is not read
    # -o: the result goes to FILE instead of stdout (FILE typed STREAM_OUTPUT via the parser table);
    #     "-o -" still writes to stdout (tested)
    # --random-source: a file read for random bytes (typed OTHER_INPUT via the parser table)
    # -n, -r, -z do not change what is read or written
    # without -e/-i: at most one FILE operand ("extra operand" otherwise); none or "-" means stdin

    def generate_info(self) -> None:
        # assumption that --help/--version not provided
        if self.does_flag_option_list_contain_at_least_one_of(["-e"]):
            # each ARG is an input line, not a file
            self.set_all_operands_as_config_arg_type_string()
        elif self.does_flag_option_list_contain_at_least_one_of(["-i"]):
            if self.get_operand_list_length() > 0:
                raise Exception('extra operand for shuf with -i')
        else:
            if self.get_operand_list_length() > 1:
                raise Exception('extra operand for shuf, the 2nd one')
            # a FILE operand of "-" is stdin as well; it is left to the generic operand handling
            if self.get_operand_list_length() == 0:
                self.set_implicit_use_of_stdin()
            else:
                self.all_operands_are_streaming_inputs()
        # output: stdout unless redirected with -o FILE (and -o - is stdout again)
        if not self.does_flag_option_list_contain_at_least_one_of(["-o"]) \
                or self._is_output_option_dash():
            self.set_implicit_use_of_stdout()

    def _is_output_option_dash(self) -> bool:
        # "-o -" / "--output -" means standard output; the option argument is the only place to see it
        for flag_option in self.get_flag_option_list_filtered_with(["-o"]):
            arg = getattr(flag_option, "option_arg", None)
            name = getattr(arg, "name", None)
            if name is None:
                name = getattr(arg, "get_name", lambda: str(arg))()
            if str(name) == "-":
                return True
        return False
