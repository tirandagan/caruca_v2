from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSha256sum(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # a digest depends on the whole content of a file, so a single input can never be split
    # into chunks (neither CC nor RR); only the file boundaries are a valid split point
    # each operand produces exactly its own output line(s), in operand order, so IF x SEQ x CONC
    # is exact for both the digest mode and the check mode (-c), independent of formatting flags
    # the per-invocation summaries of -c ("N computed checksums did NOT match", ...) go to stderr,
    # so stdout is unaffected by the split

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_if_seq_conc()
