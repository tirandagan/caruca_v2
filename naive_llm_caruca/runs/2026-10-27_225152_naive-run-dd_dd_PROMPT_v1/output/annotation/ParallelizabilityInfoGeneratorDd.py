from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorDd(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "--version"]
    # list_of_all_options = ["bs", "cbs", "conv", "count", "ibs", "if", "iflag", "obs", "of", "oflag",
    #                        "seek", "oseek", "skip", "iseek", "status"]

    # Which ones do affect parallelizability?
    # base-line: a plain dd is a byte-for-byte copy, like cat, so CC/RR x SEQ x CONC works.
    # count, skip/iseek, seek/oseek select a region by position in the stream and are not parallelized.
    # conv symbols that act byte-by-byte are safe: ascii, ebcdic, ibm, lcase, ucase (tested: output
    #   of a split input concatenates to the output of the whole input).
    # conv symbols that depend on where block or record boundaries fall are not safe:
    #   swab (pairs of bytes), sync (pads each input block to ibs), block/unblock (cbs-sized records).
    # bs/ibs/obs only change the block size used for I/O, not the bytes written; cbs is inert
    #   without block/unblock; iflag/oflag and the remaining conv symbols (sparse, excl, nocreat,
    #   notrunc, noerror, fdatasync, fsync) only affect how the files are opened or flushed.
    # status only changes what is printed on stderr.

    _CONVS_BREAKING_SPLIT = ["swab", "sync", "block", "unblock"]

    def _conv_symbols(self) -> list:
        symbols = []
        for option in self.get_flag_option_list_filtered_with(["conv"]):
            option_arg = getattr(option, "option_arg", None)
            if option_arg is None:
                continue
            text = getattr(option_arg, "name", option_arg)
            symbols.extend(symbol for symbol in str(text).split(",") if symbol)
        return symbols

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["count", "skip", "iseek", "seek", "oseek"]):
            return
        if any(symbol in self._CONVS_BREAKING_SPLIT for symbol in self._conv_symbols()):
            return
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
