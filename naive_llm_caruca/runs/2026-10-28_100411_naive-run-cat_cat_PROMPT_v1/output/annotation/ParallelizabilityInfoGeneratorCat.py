from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    AdditionalInfoSplitterToMapper, make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import make_mapper_spec_custom


class ParallelizabilityInfoGeneratorCat(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "-n", "-s", "-t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # base-line: cat is a per-line transformation, so IF/CC/RR x SEQ x CONC
    # -A, -e, -E, -t, -T, -v only rewrite each line in isolation -> no effect
    # -u is ignored by GNU cat -> no effect
    # -n numbers lines continuously across all input files, so the mapper needs the line-number offset of its part
    #    (tested: `cat -n f g` continues numbering into g) -> CC/RR with a custom mapper, no IF
    # -b numbers only non-empty lines; the splitter cannot provide that offset -> not parallelized
    # -s squeezes repeated empty lines also across part/file boundaries -> CC/RR with ADJS (the sequential
    #    command over the boundary lines merges two adjacent empty lines back into one), no IF
    # -n together with -s: the offset would have to be the squeezed line count -> not parallelized

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-b"]):
            # -b overrides -n; offset of non-empty lines is not available from the splitter
            pass
        elif self.does_flag_option_list_contain_at_least_one_of(["-n"]):
            if not self.does_flag_option_list_contain_at_least_one_of(["-s"]):
                mapper_spec = make_mapper_spec_custom('PLACEHOLDER:cat_add_line_number_offset',
                                                      is_implemented=False)
                parallelizer_cc = make_parallelizer_consec_chunks(mapper_spec=mapper_spec,
                                                                  info_splitter_mapper=AdditionalInfoSplitterToMapper.LINE_NUM_OFFSET)
                self.append_to_parallelizer_list(parallelizer_cc)
                parallelizer_rr = make_parallelizer_round_robin(mapper_spec=mapper_spec,
                                                                info_splitter_mapper=AdditionalInfoSplitterToMapper.LINE_NUM_OFFSET)
                self.append_to_parallelizer_list(parallelizer_rr)
        elif self.does_flag_option_list_contain_at_least_one_of(["-s"]):
            # just apply the sequential command to the last and first line of adjacent parts
            self.append_to_parallelizer_list_cc_seq_adjs()
            self.append_to_parallelizer_list_rr_seq_adjs()
        else:
            self.append_to_parallelizer_list_if_seq_conc()
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
