from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorTr(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-C", "-d", "-s", "-t", "-A", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # Without -s, tr is a pure byte-wise map/delete: every byte of the output depends only on the
    # corresponding input byte, so consecutive chunks can always be processed independently and
    # concatenated (CC x SEQ x CONC), even if newlines themselves are translated or deleted.
    # Round-robin splits and merges by line, so RR x SEQ x CONC is only safe when the arrays cannot
    # touch the newline character; we check this conservatively from the operand text.
    # With -s, squeezing a repeated character may span a part boundary. Boundaries of consecutive
    # chunks lie after a newline, so this only matters when the squeezed array may contain newline;
    #   - if it cannot: CC/RR x SEQ x CONC
    #   - if it may, but no translation takes place (-d given or a single operand): the command is
    #     idempotent, so re-running it over the boundary lines fixes the seam (CC/RR x SEQ x ADJS)
    #   - if it may and tr translates: not parallelised (re-running would re-translate the seam).
    # --help/--version produce no stream output: not parallelised.

    # Operand substrings that can denote the newline character (or a class containing it); a literal
    # newline is also checked. Any backslash escape is treated as suspicious (\n, \012, \12, ...).
    NEWLINE_INDICATORS = ["\\", "\n", "[:space:]", "[:cntrl:]"]

    def _operand_texts(self):
        texts = []
        for operand in self.cmd_inv.operand_list:
            name = operand.get_name() if hasattr(operand, "get_name") else operand
            texts.append(str(name))
        return texts

    def _arrays_may_involve_newline(self) -> bool:
        # complementing an array almost always puts the newline into it
        if self.does_flag_option_list_contain_at_least_one_of(["-c", "-C", "--complement"]):
            return True
        for text in self._operand_texts():
            if any(indicator in text for indicator in self.NEWLINE_INDICATORS):
                return True
        return False

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]):
            return
        newline_risk = self._arrays_may_involve_newline()
        squeezing = self.does_flag_option_list_contain_at_least_one_of(["-s", "--squeeze-repeats"])
        deleting = self.does_flag_option_list_contain_at_least_one_of(["-d", "--delete"])
        translating = (not deleting) and self.get_operand_list_length() >= 2

        if not squeezing:
            self.append_to_parallelizer_list_cc_seq_conc()
            if not newline_risk:
                self.append_to_parallelizer_list_rr_seq_conc()
        elif not newline_risk:
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
        elif not translating:
            # squeeze-only (or delete+squeeze) is idempotent: rerun tr on the boundary lines
            self.append_to_parallelizer_list_cc_seq_adjs()
            self.append_to_parallelizer_list_rr_seq_adjs()
        else:
            pass  # translation plus squeezing of a possibly-newline array: keep sequential
