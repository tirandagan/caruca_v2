from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorGrep(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        flags = {str(fo.get_name()) for fo in self.cmd_inv.flag_option_list}
        n = self.get_operand_list_length()
        if n == 1 and flags in ({'-v'}, set()):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
