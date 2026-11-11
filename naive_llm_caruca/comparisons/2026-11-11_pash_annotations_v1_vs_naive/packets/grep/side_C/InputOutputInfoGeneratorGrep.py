from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.AccessKind import make_other_input
from pash_annotations.datatypes.BasicDatatypes import FileName
from pash_annotations.datatypes.BasicDatatypesWithIO import get_from_original_filename_with_ioinfo

class InputOutputInfoGeneratorGrep(InputOutputInfoGeneratorInterface):
    QUIET_FLAGS = ['-q', '--quiet', '--silent']
    PATTERN_OPTIONS = ['-e', '--regexp', '-f', '--file']
    DIRECTORY_OPTIONS = ['-d', '--directories']
    RECURSIVE_FLAGS = ['-r', '-R', '--recursive', '--dereference-recursive']
    DIRECTORY_ACTIONS = ['read', 'skip', 'recurse']

    def generate_info(self) -> None:
        if self.has_unrecognised_option():
            raise Exception('grep option not recognised by the parser table')
        if not self.does_flag_option_list_contain_at_least_one_of(self.QUIET_FLAGS):
            self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(self.PATTERN_OPTIONS):
            first_file_index = 0
        elif self.get_operand_list_length() > 0:
            self.set_first_operand_as_config_arg_type_string()
            first_file_index = 1
        else:
            return
        if self.is_recursive():
            if first_file_index == 1:
                self.all_but_first_operand_is_other_input()
            else:
                self.all_operands_are_other_inputs()
        if self.get_operand_list_length() == first_file_index:
            if self.is_recursive():
                directory = get_from_original_filename_with_ioinfo(FileName('.'), make_other_input())
                self.input_output_info.set_implicit_use_of_streaming_input(directory)
            else:
                self.set_implicit_use_of_stdin()

    def has_unrecognised_option(self) -> bool:
        return any((operand.get_name().startswith('-') and operand.get_name() != '-' for operand in self.cmd_inv.operand_list))

    def is_recursive(self) -> bool:
        recursive = False
        for flag_option in self.cmd_inv.flag_option_list:
            name = flag_option.get_name()
            if name in self.RECURSIVE_FLAGS:
                recursive = True
            elif name in self.DIRECTORY_OPTIONS:
                recursive = self.is_recursing_action(flag_option.get_arg())
        return recursive

    def is_recursing_action(self, action: str) -> bool:
        matches = [name for name in self.DIRECTORY_ACTIONS if name.startswith(action)]
        return matches == ['recurse']
