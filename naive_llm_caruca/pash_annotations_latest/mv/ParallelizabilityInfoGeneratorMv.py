from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorMv(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "--debug", "-f", "-i", "-n", "--no-copy", "--strip-trailing-slashes",
    #                      "-T", "-u", "-v", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "-S", "-t", "--update"]

    # mv does not process a data stream: it renames or moves whole files and has no stdin/stdout data flow,
    # so there is nothing to split.  Running several copies on parts of one source would also break the
    # atomic rename semantics and the "last operand is the destination" rule.

    def generate_info(self) -> None:
        # not parallelizable
        pass
