from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        flags = {str(fo.get_name()) for fo in self.cmd_inv.flag_option_list}
        n = self.get_operand_list_length()
        if n == 0 and flags in ({'--complement', '-f'}, {'--output-delimiter', '-b'}, {'--output-delimiter', '-c'}, {'--output-delimiter', '-f'}, {'-b', '-n'}, {'-c', '-n'}, {'-d', '-f'}, {'-f', '-n'}, {'-b'}, {'-c'}, {'-f'}):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
