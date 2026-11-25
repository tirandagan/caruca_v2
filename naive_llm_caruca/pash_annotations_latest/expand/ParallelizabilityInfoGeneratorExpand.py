from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorExpand(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-i", "--help", "--version"]
    # list_of_all_options = ["-t"]

    # Which ones do affect parallelizability?
    # none: expand processes its input line by line, the column counter is reset at every
    # newline (also with -i and any -t tab stop list), so each output line depends only on
    # its own input line. Splitting at line boundaries and concatenating the results in order
    # gives exactly the sequential output (tested with the command for CC and RR).
    # Caveat: a chunk boundary inside a line would break this, but splitters cut at lines.

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
