from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSed(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--debug", "--follow-symlinks", "-i", "--posix", "-E", "-r", "-s",
    #                      "--sandbox", "-u", "-z", "-b", "--help", "--version"]
    # list_of_all_options = ["-e", "-f", "-l"]

    # Which ones do affect input/output?
    # -e/-f decide whether the first operand is the script or an input file
    # -f names a file that is read as configuration (handled by the parser table)
    # -i rewrites every input file in place and prints nothing to stdout
    # the script itself may read (r/R) or write (w/W, s///w) files; we cannot see those
    # files from the invocation alone and, thus, under-approximate for such scripts
    # -s and -z do not change which files are touched

    def generate_info(self) -> None:
        # assumption that version/help not provided
        in_place = self.does_flag_option_list_contain_at_least_one_of(["-i", "--in-place"])
        if not in_place:
            self.set_implicit_use_of_stdout()
        # case analysis how script is provided
        if self.does_flag_option_list_contain_at_least_one_of(["-e", "--expression", "-f", "--file"]):
            if self.get_operand_list_length() == 0:
                if in_place:
                    raise Exception("sed -i without input files is an error (\"no input files\")")
                self.set_implicit_use_of_stdin()
            elif in_place:
                # files are read and then replaced by a new file with the same name
                self.all_operands_are_other_outputs()
            else:
                self.all_operands_are_streaming_inputs()
        else:
            self.set_first_operand_as_config_arg_type_string()
            if self.get_operand_list_length() == 1:
                if in_place:
                    raise Exception("sed -i without input files is an error (\"no input files\")")
                self.set_implicit_use_of_stdin()
            elif in_place:
                # no "all but first is other output" helper exists; the files are
                # replaced in place, so an output is the closest available marking
                self.all_but_first_operand_is_streaming_output()
            else:
                self.all_but_first_operand_is_streaming_input()
