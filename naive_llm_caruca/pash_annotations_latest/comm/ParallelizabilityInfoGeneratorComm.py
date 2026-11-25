from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorComm(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-1", "-2", "-3", "--check-order", "--nocheck-order", "--total", "-z", "--help", "--version"]
    # list_of_all_options = ["--output-delimiter"]

    # Which ones do affect parallelizability?
    # comm is a merge-join over TWO sorted input streams, so there is no single
    # input stream that a splitter could cut up on its own:
    #  - CC/RR on one operand while replicating the other is wrong in general:
    #    lines unique to the replicated file would be emitted once per part
    #    (and RR breaks the sorted-order assumption entirely);
    #  - it is only correct for the restricted cases where the column of the
    #    replicated file is suppressed and no summary is requested
    #    (e.g. "comm -12" / "comm -23" chunking FILE1 against the whole FILE2),
    #    and --total would additionally need a summing aggregator;
    #  - IF (individual files) does not apply as both operands are needed together.
    # Hence we conservatively do not parallelize comm at all.

    def generate_info(self) -> None:
        pass
