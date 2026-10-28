from typing import Dict, Set

from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDd(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "--version"]
    # key=value operands = ["bs", "cbs", "conv", "count", "ibs", "if", "iflag", "obs", "of", "oflag",
    #                       "seek"/"oseek", "skip"/"iseek", "status"]

    # Which ones affect parallelizability?
    # Without conversions dd is a byte-for-byte copy, so splitting the input into pieces, running the
    # same dd on each and concatenating the results gives the same bytes: CC/RR x SEQ x CONC.
    # if=, of=: the file is embedded in a KEY=VALUE word that PaSh cannot rewrite to a fifo, so we only
    #   parallelize when the data flows through stdin and stdout.
    # count=, skip=/iseek=, seek=/oseek=: select a byte range of the whole stream -> not parallelizable.
    # conv=: lcase/ucase are per-byte maps and keep the property, as are ascii/ebcdic/ibm as long as
    #   no cbs= is given (with cbs= they imply unblock/block); noerror, fsync, fdatasync, excl,
    #   nocreat, notrunc, sparse only change how the output is opened/flushed. Everything else
    #   (block/unblock, swab, sync) works on record or block boundaries that depend on how the
    #   stream is cut -> not parallelizable (verified: outputs differ for odd-sized chunks).
    # bs=, ibs=, obs=, cbs= (without block/unblock), iflag=, oflag=, status= do not change the bytes
    #   produced.

    _CONV_SYMBOLS_KEEPING_BYTE_MAP = {
        "lcase", "ucase", "noerror", "fsync", "fdatasync", "excl", "nocreat", "notrunc", "sparse",
    }
    _CONV_SYMBOLS_KEEPING_BYTE_MAP_WITHOUT_CBS = {"ascii", "ebcdic", "ibm"}

    def _parse_key_value_operands(self):
        keys_given: Set[str] = set()
        list_symbols: Dict[str, Set[str]] = {"conv": set(), "iflag": set(), "oflag": set()}
        for operand in self.cmd_inv.operand_list:
            word = str(operand.get_name())
            if "=" not in word:
                continue
            key, value = word.split("=", 1)
            if key == "oseek":
                key = "seek"
            elif key == "iseek":
                key = "skip"
            keys_given.add(key)
            if key in list_symbols:
                list_symbols[key].update(s for s in value.split(",") if s != "")
        return keys_given, list_symbols

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]) or \
                any(str(operand.get_name()) in ("--help", "--version") for operand in self.cmd_inv.operand_list):
            return
        keys_given, list_symbols = self._parse_key_value_operands()
        if keys_given & {"if", "of", "count", "skip", "seek"}:
            return
        allowed_conv = set(self._CONV_SYMBOLS_KEEPING_BYTE_MAP)
        if "cbs" not in keys_given:
            allowed_conv |= self._CONV_SYMBOLS_KEEPING_BYTE_MAP_WITHOUT_CBS
        if not list_symbols["conv"] <= allowed_conv:
            return
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
