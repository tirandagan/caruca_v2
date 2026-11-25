from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorTimeout(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--preserve-status", "--foreground", "-v", "--help", "--version"]
    # list_of_all_options = ["-k", "-s"]

    # timeout [OPTION] DURATION COMMAND [ARG]...
    # None of the operands is a file that timeout itself reads or writes:
    # the first operand is a time interval, the second is the program to run and
    # the remaining ones are that program's arguments. Option processing stops at
    # DURATION, so everything after it (even words that look like options) is
    # part of COMMAND.
    # timeout does not touch stdin/stdout itself but hands both descriptors to
    # COMMAND, whose behaviour is unknown here. We therefore over-approximate and
    # declare both as used; the only output timeout produces on its own is a
    # diagnostic on stderr (with -v or on errors).

    def generate_info(self) -> None:
        self.set_all_operands_as_config_arg_type_string()
        # inherited by COMMAND, which may read/write them
        self.set_implicit_use_of_stdin()
        self.set_implicit_use_of_stdout()
