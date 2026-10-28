from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorChown(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-f", "-v", "--dereference", "-h", "--no-preserve-root", "--preserve-root",
    #                      "-R", "-H", "-L", "-P", "--help", "--version"]
    # list_of_all_options = ["--from", "--reference"]

    # Which ones do affect input/output?
    # --reference: RFILE is read (stat only, typed OTHER_INPUT in chown.json) and, more importantly,
    #              the OWNER[:GROUP] operand is then absent, so every operand is a FILE
    # -c, -v: diagnostics are written to stdout; without them chown writes nothing to stdout
    # chown never reads stdin, and '-' is an ordinary file name, not stdin
    # -R, -H, -L, -P, -h, --dereference only change which inodes below/behind the operands are touched;
    # the operands themselves stay the same, so we over-approximate by the operand names
    # --from only filters which files are changed

    def generate_info(self) -> None:
        # assumption that version/help not provided
        if self.does_flag_option_list_contain_at_least_one_of(["-c", "-v"]):
            self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["--reference"]):
            # chown --reference=RFILE FILE...
            self.all_operands_are_other_outputs()
        else:
            # chown [OWNER][:[GROUP]] FILE...
            # the first operand is the ownership spec, not a file; the rest have their metadata changed
            if hasattr(self, "all_but_first_operand_is_other_output"):
                self.set_first_operand_as_config_arg_type_string()
                self.all_but_first_operand_is_other_output()
            else:
                # the interface only offers streaming/other *input* variants of all_but_first_operand;
                # mark everything as other output first and then retype the first operand
                self.all_operands_are_other_outputs()
                self.set_first_operand_as_config_arg_type_string()
