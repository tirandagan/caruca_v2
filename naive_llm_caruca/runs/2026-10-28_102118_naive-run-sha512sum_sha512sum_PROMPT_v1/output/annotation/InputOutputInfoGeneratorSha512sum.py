from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSha512sum(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # -c: operands are no longer the data to hash but checksum lists; each list names further files
    #     that are read and verified (those are not visible from the invocation alone)
    # --status: nothing is written to stdout, the exit code carries the result (only valid with -c)
    # all others only change the output format; --help/--version assumed absent

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            # checksum lists are read as a whole and the files named in them are opened in turn
            self.all_operands_are_other_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
            if not self.does_flag_option_list_contain_at_least_one_of(["--status"]):
                self.set_implicit_use_of_stdout()
        else:
            # one digest line per FILE; with no FILE (or FILE is -) stdin is hashed
            self.all_operands_are_streaming_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
            self.set_implicit_use_of_stdout()
