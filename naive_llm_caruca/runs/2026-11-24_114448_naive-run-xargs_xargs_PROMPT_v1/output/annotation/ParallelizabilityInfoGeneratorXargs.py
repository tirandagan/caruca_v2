from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorXargs(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-0", "-e", "-i", "-l", "-o", "-p", "-r", "--show-limits", "-t", "-x",
    #                      "--help", "--version"]
    # list_of_all_options = ["-a", "-d", "-E", "-I", "-L", "-n", "-P", "--process-slot-var", "-s"]

    # Which ones do affect parallelizability?
    # xargs itself is a pure line/item consumer, but its observable behaviour is that of the
    # command it executes, which is arbitrary (rm, mkdir, a script with side effects, ...).
    # Splitting the input changes how items are batched into invocations: without -n/-L/-I the
    # batch boundaries depend on the size limit (-s), so `xargs echo` on two halves yields two lines
    # where the sequential run yields one; -E makes the rest of the input depend on an earlier item;
    # -r depends on whether the whole input is empty; -P already makes output order indeterminate.
    # Even with -n1/-L1/-I (one item per invocation) a parallel split is only sound if the executed
    # command is pure and emits output only to stdout, which cannot be decided from the invocation.
    # Hence we conservatively do not parallelize at all.

    def generate_info(self) -> None:
        pass
