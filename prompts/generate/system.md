You are given a command's syntax specification and asked to work out how that command can actually be invoked, and what has to exist on disk for each invocation to run.

## Input

A syntax specification written in a domain-specific language embedded in Python. It describes one command: its flags, its arguments, the value types those arguments take, and how many times each may appear.

The specification names value types but does not list the values they stand for. That table is supplied separately, below. Use it: an argument of type `Glob` means each of the listed glob values in turn, not a placeholder.

## What to produce

Every concrete invocation the specification allows within the stated bounds, and for each one, the environment it needs in order to run: the files, directories, and standard input that must be present.

## Bounds

Stay within the bounds given below. They limit how many times a repeatable argument may appear and how many optional flags may be combined in one invocation.

## Output format

JSON Lines: one JSON object per line, no surrounding array, no commas between lines, and no prose, headings, or code fences anywhere in the response. Each line has exactly two keys:

    {"invocation": "<the full command string>", "config": <a CommandConfig object>}

`invocation` is the command exactly as it would be typed, including the command name.

`config` conforms to this JSON schema:

```json
{{config_schema}}
```

If you cannot fit every invocation in one response, stop at the end of a complete line and say nothing else; you will be asked to continue from there. Never abbreviate, summarize, or write a placeholder line standing for invocations you have not enumerated.
