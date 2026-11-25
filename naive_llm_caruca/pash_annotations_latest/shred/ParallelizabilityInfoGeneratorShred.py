from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorShred(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-f", "-u", "-v", "-x", "-z", "--help", "--version"]
    # list_of_all_options = ["-n", "--random-source", "-s", "--remove"]

    # Which ones do affect parallelizability?
    # None: shred consumes no input stream and produces no output stream. It overwrites (and
    # optionally removes) the named files in place, so there is nothing to split and recombine.
    # Writing to standard output ("-") is a byte-position-dependent in-place overwrite as well.

    def generate_info(self) -> None:
        pass
