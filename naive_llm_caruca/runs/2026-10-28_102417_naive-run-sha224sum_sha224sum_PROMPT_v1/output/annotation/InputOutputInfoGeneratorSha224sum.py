from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSha224sum(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # -c: the operands are no longer the data to be hashed but checksum lists; each line names a
    #     further file that is read and verified (the files named in the list are not operands and
    #     so cannot be tracked here, hence the operands are marked as "other" inputs)
    # --status: with -c, nothing is written to stdout, the exit code is the result
    # all other flags only change the output format
    # with no operands, or an operand '-', stdin is read (both with and without -c)

    def generate_info(self) -> None:
        # assumption that version/help not provided
        if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            self.all_operands_are_other_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
            if not self.does_flag_option_list_contain_at_least_one_of(["--status"]):
                self.set_implicit_use_of_stdout()
        else:
            self.all_operands_are_streaming_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
            self.set_implicit_use_of_stdout()
