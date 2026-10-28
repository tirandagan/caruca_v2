from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorCp(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "--attributes-only", "-b", "--copy-contents", "-d", "--debug", "-f", "-i", "-H",
    #                      "-l", "-L", "-n", "-P", "-p", "--parents", "-R", "--remove-destination",
    #                      "--strip-trailing-slashes", "-s", "-T", "-u", "-v", "-x", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "--preserve", "--no-preserve", "--reflink", "--sparse", "-S", "-t",
    #                        "--update", "--context"]

    # Which ones do affect parallelizability?
    # none: cp neither reads stdin nor writes its result to stdout, so there is no data stream
    # to split; it copies whole files (and directory trees) by name and the copy of each source
    # is not decomposable into chunks that the command itself could recombine
    # -> no parallelizer is added, i.e. the invocation is always run sequentially

    def generate_info(self) -> None:
        pass
