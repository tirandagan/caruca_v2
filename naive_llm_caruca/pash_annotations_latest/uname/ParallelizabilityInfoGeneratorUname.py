from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorUname(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-s", "-n", "-r", "-v", "-m", "-p", "-i", "-o", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # none: uname consumes no input stream at all, so there is nothing
    # to split; it is never parallelizable.

    def generate_info(self) -> None:
        pass
