from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers
from pash_annotations.annotation_generation.datatypes.parallelizability.TransformerFlagOptionList import \
    make_transformer_add, make_transformer_remove, ChainTransformerFlagOptionList
from pash_annotations.datatypes.BasicDatatypes import Flag


class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-d", "-f", "-g", "-i", "-M", "-h", "-n", "-R", "-r", "-V", "-c", "-C", "--debug",
    #                      "-m", "-s", "-u", "-y", "-z", "--help", "--version"]
    # list_of_all_options = ["--random-source", "--sort", "--batch-size", "--compress-program", "--files0-from",
    #                        "-k", "-o", "-S", "-t", "-T", "--parallel"]

    # Which ones do affect parallelizability?
    # base-line: CC x SEQ x custom 2-ary aggregator `sort -m <same ordering flags/options>`
    #   sorting each consecutive chunk with the original invocation and merging the sorted chunks with `sort -m`
    #   under the same ordering options yields the same output as the sequential sort (verified against the binary
    #   for -b -d -f -g -i -M -h -n -r -V --sort -k -t -s -u and combinations thereof).
    #   `sort -m` is stable w.r.t. the order of its inputs, so -s and -u (which implies -s) are fine with consecutive
    #   chunks; they would not be with round-robin, and round-robin is in any case only allowed with adj-lines
    #   aggregators by the Parallelizer datatype, so only CC is offered.
    # -R/--sort=random: the hash seed differs per process, so independently shuffled chunks cannot be merged;
    #   with --random-source the seed is fixed and merging is correct again.
    # -c/-C/--check: checks instead of sorting, output is only an exit status/diagnostic -> not parallelised.
    # -m: the input is already sorted and merely merged -> nothing to gain, not parallelised.
    # -z: records are NUL-terminated, but PaSh's splitters cut at newlines -> not parallelised.
    # --debug: annotations interleaved with the output -> not parallelised.
    # -o FILE: output is a file rather than stdout; the custom aggregator's output substitution assumes stdout
    #   -> not parallelised (conservative).
    # --files0-from: inputs come from a list file, not from operands/stdin -> not parallelised.
    # -S, -T, --parallel, --batch-size, --compress-program, -y: performance/compatibility only; kept on the aggregator
    #   except -T/-S/--parallel/--batch-size/--compress-program, which are removed since the merge of two parts
    #   needs no large buffers or temporaries.

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(
                ["-c", "-C", "-m", "-z", "--debug", "-o", "--files0-from"]):
            return
        random_sort_requested = self.does_flag_option_list_contain_at_least_one_of(["-R"]) or \
            any(option.get_arg() == "random"
                for option in self.get_flag_option_list_filtered_with(["--sort"]))
        if random_sort_requested and not self.does_flag_option_list_contain_at_least_one_of(["--random-source"]):
            return
        # aggregator: the original invocation with -m added and resource options dropped
        transformer = ChainTransformerFlagOptionList([
            make_transformer_remove(["-S", "-T", "--parallel", "--batch-size", "--compress-program"]),
            make_transformer_add([Flag("-m")]),
        ])
        aggregator_spec = make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers(
            flag_option_list_transformer=transformer, is_implemented=True)
        parallelizer_cc_seq_merge = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc_seq_merge)
        # without -s (or -u, which implies -s) the last-resort comparison makes the result independent of input order
        if not self.does_flag_option_list_contain_at_least_one_of(["-s", "-u"]):
            self.set_commutative()
