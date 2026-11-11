from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorRm(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        flags = {str(fo.get_name()) for fo in self.cmd_inv.flag_option_list}
        n = self.get_operand_list_length()
        if n == 1 and flags in ({'--help', '--interactive'}, {'--help', '--no-preserve-root'}, {'--help', '--one-file-system'}, {'--help', '--preserve-root'}, {'--help', '--version'}, {'--help', '-I'}, {'--help', '-d'}, {'--help', '-f'}, {'--help', '-i'}, {'--help', '-r'}, {'--help', '-v'}, {'--interactive', '--version'}, {'--no-preserve-root', '--version'}, {'--one-file-system', '--version'}, {'--preserve-root', '--version'}, {'--version', '-I'}, {'--version', '-d'}, {'--version', '-f'}, {'--version', '-i'}, {'--version', '-r'}, {'--version', '-v'}, {'--help'}, {'--version'}):
            self.set_all_operands_as_arg_string()
            self.set_implicit_use_of_stdout()
        elif n == 1 and flags in ({'--interactive', '--no-preserve-root'}, {'--interactive', '--one-file-system'}, {'--interactive', '--preserve-root'}, {'--interactive', '-I'}, {'--interactive', '-d'}, {'--interactive', '-f'}, {'--interactive', '-i'}, {'--interactive', '-r'}, {'--no-preserve-root', '--one-file-system'}, {'--no-preserve-root', '--preserve-root'}, {'--no-preserve-root', '-I'}, {'--no-preserve-root', '-d'}, {'--no-preserve-root', '-f'}, {'--no-preserve-root', '-r'}, {'--one-file-system', '--preserve-root'}, {'--one-file-system', '-I'}, {'--one-file-system', '-d'}, {'--one-file-system', '-f'}, {'--one-file-system', '-r'}, {'--preserve-root', '-I'}, {'--preserve-root', '-d'}, {'--preserve-root', '-f'}, {'--preserve-root', '-r'}, {'-I', '-d'}, {'-I', '-f'}, {'-I', '-i'}, {'-d', '-f'}, {'-d', '-r'}, {'-f', '-r'}, {'--interactive'}, {'--no-preserve-root'}, {'--one-file-system'}, {'--preserve-root'}, {'-I'}, {'-d'}, {'-f'}, {'-r'}, set()):
            self.all_operands_are_other_outputs()
        elif n == 1 and flags in ({'--interactive', '-v'}, {'--no-preserve-root', '-v'}, {'--one-file-system', '-v'}, {'--preserve-root', '-v'}, {'-I', '-v'}, {'-d', '-v'}, {'-f', '-v'}, {'-r', '-v'}, {'-v'}):
            self.all_operands_are_other_outputs()
            self.set_implicit_use_of_stdout()
        else:
            self.input_output_info = None
