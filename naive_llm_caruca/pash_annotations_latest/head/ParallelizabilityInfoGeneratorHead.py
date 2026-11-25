from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_n_ary_from_string_representation
from pash_annotations.datatypes.BasicDatatypes import Option


class ParallelizabilityInfoGeneratorHead(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect parallelizability?
    # head prints a prefix of its input, so parallelization is only possible with CC (never RR, order matters)
    # and an aggregator that takes the same prefix of the concatenated partial outputs:
    #   head -n N (A ++ B) == head -n N (head -n N A ++ head -n N B)     (same for -c and with -z)
    # tested this against the command with random chunkings for -n, -c, -z -n; it holds for every NUM >= 0,
    # also when a chunk boundary falls inside a NUL-terminated record.
    # -n/-c with a leading '-' ("all but the last NUM") breaks the identity, so no parallelization then
    # -v, or more than one input file, prints "==> FILE <==" headers per part, so no parallelization then
    # -q and -z are passed through unchanged; -c vs -n: the last one given wins, the aggregator must keep the same order
    # the aggregator is `cat part1 ... partN | head <same flags>`, which is not the sequential command on
    # several operands (that would print NUM lines of *each* part), so it is a custom n-ary function

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]):
            return
        if self.does_flag_option_list_contain_at_least_one_of(["-v"]):
            return
        if self.get_operand_list_length() > 1:
            return
        for flag_option in self.get_flag_option_list_filtered_with(["-c", "-n"]):
            if isinstance(flag_option, Option) and str(flag_option.get_arg()).startswith("-"):
                return
        aggregator_spec = make_aggregator_spec_custom_n_ary_from_string_representation(
            cmd_inv_as_str='PLACEHOLDER:head_of_concatenation', is_implemented=False)
        parallelizer_cc_seq_cus = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc_seq_cus)
