from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorWc(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        flags = {str(fo.get_name()) for fo in self.cmd_inv.flag_option_list}
        n = self.get_operand_list_length()
        if n == 0 and flags in ({'-c', '-l'}, {'-c'}, {'-l'}, set()):
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
        else:
            self.input_output_info = None
