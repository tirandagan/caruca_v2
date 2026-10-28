from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorHead(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect input/output?
    # none: -c/-n only choose how much of each input is printed, -q/-v only
    # toggle the "==> FILE <==" headers, -z only changes the line delimiter.
    # Every operand is a file read as a stream (a lone "-" means stdin);
    # with no operand, stdin is read. Output always goes to stdout.
    # assumption that version/help not provided

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
