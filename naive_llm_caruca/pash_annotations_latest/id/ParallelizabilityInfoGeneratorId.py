from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorId(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-Z", "-g", "-G", "-n", "-r", "-u", "-z", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # none: id has no stream input at all (it never reads stdin and its operands are user names,
    # not files), so there is nothing to split; the invocation is never parallelized.

    def generate_info(self) -> None:
        pass
