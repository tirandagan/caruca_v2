from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.AccessKind import make_stream_input
from pash_annotations.datatypes.BasicDatatypes import WhichClassForArg

class InputOutputInfoGeneratorSplit(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        flags = {str(fo.get_name()) for fo in self.cmd_inv.flag_option_list}
        n = self.get_operand_list_length()
        if n == 0 and flags in ({'-d', '-n'}, {'-d'}, {'-n'}, set()):
            self.set_implicit_use_of_stdin()
        elif n == 1 and flags in ({'-d', '-n'}, {'-d'}, {'-n'}, set()):
            self.all_operands_are_streaming_inputs()
            self.set_implicit_use_of_stdin()
        elif n == 2 and flags in ({'-d', '-n'}, {'-d'}, {'-n'}, set()):
            self.input_output_info.operand_list_typer[0] = (WhichClassForArg.FILESTD, make_stream_input())
            self.input_output_info.operand_list_typer[1] = (WhichClassForArg.ARGSTRING, None)
            self.set_implicit_use_of_stdin()
        else:
            self.input_output_info = None
