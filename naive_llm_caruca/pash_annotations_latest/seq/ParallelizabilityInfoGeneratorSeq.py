from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSeq(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-w", "--help", "--version"]
    # list_of_all_options = ["-f", "-s"]

    # Which ones do affect parallelizability?
    # none: seq is a pure generator. It consumes no input stream, so there is
    # nothing for a splitter (indiv_files, consec_chunks, round_robin) to divide;
    # its output is produced sequentially from the operands alone.

    def generate_info(self) -> None:
        # no parallelizer is added: the invocation runs as a single sequential source
        pass
