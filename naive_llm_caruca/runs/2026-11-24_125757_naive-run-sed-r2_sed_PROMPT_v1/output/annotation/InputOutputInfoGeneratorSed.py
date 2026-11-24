from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSed(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--debug", "--follow-symlinks", "-i", "--posix", "-E", "-r", "-s", "--sandbox",
    #                      "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["-e", "-f", "-l"]

    # Which ones do affect input/output?
    # -e/-f: the script comes from the option, so every operand is an input file
    #        (otherwise the first operand is the script); -f names a config file (typed in sed.json)
    # -i:    files are rewritten in place; nothing is written to stdout and stdin is never read
    #        (`sed -i script` without files is an error: "no input files")
    # -s only changes how the inputs are delimited, not which they are
    # not modelled: `w`/`W` commands and the `w` flag of `s` write extra files, `r`/`R` read extra files,
    #               `e` runs shell commands, `-f -` reads the script from stdin; --help/--version assumed absent

    def generate_info(self) -> None:
        in_place = self.does_flag_option_list_contain_at_least_one_of(["-i", "--in-place"])
        script_given_by_option = self.does_flag_option_list_contain_at_least_one_of(["-e", "--expression", "-f", "--file"])

        if in_place:
            # the operands are read and then replaced by the edited result
            self.all_operands_are_other_outputs()
            if not script_given_by_option:
                self.set_first_operand_as_config_arg_type_string()
            return

        self.set_implicit_use_of_stdout()
        if script_given_by_option:
            if self.get_operand_list_length() == 0:
                self.set_implicit_use_of_stdin()
            else:
                self.all_operands_are_streaming_inputs()
        else:
            self.set_first_operand_as_config_arg_type_string()
            if self.get_operand_list_length() <= 1:
                self.set_implicit_use_of_stdin()
            else:
                self.all_but_first_operand_is_streaming_input()
