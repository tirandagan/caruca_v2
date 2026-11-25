from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorBc(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-h", "-i", "-l", "-q", "-s", "-w", "-v"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none of the flags; -h/-v print to stdout and exit, but we assume they are not given
    #
    # tested with GNU bc 1.07.1:
    #   - every operand is a file of bc source code, executed in the order given;
    #     a lone "-" is a regular (unavailable) file name, not stdin
    #   - after all files are processed, bc ALWAYS goes on to read source from stdin
    #     (unless a file executed `quit`/`halt`), so stdin is used whether or not
    #     operands are given
    #   - results are printed to stdout; warnings/errors go to stderr

    def generate_info(self) -> None:
        # operands are programs, not the data stream, so they are "other" inputs
        self.all_operands_are_other_inputs()
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
