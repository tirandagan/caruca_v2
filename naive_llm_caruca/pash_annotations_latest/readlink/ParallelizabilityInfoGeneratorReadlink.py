from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorReadlink(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-f", "-e", "-m", "-n", "-q", "-s", "-v", "-z", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # readlink never consumes a data stream: it does not read stdin and does not read the
    # contents of its operands, it only resolves their names and prints one line per operand.
    # There is thus nothing for the consec_chunks/round_robin splitters to cut and nothing for
    # indiv_files to hand out, so no parallelizer is offered and the invocation stays sequential.
    # (Per-operand work is independent, but note that -n only takes effect with a single operand,
    # so even an operand-level split would change the output when -n is given.)

    def generate_info(self) -> None:
        pass
