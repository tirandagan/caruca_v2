from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorChmod(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-f", "-v", "--no-preserve-root", "--preserve-root", "-R", "--help", "--version"]
    # list_of_all_options = ["--reference"]

    # chmod processes no data stream: it reads neither stdin nor the contents of its operands and
    # writes only file metadata (plus optional diagnostics on stdout with -c/-v).
    # None of the splitters (consecutive chunks, round robin, individual input files) applies,
    # since there is no input stream to divide, so no parallelizer is registered and the
    # invocation is executed sequentially as a whole.

    def generate_info(self) -> None:
        pass
