from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorCut(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        flags = {str(fo.get_name()) for fo in self.cmd_inv.flag_option_list}
        n = self.get_operand_list_length()
        if n == 0 and flags in ({'--complement', '--help'}, {'--complement', '--version'}, {'--help', '--output-delimiter'}, {'--help', '--version'}, {'--help', '-b'}, {'--help', '-c'}, {'--help', '-d'}, {'--help', '-f'}, {'--help', '-n'}, {'--help', '-s'}, {'--help', '-z'}, {'--output-delimiter', '--version'}, {'--version', '-b'}, {'--version', '-c'}, {'--version', '-d'}, {'--version', '-f'}, {'--version', '-n'}, {'--version', '-s'}, {'--version', '-z'}, {'--help'}, {'--version'}):
            self.set_implicit_use_of_stdout()
        elif n == 0 and flags in ({'--complement', '-b'}, {'--complement', '-c'}, {'--complement', '-f'}, {'--output-delimiter', '-b'}, {'--output-delimiter', '-c'}, {'--output-delimiter', '-f'}, {'-b', '-n'}, {'-b', '-z'}, {'-c', '-n'}, {'-c', '-z'}, {'-d', '-f'}, {'-f', '-n'}, {'-f', '-s'}, {'-f', '-z'}, {'-b'}, {'-c'}, {'-f'}):
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
        elif n == 1 and flags in ({'--help'}, {'--version'}):
            self.set_all_operands_as_arg_string()
            self.set_implicit_use_of_stdout()
        elif n == 1 and flags in ({'-b'}, {'-c'}, {'-f'}):
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
        else:
            self.input_output_info = None
