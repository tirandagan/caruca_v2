from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorInstall(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "-C", "-d", "-D", "--debug", "-p", "-s", "-T", "-v",
    #                      "--preserve-context", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "-g", "-m", "-o", "--strip-program", "-S", "-t", "--context"]

    # Which ones do affect parallelizability?
    # none: install does not process a data stream; it copies whole files and sets their
    # attributes (mode, owner, group, timestamps, security context) as a single operation
    # per destination, so splitting its input is not meaningful. No parallelizer is added.

    def generate_info(self) -> None:
        pass
