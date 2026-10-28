from typing import Optional, Set, Tuple

from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDd(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "--version"]
    # list_of_all_options = []
    # dd's settings are KEY=VALUE operands (see InputOutputInfoGeneratorDd).

    # Which ones do affect parallelizability?
    # Without conversions dd is a byte-for-byte copy, so any split of the input followed by
    # concatenation in order gives the same output: CC x SEQ x CONC and RR x SEQ x CONC.
    # Block sizes (bs=, ibs=, obs=, cbs=) only change how many bytes are moved per call and
    # leave the data untouched; status= only affects stderr; noerror/fsync/fdatasync/excl/
    # nocreat/notrunc and all iflag=/oflag= symbols do not change the data either.
    # Breaking cases:
    #   count=, skip=/iseek=, seek=/oseek=  -> depend on absolute position in the input/output
    #   conv=block, unblock, ascii, ebcdic, ibm -> record (cbs-sized) semantics across chunk boundaries
    #   conv=sync  -> pads each *input block* to ibs, so output depends on how reads are split
    #   conv=swab  -> swaps byte pairs within each input block, so byte parity of a chunk matters
    # conv=lcase and conv=ucase are per-byte and therefore fine.

    CONV_BREAKING_PARALLELISM = {"block", "unblock", "ascii", "ebcdic", "ibm", "sync", "swab"}
    KEYS_BREAKING_PARALLELISM = {"count", "skip", "iseek", "seek", "oseek"}

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]):
            return
        for operand in self.cmd_inv.operand_list:
            key, value = self.split_key_value(operand.get_name())
            if key in self.KEYS_BREAKING_PARALLELISM:
                return
            if key == "conv" and set(value.split(",")) & self.CONV_BREAKING_PARALLELISM:
                return
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()

    @staticmethod
    def split_key_value(operand: str) -> Tuple[Optional[str], str]:
        if "=" not in operand:
            return None, operand
        key, value = operand.split("=", 1)
        return key, value
