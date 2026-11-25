from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation


class ParallelizabilityInfoGeneratorWc(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-m", "-l", "-L", "-w", "--debug", "--help", "--version"]
    # list_of_all_options = ["--files0-from", "--total"]

    # Which ones do affect parallelizability?
    # wc is a pure reduction: every selected count of the whole input is a function of the counts of its
    # parts, provided the parts are split at line boundaries (CC and RR both are), so that no word and no
    # line is cut in two. Lines (-l), words (-w), characters (-m) and bytes (-c) are summed over the parts,
    # the maximum display width (-L) is the maximum over the parts; the columns stay in wc's fixed order
    # newline, word, character, byte, maximum line length, so the aggregator only needs to know whether -L
    # is among the printed columns. As the parts arrive on stdin, no filename is printed for them.
    # --files0-from: the real inputs are listed inside F, nothing to split -> not parallelized
    # several file operands: wc prints one row per file plus a total row; the per-part aggregation above
    #   does not reproduce that layout -> only parallelized for a single input stream (0 or 1 operand)
    # --total: only changes the layout for several operands, so it does not matter for a single input
    # --debug: only prints diagnostics, no effect

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["--files0-from"]):
            return
        if self.get_operand_list_length() > 1:
            return
        if self.does_flag_option_list_contain_at_least_one_of(["-L"]):
            # sum all columns but the last one, which is the maximum over the parts
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
                cmd_inv_as_str='PLACEHOLDER:wc_sum_counts_max_line_length', is_implemented=False)
        else:
            # sum the columns of the two part results
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
                cmd_inv_as_str='PLACEHOLDER:wc_sum_counts', is_implemented=False)
        self.append_to_parallelizer_list(make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec))
        self.append_to_parallelizer_list(make_parallelizer_round_robin(aggregator_spec=aggregator_spec))
        # sum and max do not depend on the order of the parts
        self.set_commutative()
