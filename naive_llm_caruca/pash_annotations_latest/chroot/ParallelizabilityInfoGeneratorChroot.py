from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorChroot(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--skip-chdir", "--help", "--version"]
    # list_of_all_options = ["--groups", "--userspec"]

    # chroot changes the root directory (and optionally the user/groups) and then executes an
    # arbitrary COMMAND, whose semantics with respect to its input are unknown. The chroot(2)
    # call itself requires privileges and is a process-wide side effect, so the invocation
    # cannot be split into parallel copies.

    def generate_info(self) -> None:
        # not parallelizable: nothing is appended to the parallelizer list
        pass
