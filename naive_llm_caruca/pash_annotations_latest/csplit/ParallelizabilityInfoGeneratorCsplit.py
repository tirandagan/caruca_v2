from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorCsplit(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-k", "--suppress-matched", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-f", "-n"]

    # Which ones do affect parallelizability?
    # none, since csplit is never parallelized:
    # its real output is the set of files PREFIX00, PREFIX01, ... whose numbering and contents depend
    # on global state of the whole input (absolute line numbers, repetition counts of {N}/{*}, and
    # the order in which patterns are consumed); a copy run on a part of the input would number its
    # pieces from zero again and would also apply the patterns from the beginning. The text written
    # to stdout is only the per-piece byte counts, in piece order, so it cannot be merged either.

    def generate_info(self) -> None:
        pass
