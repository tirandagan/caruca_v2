import shlex
from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import make_aggregator_spec_custom_n_ary_from_string_representation

class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(['-c', '-C', '--check', '-m', '--merge', '-R', '--random-sort', '--random-source', '--files0-from', '--debug', '--help', '--version']):
            return
        if 'random' in self._arguments_of(['--sort']):
            return
        aggregator_spec = make_aggregator_spec_custom_n_ary_from_string_representation(cmd_inv_as_str=self._merge_command_as_string(), is_implemented=True)
        self.append_to_parallelizer_list(make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec))
        if not self.does_flag_option_list_contain_at_least_one_of(['-s', '--stable', '-u', '--unique']):
            self.append_to_parallelizer_list(make_parallelizer_round_robin(aggregator_spec=aggregator_spec))

    def _merge_command_as_string(self) -> str:
        words = ['sort', '-m']
        for flag_option in self.cmd_inv.flag_option_list:
            name = _name_as_string(flag_option)
            if name in ['-o', '--output', '-m', '--merge']:
                continue
            words.append(name)
            arg = _argument_as_string(flag_option)
            if arg is not None:
                words.append(shlex.quote(arg))
        return ' '.join(words)

    def _arguments_of(self, names) -> list:
        return [_argument_as_string(flag_option) for flag_option in self.get_flag_option_list_filtered_with(names)]

def _name_as_string(flag_option) -> str:
    for attribute in ('get_name', 'name'):
        if hasattr(flag_option, attribute):
            name = getattr(flag_option, attribute)
            return name() if callable(name) else name
    return str(flag_option)

def _argument_as_string(option):
    arg = None
    for attribute in ('get_arg_as_string', 'get_arg', 'arg', 'option_arg', 'value'):
        if hasattr(option, attribute):
            arg = getattr(option, attribute)
            if callable(arg):
                arg = arg()
            break
    if arg is None:
        return None
    for attribute in ('get_name', 'name', 'raw', 'value'):
        if hasattr(arg, attribute):
            inner = getattr(arg, attribute)
            if callable(inner):
                inner = inner()
            if isinstance(inner, str):
                return inner
    return str(arg)
