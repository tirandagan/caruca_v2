from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorDd(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--help", "--version"]
    # list_of_all_options = ["bs", "cbs", "conv", "count", "ibs", "if", "iflag", "obs", "of", "oflag",
    #                        "seek", "oseek", "skip", "iseek", "status"]

    # Which ones do affect input/output?
    # dd has no positional operands; the data source and sink are given by if= and of=.
    # if=FILE  reads FILE (typed STREAM_INPUT in dd.json); without it, dd reads stdin.
    # of=FILE  writes FILE (typed STREAM_OUTPUT in dd.json); without it, dd writes stdout.
    # Everything else (bs/ibs/obs/cbs/count/skip/seek/conv/iflag/oflag) changes how the copy
    # is done, not which files are touched. Transfer statistics go to stderr, so status= is ignored.
    # Tested with the binary (coreutils 9.4): `if=-` opens a file literally named "-", not stdin;
    # when if= or of= is repeated, the last occurrence wins.
    # Caveat: with seek=/oseek=, conv=notrunc or oflag=append the output file is modified in place
    # rather than replaced; it is still reported as a stream output here.

    def generate_info(self) -> None:
        # assumption that help/version not provided
        if not self.does_flag_option_list_contain_at_least_one_of(["if"]):
            self.set_implicit_use_of_stdin()
        if not self.does_flag_option_list_contain_at_least_one_of(["of"]):
            self.set_implicit_use_of_stdout()
        if self.get_operand_list_length() > 0:
            # dd itself rejects these with "unrecognized operand"
            raise Exception('dd does not take positional operands')
