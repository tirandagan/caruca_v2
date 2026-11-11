from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import make_aggregator_spec_custom_2_ary_from_string_representation

class ParallelizabilityInfoGeneratorWc(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(['--files0-from']):
            return
        if self.get_operand_list_length() > 1:
            return
        if self.does_flag_option_list_contain_at_least_one_of(['-L']):
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str='PLACEHOLDER:wc_sum_counts_max_line_length', is_implemented=False)
        else:
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str='PLACEHOLDER:wc_sum_counts', is_implemented=False)
        self.append_to_parallelizer_list(make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec))
        self.append_to_parallelizer_list(make_parallelizer_round_robin(aggregator_spec=aggregator_spec))
        self.set_commutative()
