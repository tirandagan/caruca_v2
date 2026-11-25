from pash_annotations.datatypes.BasicDatatypes import Option
from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorMogrify(ParallelizabilityInfoGeneratorInterface):

    # mogrify processes each operand (image file) independently and in order: the image is
    # read, all operators are applied, and the result is written back.  Image-sequence
    # operators (-append, -flatten, -layers, ...) act on the frames of one file, never across
    # operands.  Hence the work splits by individual files (IF x SEQ x CONC); the only output
    # stream is what -identify/-print/-verbose write to stdout, one block per file, which
    # concatenation in order reproduces.
    #
    # Which flags/options affect parallelizability?
    # -help, -version, -list   -> nothing is processed, nothing to parallelize
    # -write FILE              -> every copy would write the same file; not parallelized
    # -seed VALUE              -> one random sequence spans all files; separate copies would
    #                             restart it per file; not parallelized
    # -distribute-cache PORT   -> runs a pixel-cache server; not parallelized
    # two-argument options     -> only parallelized when the parse could be repaired (see IO class)
    # operand `-`              -> stdin/stdout image; not parallelized

    TWO_ARGUMENT_OPTIONS = ["-annotate", "-copy", "-distort", "+distort", "-evaluate", "-floodfill",
                            "-function", "-limit", "-morphology", "+morphology", "-set",
                            "-sparse-color", "+sparse-color", "-statistic"]
    NON_PARALLELIZABLE_OPTIONS = ["-help", "+help", "-version", "+version", "-list", "+list",
                                  "-write", "+write", "-seed", "-distribute-cache", "+distribute-cache"]

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(self.NON_PARALLELIZABLE_OPTIONS):
            return
        operand_names = [str(operand.get_name()) for operand in self.cmd_inv.operand_list]
        flag_option_list = self.cmd_inv.flag_option_list
        if len(flag_option_list) > 0 and isinstance(flag_option_list[-1], Option) \
                and flag_option_list[-1].get_name() in self.TWO_ARGUMENT_OPTIONS:
            # the first "operand" is the option's second word
            operand_names = operand_names[1:]
        for name in operand_names:
            if name == "-" or name.endswith(":-"):
                return
            if len(name) > 1 and (name.startswith("-") or name.startswith("+")):
                return  # unparsed options after a two-argument option
        self.append_to_parallelizer_list_if_seq_conc()
