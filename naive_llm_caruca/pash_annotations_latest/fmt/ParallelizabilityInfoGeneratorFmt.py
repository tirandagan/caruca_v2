from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorFmt(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-s", "-t", "-u", "--help", "--version"]
    # list_of_all_options = ["-p", "-w", "-g"]

    # Which ones do affect parallelizability?
    # fmt refills whole paragraphs, so a split at an arbitrary line boundary lands inside a
    # paragraph and the two halves are filled differently from the sequential run; re-running
    # fmt over the boundary lines does not repair this, since the lines after the boundary would
    # have to be re-flowed as well. Hence, in general, no CC or RR parallelizer.
    # Each FILE operand is formatted independently (a paragraph never spans two files, checked
    # with the binary), so IF x SEQ x CONC is always exact.
    # -s (--split-only) never joins lines: every input line is split on its own, so with -s the
    # output of a chunk depends only on the lines in that chunk and CC x SEQ x CONC is exact
    # (checked with the binary for -s combined with -c, -t, -u, -p, -w, -g). RR would reorder
    # the lines, so it is still not applicable.
    # --help and --version read no input at all.

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["--help", "--version"]):
            self.append_to_parallelizer_list_if_seq_conc()
            if self.does_flag_option_list_contain_at_least_one_of(["-s"]):
                self.append_to_parallelizer_list_cc_seq_conc()
