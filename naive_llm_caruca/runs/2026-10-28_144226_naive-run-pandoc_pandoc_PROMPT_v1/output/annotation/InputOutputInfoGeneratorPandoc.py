from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorPandoc(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["--file-scope", "--sandbox", "-s", "--ascii", "--toc", "-N", "--no-highlight", "-p",
    #                      "--self-contained", "--embed-resources", "--no-check-certificate", "--strip-comments",
    #                      "--reference-links", "--list-tables", "--listings", "-i", "--section-divs",
    #                      "--html-q-tags", "-C", "--natbib", "--biblatex", "--mathml", "--webtex", "--mathjax",
    #                      "--katex", "--gladtex", "--trace", "--dump-args", "--ignore-args", "--verbose",
    #                      "--quiet", "--fail-if-warnings", "--bash-completion", "--list-input-formats",
    #                      "--list-output-formats", "--list-extensions", "--list-highlight-languages",
    #                      "--list-highlight-styles", "-v", "-h"]
    # list_of_all_options = ["-f", "-t", "-o", "--data-dir", "-M", "--metadata-file", "-d", "--template", "-V",
    #                        "--wrap", "--toc-depth", "--number-offset", "--top-level-division",
    #                        "--extract-media", "--resource-path", "-H", "-B", "-A", "--highlight-style",
    #                        "--syntax-definition", "--dpi", "--eol", "--columns", "--tab-stop", "--pdf-engine",
    #                        "--pdf-engine-opt", "--reference-doc", "--request-header", "--abbreviations",
    #                        "--indented-code-classes", "--default-image-extension", "-F", "-L",
    #                        "--shift-heading-level-by", "--base-header-level", "--track-changes",
    #                        "--reference-location", "--markdown-headings", "--slide-level",
    #                        "--email-obfuscation", "--id-prefix", "-T", "-c", "--epub-subdirectory",
    #                        "--epub-cover-image", "--epub-title-page", "--epub-metadata", "--epub-embed-font",
    #                        "--split-level", "--chunk-template", "--epub-chapter-level", "--ipynb-output",
    #                        "--bibliography", "--csl", "--citation-abbreviations", "--log", "-D",
    #                        "--print-default-data-file", "--print-highlight-style"]

    # Which ones do affect input/output?
    # - the informational modes (--help, --version, --list-*, --print-*, --bash-completion) print to stdout
    #   and exit without reading any document; operands are ignored
    # - no operands: the document is read from stdin; a `-` operand also means stdin
    # - all operands are concatenated into one document and read in full (not line-streamed, but
    #   they are the data the command processes, so they are its stream inputs)
    # - -o/--output FILE redirects the result from stdout to FILE; `-o -` is stdout again
    # - file-typed options (templates, filters, bibliographies, ...) are typed in the parser table
    # - --extract-media DIR and --log FILE are written (OTHER_OUTPUT, typed in the parser table)
    # - -d/--defaults FILE may itself name input and output files; this is not modelled
    # - --resource-path (colon-separated directories) and --data-dir are not modelled as inputs

    informational_modes = ["-h", "--help", "-v", "--version", "--bash-completion",
                           "--list-input-formats", "--list-output-formats", "--list-extensions",
                           "--list-highlight-languages", "--list-highlight-styles",
                           "-D", "--print-default-template", "--print-default-data-file",
                           "--print-highlight-style"]

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(self.informational_modes):
            # nothing is converted: operands are not files that get read
            self.set_all_operands_as_config_arg_type_string()
            # --print-* honour a preceding -o, the others always print to stdout; approximate with -o
            if not self.output_goes_to_file():
                self.set_implicit_use_of_stdout()
            return
        self.if_no_operands_given_stdin_implicitly_used()
        self.all_operands_are_streaming_inputs()
        if not self.output_goes_to_file():
            self.set_implicit_use_of_stdout()

    def output_goes_to_file(self) -> bool:
        """-o/--output present with an argument other than `-`"""
        output_options = self.get_flag_option_list_filtered_with(["-o", "--output"])
        if len(output_options) == 0:
            return False
        for option in output_options:
            if self.option_arg_as_string(option) == "-":
                return False
        return True

    @staticmethod
    def option_arg_as_string(option) -> str:
        arg = getattr(option, "option_arg", None)
        if arg is None:
            return ""
        for attr in ("get_name", "name"):
            value = getattr(arg, attr, None)
            if callable(value):
                try:
                    value = value()
                except Exception:
                    continue
            if isinstance(value, str):
                return value
        return str(arg)
