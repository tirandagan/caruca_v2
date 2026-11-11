from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorGrep(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(['-q']):
            self.set_implicit_use_of_stdout()
        patterns_from_options = self.does_flag_option_list_contain_at_least_one_of(['-e', '-f'])
        if patterns_from_options:
            number_of_file_operands = self.get_operand_list_length()
            self.all_operands_are_streaming_inputs()
        else:
            number_of_file_operands = self.get_operand_list_length() - 1
            if self.get_operand_list_length() >= 1:
                self.set_first_operand_as_config_arg_type_string()
            if number_of_file_operands >= 1:
                self.all_but_first_operand_is_streaming_input()
        if number_of_file_operands <= 0 and (not self.is_recursive()):
            self.set_implicit_use_of_stdin()
        if '-' in self.option_arguments_of('-f'):
            self.set_implicit_use_of_stdin()

    def is_recursive(self) -> bool:
        if self.does_flag_option_list_contain_at_least_one_of(['-r', '-R']):
            return True
        return 'recurse' in self.option_arguments_of('-d')

    def option_arguments_of(self, option_name: str) -> list:
        arguments = []
        for flag_option in self.get_flag_option_list_filtered_with([option_name]):
            argument = getattr(flag_option, 'option_arg', None)
            if argument is None and hasattr(flag_option, 'get_arg'):
                argument = flag_option.get_arg()
            if argument is None:
                continue
            if hasattr(argument, 'get_name'):
                argument = argument.get_name()
            arguments.append(str(argument))
        return arguments
