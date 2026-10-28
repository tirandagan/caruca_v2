from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorCp(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "--attributes-only", "-b", "--copy-contents", "-d", "--debug", "-f", "-i", "-H",
    #                      "-l", "-L", "-n", "-P", "-p", "--parents", "-R", "--remove-destination",
    #                      "--strip-trailing-slashes", "-s", "-T", "-u", "-v", "-x", "-Z", "--help", "--version"]
    # list_of_all_options = ["--backup", "--preserve", "--no-preserve", "--reflink", "--sparse", "-S", "-t",
    #                        "--update", "--context"]

    # Which ones do affect input/output?
    # -t DIRECTORY: the destination is the option argument (typed OTHER_OUTPUT in cp.json) and
    #               every operand is a source
    # otherwise:    the last operand is the destination (a file, or a directory copied into),
    #               all preceding operands are sources
    # cp never reads stdin or writes stdout (a "-" operand is a literal file name); -v/--debug
    # write progress to stdout but no data, which we ignore like the other annotations do
    # sources are read whole (and directories walked with -R), destinations created/overwritten,
    # so both sides are "other" rather than streaming
    # -l/-s link instead of copying but the dependency on the source is the same, so no special case
    # --parents places the copy under DIRECTORY/<source path>; the directory is still the last operand

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-t", "--target-directory"]):
            self.all_operands_are_other_inputs()
        else:
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()
