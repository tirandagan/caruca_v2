from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorRuncon(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "--help", "--version"]
    # list_of_all_options = ["-t", "-u", "-r", "-l"]

    # Which ones do affect input/output?
    # none of the options name a file; they only choose the security context
    # operands are CONTEXT (only when none of -c/-t/-u/-r/-l is given), COMMAND and
    # the arguments of COMMAND, none of which runcon itself opens as a file
    # option parsing stops at COMMAND (getopt "+r:t:u:l:c"), so anything after it
    # belongs to COMMAND and is never interpreted by runcon

    def generate_info(self) -> None:
        # assumption that version/help not provided
        self.set_all_operands_as_config_arg_type_string()
        if self.get_operand_list_length() == 0:
            # neither CONTEXT nor COMMAND: runcon prints the current security context
            self.set_implicit_use_of_stdout()
        else:
            # runcon execvp's COMMAND with inherited descriptors; we cannot know what
            # COMMAND does with them, so we over-approximate: both may be used
            self.set_implicit_use_of_stdin()
            self.set_implicit_use_of_stdout()
