from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorTouch(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-c", "-f", "-h", "-m", "--help", "--version"]
    # list_of_all_options = ["-d", "-r", "-t", "--time"]

    # touch processes no data stream: it reads neither stdin nor its operands and writes no output,
    # it only creates files or sets their timestamps (a side effect on each operand).
    # There is nothing to split or recombine, so no parallelizer is offered.

    def generate_info(self) -> None:
        pass
