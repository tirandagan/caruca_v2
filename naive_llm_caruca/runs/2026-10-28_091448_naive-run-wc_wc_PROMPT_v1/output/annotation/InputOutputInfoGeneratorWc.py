from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorWc(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-m", "-l", "-L", "-w", "--debug", "--help", "--version"]
    # list_of_all_options = ["--files0-from", "--total"]

    # Which ones do affect input/output?
    # --files0-from=F: the input files are the NUL-separated names listed in F (CONTAINER_FOR_INPUT, typed
    #   from the parser table); file operands may not be combined with it (wc rejects them), and stdin is
    #   only read when F is "-"
    # all other flags/options only select which counts are printed, never where data comes from or goes to
    # --help and --version print nothing but the help/version text; as in the other annotations we assume
    #   they are not given

    def generate_info(self) -> None:
        # the counts always go to stdout, also with --total=only / never
        self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["--files0-from"]):
            # no operands are allowed here; with F being "-" the list of names is read from stdin
            if self._files0_from_is_stdin():
                self.set_implicit_use_of_stdin()
        else:
            # with no FILE, or when FILE is -, read standard input
            self.all_operands_are_streaming_inputs()
            self.if_no_operands_given_stdin_implicitly_used()

    def _files0_from_is_stdin(self) -> bool:
        for flag_option in self.get_flag_option_list_filtered_with(["--files0-from"]):
            arg = getattr(flag_option, "option_arg", None)
            if arg is None:
                getter = getattr(flag_option, "get_arg", None)
                arg = getter() if callable(getter) else None
            if arg is None:
                # cannot inspect the argument: over-approximate and assume stdin is read
                return True
            name = getattr(arg, "name", None)
            if name is None:
                getter = getattr(arg, "get_name", None)
                name = getter() if callable(getter) else str(arg)
            if str(name) == "-":
                return True
        return False
