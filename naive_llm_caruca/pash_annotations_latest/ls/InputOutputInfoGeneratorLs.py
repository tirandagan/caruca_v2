from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorLs(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-A", "--author", "-b", "-B", "-c", "-C", "--color", "-d", "-D", "-f", "-F",
    #                      "--file-type", "--full-time", "-g", "--group-directories-first", "-G", "-h", "--si",
    #                      "-H", "--dereference-command-line-symlink-to-dir", "--hyperlink", "-i", "-k", "-l",
    #                      "-L", "-m", "-n", "-N", "-o", "-p", "-q", "--show-control-chars", "-Q", "-r", "-R",
    #                      "-s", "-S", "-t", "-u", "-U", "-v", "-x", "-X", "-Z", "--zero", "-1", "--help", "--version"]
    # list_of_all_options = ["--block-size", "--format", "--hide", "--indicator-style", "-I", "--quoting-style",
    #                        "--sort", "--time", "--time-style", "-T", "-w"]

    # Which ones do affect input/output?
    # none: ls never reads stdin and never writes a file; the listing always goes to stdout
    # (--help and --version also only write to stdout; we assume they are not given)
    # -I/--ignore and --hide take shell patterns, not file names
    # operands are files/directories whose metadata (and, for directories, entries) are read;
    # they are never read as a byte stream, so they are "other" inputs
    # with no operands, ls lists "." which we cannot express as an operand (same limitation as grep -r)
    # -R additionally reads subdirectories of the operands, and -L/-H follow symlinks;
    # both are covered by the over-approximation that the operand is an input

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.all_operands_are_other_inputs()
