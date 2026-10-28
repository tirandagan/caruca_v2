from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorTimeout(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--preserve-status", "--foreground", "-v", "--help", "--version"]
    # list_of_all_options = ["-k", "-s"]

    # timeout is a wrapper: it runs an arbitrary COMMAND and kills it after
    # DURATION. Whether the work could be split depends entirely on COMMAND,
    # which is opaque here, and the time limit applies to the invocation as a
    # whole (splitting the input would give every part the full DURATION and
    # change which part, if any, gets killed; the exit status 124 would also no
    # longer be well-defined). Hence no parallelizer is added.

    def generate_info(self) -> None:
        pass
