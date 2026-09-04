You are an expert on the shell and on the full range of command-line programs.

Given a shell command's documentation, produce the corresponding syntax specification.
The specification is a domain-specific language embedded in Python. Use only the features
you can see in the worked examples: do not invent constructors, keyword arguments, or
helper functions that no example demonstrates.

Cover the whole interface described in the documentation. Include every flag and every
argument it mentions, including ones documented as accepted but ignored. Where a flag has
both a short and a long form, give both: the long forms belong in the `alias` list of the
short form's entry.

`arity` says how many times a flag or argument may appear in an invocation. It is not the
number of values a flag consumes. The available values are `ZERO_OR_MORE`, `EXACTLY_ONE`,
`EXACTLY_TWO`, `AT_LEAST_ONE`, `ONE_OR_MORE`, `OPTIONAL`, and `ZERO_OR_ONE`.

When the documentation enumerates the values an option accepts, reproduce that
enumeration exactly. Do not omit a documented choice, and do not add a choice the
documentation does not mention.

Use the predefined value type that best fits each argument. Fall back to `Other` only
when none of these fits:

    String   # only when genuinely any string is allowed
    Integer
    Regex
    Signal
    Variable
    Glob
    Pid
    Duration
    User
    Hostname
    Command
    Group
    Filesystem
    Delimiter
    Separator
    SecurityContext
    PrintfFormat
    Size
    Permission
    OwnerGroup
    SprintfFormat
    DateFormat
    Format
    Char
    Range
    Date
    TimeStyle

Think the interface through first, then give the specification as a single fenced Python
code block. The fenced block must be the complete file: its imports, and a module-level
binding named `<command>_syntax_spec`, exactly as the examples are written.
