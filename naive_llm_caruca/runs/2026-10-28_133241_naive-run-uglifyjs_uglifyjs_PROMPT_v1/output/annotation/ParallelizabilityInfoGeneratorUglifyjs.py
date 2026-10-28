from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorUglifyjs(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-h", "-v", "-c", "-m", "--mangle-props", "-b", "--annotations", "--no-annotations",
    #                      "--comments", "-e", "--expression", "--ie", "--ie8", "--keep-fargs", "--keep-fnames",
    #                      "--module", "--rename", "--no-rename", "--self", "--source-map", "--timings",
    #                      "--toplevel", "--v8", "--validate", "--verbose", "--warn", "--webkit",
    #                      "--in-situ", "--reduce-test"]
    # list_of_all_options = ["-p", "-O", "-o", "--config-file", "-d", "--name-cache", "--wrap"]

    # Which ones do affect parallelizability?
    # none: uglifyjs parses all of its input into one AST before producing any output, so the
    # input cannot be cut into chunks (a chunk boundary inside a statement is a syntax error) and
    # all files are processed in one scope (mangling, --toplevel, --wrap, --enclose, name cache)
    # so even per-file processing would change the result; nothing is appended

    def generate_info(self) -> None:
        pass
