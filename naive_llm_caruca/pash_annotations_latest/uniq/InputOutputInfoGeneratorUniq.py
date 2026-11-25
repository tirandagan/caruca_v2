from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorUniq(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-D", "--all-repeated", "--group", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["-f", "-s", "-w"]

    # Which ones do affect input/output?
    # only the number of operands: uniq [OPTION]... [INPUT [OUTPUT]]
    # INPUT absent or "-" means stdin, OUTPUT absent or "-" means stdout (verified with coreutils 9.4);
    # --help and --version write to stdout and read nothing, but we assume they are not given

    def generate_info(self) -> None:
        if self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
        elif self.get_operand_list_length() == 1:
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
        elif self.get_operand_list_length() == 2:
            self.all_but_last_operand_is_streaming_input()
            self.only_last_operand_is_stream_output()
        else:
            # uniq itself fails with "extra operand"
            raise Exception('extra operand for uniq, the 3rd one')
