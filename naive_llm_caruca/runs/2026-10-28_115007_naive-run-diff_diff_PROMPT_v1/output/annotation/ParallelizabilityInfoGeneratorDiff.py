from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDiff(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--normal", "-q", "-s", "-c", "--context", "-u", "--unified", "-0".."-9", "-e", "-n",
    #                      "-y", "--left-column", "--suppress-common-lines", "--sdiff-merge-assist", "-p", "-t",
    #                      "-T", "--suppress-blank-empty", "-l", "-r", "--no-dereference", "-N", "-P",
    #                      "--ignore-file-name-case", "--no-ignore-file-name-case", "-i", "-E", "-Z", "-b", "-w",
    #                      "-B", "-a", "--binary", "--strip-trailing-cr", "-d", "-H", "--inhibit-hunk-merge", "-h",
    #                      "--color", "--help", "-v"]
    # list_of_all_options = ["-C", "-U", "-W", "-F", "-L", "--tabsize", "-x", "-X", "-S", "--from-file", "--to-file",
    #                        "-I", "-D", "--old-group-format", "--new-group-format", "--changed-group-format",
    #                        "--unchanged-group-format", "--line-format", "--new-line-format", "--old-line-format",
    #                        "--unchanged-line-format", "--horizon-lines", "--palette"]

    # Which ones do affect parallelizability?
    # none make it feasible: diff computes an alignment (longest common subsequence) between two complete
    # inputs, so it has no single data stream that could be split into independent parts.  Splitting one
    # file while the other stays whole changes the result, splitting both consistently requires knowing the
    # alignment first, and the hunk headers carry absolute line numbers of both files.  -q/-s exit early
    # and -e/-n/-D/--*-format change output shape but not this fundamental property.
    # Hence no parallelizer is ever appended.

    def generate_info(self) -> None:
        pass
