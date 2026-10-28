from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorPandoc(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags and list_of_all_options: see InputOutputInfoGeneratorPandoc

    # Which ones do affect parallelizability?
    # none makes it feasible: pandoc parses its whole input (all operands concatenated) into one document
    # tree before writing anything. Document structure spans lines and files: a chunk boundary can fall
    # inside a paragraph, list, table, code block or raw block, so the result on a part differs from the
    # result on the whole (consec_chunks/round_robin are unsound). Even per file (indiv_files), the
    # output is a single document: footnotes and link references are resolved across files and emitted
    # at the end, metadata blocks apply to the whole document, --standalone wraps everything in one
    # header/footer, --toc, --number-sections and citeproc (-C) need the complete document, and binary
    # output formats (docx, odt, epub, pdf) cannot be concatenated. Concatenating per-file outputs would
    # therefore not reproduce the sequential output even for plain text formats.

    def generate_info(self) -> None:
        # no parallelizer is appended: pandoc is treated as not parallelisable
        pass
