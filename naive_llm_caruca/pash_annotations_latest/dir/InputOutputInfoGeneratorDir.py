from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorDir(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-A", "--author", "-b", "-B", "-c", "-C", "-d", "-D", "-f", "-F", "--file-type",
    #                      "--full-time", "-g", "--group-directories-first", "-G", "-h", "--si", "-H",
    #                      "--dereference-command-line-symlink-to-dir", "-i", "-k", "-l", "-L", "-m", "-n", "-N",
    #                      "-o", "-p", "-q", "--show-control-chars", "-Q", "-r", "-R", "-s", "-S", "-t", "-u", "-U",
    #                      "-v", "-x", "-X", "-Z", "--zero", "-1", "--help", "--version"]
    # list_of_all_options = ["--block-size", "--color", "--classify", "--format", "--hide", "--hyperlink",
    #                        "--indicator-style", "-I", "--quoting-style", "--sort", "--time", "--time-style",
    #                        "-T", "-w"]

    # Which ones do affect input/output?
    # none: every operand is a file or directory whose metadata (and, for directories, entry list) is read;
    # the listing always goes to stdout. --hide/--ignore take shell patterns, not files.
    # dir never reads stdin; a lone "-" operand is an ordinary file name.
    # With no operands, the current directory is listed, which is not representable as an operand here
    # (same situation as `grep -r` without a directory), so nothing is added in that case.

    def generate_info(self) -> None:
        # --help and --version print to stdout as well, so stdout is used unconditionally
        self.set_implicit_use_of_stdout()
        # operands are inspected via stat/readdir, not read as a byte stream
        self.all_operands_are_other_inputs()
