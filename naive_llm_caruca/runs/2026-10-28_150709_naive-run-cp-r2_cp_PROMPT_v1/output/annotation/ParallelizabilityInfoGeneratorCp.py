from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorCp(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "--attributes-only", "-b", "--copy-contents", "-d", "--debug", "-f", "-i", "-H",
    #                      "-l", "-L", "-n", "-P", "-p", "--parents", "-R", "--remove-destination",
    #                      "--strip-trailing-slashes", "-s", "-T", "-u", "-v", "-x", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "--preserve", "--no-preserve", "--reflink", "--sparse", "-S", "-t",
    #                        "--update", "--context"]

    # Which ones do affect parallelizability?
    # none: cp never reads stdin as data and never writes its result to stdout, it only creates or
    # overwrites files in the file system, so there is no stream to split and no outputs to aggregate.
    # Splitting the sources across several copies of cp would also change the ordering guarantees of
    # -n/-u/--backup when sources collide in the destination directory.

    def generate_info(self) -> None:
        # not parallelizable: leave the parallelizer list empty
        pass
