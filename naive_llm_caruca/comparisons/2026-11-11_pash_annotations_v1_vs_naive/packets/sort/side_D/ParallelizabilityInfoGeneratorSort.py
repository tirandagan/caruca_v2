from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import make_aggregator_spec_custom_2_ary_from_string_representation

class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):
    non_parallelizable = ['-c', '-C', '--check', '-m', '--merge', '-R', '--random-sort', '--debug', '-o', '--output', '-z', '--zero-terminated', '--files0-from', '--help', '--version']
    ordering_options = ['-b', '--ignore-leading-blanks', '-d', '--dictionary-order', '-f', '--ignore-case', '-g', '--general-numeric-sort', '-i', '--ignore-nonprinting', '-M', '--month-sort', '-h', '--human-numeric-sort', '-n', '--numeric-sort', '-r', '--reverse', '-V', '--version-sort', '--sort', '-k', '--key', '-t', '--field-separator', '-s', '--stable', '-u', '--unique']

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(self.non_parallelizable):
            return
        if self.sorts_randomly():
            return
        aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str=self.merge_command_as_string(), is_implemented=True)
        parallelizer_cc = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc)
        if not self.does_flag_option_list_contain_at_least_one_of(['-s', '--stable', '-u', '--unique']):
            parallelizer_rr = make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
            self.append_to_parallelizer_list(parallelizer_rr)
            self.set_commutative()

    def sorts_randomly(self) -> bool:
        for flag_option in self.get_flag_option_list_filtered_with(['--sort']):
            if str(self._arg_of(flag_option)) == 'random':
                return True
        return False

    def merge_command_as_string(self) -> str:
        words = ['sort', '-m']
        for flag_option in self.get_flag_option_list_filtered_with(self.ordering_options):
            words.append(self._name_of(flag_option))
            arg = self._arg_of(flag_option)
            if arg is not None:
                words.append(str(arg))
        return ' '.join(words)

    @staticmethod
    def _name_of(flag_option) -> str:
        if hasattr(flag_option, 'get_name'):
            return str(flag_option.get_name())
        return str(getattr(flag_option, 'name', flag_option))

    @staticmethod
    def _arg_of(flag_option):
        if hasattr(flag_option, 'get_arg'):
            return flag_option.get_arg()
        return getattr(flag_option, 'option_arg', None)
