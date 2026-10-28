from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation


class ParallelizabilityInfoGeneratorHead(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect parallelizability?
    # head keeps a prefix of its input, so it is only parallelizable over consecutive chunks (CC),
    # never round-robin (RR): the dealt-out lines could not be put back in order.
    # With CC x SEQ, the first NUM lines/bytes of the whole input are the first NUM lines/bytes of the
    # concatenation of the per-chunk results, so the aggregator is the sequential command itself
    # applied to two adjacent results (associative, hence usable as a 2-ary merge).
    # Cases where this breaks and we do not parallelize:
    # - a leading '-' in NUM ("all but the last NUM"): each chunk would drop NUM at its own end
    # - -v, or more than one operand: "==> FILE <==" headers would be repeated per chunk
    # - -z: records are NUL-terminated, the line-based splitter would cut inside records
    # Note that head reads only a prefix of the input anyway, so parallelization is rarely a win;
    # the aggregator is therefore only given as a placeholder.

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-v", "-z", "--help", "--version"]):
            return
        if self.get_operand_list_length() > 1:
            return
        if self._any_num_option_is_negative():
            return
        aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
            cmd_inv_as_str='PLACEHOLDER:head_apply_seq_to_concatenation', is_implemented=False)
        parallelizer_cc_seq_agg = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc_seq_agg)

    def _any_num_option_is_negative(self) -> bool:
        # the argument of -c/-n is "[-]NUM"; be conservative and treat an argument whose
        # text we cannot recover as negative
        for flag_option in self.get_flag_option_list_filtered_with(["-c", "-n"]):
            arg_text = self._option_arg_as_string(flag_option)
            if arg_text is None or arg_text.strip().startswith("-"):
                return True
        return False

    @staticmethod
    def _option_arg_as_string(flag_option):
        option_arg = getattr(flag_option, "option_arg", None)
        if option_arg is None:
            return None
        if isinstance(option_arg, str):
            return option_arg
        for getter in ("get_name", "get_name_as_string"):
            if hasattr(option_arg, getter):
                return str(getattr(option_arg, getter)())
        if hasattr(option_arg, "name"):
            return str(option_arg.name)
        return None
