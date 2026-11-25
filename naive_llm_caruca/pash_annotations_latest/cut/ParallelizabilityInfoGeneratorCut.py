from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter"]

    # Which ones do affect parallelizability?
    # cut processes each line independently of every other line, so it is
    # parallelizable with both consecutive chunks and round robin, and the
    # outputs are simply concatenated.
    # -z makes NUL the line delimiter; the splitters cut the input at newlines,
    # which would then fall inside a record, so we do not parallelize in that case.

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-z", "--zero-terminated"]):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
