from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorDf(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-a", "-h", "-H", "-i", "-k", "-m", "-l", "--no-sync", "-P", "--sync",
    #                      "--total", "-T", "-v", "--help", "--version"]
    # list_of_all_options = ["-B", "--output", "-t", "-F", "-x"]

    # Which ones do affect input/output?
    # none: df never reads standard input and always writes its report to standard output
    # (assumption that --help/--version are not given).
    # The operands are files whose containing file system is looked up (stat/statfs);
    # their contents are not read, so they are "other" inputs rather than streaming inputs.
    # With no operands, df reports on all mounted file systems and still reads no stdin.

    def generate_info(self) -> None:
        self.set_implicit_use_of_stdout()
        self.all_operands_are_other_inputs()
