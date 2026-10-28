from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSha256sum(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # -c: operands are checksum-list files; the files named inside them are read as well
    # --status (only valid with -c): nothing is written to stdout, the exit code carries the result
    # all other flags only change the output format
    # assumption that version/help not provided

    def generate_info(self) -> None:
        # with no FILE, or when FILE is -, read standard input
        self.if_no_operands_given_stdin_implicitly_used()
        if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            # the operands list the real inputs (name + expected digest per line) rather than
            # being the data stream itself, so they must not be split or streamed
            self.all_operands_are_other_inputs()
            if not self.does_flag_option_list_contain_at_least_one_of(["--status"]):
                self.set_implicit_use_of_stdout()
        else:
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
