from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorId(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-Z", "-g", "-G", "-n", "-r", "-u", "-z", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none: id never reads stdin (tested: `echo root | id` ignores the pipe) and always writes to stdout;
    # the operands are user names or numeric UIDs looked up in the passwd database, not files.
    # --help and --version also only write to stdout, so no special case is needed.

    def generate_info(self) -> None:
        self.set_all_operands_as_config_arg_type_string()
        self.set_implicit_use_of_stdout()
