from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorEnv(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-i", "-", "-0", "--block-signal", "--default-signal", "--ignore-signal",
    #                      "--list-signal-handling", "-v", "--help", "--version"]
    # list_of_all_options = ["-u", "-C", "-S"]

    # env [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]
    # Operands are never files env reads or writes: leading words containing '=' are
    # environment assignments, the first word without '=' is COMMAND and the rest are its ARGs.
    # With a COMMAND, env execs it and the inherited stdin/stdout are whatever COMMAND makes of
    # them; as for xargs we over-approximate and declare both used, since we cannot recurse
    # into COMMAND here. Without a COMMAND, env prints the resulting environment to stdout and
    # does not touch stdin. -v and --list-signal-handling only write to stderr.
    # -S can hide a COMMAND inside its string argument; treated as if a COMMAND were present.

    def generate_info(self) -> None:
        self.set_all_operands_as_arg_string()
        self.set_implicit_use_of_stdout()
        if self.has_command():
            self.set_implicit_use_of_stdin()

    def has_command(self) -> bool:
        if self.does_flag_option_list_contain_at_least_one_of(["-S"]):
            return True
        for i, operand in enumerate(self.cmd_inv.operand_list):
            name = operand.get_name()
            # a '--' operand only ends option parsing; the parser keeps it in the operand list
            if i == 0 and name == "--":
                continue
            if "=" not in name:
                return True
        return False
