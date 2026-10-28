from caruca.ir.syntax import *

# uglifyjs [files...] [options]   (uglify-js 3.17.4)
#
# Options and operands may be interleaved; "--" ends option processing.
# A lone "-" is silently ignored by uglifyjs (it is neither a file nor stdin);
# standard input is read only when no file operand is given at all.
#
# Several options take an *optional* value: -c/--compress, -m/--mangle,
# --mangle-props, -b/--beautify, --comments, -e/--enclose and --source-map
# consume the following word only if it does not start with "-". The
# syntax vocabulary has no optional-value node, so they are declared as
# Flag here; a value written after them (e.g. `-c toplevel`) will be seen
# as an operand by a parser that follows this description.
uglifyjs_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            Flag("-h", alias=["--help"]),
            Flag("-v", alias=["-V", "--version"]),
            String(flag="-p", alias=["--parse"], arity=Arity.ZERO_OR_MORE),
            Flag("-c", alias=["--compress"]),
            Flag("-m", alias=["--mangle"]),
            Flag("--mangle-props"),
            Flag("-b", alias=["--beautify"]),
            String(flag="-O", alias=["--output-opts"], arity=Arity.ZERO_OR_MORE),
            Path(flag="-o", alias=["--output"]),
            Flag("--annotations"),
            Flag("--no-annotations"),
            Flag("--comments"),
            Path(flag="--config-file"),
            Expression(flag="-d", alias=["--define"], arity=Arity.ZERO_OR_MORE),
            Flag("-e", alias=["--enclose"]),
            Flag("--expression"),
            Flag("--ie"),
            Flag("--ie8"),  # accepted by the binary, not listed in --help
            Flag("--keep-fargs"),
            Flag("--keep-fnames"),
            Flag("--module"),
            Path(flag="--name-cache"),
            Flag("--rename"),
            Flag("--no-rename"),
            Flag("--self"),
            Flag("--source-map"),
            Flag("--timings"),
            Flag("--toplevel"),
            Flag("--v8"),
            Flag("--validate"),
            Flag("--verbose"),
            Flag("--warn"),
            Flag("--webkit"),
            String(flag="--wrap"),
            Flag("--in-situ"),
            Flag("--reduce-test"),
        ],
        [Path(arity=Arity.ZERO_OR_MORE)],  # [files...]; uglifyjs also expands globs itself
    ]
]
