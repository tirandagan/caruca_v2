from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorPinky(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-l", "-b", "-h", "-p", "-s", "-f", "-w", "-i", "-q", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # none: pinky has no stream input at all (it reads the utmp database,
    # not stdin or operand files), so there is nothing to split

    def generate_info(self) -> None:
        pass
