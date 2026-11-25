from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSha512sum(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # A digest is a function of the whole input, so a single stream can never be split:
    # no consecutive-chunks or round-robin parallelizer for any invocation.
    # Without -c, each FILE operand is hashed independently and yields exactly one output line
    # (the format flags -b, -t, --tag, -z only change that line), so the per-file work can be
    # distributed and the lines concatenated in operand order: IF x SEQ x CONC.
    # With -c, the operands are checksum lists; the summary warnings on stderr and the exit status
    # are computed over all lists together, so we do not parallelize check mode.

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-c", "--help", "--version"]):
            if self.get_operand_list_length() > 1:
                self.append_to_parallelizer_list_if_seq_conc()
