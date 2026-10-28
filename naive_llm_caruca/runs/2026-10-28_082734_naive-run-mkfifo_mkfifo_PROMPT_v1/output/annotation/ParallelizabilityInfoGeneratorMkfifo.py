from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorMkfifo(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-Z", "--context", "--help", "--version"]
    # list_of_all_options = ["-m", "--mode"]

    def generate_info(self) -> None:
        # mkfifo processes no data stream: it only creates filesystem entries
        # named by its operands, so there is nothing to split or recombine
        pass
