from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorSort(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(['--files0-from']):
            if self._files0_from_argument() == '-':
                self.set_implicit_use_of_stdin()
        elif self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
        else:
            self.all_operands_are_streaming_inputs()
        if self.does_flag_option_list_contain_at_least_one_of(['-c', '-C', '--check']):
            pass
        elif self.does_flag_option_list_contain_at_least_one_of(['-o', '--output']):
            pass
        else:
            self.set_implicit_use_of_stdout()

    def _files0_from_argument(self) -> str:
        for flag_option in self.get_flag_option_list_filtered_with(['--files0-from']):
            return _argument_as_string(flag_option)
        return ''

def _argument_as_string(option) -> str:
    arg = None
    for attribute in ('get_arg_as_string', 'get_arg', 'arg', 'option_arg', 'value'):
        if hasattr(option, attribute):
            arg = getattr(option, attribute)
            if callable(arg):
                arg = arg()
            break
    if arg is None:
        return ''
    for attribute in ('get_name', 'name', 'raw', 'value'):
        if hasattr(arg, attribute):
            inner = getattr(arg, attribute)
            if callable(inner):
                inner = inner()
            if isinstance(inner, str):
                return inner
    return str(arg)
