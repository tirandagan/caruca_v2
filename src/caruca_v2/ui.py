"""All terminal presentation. No logic lives here.

Machine-readable outputs (sidecars, manifests, metrics.db, conversation.jsonl, generated
spec files) never pass through this module: what gets measured is written by the stage,
not by the thing that draws boxes.

`--plain`, a non-TTY stdout, and `NO_COLOR` all degrade to line output.

**Data is never interpolated into markup.** Everything this module is handed as a plain
string is escaped; styling is applied by building `Text` objects instead. Invocation
strings routinely contain square brackets (`test [ -f x ]`, `find . -name '[a-z]*'`), and
rich would otherwise read them as style tags — silently swallowing `[a-z]` or raising
`MarkupError` on `[/]` in the middle of a run.
"""

from __future__ import annotations

import os
import sys
from collections.abc import Iterator
from contextlib import contextmanager

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

THEME = Theme(
    {
        "ok": "bold green",
        "bad": "bold red",
        "warn": "yellow",
        "muted": "dim",
        "key": "cyan",
    }
)

# What a caller may hand this module: a plain string (escaped on the way in) or a Text
# that has already been styled here.
Renderable = str | Text


def compose(*parts: Renderable) -> Text:
    """Join parts into one `Text`, escaping any plain string as literal data."""
    result = Text()
    for part in parts:
        result.append(part if isinstance(part, Text) else Text(part))
    return result


def _as_text(value: Renderable) -> Text:
    return value if isinstance(value, Text) else Text(value)


class UI:
    """The one object a stage prints through."""

    def __init__(self, plain: bool = False, stream=None) -> None:
        stream = stream or sys.stdout
        self.plain = plain or not stream.isatty() or bool(os.environ.get("NO_COLOR"))
        self.console = Console(
            file=stream,
            theme=THEME,
            no_color=self.plain,
            highlight=False,
            soft_wrap=True,
        )

    def line(self, message: Renderable = "") -> None:
        self.console.print(_as_text(message))

    def detail(self, label: str, value: Renderable) -> None:
        if self.plain:
            self.console.print(compose(f"{label}: ", value))
            return
        self.console.print(compose(Text(label, style="key"), " ", value))

    def warn(self, message: Renderable) -> None:
        prefix = Text("warning: ") if self.plain else Text("warning ", style="warn")
        self.console.print(compose(prefix, message))

    def error(self, message: Renderable) -> None:
        stderr = Console(file=sys.stderr, theme=THEME, no_color=self.plain, highlight=False)
        prefix = Text("error: ") if self.plain else Text("error ", style="bad")
        stderr.print(compose(prefix, message))

    def verdict(self, passed: bool, ok_text: str, bad_text: str) -> Text:
        """A pass/fail word, styled. Returned as `Text` so it composes without markup."""
        if self.plain:
            return Text(ok_text if passed else bad_text)
        return Text(ok_text if passed else bad_text, style="ok" if passed else "bad")

    @contextmanager
    def working(self, message: str) -> Iterator[None]:
        """A spinner while something slow happens; a plain line when not a TTY."""
        if self.plain:
            self.console.print(Text(f"{message}..."))
            yield
            return
        with self.console.status(Text(message, style="muted"), spinner="dots"):
            yield

    def summary(self, title: str, rows: list[tuple[str, Renderable]]) -> None:
        """A compact key/value summary of a finished run."""
        if self.plain:
            self.console.print(Text(title))
            for label, value in rows:
                self.console.print(compose(f"  {label}: ", value))
            return

        table = Table(
            title=title, show_header=False, box=None, pad_edge=False, title_justify="left"
        )
        table.add_column(style="key", no_wrap=True)
        table.add_column()
        for label, value in rows:
            table.add_row(Text(label), _as_text(value))
        self.console.print(table)


def money(amount: float) -> str:
    """Costs here are fractions of a cent; the usual two decimals would read as $0.00."""
    return f"${amount:.6f}"


def tokens(prompt: int, completion: int) -> str:
    return f"{prompt:,} prompt + {completion:,} completion"


def duration(seconds: float) -> str:
    return f"{seconds:.2f}s"
