from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorCol(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-f", "-h", "-p", "-x", "-H", "--help", "-V", "--version"]
    # list_of_all_options = ["-l", "--lines"]

    # Which ones do affect parallelizability?
    # None: col is not parallelizable regardless of flags.
    # Reverse and half-reverse line feeds (ESC-7, ESC-8, VT) move subsequent text onto *earlier* output
    # lines, and the shift-in/shift-out character-set state carries across lines, so the output for any
    # line depends on input that may lie arbitrarily far ahead (bounded only by the -l buffer). Splitting
    # the input into chunks (consec_chunks or round_robin) would therefore change the output whenever such
    # sequences straddle a chunk boundary, and whether they do cannot be decided from the invocation alone.

    def generate_info(self) -> None:
        pass
