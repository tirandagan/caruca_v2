from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorOd(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-b", "-c", "-d", "-f", "-i", "-l", "-o", "-s", "-x", "-v", "-w",
    #                      "--traditional", "--help", "--version"]
    # list_of_all_options = ["-A", "--endian", "-j", "-N", "-S", "-t", "--width"]

    # Which ones do affect input/output?
    # None of the flags/options name a file; od always writes its dump to stdout.
    # Input is the concatenation of all FILE operands (read as a stream), or stdin when
    # there is no FILE operand (or when FILE is "-").
    # Only the operand list matters: the last operand may be an OFFSET rather than a file
    # (second call form) when it begins with "+" or, with exactly two operands, with a digit;
    # with --traditional up to two trailing OFFSET/LABEL operands are allowed.
    # Tested with the binary (coreutils 9.4): "od -c FILE +4", "od -c FILE 4" and "od -c +4" skip
    # 4 bytes, whereas with three or more operands "+4" is treated as a file name.

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        n = self.get_operand_list_length()
        if n == 0:
            self.set_implicit_use_of_stdin()
            return
        operands = [self._operand_name(op) for op in self.cmd_inv.operand_list]
        if self.does_flag_option_list_contain_at_least_one_of(["--traditional"]):
            # od --traditional [FILE] [[+]OFFSET [+][LABEL]]; at most one file
            if n == 1 and not operands[0][:1].isdigit() and not operands[0].startswith("+"):
                self.all_operands_are_streaming_inputs()
            else:
                raise Exception("od --traditional with OFFSET/LABEL operands is not handled")
        else:
            last = operands[-1]
            offset_form = (n == 1 and last.startswith("+")) or \
                          (n == 2 and (last.startswith("+") or last[:1].isdigit()))
            if offset_form:
                if n == 1:
                    # the only operand is an OFFSET; input comes from stdin
                    self.set_first_operand_as_config_arg_type_string()
                    self.set_implicit_use_of_stdin()
                else:
                    # "od FILE OFFSET": the last operand is not a file; there is no
                    # interface call to mark only the last operand as a non-file, so bail out
                    raise Exception("od with an OFFSET operand after FILE is not handled")
            else:
                self.all_operands_are_streaming_inputs()

    @staticmethod
    def _operand_name(operand) -> str:
        if hasattr(operand, "get_name"):
            return str(operand.get_name())
        return str(operand)
