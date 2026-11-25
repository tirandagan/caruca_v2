from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorSed(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-n", "--debug", "--follow-symlinks", "-i", "--posix", "-E", "-r", "-s", "--sandbox",
    #                      "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["-e", "-f", "-l"]

    # Which ones do affect parallelizability?
    # sed is parallelizable (CC/RR x SEQ x CONC) only when the script is "line-local", i.e. every output line
    # depends on the current input line alone.  This is decided by parsing the script (from -e or the first
    # operand) with the conservative grammar in `_SedScriptChecker` below; anything it does not understand
    # counts as not line-local.
    #   not line-local: addresses by line number (`3`, `1~2`, `$`, `0,/re/`), address ranges, and the commands
    #                   n N D g G h H x (next line / hold space), = F (position/file name), q Q (stop early),
    #                   w W and the `w` flag of s (several workers would write the same file), e and the `e`
    #                   flag of s (shell commands), R (consumes a file line by line), L
    #   line-local:     s y p P d l a i c z v r b t T : { } # with no address or a single regex address (`!` ok)
    # -i (in place), -z (records are not lines), --debug (trace output), -f (script not inspectable),
    # --help/--version: not parallelized; -n -s -u -E -r -l --posix --sandbox --follow-symlinks: no influence

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(
                ["-i", "--in-place", "-z", "--null-data", "--debug", "-f", "--file", "--help", "--version"]):
            return
        script = self._get_script_text()
        if script is None:
            return
        if _SedScriptChecker(script).is_line_local():
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()

    def _get_script_text(self):
        """The script as sed sees it: all -e fragments joined by newlines, else the first operand."""
        if self.does_flag_option_list_contain_at_least_one_of(["-e", "--expression"]):
            fragments = []
            for item in self.cmd_inv.flag_option_list:
                name = item.get_name() if callable(getattr(item, "get_name", None)) else getattr(item, "name", None)
                if name not in ("-e", "--expression"):
                    continue
                arg = item.get_arg() if callable(getattr(item, "get_arg", None)) else getattr(item, "option_arg", None)
                if arg is None:
                    return None
                fragments.append(_strip_quotes(str(arg)))
            return "\n".join(fragments) if fragments else None
        if self.get_operand_list_length() == 0:
            return None
        return _strip_quotes(self.get_first_operand_name_as_string())


def _strip_quotes(text: str) -> str:
    # PaSh hands over quoted words with their (double) quotes still attached
    if len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        return text[1:-1]
    return text


class _SedScriptChecker:
    """Conservative recogniser for sed scripts whose effect is line-local (GNU sed 4.9 grammar)."""

    _NO_ARG_LINE_LOCAL = set("pPdz")
    _NO_ARG_STATEFUL = set("nNDgGhHx=F")
    _TO_END_OF_LINE_STATEFUL = set("wWeRL")

    def __init__(self, script: str):
        self.s = script
        self.i = 0
        self.n = len(script)
        self.depth = 0

    def is_line_local(self) -> bool:
        try:
            while True:
                self._skip_separators()
                if self.i >= self.n:
                    return self.depth == 0
                if not self._command():
                    return False
        except _NotLineLocal:
            return False

    # --- helpers -------------------------------------------------------------------------------------------

    def _peek(self):
        return self.s[self.i] if self.i < self.n else ""

    def _skip_blanks(self):
        while self._peek() in (" ", "\t") and self._peek() != "":
            self.i += 1

    def _skip_separators(self):
        while self._peek() != "" and self._peek() in " \t\n;":
            self.i += 1

    def _to_end_of_line(self) -> str:
        start = self.i
        while self.i < self.n and self.s[self.i] != "\n":
            self.i += 1
        return self.s[start:self.i]

    def _text_argument(self):
        # a, i, c: `a\` newline text, `a\text` or one-liner `a text`; lines ending in `\` continue
        self._skip_blanks()
        if self._peek() == "\\":
            self.i += 1
            if self._peek() == "\n":
                self.i += 1
        while self.i < self.n and self.s[self.i] != "\n":
            if self.s[self.i] == "\\":
                self.i += 1
            self.i += 1

    def _label(self):
        self._skip_blanks()
        while self.i < self.n and self.s[self.i] not in " \t\n;}":
            self.i += 1

    def _number(self) -> bool:
        start = self.i
        while self._peek().isdigit() and self._peek() != "":
            self.i += 1
        return self.i > start

    def _delimited(self, delim: str, regex: bool):
        """Advance past one `delim`-terminated part of s, y or a regex address."""
        while True:
            if self.i >= self.n:
                raise _NotLineLocal()
            c = self.s[self.i]
            if c == "\\":
                self.i += 2
            elif c == delim:
                self.i += 1
                return
            elif regex and c == "[":
                self._bracket_expression()
            else:
                self.i += 1

    def _bracket_expression(self):
        self.i += 1  # [
        if self._peek() == "^":
            self.i += 1
        if self._peek() == "]":
            self.i += 1
        while True:
            if self.i >= self.n:
                raise _NotLineLocal()
            c = self.s[self.i]
            if c == "]":
                self.i += 1
                return
            if c == "[" and self.i + 1 < self.n and self.s[self.i + 1] in ":.=":
                kind = self.s[self.i + 1]
                end = self.s.find(kind + "]", self.i + 2)
                if end < 0:
                    raise _NotLineLocal()
                self.i = end + 2
            else:
                self.i += 1

    def _regex_address(self):
        c = self._peek()
        if c == "/":
            self.i += 1
            self._delimited("/", regex=True)
        elif c == "\\":
            self.i += 1
            delim = self._peek()
            if delim in ("", "\n", "\\"):
                raise _NotLineLocal()
            self.i += 1
            self._delimited(delim, regex=True)
        else:
            raise _NotLineLocal()
        while self._peek() in ("I", "M") and self._peek() != "":
            self.i += 1

    def _address(self):
        """Parse the optional address(es); only `no address` and `single regex` are line-local."""
        c = self._peek()
        if c.isdigit() or c == "$":
            raise _NotLineLocal()  # position-dependent
        if c in ("/", "\\"):
            self._regex_address()
        else:
            return
        self._skip_blanks()
        if self._peek() == ",":
            raise _NotLineLocal()  # a range carries state across lines

    # --- commands ------------------------------------------------------------------------------------------

    def _command(self) -> bool:
        self._address()
        self._skip_blanks()
        while self._peek() == "!":
            self.i += 1
            self._skip_blanks()
        c = self._peek()
        if c == "":
            return False
        self.i += 1

        if c == "{":
            self.depth += 1
            return True  # the next command may follow directly
        elif c == "}":
            self.depth -= 1
            if self.depth < 0:
                return False
        elif c == "#":
            self._to_end_of_line()
        elif c == ":":
            self._label()
        elif c in "btT":
            self._label()
        elif c in "aic":
            self._text_argument()
        elif c in self._NO_ARG_LINE_LOCAL:
            pass
        elif c in "lqQ":
            if c in "qQ":
                return False
            self._skip_blanks()
            self._number()
        elif c == "v":
            self._skip_blanks()
            while self.i < self.n and self.s[self.i] not in "\n;":
                self.i += 1
        elif c == "r":
            self._skip_blanks()
            filename = self._to_end_of_line().strip()
            if filename in ("/dev/stdin", "-", ""):
                return False
        elif c in self._TO_END_OF_LINE_STATEFUL or c in self._NO_ARG_STATEFUL:
            return False
        elif c == "y":
            delim = self._peek()
            if delim in ("", "\n", "\\"):
                return False
            self.i += 1
            self._delimited(delim, regex=False)
            self._delimited(delim, regex=False)
        elif c == "s":
            return self._substitute()
        else:
            return False

        # a command must be followed by a separator, a closing brace, a comment, or the end
        self._skip_blanks()
        return self._peek() in ("", "\n", ";", "}", "#")

    def _substitute(self) -> bool:
        delim = self._peek()
        if delim in ("", "\n", "\\"):
            return False
        self.i += 1
        self._delimited(delim, regex=True)
        self._delimited(delim, regex=False)
        while True:
            c = self._peek()
            if c in ("w", "e"):
                return False  # writes a file / runs the pattern space as a command
            if c != "" and (c.isdigit() or c in "gpiImM"):
                self.i += 1
            else:
                break
        self._skip_blanks()
        return self._peek() in ("", "\n", ";", "}", "#")


class _NotLineLocal(Exception):
    pass
