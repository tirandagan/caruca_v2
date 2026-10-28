from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSha224sum(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status",
    #                      "--strict", "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # A SHA-224 digest is computed over a whole file, so the content of a single file can never be
    # split into chunks (neither CC nor RR); only whole files can be handled in parallel.
    # Without -c, the output is one line per operand, in operand order, and each line depends only on
    # its own file, so IF x SEQ x CONC reproduces the sequential output exactly (-b, -t, --tag and -z
    # only change the formatting of each line and are passed on to the mappers).
    # With -c, the operands are checksum lists and the command prints summary warnings on stderr and
    # computes an overall exit status over all lines, so we do not parallelize.

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            self.append_to_parallelizer_list_if_seq_conc()
