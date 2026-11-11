from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface

class InputOutputInfoGeneratorWc(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(['--files0-from']):
            if self._files0_from_is_stdin():
                self.set_implicit_use_of_stdin()
        else:
            self.all_operands_are_streaming_inputs()
            self.if_no_operands_given_stdin_implicitly_used()

    def _files0_from_is_stdin(self) -> bool:
        for flag_option in self.get_flag_option_list_filtered_with(['--files0-from']):
            arg = getattr(flag_option, 'option_arg', None)
            if arg is None:
                getter = getattr(flag_option, 'get_arg', None)
                arg = getter() if callable(getter) else None
            if arg is None:
                return True
            name = getattr(arg, 'name', None)
            if name is None:
                getter = getattr(arg, 'get_name', None)
                name = getter() if callable(getter) else str(arg)
            if str(name) == '-':
                return True
        return False
