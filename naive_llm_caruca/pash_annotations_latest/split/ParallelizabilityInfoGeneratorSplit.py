from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSplit(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-d", "-x", "-e", "-u", "--verbose", "--help", "--version"]
    # list_of_all_options = ["-a", "--additional-suffix", "-b", "-C", "--filter", "-l", "-n", "-t"]

    # Which ones do affect parallelizability?
    # None make it feasible:
    #   - In the default mode the result is a set of files PREFIXaa, PREFIXab, ... whose names
    #     depend on the position of each piece in the whole input. Running split on parts of the
    #     input would produce overlapping names (each copy starts again at PREFIXaa), and the
    #     outputs are files rather than a stream, so there is nothing to concatenate or merge.
    #   - With -n K/N, l/K/N or r/K/N the Kth chunk goes to stdout, but which bytes/lines belong
    #     to chunk K depends on the total size of the input, so a part cannot be processed
    #     independently.
    #   - --filter hands pieces to an arbitrary shell command.
    # Hence no parallelizer is appended.

    def generate_info(self) -> None:
        pass
