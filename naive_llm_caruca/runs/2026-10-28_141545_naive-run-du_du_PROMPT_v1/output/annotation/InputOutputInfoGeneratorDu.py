from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorDu(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-0", "-a", "--apparent-size", "-b", "-c", "-D", "-H", "-h", "--inodes", "-k", "-L",
    #                      "-l", "-m", "-P", "-S", "--si", "-s", "--time", "-x", "--help", "--version"]
    # list_of_all_options = ["-B", "-d", "--files0-from", "-t", "--time-style", "-X", "--exclude", "--exclude-from"]

    # Which ones do affect input/output?
    # du never reads the contents of its operands as a stream: it walks the directory tree and stats
    # every entry, so operands are OTHER_INPUT, not STREAM_INPUT.
    # --files0-from=F replaces the operands by the NUL-separated names in F (typed CONTAINER_FOR_INPUT in
    #   du.json); du rejects file operands when it is given; F may be "-" for standard input.
    # -X/--exclude-from=FILE reads patterns (typed EXCLUDES_FROM_INPUT in du.json); FILE may be "-" for stdin.
    # A lone "-" operand is an ordinary file name, not standard input (tested: "du -" -> cannot access '-').
    # With no operands and no --files0-from, du reports on "." (no stdin involved).
    # The report always goes to standard output.

    def generate_info(self) -> None:
        # assumption that version/help not provided
        self.set_implicit_use_of_stdout()
        self.all_operands_are_other_inputs()
        # standard input is read only when a file-typed option argument is "-"
        for flag_option in self.get_flag_option_list_filtered_with(["--files0-from", "-X", "--exclude-from"]):
            option_arg = getattr(flag_option, "option_arg", None)
            if option_arg is not None and str(getattr(option_arg, "name", option_arg)) == "-":
                self.set_implicit_use_of_stdin()
