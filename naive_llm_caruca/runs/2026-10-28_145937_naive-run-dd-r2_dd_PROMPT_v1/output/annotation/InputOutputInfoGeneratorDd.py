from typing import Dict, List, Optional, Set

from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.AccessKind import make_stream_input, make_stream_output, make_other_output
from pash_annotations.datatypes.BasicDatatypes import FileName
from pash_annotations.datatypes.BasicDatatypesWithIO import get_from_original_filename_with_ioinfo


class InputOutputInfoGeneratorDd(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "--version"]
    # list_of_all_options = []   (none in the dash-style sense the parser understands)
    # key=value operands = ["bs", "cbs", "conv", "count", "ibs", "if", "iflag", "obs", "of", "oflag",
    #                       "seek"/"oseek", "skip"/"iseek", "status"]

    # dd has no positional operands: every word is KEY=VALUE. The parser cannot split these, so
    # they all arrive in the operand list and are parsed here. None of them is a file by itself,
    # so all operands become config strings; the files named by if= and of= are reported through
    # the implicit streaming input/output slots, which fall back to stdin/stdout when absent
    # (dd treats a lone '-' as a literal file name, not as a std descriptor).
    #
    # Which ones affect input/output?
    # if=, of=: choose the input and output file; the last occurrence of a key wins.
    # seek=/oseek= (non-zero), conv=notrunc, oflag=append: existing output data is kept, so the
    #   output file is modified rather than written as a stream -> OTHER_OUTPUT.
    # skip=/iseek=, count=: still a sequential read of (part of) the input -> STREAM_INPUT.
    # conv=excl/nocreat only constrain creation of the output; data is still streamed.
    # status= only touches stderr.

    @staticmethod
    def _split_key_value(word: str):
        if "=" in word:
            key, value = word.split("=", 1)
            return key, value
        return word, None

    def _parse_key_value_operands(self):
        last_value: Dict[str, str] = dict()
        list_symbols: Dict[str, Set[str]] = {"conv": set(), "iflag": set(), "oflag": set()}
        for operand in self.cmd_inv.operand_list:
            key, value = self._split_key_value(str(operand.get_name()))
            if value is None:
                continue  # dd rejects such a word; nothing to record
            if key == "oseek":
                key = "seek"
            elif key == "iseek":
                key = "skip"
            if key in list_symbols:
                list_symbols[key].update(s for s in value.split(",") if s != "")
            else:
                last_value[key] = value
        return last_value, list_symbols

    @staticmethod
    def _is_zero(value: Optional[str]) -> bool:
        if value is None:
            return True
        try:
            return int(value, 0) == 0
        except ValueError:
            return False

    def _help_or_version_given(self) -> bool:
        # dd honours --help/--version anywhere on the line; the parser only recognises them before
        # the first KEY=VALUE word, after which they show up as operands
        return self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]) or \
            any(str(operand.get_name()) in ("--help", "--version") for operand in self.cmd_inv.operand_list)

    def generate_info(self) -> None:
        # --help / --version print to stdout and touch no files; as in the other annotations we
        # assume they are not given, but handle them for completeness
        if self._help_or_version_given():
            self.set_all_operands_as_config_arg_type_string()
            self.set_implicit_use_of_stdout()
            return

        last_value, list_symbols = self._parse_key_value_operands()
        self.set_all_operands_as_config_arg_type_string()

        # input side
        if "if" in last_value:
            input_file = get_from_original_filename_with_ioinfo(FileName(last_value["if"]), make_stream_input())
            self.input_output_info.set_implicit_use_of_streaming_input(input_file)
        else:
            self.set_implicit_use_of_stdin()

        # output side
        output_is_modified_in_place = ("notrunc" in list_symbols["conv"]) \
            or ("append" in list_symbols["oflag"]) \
            or not self._is_zero(last_value.get("seek"))
        if "of" in last_value:
            access = make_other_output() if output_is_modified_in_place else make_stream_output()
            output_file = get_from_original_filename_with_ioinfo(FileName(last_value["of"]), access)
            self.input_output_info.set_implicit_use_of_streaming_output(output_file)
        else:
            self.set_implicit_use_of_stdout()
