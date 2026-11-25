from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorVdir(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-A", "--author", "-b", "-B", "-c", "-C", "--color", "-d", "-D", "-f", "-F",
    #                      "--file-type", "--full-time", "-g", "--group-directories-first", "-G", "-h", "--si",
    #                      "-H", "--dereference-command-line-symlink-to-dir", "--hyperlink", "-i", "-k", "-l",
    #                      "-L", "-m", "-n", "-N", "-o", "-p", "-q", "--show-control-chars", "-Q", "-r", "-R",
    #                      "-s", "-S", "-t", "-u", "-U", "-v", "-x", "-X", "-Z", "--zero", "-1", "--help", "--version"]
    # list_of_all_options = ["--block-size", "--format", "--hide", "--indicator-style", "-I", "--quoting-style",
    #                        "--sort", "--time", "--time-style", "-T", "-w"]

    # vdir (= ls -l -b) never reads a data stream: operands are files or directories whose
    # metadata (and, for directories, entries) are read via stat/readdir, so they are "other" inputs.
    # A lone "-" operand is an ordinary file name, not stdin. Standard input is never read.
    # With no operands the current directory is listed, which is an implicit input we cannot name here.
    # -R descends into subdirectories (more is read than the operands name); -I/--hide take glob
    # patterns, not files. None of the options names a file.

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.all_operands_are_other_inputs()
