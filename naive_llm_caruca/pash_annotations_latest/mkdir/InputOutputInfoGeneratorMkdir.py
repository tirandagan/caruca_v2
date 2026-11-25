from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMkdir(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        # every operand is a directory that gets created; nothing is read,
        # stdin is never consumed and stdout only carries -v/--help/--version text
        self.all_operands_are_other_outputs()
