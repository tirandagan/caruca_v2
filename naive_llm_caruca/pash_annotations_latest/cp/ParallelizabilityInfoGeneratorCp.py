from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorCp(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "--attributes-only", "-b", "--copy-contents", "-d", "--debug", "-f", "-i", "-H",
    #                      "-l", "-L", "-n", "-P", "-p", "--parents", "-R", "--remove-destination",
    #                      "--strip-trailing-slashes", "-s", "-T", "-u", "-v", "-x", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "--preserve", "--no-preserve", "--reflink", "--sparse", "-S", "-t",
    #                        "--update", "--context"]

    # cp is not a stream transformer: it reads no data from stdin and writes no data to stdout
    # (only -v/--debug messages).  Its output is a file or directory tree named by an operand or by -t,
    # created as a side effect, so there is no output stream to split and re-aggregate.
    # Hence no parallelizer is added, whatever the flags.

    def generate_info(self) -> None:
        pass
