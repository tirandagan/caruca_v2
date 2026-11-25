from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorWho(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-b", "-d", "-H", "-l", "--lookup", "-m", "-p", "-q", "-r", "-s", "-t",
    #                      "-T", "-u", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # none: who is not parallelizable at all.
    # It consumes no stream: it never reads stdin, and its only file operand is a binary utmp/wtmp
    # database read whole with fixed-size records, not a line-oriented input that could be split.
    # Outputs such as -q (user count) and -H (heading) are also computed over the whole database.

    def generate_info(self) -> None:
        pass
