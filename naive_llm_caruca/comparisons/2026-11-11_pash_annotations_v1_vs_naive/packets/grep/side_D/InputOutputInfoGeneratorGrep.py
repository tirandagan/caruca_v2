from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.AccessKind import make_stream_input
from pash_annotations.datatypes.BasicDatatypes import WhichClassForArg

class InputOutputInfoGeneratorGrep(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        flags = {str(fo.get_name()) for fo in self.cmd_inv.flag_option_list}
        n = self.get_operand_list_length()
        if n == 2 and flags in ({'-R', '-c', '-r'}, {'-R', '-c', '-v'}, {'-R', '-r', '-v'}, {'-c', '-r', '-v'}, {'-R', '-c'}, {'-R', '-r'}, {'-R', '-v'}, {'-c', '-r'}, {'-c', '-v'}, {'-r', '-v'}, {'-R'}, {'-c'}, {'-r'}, {'-v'}, set()):
            self.input_output_info.operand_list_typer[0] = (WhichClassForArg.ARGSTRING, None)
            self.input_output_info.operand_list_typer[1] = (WhichClassForArg.FILESTD, make_stream_input())
            self.set_implicit_use_of_stdout()
        elif n == 1 and flags in ({'-c', '-v'}, {'-c'}, {'-v'}, set()):
            self.set_all_operands_as_arg_string()
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
        else:
            self.input_output_info = None
