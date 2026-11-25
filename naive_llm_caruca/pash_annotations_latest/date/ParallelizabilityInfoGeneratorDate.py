from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDate(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--debug", "-I", "--resolution", "-R", "-u", "--help", "--version"]
    # list_of_all_options = ["-d", "-f", "--rfc-3339", "-r", "-s"]

    # Which ones do affect parallelizability?
    # Without `-f -`, date consumes no input stream and emits a single line: nothing to split.
    # With `-f -`, each stdin line is parsed independently and yields exactly one output line
    # (an unparsable line yields an error on stderr and no stdout line), so the stream can be cut
    # into consecutive chunks or dealt round-robin, run through the same invocation, and the
    # outputs concatenated in order.  Output formatting options (-I, -R, --rfc-3339, -u, +FORMAT,
    # --debug) are per-line and do not matter.
    # -s sets the system clock and must never be parallelised.

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-s", "--set"]):
            return
        if self.does_file_option_read_stdin():
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()

    def does_file_option_read_stdin(self) -> bool:
        for flag_option in self.get_flag_option_list_filtered_with(["-f", "--file"]):
            if self.option_argument_as_string(flag_option) == "-":
                return True
        return False

    @staticmethod
    def option_argument_as_string(option) -> str:
        arg = option.get_arg() if hasattr(option, "get_arg") else getattr(option, "option_arg", None)
        if arg is None:
            return ""
        if hasattr(arg, "get_name"):
            return str(arg.get_name())
        return str(arg)
