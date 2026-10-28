from pash_annotations.datatypes.BasicDatatypes import Option
from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMogrify(InputOutputInfoGeneratorInterface):

    # mogrify (ImageMagick) reads every operand as an image file and, by default, writes
    # the processed image back to the same file (tested: the file is rewritten even when
    # only -identify is given).  Hence operands are both read and overwritten; we mark
    # them as OTHER_OUTPUT, which PaSh treats as side-effectful.
    #
    # Which flags/options affect input/output?
    # -help, -version, -list   -> print to stdout, no image is processed
    # -format TYPE             -> operand is only read; output goes to a sibling file with
    #                             the new suffix (a.png -> a.jpg), which is not on the command
    #                             line, so we keep the operand as OTHER_OUTPUT (over-approximation)
    # -path DIR                -> operand is only read; output goes to DIR/<basename>; DIR is
    #                             typed as a directory output in mogrify.json
    # -write FILE              -> additional output file, typed in mogrify.json
    # -cdl, -clip-mask, -decipher, -encipher, -map, -mask, -profile, -remap, -texture, -tile
    #                          -> files read for configuration, typed in mogrify.json
    # -identify, -print, -verbose -> write to stdout while processing
    # an operand `-` (or `fmt:-`) -> the image is read from stdin and written to stdout
    #
    # Options that take two words (`-morphology method kernel`, `-annotate geometry text`, ...)
    # are not supported by PaSh's parser, which stops at the second word and treats it (and
    # everything after it) as operands.  We repair the case where the two-word option is the
    # last option; otherwise we raise, which makes PaSh treat the command as side-effectful.

    TWO_ARGUMENT_OPTIONS = ["-annotate", "-copy", "-distort", "+distort", "-evaluate", "-floodfill",
                            "-function", "-limit", "-morphology", "+morphology", "-set",
                            "-sparse-color", "+sparse-color", "-statistic"]
    INFO_ONLY_OPTIONS = ["-help", "+help", "-version", "+version", "-list", "+list"]
    STDOUT_OPTIONS = ["-identify", "+identify", "-print", "+print", "-verbose"]

    def generate_info(self) -> None:
        operands_start = self.repair_second_word_of_two_argument_option()
        operand_names = [str(operand.get_name()) for operand in self.cmd_inv.operand_list]
        for name in operand_names[operands_start:]:
            if len(name) > 1 and (name.startswith("-") or name.startswith("+")):
                raise Exception("mogrify: options after a two-argument option are not parsed correctly")

        if self.does_flag_option_list_contain_at_least_one_of(self.INFO_ONLY_OPTIONS):
            # only prints information; no operand is touched
            self.set_implicit_use_of_stdout()
            self.set_all_operands_as_config_arg_type_string()
            return

        if self.does_flag_option_list_contain_at_least_one_of(self.STDOUT_OPTIONS):
            self.set_implicit_use_of_stdout()

        if any(name == "-" or name.endswith(":-") for name in operand_names[operands_start:]):
            # image read from stdin (the operand itself is reported as the stdout output below)
            self.set_implicit_use_of_stdin()

        if self.does_flag_option_list_contain_at_least_one_of(["-path"]) \
                and not self.does_flag_option_list_contain_at_least_one_of(["-format"]):
            # results go to the -path directory, operands are only read
            self.all_operands_are_other_inputs()
        else:
            # results overwrite the operands (or, with -format, a sibling file next to them)
            self.all_operands_are_other_outputs()

        if operands_start == 1:
            # re-apply after the all_operands_* call, which resets every operand
            self.set_first_operand_as_config_arg_type_string()

    def repair_second_word_of_two_argument_option(self) -> int:
        """If the last option takes two words, the first operand is really its second word.
        Returns the index of the first real operand."""
        flag_option_list = self.cmd_inv.flag_option_list
        if len(flag_option_list) > 0 and isinstance(flag_option_list[-1], Option) \
                and flag_option_list[-1].get_name() in self.TWO_ARGUMENT_OPTIONS \
                and self.get_operand_list_length() > 0:
            self.set_first_operand_as_config_arg_type_string()
            return 1
        return 0
