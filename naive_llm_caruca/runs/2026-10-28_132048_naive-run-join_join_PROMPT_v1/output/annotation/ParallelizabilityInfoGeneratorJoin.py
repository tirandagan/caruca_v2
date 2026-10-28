from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorJoin(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-i", "--check-order", "--nocheck-order", "--header", "-z", "--help", "--version"]
    # list_of_all_options = ["-a", "-e", "-j", "-o", "-t", "-v", "-1", "-2"]

    # Which ones do affect parallelizability?
    # join is a two-input merge: every output line depends on the pairing of lines from FILE1 with
    # lines from FILE2 by join field, and both inputs must be read in lockstep (both sorted).
    # The available splitters (indiv_files, consec_chunks, round_robin) divide a single input
    # stream; dealing out or chunking one file without co-partitioning the other by join key
    # breaks pairing (and -a/-v/--header/--check-order semantics), so no parallelizer applies.
    # Splitting one file into consecutive chunks while re-reading the whole other file per chunk
    # would be correct without -a 2/-v 2/--header (for FILE1 split), but that is not expressible
    # with the current splitter/mapper model, so the invocation is left sequential.

    def generate_info(self) -> None:
        pass
