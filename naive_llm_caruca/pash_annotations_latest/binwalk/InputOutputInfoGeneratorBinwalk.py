from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGeneratorBinwalk(InputOutputInfoGeneratorInterface):

    # list_of_all_flags = ["-B", "-A", "-b", "-I", "-e", "-M", "-1", "-r", "-z", "-V", "-E", "-F", "-J", "-Q",
    #                      "-N", "-W", "-G", "-i", "-U", "-u", "-w", "-X", "-Z", "-P", "-S", "-c", "-t", "-q",
    #                      "-v", "-h"]
    # list_of_all_options = ["-R", "-m", "-x", "-y", "-D", "-d", "-C", "-j", "-n", "-0", "-H", "-L", "-l", "-o",
    #                        "-O", "-K", "-g", "-f", "-a", "-p", "-s"]

    # Which ones do affect input/output?  (checked against binwalk v2.3.3)
    # - operands are the target files; binwalk opens them itself, seeks in them (-o, -l, hexdiff reads
    #   several at once), so they are "other" inputs, not streams; pipes fail with "Illegal seek"
    # - binwalk never reads stdin: with no operand it just prints its help; "-" is a literal file name
    # - stdout is written unless -q (the scan report); -h prints the help text even with -q
    # - -f FILE appends the report to FILE (typed OTHER_OUTPUT in binwalk.json)
    # - -m FILE reads a magic file (typed CONFIG_INPUT in binwalk.json)
    # - -e / -D / -z create "_<file>.extracted" directories next to the current directory
    #   (or under -C DIR, typed OTHER_OUTPUT in binwalk.json); -J writes "<file>.png" in the current
    #   directory.  These implicit outputs are not operands and cannot be expressed here, so they
    #   are over-approximated as side effects.

    def generate_info(self) -> None:
        self.all_operands_are_other_inputs()
        # -q silences the report, but -h prints the help text on stdout regardless of -q (verified)
        if self.does_flag_option_list_contain_at_least_one_of(["-h"]) or \
                not self.does_flag_option_list_contain_at_least_one_of(["-q"]):
            self.set_implicit_use_of_stdout()
