from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface
from pash_annotations.datatypes.AccessKind import make_other_input, make_other_output
from pash_annotations.datatypes.BasicDatatypes import WhichClassForArg


class InputOutputInfoGeneratorUnzip(InputOutputInfoGeneratorInterface):

    # Command line (UnZip 6.00, Unix build):
    #   unzip [-Z] [-cflptTuvz[abjnoqsCDKLMUVWX$/:^]] file[.zip] [file(s) ...] [-x xfile(s) ...] [-d exdir]
    #
    # list_of_all_flags = ["-Z", "-c", "-f", "-l", "-p", "-t", "-T", "-u", "-v", "-z", "-a", "-b", "-B", "-C",
    #                      "-D", "-F", "-j", "-K", "-L", "-M", "-n", "-o", "-q", "-U", "-V", "-W", "-X", "-:",
    #                      "-^", "-h", "-1", "-2", "-s", "-m"]
    #   (-1, -2, -s, -m are zipinfo-mode flags, only accepted after -Z)
    # list_of_all_options = ["-d", "-x", "-P", "-O", "-I"]
    #
    # Operands: the first operand is always the archive; every further operand is an archive-member
    # pattern (a string, not a file on disk).  unzip also accepts its -x xlist and -d exdir *after* the
    # archive name, and the parser hands those words to us as operands, so we look for them there.
    #
    # Which ones do affect input/output?
    # action options:
    #   -p, -c            member contents go to stdout (pure stream)
    #   -l, -v, -z, -Z, -h listing/comment/help on stdout, nothing written to disk
    #   -t                test only: summary on stdout (suppressed by -qq), nothing written to disk
    #   -T                sets the archive's own timestamp -> the archive is an output
    #   default/-f/-u     extract into the current directory or into exdir (-d)
    # modifiers:
    #   -q                suppresses the per-file progress lines on stdout while extracting (-qq: also the
    #                     -t summary); listings with -l/-v/-z/-Z are still printed
    #   -o, -n            no overwrite prompt; without them unzip reads the answer to "replace foo?" from
    #                     stdin whenever a file already exists on disk
    #   -d exdir          extraction directory (an "other output"); typed by the parser table if it
    #                     precedes the archive, handled below if it follows it
    # Assumptions/approximations:
    #   - the extraction target without -d is the current directory, which we cannot name as an output
    #   - the archive given without its .zip suffix (unzip looks for file.zip) is reported as written
    #   - a glued "-dexdir" after the archive is left as a plain string
    #   - password prompts for encrypted members (read from the terminal) are ignored
    #   - the archive is read by seeking (central directory at the end), hence OTHER_INPUT, never a stream;
    #     a lone "-" is *not* stdin for this build

    def generate_info(self) -> None:
        zipinfo_mode = self.does_flag_option_list_contain_at_least_one_of(["-Z"])
        pipe_mode = (not zipinfo_mode) and self.does_flag_option_list_contain_at_least_one_of(["-p", "-c"])
        test_mode = (not zipinfo_mode) and self.does_flag_option_list_contain_at_least_one_of(["-t"])
        timestamp_mode = (not zipinfo_mode) and self.does_flag_option_list_contain_at_least_one_of(["-T"])
        list_mode = zipinfo_mode or self.does_flag_option_list_contain_at_least_one_of(["-l", "-v", "-z", "-h"])
        extract_mode = not (zipinfo_mode or pipe_mode or test_mode or timestamp_mode or list_mode)
        quiet_count = len(self.get_flag_option_list_filtered_with(["-q"]))

        # stdout
        if pipe_mode or list_mode:
            self.set_implicit_use_of_stdout()
        elif test_mode:
            if quiet_count < 2:
                self.set_implicit_use_of_stdout()
        else:  # extraction or -T: progress messages unless quiet
            if quiet_count < 1:
                self.set_implicit_use_of_stdout()

        if self.get_operand_list_length() == 0:
            # "unzip" alone prints the usage screen, "unzip -v" the version screen
            return

        # stdin: overwrite prompt while extracting to disk
        if extract_mode and not self.does_flag_option_list_contain_at_least_one_of(["-o", "-n"]):
            self.set_implicit_use_of_stdin()

        # operands: everything but the archive is a member pattern (or a trailing -x / -d word)
        self.set_all_operands_as_config_arg_type_string()
        operand_list_typer = self.input_output_info.operand_list_typer
        if timestamp_mode:
            operand_list_typer[0] = (WhichClassForArg.FILESTD, make_other_output())
        else:
            operand_list_typer[0] = (WhichClassForArg.FILESTD, make_other_input())
        # trailing "-d exdir" after the archive (only honoured once by unzip, only when extracting)
        if extract_mode:
            operand_names = [operand.get_name() for operand in self.cmd_inv.operand_list]
            for i in range(1, len(operand_names) - 1):
                if operand_names[i] == "-d":
                    operand_list_typer[i + 1] = (WhichClassForArg.FILESTD, make_other_output())
                    break
