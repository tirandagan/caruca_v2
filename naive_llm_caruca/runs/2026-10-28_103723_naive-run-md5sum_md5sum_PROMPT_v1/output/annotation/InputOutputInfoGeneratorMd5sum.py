from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMd5sum(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # -c: operands are no longer the data to hash but checksum lists; each list names further files
    #     which md5sum opens and reads itself, so the operands are not plain stream inputs
    # --status (only valid with -c): nothing is written to stdout, the exit code carries the result
    # -b, -t, --tag, -z only change the output format
    # --quiet, --strict, -w, --ignore-missing only change what is reported, not where
    # assumption that version/help not provided

    def generate_info(self) -> None:
        # with no FILE, or when FILE is -, read standard input (tested, holds in both modes)
        self.if_no_operands_given_stdin_implicitly_used()
        if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            # checksum lists are read in full and the files they name are read as well
            self.all_operands_are_other_inputs()
            if not self.does_flag_option_list_contain_at_least_one_of(["--status"]):
                self.set_implicit_use_of_stdout()
        else:
            # one digest line per operand, in operand order
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
