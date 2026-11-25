import re

from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTail(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-f", "-F", "-q", "--retry", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n", "--max-unchanged-stats", "--pid", "-s"]

    # Which ones do affect input/output?
    # none: every FILE operand is read as a stream (a lone "-" is stdin), stdin is read when no FILE
    # is given, and everything (including the "==> FILE <==" headers for -v / several files) goes to
    # stdout. -f/-F/--pid/--retry only change *how long* the inputs are read, not which they are.
    # We assume --help/--version are not given (then nothing is read and only usage text is printed).

    # The obsolete syntax `tail -NUM FILE` / `tail +NUM FILE` (optionally with a b/c/l unit and f
    # suffix, e.g. `tail -5c FILE`) is not in the parser table, so the parser hands "-5" to us as the
    # first operand. tail only accepts it with at most one FILE after it; with more operands it is
    # either rejected ("-NUM") or taken literally as a file name ("+NUM").
    OBSOLETE_COUNT_OPERAND = re.compile(r'^[-+][0-9]+[bcl]?f?$')

    def is_first_operand_obsolete_count(self) -> bool:
        return self.get_operand_list_length() in (1, 2) \
            and self.OBSOLETE_COUNT_OPERAND.match(self.get_first_operand_name_as_string()) is not None

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        if self.is_first_operand_obsolete_count():
            # e.g. `tail -5` or `tail -5 FILE`: the first operand is a count, not a file
            self.set_first_operand_as_config_arg_type_string()
            if self.get_operand_list_length() == 1:
                self.set_implicit_use_of_stdin()
            else:
                self.all_but_first_operand_is_streaming_input()
        else:
            self.if_no_operands_given_stdin_implicitly_used()
            self.all_operands_are_streaming_inputs()
