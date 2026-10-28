from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorNl(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-p", "--help", "--version"]
    # list_of_all_options = ["-b", "-d", "-f", "-h", "-i", "-l", "-n", "-s", "-v", "-w"]

    # Which ones do affect input/output?
    # none: every option only changes how the line numbers are rendered;
    # only the number of operands matters (and --help/--version, which we assume absent)

    def generate_info(self) -> None:
        # nl [OPTION]... [FILE]...: all FILEs are read as one stream (numbering continues
        # across file boundaries), the result always goes to stdout;
        # with no FILE (or FILE being -) stdin is read, tested with the command
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
        self.set_implicit_use_of_stdout()
