from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorMknod(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-Z", "--help", "--version"]
    # list_of_all_options = ["-m", "--mode", "--context"]

    # mknod creates a single special file and processes no data stream, so
    # there is nothing to split: no parallelizer is ever added.

    def generate_info(self) -> None:
        pass
