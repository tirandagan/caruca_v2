from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorKill(ParallelizabilityInfoGeneratorInterface):

    # kill processes no data stream: it sends a signal to the PIDs given as
    # operands (a side effect on other processes) and, with -l/-L, prints a
    # fixed table.  There is no input to split, so no parallelizer is added.

    def generate_info(self) -> None:
        pass
