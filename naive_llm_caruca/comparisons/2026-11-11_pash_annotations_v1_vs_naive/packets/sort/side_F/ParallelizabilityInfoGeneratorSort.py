from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers
from pash_annotations.annotation_generation.datatypes.parallelizability.TransformerFlagOptionList import make_transformer_add, make_transformer_remove, ChainTransformerFlagOptionList
from pash_annotations.datatypes.BasicDatatypes import Flag

class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(['-c', '-C', '-m', '-z', '--debug', '-o', '--files0-from']):
            return
        random_sort_requested = self.does_flag_option_list_contain_at_least_one_of(['-R']) or any((option.get_arg() == 'random' for option in self.get_flag_option_list_filtered_with(['--sort'])))
        if random_sort_requested and (not self.does_flag_option_list_contain_at_least_one_of(['--random-source'])):
            return
        transformer = ChainTransformerFlagOptionList([make_transformer_remove(['-S', '-T', '--parallel', '--batch-size', '--compress-program']), make_transformer_add([Flag('-m')])])
        aggregator_spec = make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers(flag_option_list_transformer=transformer, is_implemented=True)
        parallelizer_cc_seq_merge = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc_seq_merge)
        if not self.does_flag_option_list_contain_at_least_one_of(['-s', '-u']):
            self.set_commutative()
