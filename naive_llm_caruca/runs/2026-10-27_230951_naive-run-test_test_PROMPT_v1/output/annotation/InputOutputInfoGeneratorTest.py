from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTest(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["!", "(", ")", "-a", "-o"]
    # list_of_all_options = ["-n", "-z", "-l", "-t",
    #                        "-b", "-c", "-d", "-e", "-f", "-g", "-G", "-h", "-k", "-L", "-N", "-O",
    #                        "-p", "-r", "-s", "-S", "-u", "-w", "-x"]

    # test communicates its result solely through the exit status: it never reads
    # stdin and never writes stdout (diagnostics go to stderr). --help/--version
    # are ordinary strings for `test` (only `[` honours them), so they are not flags.
    #
    # The unary file tests (-e FILE etc.) are options whose FILE argument is already
    # typed OTHER_INPUT by the parser table (only metadata is inspected, never the
    # content). -t FD only asks whether a descriptor is a terminal; it does not read
    # it, so even -t 0 is not treated as a use of stdin.
    #
    # Operands are what the parser could not attribute to an option: STRING / INTEGER
    # primaries, the binary operators (= != -eq ... -ef -nt -ot) and their operands,
    # and anything after the first such word (e.g. a trailing `-a -e FILE`).

    # binary operators whose operands are files
    FILE_BINARY_OPERATORS = ["-ef", "-nt", "-ot"]
    # unary operators that take a file; may land among the operands when they
    # follow a non-option word, e.g. `test x = y -a -e FILE`
    FILE_UNARY_OPERATORS = ["-b", "-c", "-d", "-e", "-f", "-g", "-G", "-h", "-k", "-L",
                            "-N", "-O", "-p", "-r", "-s", "-S", "-u", "-w", "-x"]

    @staticmethod
    def _operand_as_string(operand) -> str:
        get_name = getattr(operand, "get_name", None)
        return get_name() if callable(get_name) else str(operand)

    def generate_info(self) -> None:
        operand_strings = [self._operand_as_string(operand) for operand in self.cmd_inv.operand_list]
        file_operators = self.FILE_BINARY_OPERATORS + self.FILE_UNARY_OPERATORS
        if any(word in file_operators for word in operand_strings):
            # Some operand is a file name (FILE1 -nt FILE2, or a unary file test that
            # ended up among the operands). The interface offers no per-operand
            # marking, so over-approximate: treat all operands as files whose
            # metadata is read. The operator words themselves then look like
            # (non-existent) input files, which is harmless but imprecise.
            self.all_operands_are_other_inputs()
        else:
            # strings, integers and comparison operators: no file involved
            self.set_all_operands_as_config_arg_type_string()
