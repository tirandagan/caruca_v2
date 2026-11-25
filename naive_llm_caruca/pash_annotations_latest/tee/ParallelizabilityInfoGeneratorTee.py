from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorTee(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-i", "-p", "--help", "--version"]
    # list_of_all_options = ["--output-error"]

    # tee is a pure pass-through on stdin -> stdout, so the stream itself could
    # be split into consecutive chunks or dealt out round-robin, each part run
    # through the same command, and the outputs concatenated in order.
    #
    # However, every FILE operand is written by the command as a side effect.
    # Parallel copies would all open the same FILEs (truncating each other
    # without -a, interleaving non-deterministically with -a), so the file
    # outputs would no longer equal the sequential result.  We therefore only
    # parallelize when there are no FILE operands, i.e. when tee behaves like
    # cat.  -i, -p and --output-error only affect signal and write-error
    # handling and do not change the data, so they do not block this.

    def generate_info(self) -> None:
        if self.get_operand_list_length() == 0:
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
