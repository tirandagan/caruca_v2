from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSha1sum(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # -c: the operands are no longer the data that is hashed but lists of "checksum  filename" lines;
    #     sha1sum then reads every file named in those lists (inputs not visible on the command line)
    # --status: nothing is written to stdout, only the exit code reports the result
    # -b, -t, --tag, -z only change the output format; --ignore-missing, --quiet, --strict, -w only
    # change what is reported while checking

    def generate_info(self) -> None:
        # assumption that version/help not provided
        if not self.does_flag_option_list_contain_at_least_one_of(["--status"]):
            self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            # tested: with no operands the checksum lines are read from stdin
            self.if_no_operands_given_stdin_implicitly_used()
            # the operands are read completely but are not the stream being processed;
            # the files they name are read as well
            self.all_operands_are_other_inputs()
        else:
            # tested: with no FILE, or when FILE is -, standard input is hashed
            self.if_no_operands_given_stdin_implicitly_used()
            self.all_operands_are_streaming_inputs()
