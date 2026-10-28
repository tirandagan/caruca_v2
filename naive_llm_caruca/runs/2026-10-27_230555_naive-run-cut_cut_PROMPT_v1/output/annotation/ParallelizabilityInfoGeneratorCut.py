from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter"]

    # Which ones do affect parallelizability?
    # cut is a pure per-line function: every output line depends only on its input line,
    # lines are emitted in input order and -s only drops lines, so
    # CC/RR x SEQ x CONC is exact for -b, -c, -f, -d, -s, --complement, --output-delimiter, -n.
    # -z changes the record delimiter to NUL; the splitters split on newlines, so a chunk
    # boundary could fall inside a NUL-terminated record and change the output -> not parallelized.

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-z"]):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
