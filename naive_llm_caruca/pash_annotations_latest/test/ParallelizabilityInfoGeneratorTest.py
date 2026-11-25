from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorTest(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["!", "(", ")", "-a", "-o"]
    # list_of_all_options = ["-n", "-z", "-l", "-t",
    #                        "-b", "-c", "-d", "-e", "-f", "-g", "-G", "-h", "-k", "-L", "-N", "-O",
    #                        "-p", "-r", "-s", "-S", "-u", "-w", "-x"]

    # Which ones do affect parallelizability?
    # None: test processes no data stream at all. It reads neither stdin nor file
    # contents (file tests only stat their argument) and produces no stdout; the
    # whole result is the exit status. There is nothing to split or recombine, so
    # no parallelizer is ever appended.

    def generate_info(self) -> None:
        pass
