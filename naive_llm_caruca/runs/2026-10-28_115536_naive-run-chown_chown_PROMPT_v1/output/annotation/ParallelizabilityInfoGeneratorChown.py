from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorChown(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-f", "-v", "--dereference", "-h", "--no-preserve-root", "--preserve-root",
    #                      "-R", "-H", "-L", "-P", "--help", "--version"]
    # list_of_all_options = ["--from", "--reference"]

    # Which ones do affect parallelizability?
    # none: chown processes no data stream at all. It reads neither stdin nor the content of its
    # operands and writes no output stream (only -c/-v diagnostics). Its effect is a metadata change
    # on each FILE, so there is nothing to split into chunks or round-robin and nothing to aggregate.
    # Splitting over the FILE operands (indiv_files) is not applicable either, since the operands are
    # outputs, not inputs.

    def generate_info(self) -> None:
        # no parallelizer is appended: the invocation is not parallelised
        pass
