from typing import List
from pash_annotations.datatypes.BasicDatatypes import FlagOption, WhichClassForArg
from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorSplit(InputOutputInfoGeneratorInterface):

    @staticmethod
    def does_chunks_arg_write_to_stdout(chunks: str) -> bool:
        parts = chunks.split('/')
        if parts[0] in ('l', 'r'):
            return len(parts) == 3
        return len(parts) == 2

    def set_last_operand_as_config_arg_type_string(self) -> None:
        self.input_output_info.operand_list_typer[-1] = (WhichClassForArg.ARGSTRING, None)

    def generate_info(self) -> None:
        num_operands = self.get_operand_list_length()
        if num_operands > 2:
            raise Exception('extra operand for split, the 3rd one')
        if num_operands == 0:
            self.set_implicit_use_of_stdin()
        else:
            self.all_but_last_operand_is_streaming_input()
        number_options: List[FlagOption] = self.get_flag_option_list_filtered_with(['-n'])
        if len(number_options) > 1:
            raise Exception('multiple -n options defined for split')
        writes_to_stdout = len(number_options) == 1 and self.does_chunks_arg_write_to_stdout(str(number_options[0].get_arg()))
        if writes_to_stdout:
            if self.does_flag_option_list_contain_at_least_one_of(['--filter']):
                raise Exception('--filter does not process a chunk extracted to stdout')
            self.set_implicit_use_of_stdout()
            if num_operands == 2:
                self.set_last_operand_as_config_arg_type_string()
        else:
            if num_operands == 2:
                self.only_last_operand_is_other_output()
            if self.does_flag_option_list_contain_at_least_one_of(['--verbose']):
                self.set_implicit_use_of_stdout()
