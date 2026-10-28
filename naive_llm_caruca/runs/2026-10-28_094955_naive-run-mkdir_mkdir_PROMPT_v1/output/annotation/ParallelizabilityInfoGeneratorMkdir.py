from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorMkdir(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-p", "-v", "-Z", "--context", "--help", "--version"]
    # list_of_all_options = ["-m"]

    # mkdir processes no data stream: it only creates the named directories as a
    # side effect on the file system, so there is no input to split and no
    # output to recombine.  Not parallelizable.

    def generate_info(self) -> None:
        pass
