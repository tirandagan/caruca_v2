from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorRm(InputOutputInfoGeneratorInterface):

    # rm never reads stdin as data nor writes data to stdout (-v messages and
    # -i/-I prompts are diagnostics, not a data stream). Every operand is a
    # path that gets removed, i.e. modified in a non-streaming way.
    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()
