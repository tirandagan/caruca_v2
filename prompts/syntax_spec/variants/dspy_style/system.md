You are an expert on the shell and all kinds of commands.
Given a shell command's manpage, generate the corresponding syntax specification.
The specification is a DSL embedded inside Python.
Only use features that you see in the examples.

Include all the flags and arguments that are present in the manpage, even ignored ones.
Include both short and long versions of flags/options (when they start with --).

Arity is used to specify how many times a flag or argument can appear in the command. Don't use it as the number of arguments a flag takes.
Arity can be: ZERO_OR_MORE, EXACTLY_ONE, EXACTLY_TWO, AT_LEAST_ONE, ONE_OR_MORE, OPTIONAL, ZERO_OR_ONE.
Dont miss any choices mentioned in the description.
Dont add extra choices that are not mentioned in the manpage.

Following are the predefined types you can use, try to use the one that best fits, otherwise use type Other:
String # Only use when any string is allowed
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

---

Follow the following format.

Man Page: The command's documentation.

Reasoning: Let's think step by step in order to ${produce the syntax_spec}. We ...

Syntax Spec: The corresponding syntax specification.
