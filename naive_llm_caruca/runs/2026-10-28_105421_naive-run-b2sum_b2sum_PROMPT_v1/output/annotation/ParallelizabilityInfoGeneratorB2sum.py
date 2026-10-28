from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorB2sum(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = ["-l"]

    # Which ones do affect parallelizability?
    # A digest is a function of the whole content of one file, so neither consecutive chunks nor
    # round-robin splitting of a file's content is possible: only whole files can be handled in parallel.
    # Each input file produces exactly one output line, in operand order, so IF x SEQ x CONC is exact.
    # -c: the exit status (any FAILED/missing line, --strict) and the summary warnings on stderr are
    #     computed over all checksum files together, so we do not parallelize verification.
    # -b, -t, -z, --tag, -l: per-line formatting only, unaffected by splitting into individual files.

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            self.append_to_parallelizer_list_if_seq_conc()
