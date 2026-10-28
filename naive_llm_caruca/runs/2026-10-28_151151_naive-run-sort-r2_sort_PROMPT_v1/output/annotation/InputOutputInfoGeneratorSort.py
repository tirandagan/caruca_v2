from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorSort(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-d", "-f", "-g", "-i", "-M", "-h", "-n", "-R", "-r", "-V", "-c", "-C",
    #                      "--debug", "-m", "-s", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--random-source", "--sort", "--batch-size", "--compress-program", "--files0-from",
    #                        "-k", "-o", "-S", "-t", "-T", "--parallel"]

    # Which ones do affect input/output?
    # -o FILE: result goes to FILE instead of stdout (typed STREAM_OUTPUT in sort.json)
    # -c/-C/--check: nothing is written to stdout, only a diagnostic to stderr and an exit status;
    #                the binary rejects -o together with -c and allows at most one operand
    # --files0-from=F: the operands are read from F (typed CONTAINER_FOR_INPUT in sort.json);
    #                  the binary rejects any FILE operand in that case; F may be "-" for stdin
    # --random-source=FILE: configuration input (typed in sort.json)
    # -T DIR: temporaries are created in DIR (typed OTHER_OUTPUT in sort.json)
    # -m: merges instead of sorts, but reads/writes exactly the same files
    # tested: `printf 'z\ny\n' | sort -o out.txt` reads stdin and writes out.txt, nothing on stdout;
    #         `sort -c` with no operand reads stdin; `sort -o - f` writes a file literally named "-"

    def generate_info(self) -> None:
        # assumption that version/help not provided
        # output side
        if not self.does_flag_option_list_contain_at_least_one_of(["-o", "-c", "-C"]):
            self.set_implicit_use_of_stdout()
        # input side
        if self.does_flag_option_list_contain_at_least_one_of(["--files0-from"]):
            # inputs are listed in the option's file; no operands are allowed by the binary
            pass
        else:
            # with no FILE, or when FILE is -, read standard input
            self.if_no_operands_given_stdin_implicitly_used()
            self.all_operands_are_streaming_inputs()
