from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorRm(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-f", "-i", "-I", "--one-file-system", "--no-preserve-root",
    #                      "-r", "-d", "-v", "--help", "--version"]
    # list_of_all_options = ["--interactive", "--preserve-root"]

    # rm consumes no input stream and produces no output stream: it removes the
    # files named by its operands as a side effect. There is nothing to split
    # into chunks or recombine, so no parallelizer is ever added.
    # (-I's "more than three files" prompt and --one-file-system's per-argument
    # device check also depend on seeing the whole operand list at once, which
    # rules out even splitting the operands across copies.)
    def generate_info(self) -> None:
        pass
