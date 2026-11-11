from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorRm(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()
        if self.does_flag_option_list_contain_at_least_one_of(['-v', '--help', '--version']):
            self.set_implicit_use_of_stdout()
