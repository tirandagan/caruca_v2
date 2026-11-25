from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDf(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-h", "-H", "-i", "-k", "-m", "-l", "--no-sync", "-P", "--sync",
    #                      "--total", "-T", "-v", "--help", "--version"]
    # list_of_all_options = ["-B", "--output", "-t", "-F", "-x"]

    # Which ones do affect parallelizability?
    # none: df does not consume a data stream at all; it queries file system metadata
    # for its operands (or for every mount point) and prints a table with a header,
    # so there is nothing to split and the output cannot be recombined by concatenation.
    # Hence no parallelizer is ever appended.

    def generate_info(self) -> None:
        pass
