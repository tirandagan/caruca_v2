from typing import Dict, List, Optional, Tuple

from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.AccessKind import make_stream_input, make_stream_output, make_other_output
from pash_annotations.datatypes.BasicDatatypes import WhichClassForArg


class InputOutputInfoGeneratorDd(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "--version"]
    # list_of_all_options = []

    # dd has no dash-style options; its settings are KEY=VALUE operands, which the parser
    # hands to us unsplit as operands. So we interpret them here:
    #   if=FILE   -> the streaming input (else stdin is read)
    #   of=FILE   -> the streaming output (else stdout is written)
    #   anything else (bs=, count=, conv=, ...) -> configuration, not a file
    # A repeated key is accepted by dd and the last occurrence wins, so earlier if=/of=
    # operands are never opened and are treated as plain configuration strings.
    # Note that if=- and of=- name a file literally called "-" (verified with coreutils 9.4);
    # since the operand reaches PaSh as the whole word "if=-", it is not mistaken for stdin.
    # Known limitation: the file name PaSh records is the whole operand ("if=in.txt"), as the
    # interface offers no way to strip the key; the access kind is nevertheless correct.
    #
    # The output file is only a stream when dd truncates and writes it from the start.
    # seek=/oseek=, conv=notrunc, conv=nocreat, conv=excl, conv=sparse and oflag=append all
    # write into an existing file (or depend on its prior state), which we classify as OTHER_OUTPUT.

    OUTPUT_IS_NOT_A_STREAM_CONV = {"notrunc", "nocreat", "excl", "sparse"}
    OUTPUT_IS_NOT_A_STREAM_OFLAG = {"append"}

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]):
            # prints a message to stdout and ignores all operands
            self.set_all_operands_as_config_arg_type_string()
            self.set_implicit_use_of_stdout()
            return

        key_values: List[Tuple[Optional[str], str]] = [self.split_key_value(op.get_name())
                                                        for op in self.cmd_inv.operand_list]
        last_index_of_key: Dict[str, int] = dict()
        for i, (key, _) in enumerate(key_values):
            if key is not None:
                last_index_of_key[key] = i

        # everything is configuration by default, then we single out the input and output file
        self.set_all_operands_as_config_arg_type_string()

        if "if" in last_index_of_key:
            self.input_output_info.operand_list_typer[last_index_of_key["if"]] = \
                (WhichClassForArg.FILESTD, make_stream_input())
        else:
            self.set_implicit_use_of_stdin()

        if "of" in last_index_of_key:
            access = make_other_output() if self.output_is_modified_in_place(key_values, last_index_of_key) \
                else make_stream_output()
            self.input_output_info.operand_list_typer[last_index_of_key["of"]] = (WhichClassForArg.FILESTD, access)
        else:
            self.set_implicit_use_of_stdout()

    @staticmethod
    def split_key_value(operand: str) -> Tuple[Optional[str], str]:
        if "=" not in operand:
            return None, operand
        key, value = operand.split("=", 1)
        return key, value

    def output_is_modified_in_place(self, key_values: List[Tuple[Optional[str], str]],
                                    last_index_of_key: Dict[str, int]) -> bool:
        for seek_key in ["seek", "oseek"]:
            if seek_key in last_index_of_key and key_values[last_index_of_key[seek_key]][1] not in ["0", ""]:
                return True
        # conv= and oflag= symbol lists accumulate across repetitions
        for key, value in key_values:
            symbols = set(value.split(","))
            if key == "conv" and symbols & self.OUTPUT_IS_NOT_A_STREAM_CONV:
                return True
            if key == "oflag" and symbols & self.OUTPUT_IS_NOT_A_STREAM_OFLAG:
                return True
        return False
