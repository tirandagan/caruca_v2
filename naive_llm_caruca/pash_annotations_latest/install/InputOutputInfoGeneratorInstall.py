from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorInstall(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "-C", "-d", "-D", "--debug", "-p", "-s", "-T", "-v",
    #                      "--preserve-context", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "-g", "-m", "-o", "--strip-program", "-S", "-t", "--context"]

    # Which ones do affect input/output?
    # -d: every operand is a directory to create (output), nothing is read
    # -t: the destination is the option argument (typed OTHER_OUTPUT by the parser table),
    #     so every operand is a source
    # otherwise: the last operand is the destination, all others are sources
    # -v and --debug print the name of each created file to stdout; nothing else writes stdout
    # install never reads stdin ('-' is an ordinary file name)
    # -b/--backup/-S additionally create backup files next to the destination; we do not model them
    # --strip-program names a program to run, not a file we read

    def generate_info(self) -> None:
        # assumption that version/help not provided
        if self.does_flag_option_list_contain_at_least_one_of(["-v", "--debug"]):
            self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["-d"]):
            # install -d DIRECTORY...
            self.all_operands_are_other_outputs()
        elif self.does_flag_option_list_contain_at_least_one_of(["-t"]):
            # install -t DIRECTORY SOURCE...
            self.all_operands_are_other_inputs()
        else:
            # install [-T] SOURCE DEST  or  install SOURCE... DIRECTORY
            if self.get_operand_list_length() < 2:
                raise Exception('install requires SOURCE and DEST operands')
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
