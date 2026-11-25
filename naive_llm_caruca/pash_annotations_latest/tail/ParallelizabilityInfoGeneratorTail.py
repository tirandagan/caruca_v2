import re

from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    AdditionalInfoSplitterToMapper, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import make_mapper_spec_custom
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_n_ary_from_string_representation
from pash_annotations.datatypes.BasicDatatypes import Option


class ParallelizabilityInfoGeneratorTail(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-f", "-F", "-q", "--retry", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n", "--max-unchanged-stats", "--pid", "-s"]

    # Which ones do affect parallelizability?
    # -f, -F, --pid, --retry, --max-unchanged-stats, -s: follow mode, tail never finishes reading
    #   -> no parallelization
    # -v, or several FILE operands: output contains "==> FILE <==" headers and is the tail of *each*
    #   file rather than of one stream -> no parallelization (tail treats its operands separately,
    #   so this is not the tail of the concatenated input)
    # -n NUM / -c NUM (default: -n 10), i.e. "the last NUM lines/bytes":
    #   CC x SEQ x custom n-ary aggregator: every chunk emits its last NUM lines/bytes; the last NUM
    #   lines/bytes of the concatenation of these (in order) is the sequential result. The
    #   aggregator must run tail over the *concatenation* of the parts
    #   (`cat part1 ... partN | tail <same -n/-c/-z>`); `tail part1 ... partN` would print the tail
    #   of each part, so the generic "sequential command over all parts" aggregator cannot be used.
    #   Verified against GNU coreutils 9.4 for -n, -c, -z and the default.
    #   RR is not applicable since the aggregator needs the parts in input order.
    # -n +NUM / -c +NUM, i.e. "everything from line/byte NUM on":
    #   needs a mapper that knows the line/byte offset of its chunk (skip only in the first chunk);
    #   recorded as a not-yet-implemented custom mapper.
    # If -n and -c are both given, the last one wins (GNU getopt behaviour, verified).
    # The obsolete `tail -NUM FILE` / `tail +NUM FILE` syntax reaches us as a first operand starting
    # with "-" or "+"; we do not parallelize it since the count is not available as an option.

    FOLLOW_FLAGS_OPTIONS = ["-f", "-F", "--pid", "--retry", "--max-unchanged-stats", "-s"]
    OBSOLETE_COUNT_OPERAND = re.compile(r'^[-+][0-9]+[bcl]?f?$')

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(self.FOLLOW_FLAGS_OPTIONS + ["--help", "--version", "-v"]):
            return
        if self.get_operand_list_length() > 1:
            return
        if self.get_operand_list_length() == 1 \
                and self.OBSOLETE_COUNT_OPERAND.match(self.get_first_operand_name_as_string()):
            return

        count_options = self.get_flag_option_list_filtered_with(["-n", "-c"])
        last_count_option = count_options[-1] if len(count_options) > 0 else None
        starts_from_num = last_count_option is not None \
            and isinstance(last_count_option, Option) \
            and str(last_count_option.get_arg()).startswith("+")

        if starts_from_num:
            # -n +NUM / -c +NUM: only the first chunk skips, later chunks are passed through unchanged
            if last_count_option.get_name() == "-c":
                mapper_spec = make_mapper_spec_custom('PLACEHOLDER:tail_skip_bytes_with_byte_offset', is_implemented=False)
                add_info_from_splitter = AdditionalInfoSplitterToMapper.BYTE_OFFSET
            else:
                mapper_spec = make_mapper_spec_custom('PLACEHOLDER:tail_skip_lines_with_line_num_offset', is_implemented=False)
                add_info_from_splitter = AdditionalInfoSplitterToMapper.LINE_NUM_OFFSET
            parallelizer_cc = make_parallelizer_consec_chunks(mapper_spec=mapper_spec,
                                                              info_splitter_mapper=add_info_from_splitter)
            self.append_to_parallelizer_list(parallelizer_cc)
        else:
            # last NUM lines/bytes: `cat part1 ... partN | tail <same -n/-c/-z options>`
            aggregator_spec = make_aggregator_spec_custom_n_ary_from_string_representation(
                cmd_inv_as_str='PLACEHOLDER:tail_of_concatenated_parts', is_implemented=False)
            parallelizer_cc = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
            self.append_to_parallelizer_list(parallelizer_cc)
