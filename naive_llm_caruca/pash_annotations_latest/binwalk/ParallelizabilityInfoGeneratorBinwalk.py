from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorBinwalk(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-B", "-A", "-b", "-I", "-e", "-M", "-1", "-r", "-z", "-V", "-E", "-F", "-J", "-Q",
    #                      "-N", "-W", "-G", "-i", "-U", "-u", "-w", "-X", "-Z", "-P", "-S", "-c", "-t", "-q",
    #                      "-v", "-h"]
    # list_of_all_options = ["-R", "-m", "-x", "-y", "-D", "-d", "-C", "-j", "-n", "-0", "-H", "-L", "-l", "-o",
    #                        "-O", "-K", "-g", "-f", "-a", "-p", "-s"]

    # Which ones do affect parallelizability?
    # None make it feasible:
    # - the input is binary and is not line-oriented; signatures may straddle any cut point, and every
    #   reported offset is relative to the start of the file, so consecutive-chunk or round-robin
    #   splitting changes the result
    # - binwalk does not read stdin and needs seekable files, so a splitter cannot feed it
    # - per-file splitting (indiv_files) is not equivalent either: with two or more operands binwalk
    #   prints a "Scan Time / Target File / MD5 Checksum / Signatures" header per file that a single-file
    #   run omits (verified), -W compares the files against each other, and -f appends to one log
    # Therefore no parallelizer is appended.

    def generate_info(self) -> None:
        pass
