from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorCp(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(['-t', '--target-directory']):
            self.all_operands_are_other_inputs()
        else:
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
