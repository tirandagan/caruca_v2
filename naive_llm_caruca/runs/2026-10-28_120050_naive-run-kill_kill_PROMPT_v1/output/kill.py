from caruca.ir.syntax import *

# kill(1) from procps-ng 4.0.4.
#
# Two alternative syntaxes:
#   1. kill [-s <signal> | --signal <signal> | -<signal>] [-q <value>] <pid> [...]
#      sends a signal to one or more processes;
#   2. kill -l [<signal>] | -L | -h | -V
#      prints information (signal names, help, version) and sends nothing.
#
# The "-<signal>" shorthand accepts any signal number or name (with or without
# the SIG prefix, case-insensitively).  The syntax format has no way to say "a
# dash followed by a signal", so every spelling is enumerated as a Flag below.
# When several signal words are given the last one wins.
#
# PID operands may be negative to address a process group (a PID of -1 means
# every process the caller may signal), but a negative PID must come after
# "--": without it, this build parses "-<number>" as a signal name, and an
# unknown one makes kill exit 0 without sending anything.

kill_syntax_spec: list[SyntaxSpecification] = [
    # 1. send a signal
    [
        [
            Signal(flag="-s", alias=["--signal"]),
            Integer(flag="-q", alias=["--queue"]),
            # -<signal> shorthands, standard signals 0-31
            Flag("-0"),
            Flag("-1", alias=['-HUP', '-SIGHUP']),
            Flag("-2", alias=['-INT', '-SIGINT']),
            Flag("-3", alias=['-QUIT', '-SIGQUIT']),
            Flag("-4", alias=['-ILL', '-SIGILL']),
            Flag("-5", alias=['-TRAP', '-SIGTRAP']),
            Flag("-6", alias=['-ABRT', '-SIGABRT', '-IOT', '-SIGIOT']),
            Flag("-7", alias=['-BUS', '-SIGBUS']),
            Flag("-8", alias=['-FPE', '-SIGFPE']),
            Flag("-9", alias=['-KILL', '-SIGKILL']),
            Flag("-10", alias=['-USR1', '-SIGUSR1']),
            Flag("-11", alias=['-SEGV', '-SIGSEGV']),
            Flag("-12", alias=['-USR2', '-SIGUSR2']),
            Flag("-13", alias=['-PIPE', '-SIGPIPE']),
            Flag("-14", alias=['-ALRM', '-SIGALRM']),
            Flag("-15", alias=['-TERM', '-SIGTERM']),
            Flag("-16", alias=['-STKFLT', '-SIGSTKFLT']),
            Flag("-17", alias=['-CHLD', '-SIGCHLD', '-CLD', '-SIGCLD']),
            Flag("-18", alias=['-CONT', '-SIGCONT']),
            Flag("-19", alias=['-STOP', '-SIGSTOP']),
            Flag("-20", alias=['-TSTP', '-SIGTSTP']),
            Flag("-21", alias=['-TTIN', '-SIGTTIN']),
            Flag("-22", alias=['-TTOU', '-SIGTTOU']),
            Flag("-23", alias=['-URG', '-SIGURG']),
            Flag("-24", alias=['-XCPU', '-SIGXCPU']),
            Flag("-25", alias=['-XFSZ', '-SIGXFSZ']),
            Flag("-26", alias=['-VTALRM', '-SIGVTALRM']),
            Flag("-27", alias=['-PROF', '-SIGPROF']),
            Flag("-28", alias=['-WINCH', '-SIGWINCH']),
            Flag("-29", alias=['-POLL', '-SIGPOLL', '-IO', '-SIGIO']),
            Flag("-30", alias=['-PWR', '-SIGPWR']),
            Flag("-31", alias=['-SYS', '-SIGSYS']),
            Flag("-32"),
            Flag("-33"),
            Flag("-34", alias=['-RTMIN', '-SIGRTMIN']),
            Flag("-35", alias=['-RTMIN+1', '-SIGRTMIN+1']),
            Flag("-36", alias=['-RTMIN+2', '-SIGRTMIN+2']),
            Flag("-37", alias=['-RTMIN+3', '-SIGRTMIN+3']),
            Flag("-38", alias=['-RTMIN+4', '-SIGRTMIN+4']),
            Flag("-39", alias=['-RTMIN+5', '-SIGRTMIN+5']),
            Flag("-40", alias=['-RTMIN+6', '-SIGRTMIN+6']),
            Flag("-41", alias=['-RTMIN+7', '-SIGRTMIN+7']),
            Flag("-42", alias=['-RTMIN+8', '-SIGRTMIN+8']),
            Flag("-43", alias=['-RTMIN+9', '-SIGRTMIN+9']),
            Flag("-44", alias=['-RTMIN+10', '-SIGRTMIN+10']),
            Flag("-45", alias=['-RTMIN+11', '-SIGRTMIN+11']),
            Flag("-46", alias=['-RTMIN+12', '-SIGRTMIN+12']),
            Flag("-47", alias=['-RTMIN+13', '-SIGRTMIN+13']),
            Flag("-48", alias=['-RTMIN+14', '-SIGRTMIN+14']),
            Flag("-49", alias=['-RTMIN+15', '-SIGRTMIN+15']),
            Flag("-50", alias=['-RTMIN+16', '-SIGRTMIN+16']),
            Flag("-51", alias=['-RTMIN+17', '-SIGRTMIN+17']),
            Flag("-52", alias=['-RTMIN+18', '-SIGRTMIN+18']),
            Flag("-53", alias=['-RTMIN+19', '-SIGRTMIN+19']),
            Flag("-54", alias=['-RTMIN+20', '-SIGRTMIN+20']),
            Flag("-55", alias=['-RTMIN+21', '-SIGRTMIN+21']),
            Flag("-56", alias=['-RTMIN+22', '-SIGRTMIN+22']),
            Flag("-57", alias=['-RTMIN+23', '-SIGRTMIN+23']),
            Flag("-58", alias=['-RTMIN+24', '-SIGRTMIN+24']),
            Flag("-59", alias=['-RTMIN+25', '-SIGRTMIN+25']),
            Flag("-60", alias=['-RTMIN+26', '-SIGRTMIN+26']),
            Flag("-61", alias=['-RTMIN+27', '-SIGRTMIN+27']),
            Flag("-62", alias=['-RTMIN+28', '-SIGRTMIN+28']),
            Flag("-63", alias=['-RTMIN+29', '-SIGRTMIN+29']),
            Flag("-64", alias=['-RTMIN+30', '-SIGRTMIN+30']),
        ],
        [Pid(arity=Arity.AT_LEAST_ONE)],
    ],
    # 2. list signals / help / version (no PID operand)
    [
        [
            Flag("-l", alias=["--list"]),
            Signal(flag="--list", flag_followed_by_equals=True),
            Flag("-L", alias=["--table"]),
            Flag("-h", alias=["--help"]),
            Flag("-V", alias=["--version"]),
        ],
        # optional signal name or number to convert, used by -l / --list
        [Signal(arity=Arity.ZERO_OR_ONE)],
    ],
]
