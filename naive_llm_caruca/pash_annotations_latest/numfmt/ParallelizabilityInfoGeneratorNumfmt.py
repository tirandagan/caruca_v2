from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorNumfmt(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--debug", "--grouping", "--header", "-z", "--help", "--version"]
    # list_of_all_options = ["-d", "--field", "--format", "--from", "--from-unit", "--invalid",
    #                        "--padding", "--round", "--suffix", "--to", "--to-unit"]

    # Which ones do affect parallelizability?
    # numfmt converts every input line independently of all others (tested: output of the
    # sequential run equals the concatenation of the runs on consecutive chunks, and equals
    # the line-by-line runs), so the base-line is CC/RR x SEQ x CONC
    # --header[=N] passes the first N lines through unconverted; every parallel copy would
    #   treat the first lines of its own part as header lines, so we do not parallelize
    # -z makes records NUL-terminated, which the line-based splitters do not respect
    # --invalid=abort (the default) and --invalid=fail only matter for erroneous input: with abort,
    #   the sequential command stops at the first bad line while the parts after it would still
    #   produce output; we accept this as it only changes the output of a failing invocation
    # operands (NUMBERs on the command line) are not a stream, so there is nothing to split then

    def generate_info(self) -> None:
        if self.get_operand_list_length() == 0 and \
                not self.does_flag_option_list_contain_at_least_one_of(["--header", "-z", "--zero-terminated"]):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
