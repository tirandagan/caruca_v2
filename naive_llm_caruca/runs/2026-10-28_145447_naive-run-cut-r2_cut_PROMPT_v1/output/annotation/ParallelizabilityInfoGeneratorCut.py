from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter"]

    # Which ones do affect parallelizability?
    # cut handles every line on its own, so none of -b, -c, -d, -f, -s,
    # --complement, --output-delimiter changes that: RR/CC x SEQ x CONC is exact
    # (checked against the binary with chunked and round-robin split inputs).
    # -z makes NUL the line delimiter; the splitters cut at newlines, which may
    # fall inside a record and change the output, so we do not parallelize then.
    # --help/--version assumed not to be given.

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-z", "--zero-terminated"]):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
