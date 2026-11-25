from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorEnv(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-i", "-", "-0", "--block-signal", "--default-signal", "--ignore-signal",
    #                      "--list-signal-handling", "-v", "--help", "--version"]
    # list_of_all_options = ["-u", "-C", "-S"]

    # env does no work on its data stream itself: without a COMMAND it prints the environment
    # (no input to split), and with a COMMAND it execs a single process whose stdin/stdout
    # behaviour is that of COMMAND. Whether splitting the stream is valid depends entirely on
    # COMMAND, which we cannot inspect here, so unlike xargs (which runs COMMAND per input chunk)
    # no parallelizer is offered.

    def generate_info(self) -> None:
        pass
