from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSha1sum(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # base-line: a SHA1 digest is computed over a whole file, so a file cannot be split into chunks (no CC/RR);
    #   but every FILE operand yields exactly one independent output line, so IF x SEQ x CONC is exact
    # -c renders parallelization infeasible: the final "WARNING: n lines are improperly formatted" /
    #   "n computed checksums did NOT match" summaries and the exit status are totals over all operands
    # --status produces no output, so there is nothing to parallelize for
    # -b, -t, --tag, -z only change the per-line output format and do not matter

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-c", "--status"]):
            self.append_to_parallelizer_list_if_seq_conc()
