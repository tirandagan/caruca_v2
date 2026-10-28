from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorChcon(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--dereference", "-h", "--no-preserve-root", "--preserve-root", "-R", "-v",
    #                      "-H", "-L", "-P", "--help", "--version"]
    # list_of_all_options = ["-u", "-r", "-t", "-l", "--reference"]

    # chcon does not process a data stream: it reads no stdin and produces no stream output,
    # it only changes the security context of the FILE operands (a side effect on metadata).
    # There is therefore no input to split and nothing to aggregate, so no parallelizer is added.

    def generate_info(self) -> None:
        pass
