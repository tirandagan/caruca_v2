from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMkfifo(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        # every operand is a FIFO that gets created; nothing is read from stdin
        # and nothing is written to stdout
        self.all_operands_are_other_outputs()
