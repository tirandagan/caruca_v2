from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation


class ParallelizabilityInfoGeneratorHead(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect parallelizability?
    # head keeps a prefix of its input, so order matters: RR is never valid.
    # CC x SEQ x <head itself over the concatenated partial outputs> is correct
    # for a non-negative NUM: the first NUM lines (bytes) of the whole input are
    # the first NUM lines (bytes) of the concatenation of the first NUM lines
    # (bytes) of each consecutive chunk. The aggregator is the same invocation
    # applied pairwise, which is associative, hence a 2-ary custom aggregator.
    # A leading '-' in NUM ("all but the last NUM") removes lines from the end
    # of every chunk instead of only from the end of the input: not parallelizable.
    # -v (or more than one operand) adds "==> name <==" headers per chunk: not
    # parallelizable.
    # -z only changes the line delimiter and does not matter; -q does not matter.

    NUM_OPTIONS = ["-c", "--bytes", "-n", "--lines"]

    def _num_option_values(self):
        values = []
        for flag_option in self.cmd_inv.flag_option_list:
            name = getattr(flag_option, "name", None)
            if name is None:
                name = str(flag_option)
            if name in self.NUM_OPTIONS:
                arg = getattr(flag_option, "option_arg", None)
                values.append(str(arg) if arg is not None else "")
        return values

    def generate_info(self) -> None:
        if self.get_operand_list_length() > 1:
            return
        if self.does_flag_option_list_contain_at_least_one_of(["-v", "--help", "--version"]):
            return
        if any(value.lstrip().startswith("-") for value in self._num_option_values()):
            return
        aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
            cmd_inv_as_str='PLACEHOLDER:head_rerun_on_concatenated_outputs', is_implemented=False)
        parallelizer_cc_seq_head = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc_seq_head)
