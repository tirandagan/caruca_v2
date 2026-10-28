from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorRev(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-0", "-h", "-V"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # rev is a pure per-line map: each output line depends only on the corresponding input line,
    # and the output of several files is the concatenation of the outputs of each file.
    # Hence IF/CC/RR x SEQ x CONC all apply (tested: splitting on line boundaries and
    # concatenating gives byte-identical output).
    # -0 changes the record separator to '\0'; PaSh's splitters cut on '\n', which would fall inside
    # a NUL-terminated record and corrupt the result, so we do not parallelize in that case.
    # -h and -V do not process input at all.

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-0", "--zero", "-h", "--help", "-V", "--version"]):
            self.append_to_parallelizer_list_if_seq_conc()
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
