from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorUglifyjs(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-h", "-v", "-c", "-m", "--mangle-props", "-b", "--annotations", "--no-annotations",
    #                      "--comments", "-e", "--expression", "--ie", "--ie8", "--keep-fargs", "--keep-fnames",
    #                      "--module", "--rename", "--no-rename", "--self", "--source-map", "--timings",
    #                      "--toplevel", "--v8", "--validate", "--verbose", "--warn", "--webkit",
    #                      "--in-situ", "--reduce-test"]
    # list_of_all_options = ["-p", "-O", "-o", "--config-file", "-d", "--name-cache", "--wrap"]

    # Which ones do affect input/output?
    # operands are the JavaScript source files, all read (and glob-expanded by uglifyjs itself);
    #   with no operands the program is read from stdin (a lone "-" is ignored, it is not stdin)
    # -o FILE writes the result to FILE instead of stdout, except for the special names
    #   "ast" and "spidermonkey" which dump the AST as JSON to stdout
    # --source-map together with -o FILE additionally writes FILE.map (without -o only
    #   url=inline is allowed); --source-map content=FILE also reads FILE; both are not modelled
    # --name-cache FILE is read (if present) and rewritten; typed OTHER_OUTPUT in the parser table
    # --config-file FILE is read as configuration (CONFIG_INPUT in the parser table)
    # --in-situ minifies every operand in place, i.e. each operand is read and then overwritten
    # --self ignores the operands and builds UglifyJS from its own sources
    # -c, -m, -b, --mangle-props, --comments, -e, --source-map take an optional value that is only
    #   consumed when the next word does not start with "-"; the parser table lists them as flags
    #   (the common `-c -m -o out.js` shape), so a value given to them shows up as an extra operand

    def generate_info(self) -> None:
        # assumption that help/version not provided
        if self.does_flag_option_list_contain_at_least_one_of(["--in-situ"]):
            # every operand is read and then replaced with the minified output
            self.all_operands_are_other_outputs()
            return
        if self.does_flag_option_list_contain_at_least_one_of(["--self"]):
            # operands are ignored, the library's own files are the input
            self.set_all_operands_as_config_arg_type_string()
        else:
            self.all_operands_are_streaming_inputs()
            self.if_no_operands_given_stdin_implicitly_used()
        if self.does_flag_option_list_contain_at_least_one_of(["-o", "--output"]):
            # -o ast / -o spidermonkey print to stdout instead of writing a file
            if self.__output_option_is_ast_dump():
                self.set_implicit_use_of_stdout()
            # otherwise the -o argument is already typed STREAM_OUTPUT by the parser table
        else:
            self.set_implicit_use_of_stdout()

    def __output_option_is_ast_dump(self) -> bool:
        for flag_option in self.get_flag_option_list_filtered_with(["-o", "--output"]):
            arg = flag_option.get_arg() if hasattr(flag_option, "get_arg") else None
            if arg is None:
                continue
            name = arg.get_name() if hasattr(arg, "get_name") else str(arg)
            if name in ["ast", "spidermonkey"]:
                return True
        return False
