from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCp(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "--attributes-only", "-b", "--copy-contents", "-d", "--debug", "-f", "-i", "-H",
    #                      "-l", "-L", "-n", "-P", "-p", "--parents", "-R", "--remove-destination",
    #                      "--strip-trailing-slashes", "-s", "-T", "-u", "-v", "-x", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "--preserve", "--no-preserve", "--reflink", "--sparse", "-S", "-t",
    #                        "--update", "--context"]

    # Which ones do affect input/output?
    # -t DIRECTORY: the destination is the option argument (typed OTHER_OUTPUT in cp.json), so every operand is a source
    # -v / --debug: progress messages are written to stdout
    # -i: the overwrite prompt is answered from stdin (we over-approximate: a later -n or -f may suppress the prompt)
    # -l / -s: sources are linked rather than read; they are still kept as (other) inputs, an over-approximation
    # a lone '-' is an ordinary file name for cp, never stdin/stdout

    def generate_info(self) -> None:
        # sources are files, directories (with -R) or symlinks and are not consumed as a line stream,
        # and the destination is either a file to be created/overwritten or a directory to be populated,
        # so everything is "other" input/output rather than streaming
        if self.does_flag_option_list_contain_at_least_one_of(["-t"]):
            self.all_operands_are_other_inputs()
        else:
            if self.get_operand_list_length() < 2:
                raise Exception('cp needs at least a SOURCE and a DEST operand unless -t is given')
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
        if self.does_flag_option_list_contain_at_least_one_of(["-v", "--debug"]):
            self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["-i"]):
            self.set_implicit_use_of_stdin()
