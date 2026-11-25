from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorRuncon(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "--help", "--version"]
    # list_of_all_options = ["-t", "-u", "-r", "-l"]

    # Which ones do affect parallelizability?
    # none directly: runcon only sets the SELinux context and then execs COMMAND
    # the observable behaviour on the stream is entirely that of COMMAND, which is
    # opaque here, so we do not parallelize at all
    # (with no operands runcon just prints the current context, nothing to split)

    def generate_info(self) -> None:
        pass
