from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.AccessKind import make_stream_input
from pash_annotations.datatypes.BasicDatatypes import WhichClassForArg


class InputOutputInfoGeneratorCsplit(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-k", "--suppress-matched", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-f", "-n"]

    # Which ones do affect input/output?
    # -s (aliases -q, --quiet, --silent) suppresses the byte counts written to stdout
    # -f PREFIX names where the pieces are written (typed as FILE/OTHER_OUTPUT in csplit.json);
    #   without -f the pieces still go to 'xx00', 'xx01', ... in the working directory, which is
    #   an output that no argument of the invocation names and thus cannot be declared here
    # -b, -n, -k, -z and --suppress-matched only change the names or contents of the pieces

    def generate_info(self) -> None:
        # byte counts of the pieces are printed to stdout unless silenced
        if not self.does_flag_option_list_contain_at_least_one_of(["-s"]):
            self.set_implicit_use_of_stdout()
        # operands: FILE PATTERN...
        # the first operand is the data stream ('-' denotes stdin), all remaining operands
        # are patterns (line numbers, /REGEXP/, %REGEXP%, {N}, {*}) and thus not files
        self.set_all_operands_as_config_arg_type_string()
        if self.get_operand_list_length() > 0:
            self.input_output_info.operand_list_typer[0] = (WhichClassForArg.FILESTD, make_stream_input())
