from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorB2sum(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = ["-l"]

    # Which ones do affect input/output?
    # -c: operands are no longer the data to hash but files listing "checksum  name" lines;
    #     b2sum reads them and then reads every named file to verify it.
    # --status: nothing is written to stdout (only the exit status reports the result).
    # --quiet only suppresses the "OK" lines, failures are still printed, so stdout is still used.
    # -b, -t, -z, --tag, -l only change the format of the output, not what is read or written.
    # In every mode, no operands (or an operand of "-") means standard input is read.

    def generate_info(self) -> None:
        # assumption that version/help not provided
        if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            # the checksum files are read as configuration; the files they name are read as well,
            # which cannot be expressed through the operand list and is thus under-approximated here
            self.all_operands_are_other_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
            if not self.does_flag_option_list_contain_at_least_one_of(["--status"]):
                self.set_implicit_use_of_stdout()
        else:
            self.all_operands_are_streaming_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
            self.set_implicit_use_of_stdout()
