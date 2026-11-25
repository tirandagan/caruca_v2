from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorYes(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "--version"]
    # list_of_all_options = []

    # yes is a pure source: it consumes no input stream and produces an
    # unbounded output, so there is nothing to split across parallel copies.
    # No parallelizer is appended.

    def generate_info(self) -> None:
        pass
