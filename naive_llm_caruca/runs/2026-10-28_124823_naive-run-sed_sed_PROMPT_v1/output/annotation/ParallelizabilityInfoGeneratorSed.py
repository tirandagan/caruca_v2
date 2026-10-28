from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSed(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--debug", "--follow-symlinks", "-i", "--posix", "-E", "-r", "-s",
    #                      "--sandbox", "-u", "-z", "-b", "--help", "--version"]
    # list_of_all_options = ["-e", "-f", "-l"]

    # Which ones do affect parallelizability?
    # -i writes the input files in place, so there is no output stream to recombine
    # -z makes records NUL-terminated while the splitters cut at newlines
    # --debug prints a trace that depends on the whole run
    # -f hides the script in a file, so we cannot check it and do not parallelize
    # -n, -E/-r, -s, -u, -l, --posix, --sandbox do not matter by themselves
    # The script matters most: sed is parallelizable with RR/CC x SEQ x CONC iff every
    # command works on the current line alone, i.e. the script
    #   - has no line-number addresses (N, $, first~step, 0,/re/, addr,+N, addr,~N)
    #   - has no range addresses (addr1,addr2), which span lines
    #   - does not use the hold space (h H g G x) or multi-line commands (n N D P)
    #   - does not stop early (q Q), print line numbers (=) or file names (F)
    #   - does not touch files or run commands (r R w W e, s///w, s///e)
    # Allowed: p d z l v y s a i c b t T : { } # with regex (/re/, \cREc) addresses and !

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-i", "--in-place", "-z", "--null-data", "--debug"]):
            return
        if self.does_flag_option_list_contain_at_least_one_of(["-f", "--file"]):
            return
        script = self._get_script()
        if script is None:
            return
        if _script_is_line_local(script):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()

    def _get_script(self):
        expressions = self.get_flag_option_list_filtered_with(["-e", "--expression"])
        if len(expressions) > 0:
            parts = []
            for option in expressions:
                arg = _option_argument_as_string(option)
                if arg is None:
                    return None
                parts.append(arg)
            # GNU sed joins multiple -e scripts with newlines
            return "\n".join(parts)
        if self.get_operand_list_length() == 0:
            return None
        return self.get_first_operand_name_as_string()


def _option_argument_as_string(option):
    # the parsed option stores its argument in different shapes; be defensive
    for attr in ("get_arg_name_as_string", "get_option_arg_as_string"):
        if hasattr(option, attr):
            try:
                return str(getattr(option, attr)())
            except Exception:
                pass
    for attr in ("option_arg", "arg", "argument", "value"):
        if hasattr(option, attr):
            value = getattr(option, attr)
            if hasattr(value, "get_name"):
                value = value.get_name()
            return str(value)
    return None


# ---------------------------------------------------------------------------
# A conservative recogniser for sed scripts that operate on one line at a time.
# Anything it does not fully understand is reported as not line-local.
# ---------------------------------------------------------------------------

_SIMPLE_SAFE_COMMANDS = set("pdzlv")        # no argument (l may take a number)
_TEXT_COMMANDS = set("aic")                 # text to the end of the line
_LABEL_COMMANDS = set("btT:")               # label up to ';' or newline
_UNSAFE_COMMANDS = set("hHgGxnNDPqQ=FrRwWe")


def _script_is_line_local(script: str) -> bool:
    try:
        return _Checker(script).check()
    except Exception:
        return False


class _Checker:
    def __init__(self, script: str):
        self.s = script
        self.i = 0
        self.depth = 0

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else None

    def skip_blanks(self):
        while self.peek() is not None and self.peek() in " \t":
            self.i += 1

    def skip_separators(self):
        while self.peek() is not None and self.peek() in " \t\n;":
            self.i += 1

    def skip_delimited(self, delim: str) -> bool:
        # skip up to and including the closing delimiter, honouring backslash
        # escapes and bracket expressions (a delimiter inside [...] is literal)
        while True:
            c = self.peek()
            if c is None:
                return False
            if c == "\\":
                self.i += 2
                continue
            if c == delim:
                self.i += 1
                return True
            if c == "[":
                self.i += 1
                if self.peek() == "^":
                    self.i += 1
                if self.peek() == "]":
                    self.i += 1
                while True:
                    c = self.peek()
                    if c is None:
                        return False
                    if c == "[" and self.i + 1 < len(self.s) and self.s[self.i + 1] in ".:=":
                        kind = self.s[self.i + 1]
                        end = self.s.find(kind + "]", self.i + 2)
                        if end < 0:
                            return False
                        self.i = end + 2
                        continue
                    self.i += 1
                    if c == "]":
                        break
                continue
            self.i += 1

    def parse_address(self) -> str:
        # returns "none", "regex" or "line"
        c = self.peek()
        if c is None:
            return "none"
        if c.isdigit() or c == "$":
            return "line"
        if c == "/":
            self.i += 1
            if not self.skip_delimited("/"):
                raise ValueError("unterminated regex")
        elif c == "\\":
            self.i += 1
            delim = self.peek()
            if delim is None or delim in "\n\\":
                raise ValueError("bad custom delimiter")
            self.i += 1
            if not self.skip_delimited(delim):
                raise ValueError("unterminated regex")
        else:
            return "none"
        while self.peek() is not None and self.peek() in "IM":
            self.i += 1
        return "regex"

    def end_of_command(self) -> bool:
        self.skip_blanks()
        c = self.peek()
        if c is None or c in ";\n":
            return True
        if c == "}":
            return True  # handled by the main loop
        if c == "#":
            return True
        return False

    def check(self) -> bool:
        while True:
            self.skip_separators()
            c = self.peek()
            if c is None:
                return self.depth == 0
            if c == "}":
                if self.depth == 0:
                    return False
                self.depth -= 1
                self.i += 1
                continue
            if c == "#":
                nl = self.s.find("\n", self.i)
                self.i = len(self.s) if nl < 0 else nl
                continue
            kind = self.parse_address()
            if kind == "line":
                return False
            self.skip_blanks()
            if kind == "regex" and self.peek() == ",":
                return False  # range address
            if self.peek() == "!":
                self.i += 1
                self.skip_blanks()
            cmd = self.peek()
            if cmd is None:
                return False
            self.i += 1
            if cmd in _UNSAFE_COMMANDS:
                return False
            if cmd == "{":
                self.depth += 1
                continue
            if cmd in _SIMPLE_SAFE_COMMANDS:
                if cmd == "l":
                    self.skip_blanks()
                    while self.peek() is not None and self.peek().isdigit():
                        self.i += 1
                if not self.end_of_command():
                    return False
                continue
            if cmd in _TEXT_COMMANDS:
                # a\ <newline> text  or GNU one-liner a text; a trailing backslash continues
                while True:
                    nl = self.s.find("\n", self.i)
                    if nl < 0:
                        self.i = len(self.s)
                        break
                    if self.s[nl - 1] == "\\" and nl - 1 >= self.i:
                        self.i = nl + 1
                        continue
                    self.i = nl
                    break
                continue
            if cmd in _LABEL_COMMANDS:
                while self.peek() is not None and self.peek() not in ";\n":
                    self.i += 1
                continue
            if cmd == "y":
                delim = self.peek()
                if delim is None or delim in "\n\\":
                    return False
                self.i += 1
                if not self.skip_delimited(delim) or not self.skip_delimited(delim):
                    return False
                if not self.end_of_command():
                    return False
                continue
            if cmd == "s":
                delim = self.peek()
                if delim is None or delim in "\n\\":
                    return False
                self.i += 1
                if not self.skip_delimited(delim):
                    return False
                # replacement: only backslash escapes matter, no bracket expressions
                while True:
                    c = self.peek()
                    if c is None:
                        return False
                    if c == "\\":
                        self.i += 2
                        continue
                    self.i += 1
                    if c == delim:
                        break
                while True:
                    c = self.peek()
                    if c is None or c in ";\n}# \t":
                        break
                    if c in "gpiImM" or c.isdigit():
                        self.i += 1
                        continue
                    return False  # 'w file' or 'e' or something unknown
                if not self.end_of_command():
                    return False
                continue
            return False  # unknown command
