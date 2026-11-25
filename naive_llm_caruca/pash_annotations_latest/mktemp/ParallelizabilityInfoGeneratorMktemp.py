from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorMktemp(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-d", "-u", "-q", "--tmpdir", "-t", "--help", "--version"]
    # list_of_all_options = ["--suffix", "-p"]

    # mktemp consumes no input stream: it creates exactly one file or directory
    # and prints its name. There is nothing to split, and running several copies
    # would create several distinct files, so no parallelizer applies.

    def generate_info(self) -> None:
        pass
