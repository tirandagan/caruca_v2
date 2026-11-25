from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorPtx(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-G", "-O", "-R", "-T", "-f", "-r", "-t", "--help", "--version"]
    # list_of_all_options = ["-F", "-M", "--format", "-S", "-W", "-b", "-g", "-i", "-o", "-w"]

    # Which ones do affect parallelizability?
    # ptx reads all of its input, then emits one index line per keyword occurrence, sorted by keyword
    # over the whole input (tested: two input files are interleaved in a single sorted index).
    # Concatenating the outputs of parts therefore does not reproduce the sequential output, and a
    # sorted merge would still be wrong because the context of a keyword can span input lines
    # (the default -S sentence regexp lets a sentence continue on the next line) and -A/-r references
    # depend on line numbers / file names of the original input.
    # Hence no parallelizer is added; a merging aggregator would be needed for a safe parallelization.

    def generate_info(self) -> None:
        pass
