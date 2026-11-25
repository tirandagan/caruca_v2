from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDirname(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-z", "--zero", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # none. dirname reads no stream (neither stdin nor any file): all of its input is on the
    # command line, so there is nothing for a splitter to divide. The invocation is left
    # sequential by appending no parallelizer.

    def generate_info(self) -> None:
        pass
