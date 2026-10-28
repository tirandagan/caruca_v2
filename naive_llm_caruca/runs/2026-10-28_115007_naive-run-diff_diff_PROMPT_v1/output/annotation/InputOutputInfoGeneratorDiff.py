from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorDiff(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--normal", "-q", "-s", "-c", "--context", "-u", "--unified", "-0".."-9", "-e", "-n",
    #                      "-y", "--left-column", "--suppress-common-lines", "--sdiff-merge-assist", "-p", "-t",
    #                      "-T", "--suppress-blank-empty", "-l", "-r", "--no-dereference", "-N", "-P",
    #                      "--ignore-file-name-case", "--no-ignore-file-name-case", "-i", "-E", "-Z", "-b", "-w",
    #                      "-B", "-a", "--binary", "--strip-trailing-cr", "-d", "-H", "--inhibit-hunk-merge", "-h",
    #                      "--color", "--help", "-v"]
    # list_of_all_options = ["-C", "-U", "-W", "-F", "-L", "--tabsize", "-x", "-X", "-S", "--from-file", "--to-file",
    #                        "-I", "-D", "--old-group-format", "--new-group-format", "--changed-group-format",
    #                        "--unchanged-group-format", "--line-format", "--old-line-format", "--new-line-format",
    #                        "--unchanged-line-format", "--horizon-lines", "--palette"]

    # Which ones do affect input/output?
    # -X names a file of exclusion patterns (typed in diff.json as EXCLUDES_FROM_INPUT)
    # --from-file/--to-file name an additional file compared against every operand (typed as STREAM_INPUT)
    # -r (and operands that are directories in general) means the operands are read as directory trees,
    #   not as single data streams
    # -q/-s only change what is printed; the result still goes to stdout, so stdout is always used
    #   (--help/--version are assumed absent)
    # -l pipes the output through 'pr', still ending on stdout
    # an operand of '-' (also for --from-file/--to-file) means standard input

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        if self.does_flag_option_list_contain_at_least_one_of(["-r"]):
            # recursive comparison of directory trees: the operands are directories
            self.all_operands_are_other_inputs()
        else:
            # FILE1 FILE2, or FILE... with --from-file/--to-file; both are read completely
            self.all_operands_are_streaming_inputs()
