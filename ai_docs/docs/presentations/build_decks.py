#!/usr/bin/env python3
"""
Builds the caruca_v2 status decks for both advisors from a single content
definition, so the two versions cannot silently drift apart.

Run:  ../../../.venv/bin/python build_decks.py
"""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

# ---------------------------------------------------------------- constants

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DIAGRAMS = REPO / "ai_docs" / "diagrams"

SLIDE_W, SLIDE_H = 13.333, 7.5
MARGIN = 0.7
CONTENT_W = SLIDE_W - 2 * MARGIN

TITLE_Y = 0.5
BODY_Y = 1.65
BODY_BOTTOM = 6.45
FOOTNOTE_Y = 6.72
FOOTER_Y = 7.02

FONT = "Segoe UI"

GREEN = RGBColor(0x5B, 0x8C, 0x5A)
GREEN_FILL = RGBColor(0xED, 0xF3, 0xEB)
BLUE = RGBColor(0x4A, 0x6F, 0xA5)
BLUE_FILL = RGBColor(0xEA, 0xF0, 0xF8)
AMBER = RGBColor(0xC0, 0x8A, 0x2E)
AMBER_FILL = RGBColor(0xFB, 0xF0, 0xDC)
TEXT = RGBColor(0x33, 0x33, 0x33)
MUTED = RGBColor(0x66, 0x66, 0x66)
FAINT = RGBColor(0x99, 0x99, 0x99)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RULE = RGBColor(0xDD, 0xDD, 0xDD)

DATE = "August 2026"
PROJECT = "caruca_v2"


# ---------------------------------------------------------------- helpers

def textbox(slide, x, y, w, h, *, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    return tf


def write(tf, text, *, size, bold=False, color=TEXT, space_after=0,
          space_before=0, align=PP_ALIGN.LEFT, italic=False, first=False,
          line_spacing=None):
    para = tf.paragraphs[0] if first else tf.add_paragraph()
    para.alignment = align
    if space_after:
        para.space_after = Pt(space_after)
    if space_before:
        para.space_before = Pt(space_before)
    if line_spacing:
        para.line_spacing = line_spacing
    run = para.add_run()
    run.text = text
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return para


def rect(slide, x, y, w, h, fill, line=None, width=1.0,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.shadow.inherit = False
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(width)
    sh.text_frame.word_wrap = True
    return sh


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def add_title(slide, title, kicker=None):
    y = TITLE_Y
    if kicker:
        tf = textbox(slide, MARGIN, y - 0.02, CONTENT_W, 0.3)
        write(tf, kicker.upper(), size=11, bold=True, color=BLUE, first=True)
        y += 0.34
    tf = textbox(slide, MARGIN, y, CONTENT_W, 0.75)
    write(tf, title, size=30, bold=True, color=TEXT, first=True)
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(MARGIN), Inches(y + 0.78),
        Inches(1.1), Inches(0.045))
    line.shadow.inherit = False
    line.fill.solid()
    line.fill.fore_color.rgb = BLUE
    line.line.fill.background()


def add_footnote(slide, sources):
    if not sources:
        return
    tf = textbox(slide, MARGIN, FOOTNOTE_Y, CONTENT_W, 0.26)
    label = "Source document: " if len(sources) == 1 else "Source documents: "
    write(tf, label + ", ".join(sources), size=10, color=FAINT, first=True)


def add_chrome(slide, number, step=None):
    """Footer rule, project/date, slide number, and the step marker."""
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(MARGIN), Inches(FOOTER_Y - 0.1),
        Inches(CONTENT_W), Inches(0.012))
    line.shadow.inherit = False
    line.fill.solid()
    line.fill.fore_color.rgb = RULE
    line.line.fill.background()

    tf = textbox(slide, MARGIN, FOOTER_Y, 5.0, 0.28)
    write(tf, f"{PROJECT}  ·  {DATE}", size=9.5, color=FAINT, first=True)

    tf = textbox(slide, SLIDE_W - MARGIN - 1.0, FOOTER_Y, 1.0, 0.28)
    write(tf, str(number), size=9.5, color=FAINT, align=PP_ALIGN.RIGHT, first=True)

    if step:
        # Unobtrusive marker: which of the two steps this slide belongs to.
        w = 1.62
        x = SLIDE_W - MARGIN - 1.15 - w
        fill, edge = (BLUE_FILL, BLUE) if step == 1 else (WHITE, FAINT)
        sh = rect(slide, x, FOOTER_Y - 0.02, w, 0.26, fill, edge, 0.75)
        tf = sh.text_frame
        tf.margin_left = tf.margin_right = 0
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        write(tf, f"Step {'one' if step == 1 else 'two'}", size=9,
              color=BLUE if step == 1 else MUTED, align=PP_ALIGN.CENTER,
              first=True)


def add_notes(slide, notes):
    if notes:
        slide.notes_slide.notes_text_frame.text = notes


# ---------------------------------------------------------------- slide kinds

def slide_title(prs, audience):
    slide = blank(prs)
    band = rect(slide, 0, 0, SLIDE_W, 2.45, BLUE_FILL, None)
    band.text_frame.text = ""

    tf = textbox(slide, MARGIN, 0.85, CONTENT_W, 0.5)
    write(tf, "CARUCA v2  ·  STATUS AND OPEN QUESTIONS", size=13, bold=True,
          color=BLUE, first=True)

    tf = textbox(slide, MARGIN, 1.28, CONTENT_W, 0.9)
    write(tf, "Can an LLM do what Caruca does?", size=40, bold=True, first=True)

    tf = textbox(slide, MARGIN, 2.85, CONTENT_W, 1.5)
    write(tf, "A plan to replicate Caruca's results using a language model,",
          size=19, color=MUTED, first=True, space_after=4)
    write(tf, "measure the two head to head, and only then extend further.",
          size=19, color=MUTED)

    tf = textbox(slide, MARGIN, 4.75, CONTENT_W, 1.2)
    write(tf, f"Prepared for {audience}", size=17, bold=True, first=True,
          space_after=6)
    write(tf, "Tiran Dagan", size=16, color=MUTED, space_after=2)
    write(tf, DATE, size=14, color=FAINT)

    add_notes(slide, NOTES_TITLE)
    return slide


def slide_bullets(prs, spec, number):
    slide = blank(prs)
    add_title(slide, spec["title"], spec.get("kicker"))

    y = BODY_Y
    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W - 0.4, 0.6)
        write(tf, spec["lead"], size=19, color=MUTED, first=True)
        y += 0.85

    for item in spec["bullets"]:
        head, sub = (item if isinstance(item, tuple) else (item, None))
        dot = rect(slide, MARGIN + 0.02, y + 0.16, 0.11, 0.11, BLUE, None,
                   shape=MSO_SHAPE.OVAL)
        dot.text_frame.text = ""
        tf = textbox(slide, MARGIN + 0.34, y, CONTENT_W - 0.34, 0.42)
        write(tf, head, size=18, bold=bool(sub), first=True)
        y += 0.44
        if sub:
            tf = textbox(slide, MARGIN + 0.34, y - 0.05, CONTENT_W - 0.9, 0.42)
            write(tf, sub, size=15, color=MUTED, first=True)
            y += 0.42
        y += 0.16

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number, spec.get("step"))
    add_notes(slide, spec.get("notes"))
    return slide


def slide_two_steps(prs, spec, number):
    """The anchor slide: step one now, step two later."""
    slide = blank(prs)
    add_title(slide, spec["title"], spec.get("kicker"))

    tf = textbox(slide, MARGIN, BODY_Y, CONTENT_W, 0.5)
    write(tf, spec["lead"], size=19, color=MUTED, first=True)

    top = BODY_Y + 0.85
    h = 3.05
    w = (CONTENT_W - 0.85) / 2

    # Step one: solid, present tense, emphasised
    card = rect(slide, MARGIN, top, w, h, BLUE_FILL, BLUE, 2.0)
    card.text_frame.text = ""
    tf = textbox(slide, MARGIN + 0.42, top + 0.35, w - 0.84, 2.4)
    write(tf, "STEP ONE  ·  NOW", size=12, bold=True, color=BLUE, first=True,
          space_after=8)
    write(tf, "Replicate", size=27, bold=True, space_after=10)
    for line in spec["step_one"]:
        write(tf, line, size=15.5, color=TEXT, space_after=7)

    # Step two: dashed-feel, muted, explicitly later
    x2 = MARGIN + w + 0.85
    card = rect(slide, x2, top, w, h, WHITE, FAINT, 1.25)
    card.text_frame.text = ""
    tf = textbox(slide, x2 + 0.42, top + 0.35, w - 0.84, 2.4)
    write(tf, "STEP TWO  ·  LATER", size=12, bold=True, color=MUTED, first=True,
          space_after=8)
    write(tf, "Extend", size=27, bold=True, color=MUTED, space_after=10)
    for line in spec["step_two"]:
        write(tf, line, size=15.5, color=MUTED, space_after=7)

    # The restraint statement, given its own weight
    bar = rect(slide, MARGIN, top + h + 0.28, CONTENT_W, 0.62, AMBER_FILL, AMBER, 1.25)
    tf = bar.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.3)
    write(tf, spec["banner"], size=16.5, bold=True, color=TEXT, first=True)

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number)
    add_notes(slide, spec.get("notes"))
    return slide


def slide_findings(prs, spec, number):
    """Each finding stated plainly, paired with what we do about it."""
    slide = blank(prs)
    add_title(slide, spec["title"], spec.get("kicker"))

    y = BODY_Y
    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W, 0.45)
        write(tf, spec["lead"], size=17, color=MUTED, first=True)
        y += 0.62

    n = len(spec["findings"])
    h = 1.30 if n > 2 else 1.62
    gap = 0.26 if n > 2 else 0.34

    for found, response in spec["findings"]:
        card = rect(slide, MARGIN, y, CONTENT_W, h, WHITE, RULE, 1.0)
        card.text_frame.text = ""

        tf = textbox(slide, MARGIN + 0.36, y + 0.24, CONTENT_W * 0.52, h - 0.4)
        write(tf, "WHAT WE FOUND", size=9.5, bold=True, color=FAINT, first=True,
              space_after=5)
        write(tf, found, size=15, color=TEXT)

        div = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(MARGIN + CONTENT_W * 0.56),
            Inches(y + 0.22), Inches(0.012), Inches(h - 0.44))
        div.shadow.inherit = False
        div.fill.solid()
        div.fill.fore_color.rgb = RULE
        div.line.fill.background()

        tf = textbox(slide, MARGIN + CONTENT_W * 0.60, y + 0.24,
                     CONTENT_W * 0.37, h - 0.4)
        write(tf, "WHAT WE DO ABOUT IT", size=9.5, bold=True, color=BLUE,
              first=True, space_after=5)
        write(tf, response, size=15, color=TEXT)
        y += h + gap

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number, spec.get("step"))
    add_notes(slide, spec.get("notes"))
    return slide


def slide_image(prs, spec, number):
    slide = blank(prs)
    add_title(slide, spec["title"], spec.get("kicker"))

    y = BODY_Y
    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W, 0.42)
        write(tf, spec["lead"], size=17, color=MUTED, first=True)
        y += 0.55

    img = DIAGRAMS / spec["image"]
    avail_h = FOOTNOTE_Y - 0.18 - y
    avail_w = CONTENT_W

    from PIL import Image  # noqa: F401  (only used if available)
    import struct
    with open(img, "rb") as fh:
        head = fh.read(33)
    iw, ih = struct.unpack(">II", head[16:24])
    scale = min(avail_w / iw, avail_h / ih)
    w, h = iw * scale, ih * scale
    slide.shapes.add_picture(
        str(img), Inches(MARGIN + (avail_w - w) / 2), Inches(y),
        Inches(w), Inches(h))

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number, spec.get("step"))
    add_notes(slide, spec.get("notes"))
    return slide


def slide_cards(prs, spec, number):
    """A row of short cards. Used for build order and the 'not doing' slide."""
    slide = blank(prs)
    add_title(slide, spec["title"], spec.get("kicker"))

    y = BODY_Y
    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W, 0.45)
        write(tf, spec["lead"], size=18, color=MUTED, first=True)
        y += 0.72

    cards = spec["cards"]
    n = len(cards)
    gap = 0.28
    w = (CONTENT_W - gap * (n - 1)) / n
    h = 2.85

    for i, (head, body) in enumerate(cards):
        x = MARGIN + i * (w + gap)
        muted = spec.get("muted", False)
        fill = WHITE if muted else BLUE_FILL
        edge = FAINT if muted else BLUE
        card = rect(slide, x, y, w, h, fill, edge, 1.5)
        card.text_frame.text = ""

        if spec.get("numbered"):
            badge = rect(slide, x + 0.32, y + 0.32, 0.46, 0.46, BLUE, None,
                         shape=MSO_SHAPE.OVAL)
            tfb = badge.text_frame
            tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
            tfb.margin_left = tfb.margin_right = 0
            write(tfb, str(i + 1), size=14, bold=True, color=WHITE,
                  align=PP_ALIGN.CENTER, first=True)
            head_y = y + 0.95
        else:
            head_y = y + 0.38

        tf = textbox(slide, x + 0.32, head_y, w - 0.64, 0.8)
        write(tf, head, size=17, bold=True,
              color=MUTED if muted else TEXT, first=True)
        tf = textbox(slide, x + 0.32, head_y + 0.72, w - 0.64, h - (head_y - y) - 0.9)
        write(tf, body, size=14, color=MUTED, first=True)

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number, spec.get("step"))
    add_notes(slide, spec.get("notes"))
    return slide


def slide_questions(prs, spec, number):
    slide = blank(prs)
    add_title(slide, spec["title"], spec.get("kicker"))

    tf = textbox(slide, MARGIN, BODY_Y, CONTENT_W, 0.45)
    write(tf, spec["lead"], size=17, color=MUTED, first=True)

    y = BODY_Y + 0.62
    h = 1.06
    for i, (q, why, lean) in enumerate(spec["questions"]):
        badge = rect(slide, MARGIN, y + 0.22, 0.42, 0.42, BLUE_FILL, BLUE, 1.0,
                     shape=MSO_SHAPE.OVAL)
        tfb = badge.text_frame
        tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
        tfb.margin_left = tfb.margin_right = 0
        write(tfb, str(i + 1), size=13, bold=True, color=BLUE,
              align=PP_ALIGN.CENTER, first=True)

        tf = textbox(slide, MARGIN + 0.62, y + 0.06, CONTENT_W - 0.62, 0.9)
        write(tf, q, size=17, bold=True, first=True, space_after=4)
        write(tf, why, size=13.5, color=MUTED, space_after=3)
        write(tf, f"My current lean: {lean}", size=13.5, color=BLUE, italic=True)
        y += h + 0.12

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number)
    add_notes(slide, spec.get("notes"))
    return slide


def slide_closing(prs, spec, number):
    slide = blank(prs)
    rect(slide, 0, 0, SLIDE_W, SLIDE_H, BLUE_FILL, None).text_frame.text = ""

    tf = textbox(slide, MARGIN, 1.55, CONTENT_W, 0.4)
    write(tf, "NEXT STEP", size=13, bold=True, color=BLUE, first=True)

    tf = textbox(slide, MARGIN, 2.05, CONTENT_W * 0.82, 1.2)
    write(tf, spec["headline"], size=33, bold=True, first=True)

    tf = textbox(slide, MARGIN, 3.5, CONTENT_W * 0.78, 1.6)
    for line in spec["body"]:
        write(tf, line, size=17, color=TEXT, space_after=10,
              first=(line is spec["body"][0]))

    bar = rect(slide, MARGIN, 5.35, CONTENT_W * 0.78, 0.72, WHITE, BLUE, 1.5)
    tf = bar.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.3)
    write(tf, spec["ask"], size=16.5, bold=True, color=BLUE, first=True)

    add_chrome(slide, number)
    add_notes(slide, spec.get("notes"))
    return slide


def slide_section(prs, title, subtitle, number):
    slide = blank(prs)
    rect(slide, 0, 0, SLIDE_W, SLIDE_H, WHITE, None).text_frame.text = ""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(MARGIN), Inches(3.05),
        Inches(1.1), Inches(0.05))
    bar.shadow.inherit = False
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()

    tf = textbox(slide, MARGIN, 3.35, CONTENT_W, 0.9)
    write(tf, title, size=34, bold=True, first=True)
    tf = textbox(slide, MARGIN, 4.25, CONTENT_W * 0.7, 0.6)
    write(tf, subtitle, size=17, color=MUTED, first=True)
    add_chrome(slide, number)
    return slide


def slide_table(prs, spec, number):
    """Simple two-column reference list, used in the appendix."""
    slide = blank(prs)
    add_title(slide, spec["title"], spec.get("kicker"))

    y = BODY_Y
    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W, 0.4)
        write(tf, spec["lead"], size=16, color=MUTED, first=True)
        y += 0.55

    for left, right in spec["rows"]:
        tf = textbox(slide, MARGIN, y, CONTENT_W * 0.36, 0.5)
        write(tf, left, size=14, bold=True, first=True)
        tf = textbox(slide, MARGIN + CONTENT_W * 0.38, y, CONTENT_W * 0.62, 0.5)
        write(tf, right, size=14, color=MUTED, first=True)
        y += spec.get("row_h", 0.52)

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number)
    add_notes(slide, spec.get("notes"))
    return slide


BUILDERS = {
    "bullets": slide_bullets,
    "two_steps": slide_two_steps,
    "findings": slide_findings,
    "image": slide_image,
    "cards": slide_cards,
    "questions": slide_questions,
    "closing": slide_closing,
    "table": slide_table,
}
