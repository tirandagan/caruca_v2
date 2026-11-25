from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorVdir(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-A", "--author", "-b", "-B", "-c", "-C", "--color", "-d", "-D", "-f", "-F",
    #                      "--file-type", "--full-time", "-g", "--group-directories-first", "-G", "-h", "--si",
    #                      "-H", "--dereference-command-line-symlink-to-dir", "--hyperlink", "-i", "-k", "-l",
    #                      "-L", "-m", "-n", "-N", "-o", "-p", "-q", "--show-control-chars", "-Q", "-r", "-R",
    #                      "-s", "-S", "-t", "-u", "-U", "-v", "-x", "-X", "-Z", "--zero", "-1", "--help", "--version"]
    # list_of_all_options = ["--block-size", "--format", "--hide", "--indicator-style", "-I", "--quoting-style",
    #                        "--sort", "--time", "--time-style", "-T", "-w"]

    # vdir does not consume a data stream (neither stdin nor the operands' contents), so there is no
    # input to split. Its output is also a sorted, globally formatted listing (column widths, the
    # per-directory "total" line, sort order across operands), which cannot be produced by
    # concatenating the outputs of independent copies. Hence no parallelizer is appended.

    def generate_info(self) -> None:
        pass
