# Format: the behaviour annotation, as PaSh consumes it

PaSh describes a command with three files. Together they let PaSh parse an invocation of the command,
work out which of its arguments are inputs and outputs, and decide whether the invocation's work can be
split across parallel copies. The files live in the `pash_annotations` Python package (the module
paths below are that package's), and the samples under `samples/*/pash/` are copied from it unchanged.

| File | What it is |
|---|---|
| `<command>.json` | the parser table: the command's flags and options, and the type of each option's argument |
| `InputOutputInfoGenerator<Command>.py` | a class that, given a parsed invocation, marks which operands and option arguments are read, which are written, and whether standard input and standard output are used |
| `ParallelizabilityInfoGenerator<Command>.py` | a class that, given a parsed invocation, lists the ways its work may be split and recombined; when the file is absent, PaSh treats the command as not parallelisable |

`<Command>` is the command's name with its first letter capitalised (`grep` → `Grep`).

## 1. The parser table, `<command>.json`

```json
{
    "flag": [
        ["-c", "--count"],
        ["-D"],
        "-f"
    ],
    "option": [
        ["-e", "PATTERNS"],
        ["--regexp", "PATTERNS"],
        ["-f", "--file", ["FILE", "CONFIG_INPUT"]]
    ]
}
```

- `flag` lists the options that take no argument. Each entry is a list of the spellings of one flag;
  the first spelling is the one the parser reports. A bare string is accepted as a one-spelling entry.
- `option` lists the options that take an argument. Each entry is one or more spellings followed by
  the argument's type name. The type name is free text taken from the manual (`NUM`, `WHEN`, `MODE`),
  except that a file argument is written as a two-element list, `["FILE", <access>]`, where `FILE`,
  `DIR` or `DIRECTORY` marks it as a path and `<access>` is one of the access kinds in section 4.
- Two spellings of the same option may be listed as separate entries (grep's `-e` and `--regexp`) or in
  one entry (`-f`, `--file`).

PaSh's parser reads an invocation left to right: words found in `flag` or `option` are collected, with
an option consuming the following word as its argument; a word of the form `-abc` whose letters are all
flags is split into them; the first word that is none of these starts the operand list.

## 2. The input/output class

```python
from pash_annotations.annotation_generation.annotation_generators.InputOutputInfoGenerator_Interface import InputOutputInfoGeneratorInterface


class InputOutputInfoGenerator<Command>(InputOutputInfoGeneratorInterface):

    def generate_info(self) -> None:
        ...
```

The class defines one method, `generate_info`. PaSh constructs the object with the parsed invocation,
calls `generate_info`, and reads the result. Before `generate_info` runs, every operand is already
marked as a streaming input and option arguments are already typed from the parser table; the method
changes what differs for this command and this invocation.

**Inspecting the invocation** (inherited):

| Call | Returns |
|---|---|
| `self.does_flag_option_list_contain_at_least_one_of(["-q", "-c"])` | whether any of the named flags or options is present |
| `self.get_flag_option_list_filtered_with([...])` | the present ones among those named |
| `self.get_operand_list_length()` | the number of operands |
| `self.get_first_operand_name_as_string()` | the first operand's text |
| `self.does_first_operand_start_with(s)`, `self.does_first_operand_contain(s)` | tests on that text |
| `self.cmd_inv.flag_option_list`, `self.cmd_inv.operand_list` | the parsed lists themselves |

**Declaring inputs and outputs** (inherited):

| Call | Effect |
|---|---|
| `self.set_implicit_use_of_stdin()` | standard input is read even though no operand names it |
| `self.set_implicit_use_of_stdout()` | standard output is written |
| `self.if_no_operands_given_stdin_implicitly_used()` | the first, only when there are no operands |
| `self.all_operands_are_streaming_inputs()` | every operand is a file read as a stream (the default) |
| `self.all_operands_are_streaming_outputs()` | every operand is a file written as a stream |
| `self.all_operands_are_other_inputs()` / `..._other_outputs()` | every operand is a file read, or written, in some non-streaming way |
| `self.all_but_last_operand_is_streaming_input()` / `..._other_input()` | the last operand is left for a separate call |
| `self.all_but_first_operand_is_streaming_input()` / `..._streaming_output()` / `..._other_input()` | the first operand is left for a separate call |
| `self.only_last_operand_is_stream_output()` / `..._other_output()` | the last operand alone is an output |
| `self.set_first_operand_as_config_arg_type_string()` | the first operand is not a file but a value, such as a pattern |
| `self.set_all_operands_as_config_arg_type_string()` | no operand is a file |
| `self.set_first_operand_as_config_arg_type_filename_or_std_descriptor()` | the first operand is a file read as configuration rather than as a stream |

## 3. The parallelizability class

```python
from pash_annotations.annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface


class ParallelizabilityInfoGenerator<Command>(ParallelizabilityInfoGeneratorInterface):

    def generate_info(self) -> None:
        ...
```

Again one method, `generate_info`, with the same inspection calls as above. It appends zero or more
**parallelizers** to a list. A parallelizer is a splitter, a mapper and an aggregator: how the input is
divided, what runs on each part, and how the parts' outputs are recombined. Appending nothing means the
invocation is not parallelised.

**Splitters:** `indiv_files` (each input file is its own part), `consec_chunks` (the input is cut into
consecutive pieces), `round_robin` (lines are dealt out to parts in turn).

**Mappers:** by default the same command runs on each part (`seq`). A custom mapper is named with
`make_mapper_spec_custom(name, is_implemented=...)` from
`pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec`.

**Aggregators:** `conc` (concatenate the parts' outputs in order; the default), `adj_lines_merge`
(merge the boundary lines of adjacent parts), `adj_lines_seq` (run the command itself over the boundary
lines of adjacent parts), `adj_lines_func` (a named function over the boundary lines), and custom
2-ary or n-ary functions. The `make_aggregator_spec_*` constructors live in
`pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec`; the ones that take
a function name also take `is_implemented`, and a name beginning `PLACEHOLDER:` marks a function PaSh
does not yet provide.

**Appending a parallelizer**, in two forms:

- The inherited one-call shortcuts, named `append_to_parallelizer_list_<splitter>_seq_<aggregator>`
  with splitter in `if`, `cc`, `rr` and aggregator in `conc`, `adjm`, `adjs`, `adjf`; the `adjf` ones
  take `(string_repr_func, is_implemented)`. Examples: `self.append_to_parallelizer_list_cc_seq_conc()`,
  `self.append_to_parallelizer_list_rr_seq_adjs()`.
- Building one explicitly with `make_parallelizer_consec_chunks(...)`,
  `make_parallelizer_round_robin(...)` or `make_parallelizer_indiv_files(...)` from
  `pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer`, each taking
  optional `mapper_spec`, `aggregator_spec` and `info_splitter_mapper` (an
  `AdditionalInfoSplitterToMapper` value: `NO_ADD_INPUT`, `LINE_NUM_OFFSET`, `BYTE_OFFSET`,
  `LINE_NUM_AND_BYTE_OFFSET`, for mappers that need to know where their part began), then
  `self.append_to_parallelizer_list(parallelizer)`.

`self.set_commutative()` records that the parts' outputs may be recombined in any order.

## 4. Access kinds

Used in the parser table's file-argument entries and behind the input/output calls above:

| Name | Meaning |
|---|---|
| `STREAM_INPUT` | a file read as the data stream the command processes |
| `CONFIG_INPUT` | a file read for configuration, such as a pattern file |
| `CONTAINER_FOR_INPUT` | a file that lists the real input files |
| `EXCLUDES_FROM_INPUT` | a file that lists what to leave out |
| `OTHER_INPUT` | read in some other way |
| `STREAM_OUTPUT` | a file written as the output stream |
| `OTHER_OUTPUT` | written, created or removed in some other way |
