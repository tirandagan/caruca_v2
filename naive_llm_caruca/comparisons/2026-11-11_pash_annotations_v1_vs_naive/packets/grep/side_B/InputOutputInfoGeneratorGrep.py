from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorGrep(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(['-q', '--quiet', '--silent']):
            self.set_implicit_use_of_stdout()
        recursive = self.does_flag_option_list_contain_at_least_one_of(['-r', '--recursive', '-R', '--dereference-recursive'])
        if self.does_flag_option_list_contain_at_least_one_of(['-e', '--regexp', '-f', '--file']):
            number_of_files = self.get_operand_list_length()
            self.all_operands_are_streaming_inputs()
        else:
            self.set_first_operand_as_config_arg_type_string()
            number_of_files = self.get_operand_list_length() - 1
            self.all_but_first_operand_is_streaming_input()
        if number_of_files <= 0 and (not recursive):
            self.set_implicit_use_of_stdin()
