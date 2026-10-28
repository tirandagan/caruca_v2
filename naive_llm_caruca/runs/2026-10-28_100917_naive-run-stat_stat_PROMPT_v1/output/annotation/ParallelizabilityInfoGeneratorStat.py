from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorStat(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-L", "-f", "-t", "--help", "--version"]
    # list_of_all_options = ["--cached", "-c", "--printf"]

    # Which ones do affect parallelizability?
    # none, because stat does not process a data stream at all: it only queries metadata of the
    # named operands and prints one report per operand. There is no input stream to split with
    # consec_chunks or round_robin (even "-" is merely fstat'ed, never read), so no parallelizer
    # applies and the invocation is left sequential.

    def generate_info(self) -> None:
        pass
