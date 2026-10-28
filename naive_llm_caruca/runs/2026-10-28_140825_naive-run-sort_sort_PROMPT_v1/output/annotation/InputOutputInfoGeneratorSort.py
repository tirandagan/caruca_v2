from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSort(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-d", "-f", "-g", "-i", "-M", "-h", "-n", "-R", "-r", "-V", "-c", "-C", "--debug",
    #                      "-m", "-s", "-u", "-y", "-z", "--help", "--version"]
    # list_of_all_options = ["--random-source", "--sort", "--batch-size", "--compress-program", "--files0-from",
    #                        "-k", "-o", "-S", "-t", "-T", "--parallel"]

    # Which ones do affect input/output?
    # operands: all are streaming inputs ('-' is stdin); with no operand, stdin is read
    # --files0-from=F: F lists the inputs (CONTAINER_FOR_INPUT via sort.json); operands are then rejected by sort,
    #                  and F being '-' means the list of names is read from stdin
    # -o FILE: result goes to FILE (STREAM_OUTPUT via sort.json) instead of stdout; '-o -' is a file literally named '-'
    # -c/-C/--check: nothing is written to stdout (only a diagnostic on stderr and the exit status); -c with -o is an error
    # -T DIR: temporaries are created in DIR (OTHER_OUTPUT via sort.json)
    # --random-source FILE: read for random bytes (CONFIG_INPUT via sort.json)
    # --debug: annotations are written to stdout together with the output, so stdout usage is unchanged
    # --help/--version: assumed not to be given

    def generate_info(self) -> None:
        # inputs
        if self.does_flag_option_list_contain_at_least_one_of(["--files0-from"]):
            # the input files are listed in the option argument; sort rejects file operands in this case
            # (an argument of '-' is turned into stdin by the option-argument typing, so nothing to add here)
            if self.get_operand_list_length() > 0:
                raise Exception('file operands cannot be combined with --files0-from')
        else:
            self.all_operands_are_streaming_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
        # outputs
        if self.does_flag_option_list_contain_at_least_one_of(["-c", "-C"]):
            # check mode writes nothing to stdout
            pass
        elif self.does_flag_option_list_contain_at_least_one_of(["-o"]):
            # output goes to the file given with -o, which is typed as STREAM_OUTPUT from sort.json
            pass
        else:
            self.set_implicit_use_of_stdout()
