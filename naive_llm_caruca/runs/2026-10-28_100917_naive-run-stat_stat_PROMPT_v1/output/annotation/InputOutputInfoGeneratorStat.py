from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorStat(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-L", "-f", "-t", "--help", "--version"]
    # list_of_all_options = ["--cached", "-c", "--printf"]

    # Which ones do affect input/output?
    # none: every operand is a path whose metadata (or whose file system's metadata, with -f)
    # is queried via stat(2)/statx(2); the file contents are never read, so operands are
    # "other" inputs rather than streams. An operand of "-" makes stat fstat its standard input
    # (still metadata only). stat requires at least one operand ("missing operand" otherwise),
    # so stdin is never implicitly used. The report for each operand goes to stdout.
    # -c/--format/--printf only change how the report is rendered.

    def generate_info(self) -> None:
        # assumption that version/help not provided
        self.all_operands_are_other_inputs()
        self.set_implicit_use_of_stdout()
