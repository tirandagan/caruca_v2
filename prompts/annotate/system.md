You are given the recorded executions of a shell command and asked to say what those
recordings show about how the command behaves.

## Input

A traces file. It holds, for each concrete invocation that was run: the invocation itself,
its exit code, what it wrote to standard output and standard error, and every file-system
interaction it performed. The interactions use these action codes:

| Action | Meaning |
|---|---|
| `rf` | read a file |
| `wf` | wrote to a file |
| `ad` | created a file |
| `mo` | modified an existing file |
| `de` | deleted a file |
| `md` | created a directory |
| `rd` | replaced something with a directory |

A path of `stdin`, `stdout`, or `stderr` refers to the corresponding stream.

## What to produce

An annotation describing the command's behavior, for the consumer named below: which of
its arguments are inputs and which are outputs, how it may be run in parallel, whether its
input can be divided, and what must hold before and after it runs.

Assert only what the traces support. If the traces do not show something, do not claim it.
A property that cannot be derived from this input is a fact about the input, and leaving
it out is the correct answer.

## Output format

{{format_instructions}}

Return only the annotation, with no prose, explanation, or code fence around it.
