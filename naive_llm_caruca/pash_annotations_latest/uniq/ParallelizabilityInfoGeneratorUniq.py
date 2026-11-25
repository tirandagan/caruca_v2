from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_adj_lines_func_from_string_representation


class ParallelizabilityInfoGeneratorUniq(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-D", "--all-repeated", "--group", "--group=separate", "--group=prepend",
    #                      "--group=append", "--group=both", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["-f", "-s", "-w"]

    # Which ones do affect parallelizability?
    # uniq only compares adjacent lines, so with consecutive chunks (CC) the only lines whose treatment
    # depends on another chunk are the ones at a chunk boundary; running the sequential command over the
    # last/first output lines of adjacent chunks (ADJS) yields exactly the sequential result.
    # This was checked against coreutils 9.4 for no flags and for -i, -f, -s, -w, --group, --group=separate.
    # Round-robin (RR) splitting is never correct: it makes non-adjacent lines adjacent.
    # -d, -D, --all-repeated: whether a boundary line is printed depends on lines that the other chunk
    #   already dropped (e.g. one "x" at the end of chunk 1 and one at the start of chunk 2 is a repeated
    #   line, but neither chunk prints it) -> infeasible with ADJS
    # -u: same problem in the other direction (a line dropped as repeated in chunk 1 can reappear as
    #   unique in chunk 2) -> infeasible with ADJS
    # --group=prepend/append/both: the group separator around the boundary group ends up in the wrong
    #   place -> infeasible with ADJS
    # -c: the counts of the boundary group must be summed -> custom aggregator over adjacent lines
    # -z: chunks and boundary lines are NUL- rather than newline-delimited; left out to be safe

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(
                ["-d", "-D", "--all-repeated", "-u", "-z",
                 "--group=prepend", "--group=append", "--group=both"]):
            if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
                # merge the boundary lines of adjacent chunks, summing the count prefix when the
                # lines (without their count) compare equal under the given -i/-f/-s/-w
                aggregator_spec = make_aggregator_spec_adj_lines_func_from_string_representation(
                    cmd_inv_as_str='PLACEHOLDER:uniq_merge_count_uniq', is_implemented=False)
                parallelizer_cc_seq_adjf = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
                self.append_to_parallelizer_list(parallelizer_cc_seq_adjf)
            else:
                # just apply the sequential command to the last and first line of adjacent chunks
                self.append_to_parallelizer_list_cc_seq_adjs()
