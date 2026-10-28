import re

from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGeneratorIconv(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-l", "-c", "-s", "--verbose", "-?", "--usage", "-V"]
    # list_of_all_options = ["-f", "-t", "-o"]

    # Which ones do affect parallelizability?
    # -l, -?/--help, --usage, -V: informational, nothing to parallelize
    # -f/-t: the encodings decide whether the stream may be cut at newlines:
    #   iconv restarts the conversion for every input file (verified: a UTF-16 target gets a BOM per file,
    #   an ISO-2022-JP target returns to the initial shift state per file), so IF x SEQ x CONC is always
    #   exact. Cutting a single stream into chunks (CC/RR) is only exact when both encodings are
    #   ASCII-compatible, stateless and emit no byte-order mark: then a newline is a single 0x0A byte in
    #   input and output, and converting the chunks separately and concatenating equals the sequential run.
    #   UTF-16/UTF-32 (BOM, two-/four-byte newline), UTF-7 and ISO-2022-* (shift state) are excluded.
    #   An omitted -f/-t falls back to the locale's charset, which we assume to be ASCII-compatible.
    # -c, //TRANSLIT, //IGNORE: per-character decisions, do not affect splitting
    # -o, -s, --verbose: do not affect splitting
    # On an illegal input sequence the sequential command stops and exits 1; we ignore the error case.

    # names as accepted by `iconv -l`, compared after normalisation (upper case, //suffixes removed)
    SAFE_ENCODING_PATTERNS = [
        r"UTF-?8",
        r"(US-?)?ASCII", r"ANSI[-_]X3\.4-19(68|86)", r"ISO646-US", r"ISO-IR-6", r"US", r"646", r"CP367", r"IBM367",
        r"ISO[-_]?8859-?[0-9]{1,2}", r"LATIN-?[0-9]{1,2}", r"L[0-9]{1,2}",
        r"(CP|WINDOWS-|MS-?)125[0-8]", r"(CP|IBM)(437|85[0-9]|86[0-9]|437)",
        r"KOI8-?(R|U|RU|T)", r"MAC(INTOSH|ROMAN|CYRILLIC)?",
        r"EUC-?(JP|KR|CN|TW)", r"GB2312", r"GBK", r"GB18030", r"BIG-?5(-?HKSCS)?", r"CP9(32|36|49|50)",
        r"SHIFT[-_]?JIS", r"SJIS", r"TIS-?620", r"VISCII", r"ARMSCII-?8", r"GEORGIAN-(PS|ACADEMY)",
    ]

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(["-l", "--list", "-?", "--help", "--usage", "-V", "--version"]):
            return
        # each file is converted from a fresh state and the results are concatenated, hence always exact
        self.append_to_parallelizer_list_if_seq_conc()
        from_code = self._get_option_arg(["-f", "--from-code"])
        to_code = self._get_option_arg(["-t", "--to-code"])
        if self._is_safe_encoding(from_code) and self._is_safe_encoding(to_code):
            self.append_to_parallelizer_list_cc_seq_conc()
            self.append_to_parallelizer_list_rr_seq_conc()

    def _get_option_arg(self, names):
        """returns the argument of the last occurrence of one of names as a string, None if absent,
        and False if present but the argument cannot be read"""
        result = None
        for flag_option in self.cmd_inv.flag_option_list:
            name = getattr(flag_option, "name", None)
            if name is None and hasattr(flag_option, "get_name"):
                name = flag_option.get_name()
            if name not in names:
                continue
            arg = getattr(flag_option, "arg", None)
            if arg is None:
                result = False
            elif hasattr(arg, "get_name"):
                result = str(arg.get_name())
            else:
                result = str(arg)
        return result

    @classmethod
    def _is_safe_encoding(cls, encoding):
        if encoding is None:  # not given: locale default, assumed ASCII-compatible
            return True
        if encoding is False:  # given but unreadable: be conservative
            return False
        normalised = encoding.split("//")[0].strip().upper()
        return any(re.fullmatch(pattern, normalised) for pattern in cls.SAFE_ENCODING_PATTERNS)
