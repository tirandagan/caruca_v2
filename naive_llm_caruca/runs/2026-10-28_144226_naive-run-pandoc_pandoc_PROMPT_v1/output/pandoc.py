from caruca.ir.syntax import *

# pandoc 3.1.3: `pandoc [OPTIONS] [FILES]`
# Options may appear before, between or after the input files. Short options accept their
# value either attached (`-ofile`) or as the next word; long options accept `--opt=VAL` or
# `--opt VAL`, except the optional-argument options (--webtex, --mathjax, --katex,
# --list-extensions), whose value must be attached with `=`.
pandoc_syntax_spec: list[SyntaxSpecification] = [
    [
        [
            # General options
            Format(flag="-f", alias=["-r", "--from", "--read"]),
            Format(flag="-t", alias=["-w", "--to", "--write"]),
            Path(flag="-o", alias=["--output"], dash_as_stdin=True),  # `-o -` means stdout
            Path(flag="--data-dir"),
            String(flag="-M", alias=["--metadata"], arity=Arity.ZERO_OR_MORE),  # KEY[:VALUE]
            Path(flag="--metadata-file", arity=Arity.ZERO_OR_MORE),
            Path(flag="-d", alias=["--defaults"], arity=Arity.ZERO_OR_MORE),
            Flag("--file-scope"),
            Flag("--sandbox"),
            Flag("-s", alias=["--standalone"]),
            Path(flag="--template"),  # FILE|URL
            String(flag="-V", alias=["--variable"], arity=Arity.ZERO_OR_MORE),  # KEY[:VALUE]
            Selection(flag="--wrap", choices=["auto", "none", "preserve"]),
            Flag("--ascii"),
            Flag("--toc", alias=["--table-of-contents"]),
            Integer(flag="--toc-depth", min=1, max=6),
            Flag("-N", alias=["--number-sections"]),
            List(flag="--number-offset", of=Integer, separator=","),
            Selection(
                flag="--top-level-division",
                choices=["default", "section", "chapter", "part"],
            ),
            Path(flag="--extract-media"),  # directory, created if necessary
            List(flag="--resource-path", of=Path, separator=":", arity=Arity.ZERO_OR_MORE),
            Path(flag="-H", alias=["--include-in-header"], arity=Arity.ZERO_OR_MORE),
            Path(flag="-B", alias=["--include-before-body"], arity=Arity.ZERO_OR_MORE),
            Path(flag="-A", alias=["--include-after-body"], arity=Arity.ZERO_OR_MORE),
            Flag("--no-highlight"),
            String(flag="--highlight-style"),  # STYLE name or a .theme FILE
            Path(flag="--syntax-definition", arity=Arity.ZERO_OR_MORE),
            Integer(flag="--dpi", min=1),
            Selection(flag="--eol", choices=["crlf", "lf", "native"]),
            Integer(flag="--columns", min=1),
            Flag("-p", alias=["--preserve-tabs"]),
            Integer(flag="--tab-stop", min=1),
            Command(flag="--pdf-engine"),
            String(flag="--pdf-engine-opt", arity=Arity.ZERO_OR_MORE),
            Path(flag="--reference-doc"),
            Flag("--self-contained"),
            Flag("--embed-resources"),
            String(flag="--request-header", arity=Arity.ZERO_OR_MORE),  # NAME:VALUE
            Flag("--no-check-certificate"),
            Path(flag="--abbreviations"),
            String(flag="--indented-code-classes"),
            String(flag="--default-image-extension"),
            Command(flag="-F", alias=["--filter"], arity=Arity.ZERO_OR_MORE),
            Path(flag="-L", alias=["--lua-filter"], arity=Arity.ZERO_OR_MORE),
            Integer(flag="--shift-heading-level-by"),
            Integer(flag="--base-header-level", min=1, max=5),  # deprecated
            Selection(flag="--track-changes", choices=["accept", "reject", "all"]),
            Flag("--strip-comments"),
            Flag("--reference-links"),
            Selection(
                flag="--reference-location", choices=["block", "section", "document"]
            ),
            Selection(flag="--markdown-headings", choices=["setext", "atx"]),
            Flag("--list-tables"),
            Flag("--listings"),
            Flag("-i", alias=["--incremental"]),
            Integer(flag="--slide-level", min=0, max=6),
            Flag("--section-divs"),
            Flag("--html-q-tags"),
            Selection(
                flag="--email-obfuscation", choices=["none", "javascript", "references"]
            ),
            String(flag="--id-prefix"),
            String(flag="-T", alias=["--title-prefix"]),
            String(flag="-c", alias=["--css"], arity=Arity.ZERO_OR_MORE),  # URL
            String(flag="--epub-subdirectory"),
            Path(flag="--epub-cover-image"),
            Selection(flag="--epub-title-page", choices=["true", "false"]),
            Path(flag="--epub-metadata"),
            Path(flag="--epub-embed-font", arity=Arity.ZERO_OR_MORE),
            Integer(flag="--split-level", min=1, max=6),
            String(flag="--chunk-template"),
            Integer(flag="--epub-chapter-level", min=1, max=6),  # deprecated alias of --split-level
            Selection(flag="--ipynb-output", choices=["all", "none", "best"]),
            Flag("-C", alias=["--citeproc"]),
            Path(flag="--bibliography", arity=Arity.ZERO_OR_MORE),
            Path(flag="--csl"),
            Path(flag="--citation-abbreviations"),
            Flag("--natbib"),
            Flag("--biblatex"),
            Flag("--mathml"),
            # Optional-argument options: bare `--webtex` or `--webtex=URL`; never `--webtex URL`.
            String(flag="--webtex", flag_followed_by_equals=True),
            String(flag="--mathjax", flag_followed_by_equals=True),
            String(flag="--katex", flag_followed_by_equals=True),
            Flag("--gladtex"),
            Flag("--trace"),
            Flag("--dump-args"),
            Flag("--ignore-args"),
            Flag("--verbose"),
            Flag("--quiet"),
            Flag("--fail-if-warnings"),
            Path(flag="--log"),
            # Informational modes: print to stdout and exit, without converting anything
            Flag("--bash-completion"),
            Flag("--list-input-formats"),
            Flag("--list-output-formats"),
            Format(flag="--list-extensions", flag_followed_by_equals=True),
            Flag("--list-highlight-languages"),
            Flag("--list-highlight-styles"),
            Format(flag="-D", alias=["--print-default-template"]),
            String(flag="--print-default-data-file"),  # name of a bundled data file
            String(flag="--print-highlight-style"),  # STYLE name or a .theme FILE
            Flag("-v", alias=["--version"]),
            Flag("-h", alias=["--help"]),
        ],
        [
            Path(arity=Arity.ZERO_OR_MORE, dash_as_stdin=True),  # [FILES]; none means stdin
        ],
    ]
]
