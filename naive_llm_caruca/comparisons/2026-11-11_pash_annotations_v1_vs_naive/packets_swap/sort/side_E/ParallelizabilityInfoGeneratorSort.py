import shlex
from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import make_aggregator_spec_custom_2_ary_from_string_representation

class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):
    ORDERING_FLAGS = ['-b', '--ignore-leading-blanks', '-d', '--dictionary-order', '-f', '--ignore-case', '-g', '--general-numeric-sort', '-i', '--ignore-nonprinting', '-M', '--month-sort', '-h', '--human-numeric-sort', '-n', '--numeric-sort', '-R', '--random-sort', '-r', '--reverse', '-V', '--version-sort', '-s', '--stable', '-u', '--unique']
    ORDERING_OPTIONS = ['-k', '--key', '-t', '--field-separator', '--sort', '--random-source']

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(['-c', '-C', '--check', '-m', '--merge', '--debug', '-z', '--zero-terminated', '--files0-from']):
            return
        if self.does_flag_option_list_contain_at_least_one_of(['-R', '--random-sort']) and (not self.does_flag_option_list_contain_at_least_one_of(['--random-source'])):
            return
        if self.does_flag_option_list_contain_at_least_one_of(['--sort']) and (not self.does_flag_option_list_contain_at_least_one_of(['--random-source'])) and self._has_option_with_arg('--sort', 'random'):
            return
        aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str=self._merge_command_as_str(), is_implemented=True)
        self.append_to_parallelizer_list(make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec))
        if not self.does_flag_option_list_contain_at_least_one_of(['-s', '--stable', '-u', '--unique']):
            self.set_commutative()
            self.append_to_parallelizer_list(make_parallelizer_round_robin(aggregator_spec=aggregator_spec))

    def _merge_command_as_str(self) -> str:
        words = ['sort', '-m']
        for flag_option in self.get_flag_option_list_filtered_with(self.ORDERING_FLAGS + self.ORDERING_OPTIONS):
            name = self._name_of(flag_option)
            arg = self._arg_of(flag_option)
            words.append(name if arg is None else f'{name} {shlex.quote(str(arg))}')
        return ' '.join(words)

    def _has_option_with_arg(self, option_name: str, value: str) -> bool:
        for flag_option in self.get_flag_option_list_filtered_with([option_name]):
            if str(self._arg_of(flag_option)) == value:
                return True
        return False

    @staticmethod
    def _name_of(flag_option) -> str:
        if hasattr(flag_option, 'get_name'):
            return str(flag_option.get_name())
        return str(getattr(flag_option, 'name', flag_option))

    @staticmethod
    def _arg_of(flag_option):
        for attr in ('get_arg', 'get_option_arg'):
            if hasattr(flag_option, attr):
                return getattr(flag_option, attr)()
        for attr in ('option_arg', 'arg'):
            if hasattr(flag_option, attr):
                return getattr(flag_option, attr)
        return None
