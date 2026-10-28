from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    AdditionalInfoSplitterToMapper, make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import make_mapper_spec_custom
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation


class ParallelizabilityInfoGeneratorGrep(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "-V", "-E", "-F", "-G", "-P", "-i", "-y", "--no-ignore-case", "-v", "-w",
    #                      "-x", "-c", "--color", "-L", "-l", "-o", "-q", "-s", "-b", "-u", "-H", "-h", "-n",
    #                      "-T", "-Z", "--no-group-separator", "-a", "-I", "-r", "-R", "--line-buffered",
    #                      "-U", "-z"]
    # list_of_all_options = ["-e", "-f", "-m", "--label", "-A", "-B", "-C", "--group-separator",
    #                        "--binary-files", "-D", "-d", "--include", "--exclude", "--exclude-from",
    #                        "--exclude-dir"]

    # Which ones do affect parallelizability?  (checked against GNU grep 3.11)
    # grep is line-by-line, so by default RR/CC x SEQ x CONC is exact.
    # -q: output is empty and grep stops reading at the first match; nothing to parallelize
    # -z: records end in NUL, not newline, so the line-based splitters would cut records; no parallelization
    # -A, -B, -C: context crosses part boundaries and group separators depend on adjacency; no parallelization
    # -m: the limit applies to the whole input, not per part; no parallelization
    # -L, -l: each part prints either nothing or the (same) file name; keep the non-empty one
    #         (-L and -l overrule -c, which overrules -b and -n; the binary accepts them together)
    # -c: the per-part counts have to be summed
    # -n, -b: the mapper needs the line-number / byte offset at which its part starts
    #         (-n output always precedes -b output, so one mapper handles both)
    # -o with -b prints the offset of the match, still shifted by the part's byte offset
    # -v, -w, -x, -i, -E/-F/-G/-P, -H/-h, --label, -T, -Z, -s, --color are per line and need nothing

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-q", "-z", "-A", "-B", "-C", "-m"]):
            return
        mapper_spec = None
        aggregator_spec = None
        add_info_from_splitter = None
        if self.does_flag_option_list_contain_at_least_one_of(["-L", "-l"]):
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
                cmd_inv_as_str='PLACEHOLDER:merge_keeping_longer_output', is_implemented=False)
        elif self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
                cmd_inv_as_str='PLACEHOLDER:sum_indiv_results_up', is_implemented=False)
        elif self.does_flag_option_list_contain_at_least_one_of(["-n"]) \
                and self.does_flag_option_list_contain_at_least_one_of(["-b"]):
            mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_line_number_and_byte_offset',
                                                  is_implemented=False)
            add_info_from_splitter = AdditionalInfoSplitterToMapper.LINE_NUM_AND_BYTE_OFFSET
        elif self.does_flag_option_list_contain_at_least_one_of(["-n"]):
            mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_line_number_offset',
                                                  is_implemented=False)
            add_info_from_splitter = AdditionalInfoSplitterToMapper.LINE_NUM_OFFSET
        elif self.does_flag_option_list_contain_at_least_one_of(["-b"]):
            mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_byte_offset',
                                                  is_implemented=False)
            add_info_from_splitter = AdditionalInfoSplitterToMapper.BYTE_OFFSET
        # mapper_spec None becomes SEQ and aggregator_spec None becomes CONC
        # placeholders are skipped until they are implemented
        if (mapper_spec is None or mapper_spec.is_implemented) and \
                (aggregator_spec is None or aggregator_spec.is_implemented):
            parallelizer_cc = make_parallelizer_consec_chunks(mapper_spec=mapper_spec,
                                                              aggregator_spec=aggregator_spec,
                                                              info_splitter_mapper=add_info_from_splitter)
            self.append_to_parallelizer_list(parallelizer_cc)
            parallelizer_rr = make_parallelizer_round_robin(mapper_spec=mapper_spec,
                                                            aggregator_spec=aggregator_spec,
                                                            info_splitter_mapper=add_info_from_splitter)
            self.append_to_parallelizer_list(parallelizer_rr)
