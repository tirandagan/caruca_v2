from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorMktemp(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-d", "-u", "-q", "--tmpdir", "-t", "--help", "--version"]
    # list_of_all_options = ["--suffix", "-p"]

    # mktemp never reads stdin; it always prints the created name to stdout.
    # The optional TEMPLATE operand (default tmp.XXXXXXXXXX) names where the
    # file/directory is created, with its X's replaced, so it is an "other output"
    # (an over-approximation: with -t/-p/--tmpdir the actual path lives under
    # that directory). The -p DIR argument is typed from mktemp.json as a
    # directory that gets a new entry (OTHER_OUTPUT).
    # With -u/--dry-run nothing is created: the template is just a string.

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["-u"]):
            self.set_all_operands_as_config_arg_type_string()
        else:
            self.all_operands_are_other_outputs()
