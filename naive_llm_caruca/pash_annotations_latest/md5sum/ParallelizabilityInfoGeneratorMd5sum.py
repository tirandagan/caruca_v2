from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorMd5sum(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # the digest of a file depends on all of its bytes, so a single input can never be split (no CC, no RR)
    # each operand produces exactly one output line, independent of the other operands and in operand
    # order, so IF x SEQ x CONC is exact in the default mode
    # -c: the per-list output lines are still independent, but the trailing summary on stderr
    #     ("WARNING: n lines are improperly formatted", mismatch counts) and the exit code are computed
    #     over all lists together, so we do not parallelize at all
    # -b, -t, --tag, -z only change the per-line output format and do not matter

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-c", "--help", "--version"]):
            self.append_to_parallelizer_list_if_seq_conc()
