from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorBasenc(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--base64", "--base64url", "--base32", "--base32hex", "--base16", "--base2msbf",
    #                      "--base2lsbf", "--z85", "-d", "-i", "--help", "--version"]
    # list_of_all_options = ["-w"]

    # Which ones do affect parallelizability?
    # basenc is byte-oriented, not line-oriented: the encoders consume the input in fixed-size groups
    # (3 bytes for base64, 5 for base32, 4 for z85) and emit padding at the end of the input, and the
    # output is re-wrapped every COLS characters across the whole stream.  Cutting the input at line
    # boundaries (consec_chunks / round_robin) therefore changes the groups, inserts padding mid-stream
    # and resets the wrap column, so concatenating the parts' outputs is not equivalent to the
    # sequential run.  The same holds for decoding (-d): a line of the encoded input is only a whole
    # number of groups for particular combinations of encoding and wrap width, and -i may discard bytes
    # across the cut.  Hence no parallelizer is offered for any invocation.

    def generate_info(self) -> None:
        pass
