from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorPinky(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-l", "-b", "-h", "-p", "-s", "-f", "-w", "-i", "-q", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none: every flag only changes which columns/sections are printed

    def generate_info(self) -> None:
        # operands are user names, not files; pinky never reads stdin
        # (verified with strace) and reads /var/run/utmp (and ~/.plan,
        # ~/.project with -l) on its own
        self.set_all_operands_as_config_arg_type_string()
        self.set_implicit_use_of_stdout()
