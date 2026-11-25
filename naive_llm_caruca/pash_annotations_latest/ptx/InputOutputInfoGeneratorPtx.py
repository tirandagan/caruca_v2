from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorPtx(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-G", "-O", "-R", "-T", "-f", "-r", "-t", "--help", "--version"]
    # list_of_all_options = ["-F", "-M", "--format", "-S", "-W", "-b", "-g", "-i", "-o", "-w"]

    # Which ones do affect input/output?
    # -b, -i, -o name files read as configuration (word lists); typed CONFIG_INPUT in ptx.json
    # -G switches to the System V syntax `ptx -G [INPUT [OUTPUT]]`, where the second operand
    #   is written instead of read (tested: it overwrites the file; a lone "-" there is a literal file name)
    # without -G, every operand is an input and the index always goes to stdout

    def generate_info(self) -> None:
        # assumption that version/help not provided
        if self.does_flag_option_list_contain_at_least_one_of(["-G"]):
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
                raise Exception('extra operand for ptx -G, the 3rd one')
        else:
            self.if_no_operands_given_stdin_implicitly_used()
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
