from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorPr(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-c", "-d", "-e", "-F", "-f", "-i", "-J", "-m", "-n", "-r", "-s", "-S",
    #                      "-t", "-T", "-v", "-1".."-9", "--help", "--version"]
    # list_of_all_options = ["--pages", "--columns", "-D", "-h", "-l", "-N", "-o", "-w", "-W"]

    # Which ones do affect input/output?
    # none: pr always writes the formatted text to stdout and reads every FILE operand
    # (with -m all of them in parallel, otherwise one after the other);
    # with no FILE, or when FILE is -, it reads stdin.
    # -e, -i, -n, -s, -S only accept an attached value (-e8, -s,); a separate word is a FILE.
    # -h HEADER and -D FORMAT are plain strings, not files.
    # assumption that version/help not provided

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
