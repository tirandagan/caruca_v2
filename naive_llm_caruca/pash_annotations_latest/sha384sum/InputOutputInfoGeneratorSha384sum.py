from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.AccessKind import make_container_for_input
from pash_annotations.datatypes.BasicDatatypes import WhichClassForArg


class InputOutputInfoGeneratorSha384sum(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status", "--strict",
    #                      "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # -c: operands are no longer the data to digest but checksum lists; the files named in them are the
    #     ones actually read (CONTAINER_FOR_INPUT, as sort's --files0-from); stdout gets one "NAME: OK/FAILED"
    #     line per entry
    # --status: suppresses all stdout (only meaningful with -c); a later -w turns it off again, so we only
    #     treat stdout as unused when --status is given without -w
    # --quiet only drops the OK lines, so stdout may still be written
    # -b, -t, --tag, -z only change the output format
    # assumption that --help/--version are not given

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            # checksum lists: a lone '-' or no operand means the list comes from stdin
            if self.get_operand_list_length() == 0:
                self.set_implicit_use_of_stdin()
            else:
                number_of_operands = self.get_operand_list_length()
                self.input_output_info.operand_list_typer = \
                    [(WhichClassForArg.FILESTD, make_container_for_input())] * number_of_operands
            if not self.does_flag_option_list_contain_at_least_one_of(["--status"]) \
                    or self.does_flag_option_list_contain_at_least_one_of(["-w"]):
                self.set_implicit_use_of_stdout()
        else:
            # default mode: digest each operand (whole file read once, output one line per file)
            if self.get_operand_list_length() == 0:
                self.set_implicit_use_of_stdin()
            else:
                self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdout()
