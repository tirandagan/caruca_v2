from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorTruncate(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-o", "--help", "--version"]
    # list_of_all_options = ["-r", "-s"]

    # truncate consumes no data stream: it resizes its operand files in place via
    # ftruncate(2) and produces no stdout. There is nothing to split or recombine,
    # so no parallelizer applies regardless of flags.

    def generate_info(self) -> None:
        pass
