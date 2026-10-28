from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorChgrp(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-f", "-v", "--dereference", "-h", "--no-preserve-root", "--preserve-root",
    #                      "-R", "-H", "-L", "-P", "--help", "--version"]
    # list_of_all_options = ["--reference"]

    # chgrp never reads stdin or any data stream: it only changes the group metadata of the FILE operands
    # (and, with -R, of the files below them). There is no input that a splitter could cut into chunks or
    # deal out round-robin, and the only output is diagnostics (-c/-v), whose order PaSh would have to
    # preserve across the operand list. Hence no parallelizer is offered for any invocation.

    def generate_info(self) -> None:
        pass
