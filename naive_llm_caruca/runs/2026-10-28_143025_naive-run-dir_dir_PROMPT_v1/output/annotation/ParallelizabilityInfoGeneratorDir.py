from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDir(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-A", "--author", "-b", "-B", "-c", "-C", "-d", "-D", "-f", "-F", "--file-type",
    #                      "--full-time", "-g", "--group-directories-first", "-G", "-h", "--si", "-H",
    #                      "--dereference-command-line-symlink-to-dir", "-i", "-k", "-l", "-L", "-m", "-n", "-N",
    #                      "-o", "-p", "-q", "--show-control-chars", "-Q", "-r", "-R", "-s", "-S", "-t", "-u", "-U",
    #                      "-v", "-x", "-X", "-Z", "--zero", "-1", "--help", "--version"]
    # list_of_all_options = ["--block-size", "--color", "--classify", "--format", "--hide", "--hyperlink",
    #                        "--indicator-style", "-I", "--quoting-style", "--sort", "--time", "--time-style",
    #                        "-T", "-w"]

    # Which ones do affect parallelizability?
    # none, because dir is never parallelizable:
    # - it reads no stream input (no stdin, operands are only stat'ed / readdir'ed), so consec_chunks and
    #   round_robin splitting of input has nothing to split;
    # - splitting over operands (indiv_files) is not sound either: operands are sorted globally (files first,
    #   then directories, each group ordered by the active --sort), column layout (-C/-x/-m, the default to a
    #   terminal) depends on the whole set of entries, -l prints a "total" line per directory, and -D (dired)
    #   emits byte offsets over the entire output.

    def generate_info(self) -> None:
        pass
