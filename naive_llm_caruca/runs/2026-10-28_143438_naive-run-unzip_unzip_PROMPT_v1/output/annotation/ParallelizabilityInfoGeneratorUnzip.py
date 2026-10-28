from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorUnzip(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-Z", "-c", "-f", "-l", "-p", "-t", "-T", "-u", "-v", "-z", "-a", "-b", "-B", "-C",
    #                      "-D", "-F", "-j", "-K", "-L", "-M", "-n", "-o", "-q", "-U", "-V", "-W", "-X", "-:",
    #                      "-^", "-h", "-1", "-2", "-s", "-m"]
    # list_of_all_options = ["-d", "-x", "-P", "-O", "-I"]

    # Which ones do affect parallelizability?
    # none: unzip never consumes a data stream.  Its only input is the archive operand, which it reads by
    # seeking (the central directory sits at the end of the file and "-" is not accepted as stdin), so
    # there is no stream to split into chunks or lines.  The outputs are either files on disk or, with
    # -p/-c, the concatenated member contents on stdout, which cannot be produced from pieces of the
    # archive.  Hence no parallelizer is added for any invocation.

    def generate_info(self) -> None:
        pass
