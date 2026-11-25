from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSort(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-d", "-f", "-g", "-i", "-M", "-h", "-n", "-R", "-r", "-V", "-c", "-C", "--check",
    #                      "--debug", "-m", "-s", "-u", "-z", "-y", "--help", "--version"]
    # list_of_all_options = ["--random-source", "--sort", "--batch-size", "--compress-program", "--files0-from",
    #                        "-k", "-o", "-S", "-t", "-T", "--parallel"]

    # Which ones do affect input/output?
    # -o/--output: result is written to the file instead of stdout (tested: nothing on stdout; "-o -" is a file named "-")
    # -c/-C/--check: nothing is written to stdout (only diagnostics to stderr and an exit status); incompatible with -o
    # --files0-from=F: input files are listed in F (NUL-separated); file operands are rejected; F may be - for stdin
    # -m/--merge: inputs are still read as streams, output is the same
    # --random-source=FILE and -T DIR are typed in sort.json (CONFIG_INPUT, OTHER_OUTPUT)
    # --debug: annotations go to stdout together with the sorted lines; no change in io

    def generate_info(self) -> None:
        # assumption: --help/--version not provided
        # inputs
        if self.does_flag_option_list_contain_at_least_one_of(["--files0-from"]):
            # no operands allowed; the real inputs are the names found in F (CONTAINER_FOR_INPUT via sort.json)
            if self._files0_from_argument() == "-":
                self.set_implicit_use_of_stdin()
        elif self.get_operand_list_length() == 0:
            self.set_implicit_use_of_stdin()
        else:
            # operands are streaming inputs by default, "-" among them stands for stdin
            self.all_operands_are_streaming_inputs()
        # outputs
        if self.does_flag_option_list_contain_at_least_one_of(["-c", "-C", "--check"]):
            pass  # nothing is written to stdout
        elif self.does_flag_option_list_contain_at_least_one_of(["-o", "--output"]):
            pass  # output goes to the file given to -o (STREAM_OUTPUT via sort.json)
        else:
            self.set_implicit_use_of_stdout()

    def _files0_from_argument(self) -> str:
        for flag_option in self.get_flag_option_list_filtered_with(["--files0-from"]):
            return _argument_as_string(flag_option)
        return ""


def _argument_as_string(option) -> str:
    # the option argument is wrapped in an ArgStringType; take its text whichever accessor the datatype offers
    arg = None
    for attribute in ("get_arg_as_string", "get_arg", "arg", "option_arg", "value"):
        if hasattr(option, attribute):
            arg = getattr(option, attribute)
            if callable(arg):
                arg = arg()
            break
    if arg is None:
        return ""
    for attribute in ("get_name", "name", "raw", "value"):
        if hasattr(arg, attribute):
            inner = getattr(arg, attribute)
            if callable(inner):
                inner = inner()
            if isinstance(inner, str):
                return inner
    return str(arg)
