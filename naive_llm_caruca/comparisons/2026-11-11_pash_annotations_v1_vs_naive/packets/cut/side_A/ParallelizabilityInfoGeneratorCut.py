from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorCut(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        if not self.does_flag_option_list_contain_at_least_one_of(['-z']):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
