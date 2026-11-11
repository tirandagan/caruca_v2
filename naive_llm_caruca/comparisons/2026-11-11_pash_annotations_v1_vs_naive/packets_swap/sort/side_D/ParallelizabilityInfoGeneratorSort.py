from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface

class ParallelizabilityInfoGeneratorSort(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        flags = {str(fo.get_name()) for fo in self.cmd_inv.flag_option_list}
        n = self.get_operand_list_length()
        if n == 0 and flags in ({'--compress-program', '-m'}, {'--parallel', '-m'}, {'--random-source', '-T'}, {'--random-source', '-m'}, {'--sort', '-m'}, {'--sort', '-s'}, {'--sort', '-u'}, {'-M', '-m'}, {'-M', '-s'}, {'-R', '-m'}, {'-T', '-m'}, {'-V', '-m'}, {'-b', '-m'}, {'-d', '-m'}, {'-f', '-m'}, {'-g', '-m'}, {'-g', '-s'}, {'-g', '-u'}, {'-h', '-m'}, {'-h', '-s'}, {'-h', '-u'}, {'-i', '-m'}, {'-k', '-m'}, {'-k', '-s'}, {'-k', '-u'}, {'-m', '-n'}, {'-m', '-r'}, {'-m', '-s'}, {'-m', '-t'}, {'-m', '-u'}, {'-n', '-s'}, {'-n', '-u'}, {'-m'}) or (n == 1 and flags in ({'-m'},)):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()
