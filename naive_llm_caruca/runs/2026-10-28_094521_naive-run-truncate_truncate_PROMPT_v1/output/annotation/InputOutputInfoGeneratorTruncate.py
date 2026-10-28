from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTruncate(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-o", "--help", "--version"]
    # list_of_all_options = ["-r", "-s"]

    # truncate never reads stdin and writes nothing to stdout; every operand is a
    # file whose size is set in place (created first unless -c is given).
    # -r RFILE is only stat'ed for its size; it is typed OTHER_INPUT in truncate.json.
    # -c only changes whether missing operands get created; existing ones are still
    # modified, so operands stay outputs either way.

    def generate_info(self) -> None:
        self.all_operands_are_other_outputs()
