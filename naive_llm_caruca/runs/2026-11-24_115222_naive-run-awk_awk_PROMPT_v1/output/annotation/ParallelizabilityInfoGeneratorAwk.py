import re

from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


# anything that carries state across records, reads or writes beyond the current record, or
# depends on the position within the whole input makes the program non-parallelizable
_STATEFUL_PROGRAM = re.compile(
    r"|".join([
        r"\bBEGIN\b", r"\bEND\b", r"\bBEGINFILE\b", r"\bENDFILE\b",
        r"\bNR\b", r"\bFNR\b", r"\bFILENAME\b", r"\bARGV\b", r"\bARGC\b", r"\bARGIND\b",
        r"\bRS\b", r"\bRT\b", r"\bORS\b",
        r"\bfunction\b", r"\bfunc\b",
        r"\bgetline\b", r"\bexit\b", r"\bnextfile\b", r"\bsystem\b", r"\bclose\b", r"\bfflush\b",
        r"\bsplit\b", r"\bpatsplit\b", r"\basort\b", r"\basorti\b", r"\bdelete\b", r"\bsrand\b", r"\brand\b",
        r"\bSYMTAB\b", r"\bFUNCTAB\b", r"\bPROCINFO\b",
        r"@",                               # @include, @load, @namespace, indirect calls
        r"\+\+", r"--", r"[-+*/%^]=",       # increments and compound assignments
        r"(?<![=!<>~])=(?!=)",              # plain assignment (not ==, !=, <=, >=)
        r">", r"\|",                        # output redirection / pipes (also excludes > and || comparisons)
    ])
)

# these write a side file (awkvars.out / awkprof.out), which parallel copies would clobber,
# or do not process the input at all
_NON_PARALLELIZABLE_FLAGS = ["-d", "--dump-variables", "-D", "--debug", "-g", "--gen-pot",
                             "-o", "--pretty-print", "-p", "--profile", "-I", "--trace",
                             "-h", "--help", "-V", "--version", "-C", "--copyright"]

# assignments of these variables (via -v or var=val operands) change the record structure
_RECORD_VARIABLE_ASSIGNMENT = re.compile(r"(^|[\s=])(RS|RT|ORS|NR|FNR)=")


def _as_string(obj) -> str:
    # the exact accessor names of Operand / OptionWithArg are not relied upon: collect everything
    parts = [str(obj)]
    for accessor in ("get_name_as_string", "get_arg_as_string", "get_arg_as_str", "get_value_as_string"):
        if hasattr(obj, accessor):
            parts.append(str(getattr(obj, accessor)()))
    return " ".join(parts)


class ParallelizabilityInfoGeneratorAwk(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-b", "-c", "-C", "-d", "-D", "-g", "-h", "-I", "-L", "-M", "-N", "-n", "-o",
    #                      "-O", "-p", "-P", "-r", "-s", "-S", "-t", "-V"]
    # list_of_all_options = ["-f", "-F", "-v", "-e", "-E", "-i", "-l", "-W"]

    # Which ones do affect parallelizability?
    # awk is stateful in general (variables, NR, BEGIN/END), so nothing is parallelized unless the
    # program text is given on the command line (not via -f/-e/-E, whose contents we cannot see)
    # and it is a pure per-record program: no BEGIN/END, no assignments, no NR/FNR, no getline,
    # no exit, no I/O redirection, ...  Such a program handles every line independently, so both
    # consecutive chunks and round robin with plain concatenation are valid.
    # -i and -l load code we cannot see, -d/-o/-p write side files: no parallelization then.
    # -F, -v (except for record variables), -b, -c, -P, -M, -N, -n, -O, -s, -S, -t, -r, -L
    # do not affect per-record independence.

    def generate_info(self) -> None:
        if self.does_flag_option_list_contain_at_least_one_of(
                _NON_PARALLELIZABLE_FLAGS + ["-f", "--file", "-e", "--source", "-E", "--exec",
                                             "-i", "--include", "-l", "--load", "-W"]):
            return
        if self.get_operand_list_length() == 0:
            return
        program_text = self.get_first_operand_name_as_string()
        if _STATEFUL_PROGRAM.search(program_text):
            return
        # record-structure assignments through -v or var=val operands
        for option in self.get_flag_option_list_filtered_with(["-v", "--assign"]):
            if _RECORD_VARIABLE_ASSIGNMENT.search(_as_string(option)):
                return
        for operand in self.cmd_inv.operand_list[1:]:
            if _RECORD_VARIABLE_ASSIGNMENT.search(_as_string(operand)):
                return
        self.append_to_parallelizer_list_cc_seq_conc()
        self.append_to_parallelizer_list_rr_seq_conc()
