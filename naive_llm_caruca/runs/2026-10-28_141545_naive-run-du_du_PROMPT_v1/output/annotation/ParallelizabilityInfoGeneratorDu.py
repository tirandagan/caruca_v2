from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDu(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-0", "-a", "--apparent-size", "-b", "-c", "-D", "-H", "-h", "--inodes", "-k", "-L",
    #                      "-l", "-m", "-P", "-S", "--si", "-s", "--time", "-x", "--help", "--version"]
    # list_of_all_options = ["-B", "-d", "--files0-from", "-t", "--time-style", "-X", "--exclude", "--exclude-from"]

    # Which ones do affect parallelizability?
    # None make it feasible: du does not consume a data stream, so consec_chunks and round_robin do not apply
    # (there is no input to cut into pieces; du never reads stdin unless --files0-from=- or -X - is given,
    # and even then stdin carries names/patterns, not data).
    # indiv_files is not sound either: PaSh would hand each copy its operand through a fifo, and du reports
    # the size of the fifo (0) rather than walking the named tree. Even on real paths, "du a b" differs from
    # "du a; du b" because hard links shared between arguments are counted once (unless -l), and -c needs the
    # per-argument totals summed rather than concatenated.

    def generate_info(self) -> None:
        # not parallelizable: nothing is appended
        pass
