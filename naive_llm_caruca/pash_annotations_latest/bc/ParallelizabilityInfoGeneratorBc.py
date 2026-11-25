from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorBc(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-h", "-i", "-l", "-q", "-s", "-w", "-v"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # none: bc is a stateful interpreter regardless of flags.
    # Its input is a program, not a sequence of independent records: variables
    # (including `scale`, `ibase`, `obase`), function definitions and `{ }` blocks
    # carry state from one line to the next, a statement may span several lines
    # (backslash continuation, open braces/strings), and `quit` stops all further
    # reading. Splitting the input by lines (consecutive chunks or round robin)
    # therefore changes the result in general, so no parallelizer is offered.

    def generate_info(self) -> None:
        pass
