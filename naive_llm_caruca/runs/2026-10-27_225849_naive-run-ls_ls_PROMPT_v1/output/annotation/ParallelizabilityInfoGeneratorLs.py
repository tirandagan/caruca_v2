from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorLs(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-A", "--author", "-b", "-B", "-c", "-C", "--color", "-d", "-D", "-f", "-F",
    #                      "--file-type", "--full-time", "-g", "--group-directories-first", "-G", "-h", "--si",
    #                      "-H", "--dereference-command-line-symlink-to-dir", "--hyperlink", "-i", "-k", "-l",
    #                      "-L", "-m", "-n", "-N", "-o", "-p", "-q", "--show-control-chars", "-Q", "-r", "-R",
    #                      "-s", "-S", "-t", "-u", "-U", "-v", "-x", "-X", "-Z", "--zero", "-1", "--help", "--version"]
    # list_of_all_options = ["--block-size", "--format", "--hide", "--indicator-style", "-I", "--quoting-style",
    #                        "--sort", "--time", "--time-style", "-T", "-w"]

    # Which ones do affect parallelizability?
    # none, because there is nothing to split: ls has no stream input (neither stdin nor the operands are
    # read as streams), so consecutive-chunk and round-robin splitting do not apply.
    # Splitting the operands into individual files is not sound either:
    #   - ls sorts all command-line operands together (unless -U/-f/--sort=none), so the output of
    #     `ls -d b a` is not `ls -d b` followed by `ls -d a`;
    #   - the column layout (-C/-x/-m, the default on a terminal) and the field widths of -l/-s/-i
    #     are computed over all entries of a listing, and -l/-s print a per-directory "total" line;
    #   - with several operands, files are listed first and directories afterwards with a header.
    # Hence no parallelizer is added and ls runs sequentially.

    def generate_info(self) -> None:
        pass
