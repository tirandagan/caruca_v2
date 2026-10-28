from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorFold(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-s", "--help", "--version"]
    # list_of_all_options = ["-w"]

    # Which ones do affect parallelizability?
    # none: fold wraps each input line on its own; the column counter is reset at every newline,
    # so lines are processed independently of each other (also with -b, -s and -w).
    # Tested with the command: fold f1 f2 == cat <(fold f1) <(fold f2), even when f1 lacks a
    # trailing newline (the pending partial line is flushed at the end of each file).
    # Hence splitting the input at line boundaries (CC or RR) and concatenating the parts is exact.

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
