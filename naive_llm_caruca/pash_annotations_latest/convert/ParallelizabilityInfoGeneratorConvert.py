from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorConvert(ParallelizabilityInfoGeneratorInterface):

    # convert reads whole image files (binary, not line-structured) and writes whole image files.
    # Neither splitting its input into consecutive chunks nor dealing lines out round-robin yields
    # valid images, and with several input operands the result is a single multi-image document
    # (or a numbered series out-0.png, out-1.png, ...) rather than a concatenation of per-file outputs,
    # so even an individual-files split cannot be recombined by concatenation.
    # The invocation is therefore never parallelised; no parallelizer is appended.

    def generate_info(self) -> None:
        pass
