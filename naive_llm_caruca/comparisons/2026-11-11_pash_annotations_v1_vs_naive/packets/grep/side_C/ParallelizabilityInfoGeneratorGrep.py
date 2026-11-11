from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorGrep(ParallelizabilityInfoGeneratorInterface):
    QUIET_FLAGS = ['-q', '--quiet', '--silent']
    MAX_COUNT_OPTIONS = ['-m', '--max-count']
    CONTEXT_OPTIONS = ['-A', '--after-context', '-B', '--before-context', '-C', '--context']
    CONTEXT_FLAGS = [f'-{digit}' for digit in '0123456789']
    PER_INPUT_OUTPUT_FLAGS = ['-c', '--count', '-l', '--files-with-matches', '-L', '--files-without-match', '-n', '--line-number', '-b', '--byte-offset']
    NULL_DATA_FLAGS = ['-z', '--null-data']
    PATTERN_OPTIONS = ['-e', '--regexp', '-f', '--file']
    RECURSIVE_FLAGS = ['-r', '-R', '--recursive', '--dereference-recursive']
    DIRECTORY_OPTIONS = ['-d', '--directories']
    DIRECTORY_ACTIONS = ['read', 'skip', 'recurse']

    def generate_info(self) -> None:
        if self.can_split_input():
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()

    def can_split_input(self) -> bool:
        if self.has_unrecognised_option():
            return False
        if self.does_flag_option_list_contain_at_least_one_of(self.QUIET_FLAGS + self.MAX_COUNT_OPTIONS + self.CONTEXT_OPTIONS + self.CONTEXT_FLAGS + self.PER_INPUT_OUTPUT_FLAGS + self.NULL_DATA_FLAGS):
            return False
        if self.is_recursive():
            return False
        if self.does_flag_option_list_contain_at_least_one_of(self.PATTERN_OPTIONS):
            file_count = self.get_operand_list_length()
        elif self.get_operand_list_length() > 0:
            file_count = self.get_operand_list_length() - 1
        else:
            return False
        return file_count <= 1

    def has_unrecognised_option(self) -> bool:
        return any((operand.get_name().startswith('-') and operand.get_name() != '-' for operand in self.cmd_inv.operand_list))

    def is_recursive(self) -> bool:
        recursive = False
        for flag_option in self.cmd_inv.flag_option_list:
            name = flag_option.get_name()
            if name in self.RECURSIVE_FLAGS:
                recursive = True
            elif name in self.DIRECTORY_OPTIONS:
                recursive = self.is_recursing_action(flag_option.get_arg())
        return recursive

    def is_recursing_action(self, action: str) -> bool:
        matches = [name for name in self.DIRECTORY_ACTIONS if name.startswith(action)]
        return matches == ['recurse']
