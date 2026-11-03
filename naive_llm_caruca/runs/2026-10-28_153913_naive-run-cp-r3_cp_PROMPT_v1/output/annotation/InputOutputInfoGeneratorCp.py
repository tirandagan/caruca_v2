from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCp(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "--attributes-only", "-b", "--copy-contents", "-d", "--debug", "-f", "-i", "-H",
    #                      "-l", "-L", "-n", "-P", "-p", "--parents", "-R", "--remove-destination",
    #                      "--strip-trailing-slashes", "-s", "-T", "-u", "-v", "-x", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "--preserve", "--no-preserve", "--reflink", "--sparse", "-S", "-t",
    #                        "--update", "--context"]

    # Which ones do affect input/output?
    # -t DIRECTORY: the destination is the option argument (typed OTHER_OUTPUT via cp.json) and *all*
    #               operands are sources; otherwise the last operand is the destination
    # -v, --debug: progress messages are written to stdout
    # -i: asks for confirmation on stdin (only when the destination already exists)
    # A lone "-" operand is an ordinary file name for cp, not stdin.
    #
    # Sources are marked as "other" rather than streaming inputs: with -R/-a a source may be a directory
    # (or a FIFO/device that is re-created instead of read), with -l/-s nothing is read at all, and
    # -p/--preserve/--parents inspect metadata and paths.  The destination is "other" output since it is
    # commonly a directory into which files are created (and -b/--backup, -l, -s, -n, -u, -i change what
    # is written).  -t, --parents and --backup can create files beyond the named operands; these are not
    # tracked individually.

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-v", "--debug"]):
            self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["-i"]):
            self.set_implicit_use_of_stdin()
        if self.does_flag_option_list_contain_at_least_one_of(["-t"]):
            # cp -t DIRECTORY SOURCE...
            self.all_operands_are_other_inputs()
        else:
            # cp [-T] SOURCE DEST  /  cp SOURCE... DIRECTORY
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
