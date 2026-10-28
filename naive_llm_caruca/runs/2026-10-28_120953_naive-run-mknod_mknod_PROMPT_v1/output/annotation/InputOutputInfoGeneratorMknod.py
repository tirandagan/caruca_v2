from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMknod(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-Z", "--help", "--version"]
    # list_of_all_options = ["-m", "--mode", "--context"]

    # mknod NAME TYPE [MAJOR MINOR]
    # The only file involved is NAME, which is created; it is never read and
    # nothing is streamed through it. TYPE, MAJOR and MINOR are plain values.
    # Neither stdin nor stdout is used.
    # None of the flags/options changes which files are touched.

    def generate_info(self) -> None:
        # The interface offers no way to mark only the first operand as a
        # created file while leaving the rest as values, so we over-approximate
        # and treat every operand as a non-streaming output. This never misses
        # NAME; it merely adds spurious outputs named after TYPE/MAJOR/MINOR.
        self.all_operands_are_other_outputs()
