from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorKill(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        # operands are process ids (or negative process-group ids), never files
        self.set_all_operands_as_config_arg_type_string()
        # kill never reads stdin; it only writes stdout when asked to print
        # signal names (-l/-L), help or version
        if self.does_flag_option_list_contain_at_least_one_of(
                ["-l", "--list", "-L", "--table", "-h", "--help", "-V", "--version"]):
            self.set_implicit_use_of_stdout()
