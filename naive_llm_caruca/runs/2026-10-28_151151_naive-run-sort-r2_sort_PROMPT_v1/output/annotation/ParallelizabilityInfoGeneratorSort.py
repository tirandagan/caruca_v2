import shlex

from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation


class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-d", "-f", "-g", "-i", "-M", "-h", "-n", "-R", "-r", "-V", "-c", "-C",
    #                      "--debug", "-m", "-s", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--random-source", "--sort", "--batch-size", "--compress-program", "--files0-from",
    #                        "-k", "-o", "-S", "-t", "-T", "--parallel"]

    # Which ones do affect parallelizability?
    # base-line: sort each part with the sequential command, then merge the sorted parts with
    #   `sort -m <same ordering options>`; this is exact for CC (tested with all ordering flags, -k, -t, -u, -s)
    # -s and -u disable the last-resort comparison, so equal keys keep their input order:
    #   CC + stable merge still reproduces this, RR does not (tested) -> only CC
    # -R without --random-source seeds the hash per process, parts cannot be merged consistently -> none
    # -c/-C/--check: no sorting, exit status semantics over the whole input -> none
    # -m: input is already sorted, nothing to parallelize -> none
    # --debug writes per-process annotations to stderr, -z changes the record delimiter the splitters use -> none
    # --files0-from: the inputs are listed in a file, not given as operands/stdin -> none
    # -o, -S, -T, --parallel, --batch-size, --compress-program do not change the result;
    #   they are dropped from the aggregator so that it writes to stdout and keeps the default resources

    # ordering options that must be repeated for the merge step
    ORDERING_FLAGS = ["-b", "--ignore-leading-blanks", "-d", "--dictionary-order", "-f", "--ignore-case",
                      "-g", "--general-numeric-sort", "-i", "--ignore-nonprinting", "-M", "--month-sort",
                      "-h", "--human-numeric-sort", "-n", "--numeric-sort", "-R", "--random-sort",
                      "-r", "--reverse", "-V", "--version-sort", "-s", "--stable", "-u", "--unique"]
    ORDERING_OPTIONS = ["-k", "--key", "-t", "--field-separator", "--sort", "--random-source"]

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(
                ["-c", "-C", "--check", "-m", "--merge", "--debug", "-z", "--zero-terminated", "--files0-from"]):
            return
        if self.does_flag_option_list_contain_at_least_one_of(["-R", "--random-sort"]) \
                and not self.does_flag_option_list_contain_at_least_one_of(["--random-source"]):
            return
        if self.does_flag_option_list_contain_at_least_one_of(["--sort"]) \
                and not self.does_flag_option_list_contain_at_least_one_of(["--random-source"]) \
                and self._has_option_with_arg("--sort", "random"):
            return
        aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
            cmd_inv_as_str=self._merge_command_as_str(), is_implemented=True)
        self.append_to_parallelizer_list(make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec))
        if not self.does_flag_option_list_contain_at_least_one_of(["-s", "--stable", "-u", "--unique"]):
            # without -s/-u the result is a total order of the lines, so parts may arrive in any order
            self.set_commutative()
            self.append_to_parallelizer_list(make_parallelizer_round_robin(aggregator_spec=aggregator_spec))

    def _merge_command_as_str(self) -> str:
        words = ["sort", "-m"]
        for flag_option in self.get_flag_option_list_filtered_with(self.ORDERING_FLAGS + self.ORDERING_OPTIONS):
            name = self._name_of(flag_option)
            arg = self._arg_of(flag_option)
            words.append(name if arg is None else f"{name} {shlex.quote(str(arg))}")
        return " ".join(words)

    def _has_option_with_arg(self, option_name: str, value: str) -> bool:
        for flag_option in self.get_flag_option_list_filtered_with([option_name]):
            if str(self._arg_of(flag_option)) == value:
                return True
        return False

    @staticmethod
    def _name_of(flag_option) -> str:
        if hasattr(flag_option, "get_name"):
            return str(flag_option.get_name())
        return str(getattr(flag_option, "name", flag_option))

    @staticmethod
    def _arg_of(flag_option):
        for attr in ("get_arg", "get_option_arg"):
            if hasattr(flag_option, attr):
                return getattr(flag_option, attr)()
        for attr in ("option_arg", "arg"):
            if hasattr(flag_option, attr):
                return getattr(flag_option, attr)
        return None
