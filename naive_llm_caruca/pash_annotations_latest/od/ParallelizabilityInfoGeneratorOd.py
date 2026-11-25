from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorOd(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-b", "-c", "-d", "-f", "-i", "-l", "-o", "-s", "-x", "-v", "-w",
    #                      "--traditional", "--help", "--version"]
    # list_of_all_options = ["-A", "--endian", "-j", "-N", "-S", "-t", "--width"]

    # Which ones do affect parallelizability?
    # od is a byte-oriented command and is not parallelizable with any of the available splitters:
    # - every output row covers a fixed number of input bytes (16 by default, -w), so parts produced
    #   by a line-based splitter (consec_chunks, round_robin) or by file boundaries (indiv_files;
    #   od concatenates all FILE operands into one input) start mid-row and the rows of a part do
    #   not line up with those of the sequential run; tested: even "od -A n -v -c" on three
    #   line-split chunks differs from the sequential output
    # - the address column (unless -A n) and the trailing end-address line are absolute offsets
    #   into the combined input, so each part would need a BYTE_OFFSET-aware custom mapper and the
    #   per-part trailer lines would have to be dropped
    # - "*" duplicate-row suppression (unless -v), -j/-N (skip/limit on the combined input), -S
    #   (NUL-terminated strings can span part boundaries) and the OFFSET/LABEL operands all depend
    #   on global position in the input
    # Hence no parallelizer is added; PaSh runs od sequentially.

    def generate_info(self) -> None:
        pass
