from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorLn(InputOutputInfoGeneratorInterface):

    # ln [-T] TARGET LINK_NAME   -> TARGET read, LINK_NAME created
    # ln TARGET                  -> link created in the current directory
    # ln TARGET... DIRECTORY     -> links created inside DIRECTORY
    # ln -t DIRECTORY TARGET...  -> DIRECTORY comes from the option table

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-t", "--target-directory"]):
            # the destination is the -t argument, already typed as OTHER_OUTPUT
            self.all_operands_are_other_inputs()
        elif self.get_operand_list_length() == 1:
            # link is created under the same name in the current directory
            self.all_operands_are_other_inputs()
        else:
            # last operand is LINK_NAME or DIRECTORY, either way written to
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
        if self.does_flag_option_list_contain_at_least_one_of(["-i", "--interactive"]):
            # prompts on stdin before replacing an existing destination
            self.set_implicit_use_of_stdin()
        if self.does_flag_option_list_contain_at_least_one_of(["-v", "--verbose"]):
            self.set_implicit_use_of_stdout()
