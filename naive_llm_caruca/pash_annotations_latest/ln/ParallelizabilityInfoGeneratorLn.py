from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorLn(ParallelizabilityInfoGeneratorInterface):

    # ln does not process a data stream: it creates directory entries for its
    # operands and produces no output to split or recombine, so no
    # parallelizer applies.

    def generate_info(self) -> None:
        pass
