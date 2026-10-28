from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorShuf(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-e", "-r", "-z", "--help", "--version"]
    # list_of_all_options = ["-i", "-n", "-o", "--random-source"]

    # Which ones do affect parallelizability?
    # shuf draws a uniformly random permutation of its whole input, so every output line depends on
    # every input line. Shuffling consecutive chunks or round-robin parts independently and
    # concatenating them does not yield a uniform permutation (lines never leave their part);
    # restoring uniformity would mean shuffling the concatenation again, i.e. running the
    # sequential command on the full input, so nothing is gained.
    # -n COUNT additionally selects a global random sample: a per-part -n would over-produce and a
    #   second pass would be needed to subsample uniformly.
    # -r -n COUNT samples with replacement; per-part sampling is not uniform over the whole input.
    # -e and -i do not read a data stream at all, so there is nothing to split.
    # Hence shuf is not parallelized in any configuration.

    def generate_info(self) -> None:
        pass
