from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorHead(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect input/output?
    # only the number of operands: with no FILE (or FILE being -) stdin is read;
    # output always goes to stdout. -q/-v only change whether "==> FILE <==" headers
    # are printed, -c/-n/-z only change how much of each input is read.
    # assumption that version/help not provided

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
