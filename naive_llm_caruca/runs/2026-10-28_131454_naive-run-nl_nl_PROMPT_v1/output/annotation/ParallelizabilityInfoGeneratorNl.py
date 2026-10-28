from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import \
    AdditionalInfoSplitterToMapper, make_parallelizer_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import make_mapper_spec_custom


class ParallelizabilityInfoGeneratorNl(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-p", "--help", "--version"]
    # list_of_all_options = ["-b", "-d", "-f", "-h", "-i", "-l", "-n", "-s", "-v", "-w"]

    # Which ones do affect parallelizability?
    # nl numbers lines by their position in the whole input (numbering continues across FILE
    # boundaries), so the sequential command on a part never gives the right numbers: no SEQ mapper,
    # and no round-robin at all (a mapper would need the global index of every single line).
    # Consecutive chunks work with a custom mapper that is told the line-number offset of its chunk,
    # but only if the offset of raw lines is exactly the offset of numbered lines, i.e.
    #   - every body line is numbered: -b a (default is -b t, which skips empty lines; -b pBRE
    #     numbers only matching lines) -> the mapper cannot know how many lines before its chunk
    #     were numbered,
    #   - blank lines are not grouped: -l 1 (the default), since a group may straddle a chunk boundary,
    #   - section matching is disabled: -d '' (GNU extension), since a chunk may begin inside a
    #     header/footer section (different style, and numbering restarts at each section unless -p),
    #     which the mapper cannot know; with sections disabled -h, -f and -p have no effect.
    # -v, -i, -w, -n, -s only change how numbers are rendered; the mapper computes
    # v + i * offset as the first number of its chunk and renders like the sequential command.

    def generate_info(self) -> None:
        body_styles = self._get_option_values(["-b", "--body-numbering"])
        delimiters = self._get_option_values(["-d", "--section-delimiter"])
        join_blank = self._get_option_values(["-l", "--join-blank-lines"])
        all_body_lines_numbered = len(body_styles) > 0 and body_styles[-1] == "a"
        sections_disabled = len(delimiters) > 0 and delimiters[-1] == ""
        blank_lines_not_grouped = all(value.strip() == "1" for value in join_blank)
        if all_body_lines_numbered and sections_disabled and blank_lines_not_grouped:
            mapper_spec = make_mapper_spec_custom('PLACEHOLDER:nl_add_line_number_offset',
                                                  is_implemented=False)
            parallelizer_cc = make_parallelizer_consec_chunks(
                mapper_spec=mapper_spec,
                info_splitter_mapper=AdditionalInfoSplitterToMapper.LINE_NUM_OFFSET)
            self.append_to_parallelizer_list(parallelizer_cc)
        # otherwise: not parallelizable

    def _get_option_values(self, names) -> list:
        # the argument strings of the given options, in command-line order
        values = []
        for flag_option in self.cmd_inv.flag_option_list:
            if flag_option.get_name() not in names:
                continue
            arg = flag_option.get_arg() if hasattr(flag_option, "get_arg") else getattr(flag_option, "option_arg", None)
            if arg is None:
                continue
            raw = getattr(arg, "raw_str", None)
            values.append(raw if isinstance(raw, str) else str(arg))
        return values
