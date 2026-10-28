from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorChmod(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-f", "-v", "--no-preserve-root", "--preserve-root", "-R", "--help", "--version"]
    # list_of_all_options = ["--reference"]

    # Which ones do affect input/output?
    # --reference: RFILE (typed OTHER_INPUT via the parser table) supplies the mode, so there is
    #              no MODE operand and every operand is a file whose mode bits are changed
    # -c, -v: diagnostics ("mode of 'f' changed from ...") are printed to stdout
    # -R: does not change the picture, directories are identified by their name as well
    # chmod never reads stdin; '-' is an ordinary file name, not stdin
    # --help/--version print to stdout and touch no file, but we assume they are not given

    def generate_info(self) -> None:
        # the files whose mode bits are modified (metadata write, not a stream)
        self.all_operands_are_other_outputs()
        if not self.does_flag_option_list_contain_at_least_one_of(["--reference"]):
            # chmod MODE FILE...: the first operand is the mode, not a file
            self.set_first_operand_as_config_arg_type_string()
        if self.does_flag_option_list_contain_at_least_one_of(["-c", "-v"]):
            self.set_implicit_use_of_stdout()
