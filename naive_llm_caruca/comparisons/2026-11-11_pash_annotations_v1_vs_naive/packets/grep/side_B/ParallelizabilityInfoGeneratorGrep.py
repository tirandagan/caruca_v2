from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import AdditionalInfoSplitterToMapper, make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import make_mapper_spec_custom
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import make_aggregator_spec_custom_2_ary_from_string_representation

class ParallelizabilityInfoGeneratorGrep(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(['-q', '--quiet', '--silent', '-m', '--max-count', '-A', '--after-context', '-B', '--before-context', '-C', '--context', '-z', '--null-data', '--help', '-V', '--version']):
            return
        mapper_spec = None
        aggregator_spec = None
        add_info_from_splitter = None
        if self.does_flag_option_list_contain_at_least_one_of(['-l', '--files-with-matches']):
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str='PLACEHOLDER:merge_keeping_longer_output', is_implemented=False)
            self.set_commutative()
        elif self.does_flag_option_list_contain_at_least_one_of(['-L', '--files-without-match']):
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str='PLACEHOLDER:merge_keeping_output_if_all_nonempty', is_implemented=False)
            self.set_commutative()
        elif self.does_flag_option_list_contain_at_least_one_of(['-c', '--count']):
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str='PLACEHOLDER:sum_indiv_results_up', is_implemented=False)
            self.set_commutative()
        elif self.does_flag_option_list_contain_at_least_one_of(['-n', '--line-number']) and self.does_flag_option_list_contain_at_least_one_of(['-b', '--byte-offset']):
            mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_line_number_and_byte_offset', is_implemented=False)
            add_info_from_splitter = AdditionalInfoSplitterToMapper.LINE_NUM_AND_BYTE_OFFSET
        elif self.does_flag_option_list_contain_at_least_one_of(['-n', '--line-number']):
            mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_line_number_offset', is_implemented=False)
            add_info_from_splitter = AdditionalInfoSplitterToMapper.LINE_NUM_OFFSET
        elif self.does_flag_option_list_contain_at_least_one_of(['-b', '--byte-offset']):
            mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_byte_offset', is_implemented=False)
            add_info_from_splitter = AdditionalInfoSplitterToMapper.BYTE_OFFSET
        if (mapper_spec is None or mapper_spec.is_implemented) and (aggregator_spec is None or aggregator_spec.is_implemented):
            self.append_to_parallelizer_list(make_parallelizer_consec_chunks(mapper_spec=mapper_spec, aggregator_spec=aggregator_spec, info_splitter_mapper=add_info_from_splitter))
            self.append_to_parallelizer_list(make_parallelizer_round_robin(mapper_spec=mapper_spec, aggregator_spec=aggregator_spec, info_splitter_mapper=add_info_from_splitter))
