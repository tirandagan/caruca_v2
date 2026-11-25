from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    AdditionalInfoSplitterToMapper, make_parallelizer_round_robin, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import make_mapper_spec_custom


class ParallelizabilityInfoGeneratorPr(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-c", "-d", "-e", "-F", "-f", "-i", "-J", "-m", "-n", "-r", "-s", "-S",
    #                      "-t", "-T", "-v", "-1".."-9", "--help", "--version"]
    # list_of_all_options = ["--pages", "--columns", "-D", "-h", "-l", "-N", "-o", "-w", "-W"]

    # Which ones do affect parallelizability?
    # pr paginates: without -t/-T every page gets a header (date, file name, page number) and trailer,
    # so the output of a chunk depends on where in the input it starts -> no parallelization.
    # With -t or -T (headers and trailers omitted) and none of the options below, pr is a per-line
    # transformation (tab expansion -e/-i, control chars -c/-v, double spacing -d, indent -o,
    # truncation -W, -F/-f, -J, -s/-S have no effect without columns) and CC/RR x SEQ x CONC is exact
    # (verified against the binary with chunked input).
    # -l PAGE_LENGTH <= 10 implies -t, but we only look at the flags and thus under-approximate.
    # Not parallelizable:
    #   -COLUMN/--columns and -a: columns are balanced per page, depends on the whole page
    #   +FIRST[:LAST]/--pages: selects pages, depends on absolute position
    #   -m: merges the files side by side, every file is read in parallel
    #   -n: line numbers restart in each part; would need a mapper that passes the offset via -N

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-t", "-T"]) and \
                not self.does_flag_option_list_contain_at_least_one_of(
                    ["-m", "-a", "--pages", "--columns",
                     "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9"]):
            mapper_spec = None
            add_info_from_splitter = None
            if self.does_flag_option_list_contain_at_least_one_of(["-n"]):
                # pr -N <offset+1> on each part would give the correct numbering
                mapper_spec = make_mapper_spec_custom('PLACEHOLDER:pr_add_line_number_offset',
                                                      is_implemented=False)
                add_info_from_splitter = AdditionalInfoSplitterToMapper.LINE_NUM_OFFSET
            # mapper_spec None becomes seq, aggregator conc
            if mapper_spec is None or mapper_spec.is_implemented:
                parallelizer_cc = make_parallelizer_consec_chunks(mapper_spec=mapper_spec,
                                                                  info_splitter_mapper=add_info_from_splitter)
                self.append_to_parallelizer_list(parallelizer_cc)
                parallelizer_rr = make_parallelizer_round_robin(mapper_spec=mapper_spec,
                                                                info_splitter_mapper=add_info_from_splitter)
                self.append_to_parallelizer_list(parallelizer_rr)
