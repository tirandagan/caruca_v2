from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorSort(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(['--files0-from']):
            pass
        else:
            self.if_no_operands_given_stdin_implicitly_used()
            self.all_operands_are_streaming_inputs()
        if self.does_flag_option_list_contain_at_least_one_of(['-c', '-C', '--check']):
            pass
        elif self.does_flag_option_list_contain_at_least_one_of(['-o', '--output']):
            pass
        else:
            self.set_implicit_use_of_stdout()
