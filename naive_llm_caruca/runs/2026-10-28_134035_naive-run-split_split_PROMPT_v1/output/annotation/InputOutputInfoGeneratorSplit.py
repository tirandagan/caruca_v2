from typing import List

from pash_annotations.datatypes.BasicDatatypes import FlagOption, WhichClassForArg
from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSplit(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-d", "-x", "-e", "-u", "--verbose", "--help", "--version"]
    # list_of_all_options = ["-a", "--additional-suffix", "-b", "-C", "--filter", "-l", "-n", "-t"]

    # split [OPTION]... [FILE [PREFIX]]
    #
    # Input: FILE (or stdin when absent or '-'), always read as a stream.
    #
    # Output depends on -n CHUNKS (tested with GNU coreutils 9.4):
    #   - CHUNKS of the form K/N, l/K/N or r/K/N: the Kth chunk is written to stdout,
    #     no files are created (even when a PREFIX is given), --filter is rejected.
    #   - otherwise: pieces are written to files PREFIXaa, PREFIXab, ... (default PREFIX 'x'),
    #     or with --filter to a shell command that receives the piece's name in $FILE.
    #     The pieces are not operands themselves; the closest sound description is to mark
    #     the PREFIX operand as an "other output" (every piece's path starts with it).
    #     With no PREFIX operand the pieces land in the current directory as xaa, xab, ...
    #     and no operand exists to carry that information.
    #
    # -l, -b, -C and -n are mutually exclusive, and -n may be given only once
    # ("cannot split in more than one way"), so at most one -n option is present.
    #
    # --verbose prints "creating file 'PREFIXaa'" lines to stdout (checked with the binary).
    #
    # Other options (-a, --additional-suffix, -d, -x, -e, -t, -u) only change
    # how pieces are named or cut and do not affect which resources are used.

    @staticmethod
    def does_chunks_arg_write_to_stdout(chunks: str) -> bool:
        parts = chunks.split('/')
        if parts[0] in ('l', 'r'):
            return len(parts) == 3   # l/K/N, r/K/N
        return len(parts) == 2       # K/N

    def set_last_operand_as_config_arg_type_string(self) -> None:
        self.input_output_info.operand_list_typer[-1] = (WhichClassForArg.ARGSTRING, None)

    def generate_info(self) -> None:
        # assumption that version/help not provided
        num_operands = self.get_operand_list_length()
        if num_operands > 2:
            raise Exception('extra operand for split, the 3rd one')

        # input
        if num_operands == 0:
            self.set_implicit_use_of_stdin()
        else:
            # the first operand is FILE, '-' is handled as stdin by the library
            self.all_but_last_operand_is_streaming_input()

        # output
        number_options: List[FlagOption] = self.get_flag_option_list_filtered_with(["-n"])
        if len(number_options) > 1:
            raise Exception('multiple -n options defined for split')
        writes_to_stdout = len(number_options) == 1 and \
            self.does_chunks_arg_write_to_stdout(str(number_options[0].get_arg()))

        if writes_to_stdout:
            if self.does_flag_option_list_contain_at_least_one_of(["--filter"]):
                raise Exception('--filter does not process a chunk extracted to stdout')
            self.set_implicit_use_of_stdout()
            if num_operands == 2:
                # PREFIX is accepted but unused in this mode
                self.set_last_operand_as_config_arg_type_string()
        else:
            if num_operands == 2:
                self.only_last_operand_is_other_output()
            # with 0 or 1 operands the pieces are created as xaa, xab, ... in the working
            # directory; there is no operand to attach this information to
            if self.does_flag_option_list_contain_at_least_one_of(["--verbose"]):
                self.set_implicit_use_of_stdout()
