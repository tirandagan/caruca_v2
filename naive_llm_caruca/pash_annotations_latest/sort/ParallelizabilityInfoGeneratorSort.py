import shlex

from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_n_ary_from_string_representation


class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-d", "-f", "-g", "-i", "-M", "-h", "-n", "-R", "-r", "-V", "-c", "-C", "--check",
    #                      "--debug", "-m", "-s", "-u", "-z", "-y", "--help", "--version"]
    # list_of_all_options = ["--random-source", "--sort", "--batch-size", "--compress-program", "--files0-from",
    #                        "-k", "-o", "-S", "-t", "-T", "--parallel"]

    # Which ones do affect parallelizability?
    # base-line: sort each part with the sequential command and merge the sorted parts with `sort -m`
    #   carrying the same ordering options (-b -d -f -g -i -M -h -n -r -V -k -t -z -u -s, --sort);
    #   without -s, sort's last-resort whole-line comparison makes the output of CC and RR deterministic
    # -s/--stable and -u/--unique: which of several lines with equal keys comes first/is kept depends on
    #   input order, which RR destroys but CC preserves; so only CC
    # -c/-C/--check: no output, only an exit status; not parallelized
    # -m/--merge: the inputs are already sorted and merging is a linear pass; nothing to gain
    # -R/--random-sort, --sort=random, --random-source: the hash salt differs between the mappers and
    #   the merger, so identical keys would not stay grouped; not parallelized
    # --files0-from: the inputs are not operands; not parallelized
    # --debug: annotation lines interleaved with the output; not parallelized
    # -o/--output: writes to a file instead of stdout, which does not change how the stream is split
    # -S, -T, --batch-size, --compress-program, --parallel: resource tuning only, forwarded to the merger

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(
                ["-c", "-C", "--check", "-m", "--merge", "-R", "--random-sort", "--random-source",
                 "--files0-from", "--debug", "--help", "--version"]):
            return
        if "random" in self._arguments_of(["--sort"]):
            return
        aggregator_spec = make_aggregator_spec_custom_n_ary_from_string_representation(
            cmd_inv_as_str=self._merge_command_as_string(), is_implemented=True)
        self.append_to_parallelizer_list(make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec))
        if not self.does_flag_option_list_contain_at_least_one_of(["-s", "--stable", "-u", "--unique"]):
            self.append_to_parallelizer_list(make_parallelizer_round_robin(aggregator_spec=aggregator_spec))

    def _merge_command_as_string(self) -> str:
        # `sort -m` with every option of the original invocation except the output file,
        # so that the merge compares lines exactly as the mappers did;
        # arguments are shell-quoted since a field separator may be a blank
        words = ["sort", "-m"]
        for flag_option in self.cmd_inv.flag_option_list:
            name = _name_as_string(flag_option)
            if name in ["-o", "--output", "-m", "--merge"]:
                continue
            words.append(name)
            arg = _argument_as_string(flag_option)
            if arg is not None:
                words.append(shlex.quote(arg))
        return " ".join(words)

    def _arguments_of(self, names) -> list:
        return [_argument_as_string(flag_option) for flag_option in self.get_flag_option_list_filtered_with(names)]


def _name_as_string(flag_option) -> str:
    for attribute in ("get_name", "name"):
        if hasattr(flag_option, attribute):
            name = getattr(flag_option, attribute)
            return name() if callable(name) else name
    return str(flag_option)


def _argument_as_string(option):
    # returns None for a flag; the option argument is wrapped in an ArgStringType,
    # take its text whichever accessor the datatype offers
    arg = None
    for attribute in ("get_arg_as_string", "get_arg", "arg", "option_arg", "value"):
        if hasattr(option, attribute):
            arg = getattr(option, attribute)
            if callable(arg):
                arg = arg()
            break
    if arg is None:
        return None
    for attribute in ("get_name", "name", "raw", "value"):
        if hasattr(arg, attribute):
            inner = getattr(arg, attribute)
            if callable(inner):
                inner = inner()
            if isinstance(inner, str):
                return inner
    return str(arg)
