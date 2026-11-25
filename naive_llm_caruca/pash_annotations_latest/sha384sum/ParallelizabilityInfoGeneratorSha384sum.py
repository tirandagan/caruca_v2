from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSha384sum(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "--tag", "-t", "-z", "--ignore-missing", "--quiet", "--status", "--strict",
    #                      "-w", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # base-line: a digest depends on every byte of a file, so a single file can never be split (no CC/RR);
    #   but each FILE operand yields exactly one independent output line, in operand order, so
    #   `sha384sum a b` == `sha384sum a; sha384sum b` -> IF x SEQ x CONC
    # -b, -t, --tag, -z only change the per-line format and keep the per-file independence
    # -c renders parallelization infeasible: the operands are checksum lists, the exit status and the
    #   "WARNING: N computed checksums did NOT match" summary on stderr aggregate over all lines

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(["-c"]):
            self.append_to_parallelizer_list_if_seq_conc()
