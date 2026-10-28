from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorConvert(InputOutputInfoGeneratorInterface):

    # convert (ImageMagick 6): `convert [options] input-file ... [options] output-file`
    #
    # Which flags/options affect input/output?
    # - operands: every operand but the last is an input image, the last operand is the output image.
    #   Images are whole-file binary data, so they are "other" inputs/outputs, never line streams.
    # - `-` as an operand is stdin (input position) or stdout (output position); PaSh resolves a bare
    #   `-` itself, but convert also accepts `fmt:-` (e.g. `png:-`) and the `info:` pseudo-output,
    #   which we translate to implicit stdin/stdout use.
    # - pseudo-image operands (xc:red, logo:, rose:, label:..., gradient:..., null:, ...) are not files;
    #   we can only re-type the first operand with the available interface.
    # - options with file arguments are typed in convert.json: -cdl/-decipher/-encipher/-profile are
    #   CONFIG_INPUT, -clip-mask/-mask/-remap/-map/-texture/-tile are OTHER_INPUT, -write/+write is
    #   OTHER_OUTPUT. `-write info:` / `-write -` print to stdout.
    # - -identify, -print, -verbose, -bench, -help, -version, -list print to stdout.
    #
    # Known over-approximations:
    # - a multi-image result written to a single-image format produces out-0.png, out-1.png, ...
    #   instead of out.png; we still report the operand as written.
    # - `(` and `)` (image stack parentheses) and `@list.txt` (file containing input file names) appear
    #   as ordinary input operands.
    # - -draw and -fx strings may reference further image files; these are not tracked.

    PSEUDO_IMAGE_PREFIXES = ("xc:", "canvas:", "logo:", "rose:", "wizard:", "granite:", "netscape:",
                             "label:", "caption:", "gradient:", "radial-gradient:", "plasma:",
                             "pattern:", "null:", "text:", "tile:", "pango:", "fractal:", "hald:",
                             "inline:", "info:", "magick:", "fd:", "x:", "print:", "win:", "clipboard:",
                             "screenshot:", "stegano:", "vid:")

    STDOUT_FLAGS = ["-identify", "+identify", "-print", "+print", "-verbose", "-bench", "+bench",
                    "-help", "+help", "-version", "+version", "-list", "+list"]

    @staticmethod
    def _is_std_descriptor(name: str) -> bool:
        # "-" is handled by PaSh itself (operand type filename-or-std-descriptor)
        return name.endswith(":-") or name in ("fd:0", "fd:1", "/dev/stdin", "/dev/stdout")

    @staticmethod
    def _operand_name(operand) -> str:
        for attr in ("get_name_as_string", "get_name"):
            if hasattr(operand, attr):
                return str(getattr(operand, attr)())
        return str(getattr(operand, "name", operand))

    def _option_args(self, names):
        args = []
        for flag_option in self.get_flag_option_list_filtered_with(names):
            arg = getattr(flag_option, "get_arg_as_string", None)
            if callable(arg):
                args.append(str(arg()))
            elif hasattr(flag_option, "arg"):
                args.append(str(flag_option.arg))
        return args

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(self.STDOUT_FLAGS):
            self.set_implicit_use_of_stdout()

        n = self.get_operand_list_length()
        if n == 0:
            # only meaningful for -help/-version/-list, which produce output on stdout (already set)
            return
        if n == 1:
            # convert rejects this ("no images defined"); treat the operand as an input image
            self.all_operands_are_other_inputs()
        else:
            self.all_but_last_operand_is_other_input()
            self.only_last_operand_is_other_output()

        operand_names = [self._operand_name(op) for op in self.cmd_inv.operand_list]
        inputs, output = operand_names[:-1], operand_names[-1]

        # std descriptors spelled with an explicit format, e.g. `png:-`
        if any(self._is_std_descriptor(name) for name in inputs):
            self.set_implicit_use_of_stdin()
        if n >= 2 and (self._is_std_descriptor(output) or output.startswith("info:")):
            self.set_implicit_use_of_stdout()

        # `-write info:` or `-write -` prints image characteristics to stdout
        for arg in self._option_args(["-write", "+write"]):
            if arg == "-" or arg.startswith("info:") or self._is_std_descriptor(arg):
                self.set_implicit_use_of_stdout()

        # pseudo-image operands are generated in memory, not read from a file
        first = operand_names[0].lower()
        if n >= 2 and first.startswith(self.PSEUDO_IMAGE_PREFIXES):
            self.set_first_operand_as_config_arg_type_string()
