from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorUnexpand(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "--first-only", "--help", "--version"]
    # list_of_all_options = ["-t"]

    # Which ones do affect parallelizability?
    # none: unexpand processes each line independently (the column counter and tab
    # stops reset at every newline), so any split on line boundaries followed by
    # plain concatenation reproduces the sequential output, whatever flags are given.
    # Verified against the binary with -a, -t N, -t LIST (incl. '/' and '+'), --first-only.
    # No IF parallelizer: unexpand treats all FILE operands as one stream, so a file
    # without a trailing newline is joined with the next file's first line; processing
    # files individually would convert that joined line differently.

    def generate_info(self) -> None:
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
