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


def est_lines(text, size, width_in):
    """
    Rough wrapped-line count. The 0.55em per character figure is deliberately
    conservative: underestimating wrapping causes overlapping text, while
    overestimating only leaves a little extra whitespace.
    """
    if not text:
        return 0
    chars_per_line = max(1, int((width_in * 72) / (size * 0.55)))
    return max(1, -(-len(text) // chars_per_line))


def est_height(text, size, width_in, leading=1.24):
    return est_lines(text, size, width_in) * size * leading / 72.0


def add_title(slide, title, kicker=None):
    """Draws the title block. Returns the y where body content may start."""
    y = TITLE_Y
    if kicker:
        tf = textbox(slide, MARGIN, y - 0.02, CONTENT_W, 0.3)
        write(tf, kicker.upper(), size=11, bold=True, color=BLUE, first=True)
        y += 0.36
    tf = textbox(slide, MARGIN, y, CONTENT_W, 0.75)
    write(tf, title, size=30, bold=True, color=TEXT, first=True)
    rule_y = y + 0.78
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(MARGIN), Inches(rule_y),
        Inches(1.1), Inches(0.045))
    line.shadow.inherit = False
    line.fill.solid()
    line.fill.fore_color.rgb = BLUE
    line.line.fill.background()
    # Body must clear the rule, otherwise it collides on kicker slides.
    return rule_y + 0.30


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
    band = rect(slide, 0, 0, SLIDE_W, 2.45, BLUE_FILL, None,
                shape=MSO_SHAPE.RECTANGLE)
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
    top = add_title(slide, spec["title"], spec.get("kicker"))

    items = [(i if isinstance(i, tuple) else (i, None)) for i in spec["bullets"]]
    head_w = CONTENT_W - 0.34
    sub_w = CONTENT_W - 0.9
    limit = FOOTNOTE_Y - 0.16

    # Shrink type and spacing together until the content fits the slide.
    for head_s, sub_s, lead_s, gap in [
        (18, 15, 19, 0.17), (17, 14.5, 18, 0.15), (16.5, 14, 17, 0.13),
        (16, 13.5, 16.5, 0.11), (15, 13, 16, 0.09), (14, 12.5, 15, 0.07),
    ]:
        y = top
        if spec.get("lead"):
            y += est_height(spec["lead"], lead_s, CONTENT_W - 0.4) + 0.34
        for head, sub in items:
            y += est_height(head, head_s, head_w) + 0.10
            if sub:
                y += est_height(sub, sub_s, sub_w) + 0.04
            y += gap
        if y <= limit:
            break

    y = top
    if spec.get("lead"):
        h = est_height(spec["lead"], lead_s, CONTENT_W - 0.4)
        tf = textbox(slide, MARGIN, y, CONTENT_W - 0.4, h + 0.1)
        write(tf, spec["lead"], size=lead_s, color=MUTED, first=True)
        y += h + 0.34

    for head, sub in items:
        hh = est_height(head, head_s, head_w)
        dot = rect(slide, MARGIN + 0.03, y + hh / 2 - 0.055, 0.105, 0.105, BLUE,
                   None, shape=MSO_SHAPE.OVAL)
        dot.text_frame.text = ""
        tf = textbox(slide, MARGIN + 0.34, y, head_w, hh + 0.1)
        write(tf, head, size=head_s, bold=bool(sub), first=True)
        y += hh + 0.10
        if sub:
            sh = est_height(sub, sub_s, sub_w)
            tf = textbox(slide, MARGIN + 0.34, y, sub_w, sh + 0.1)
            write(tf, sub, size=sub_s, color=MUTED, first=True)
            y += sh + 0.04
        y += gap

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number, spec.get("step"))
    add_notes(slide, spec.get("notes"))
    return slide


def slide_two_steps(prs, spec, number):
    """The anchor slide: step one now, step two later."""
    slide = blank(prs)
    title_bottom = add_title(slide, spec["title"], spec.get("kicker"))

    tf = textbox(slide, MARGIN, title_bottom, CONTENT_W, 0.4)
    write(tf, spec["lead"], size=18, color=MUTED, first=True)

    top = title_bottom + 0.5
    banner_h = 0.62
    bottom_limit = FOOTNOTE_Y - 0.16
    h = bottom_limit - banner_h - 0.24 - top
    w = (CONTENT_W - 0.85) / 2
    inner_w = w - 0.84

    # Size body text so the longest column fits inside the card.
    for body_s in (15.5, 15, 14.5, 14, 13.5, 13):
        need = 0.35 + 0.26 + 0.10 + (27 * 1.2 / 72) + 0.14
        worst = max(
            sum(est_height(t, body_s, inner_w) + 0.10 for t in spec["step_one"]),
            sum(est_height(t, body_s, inner_w) + 0.10 for t in spec["step_two"]),
        )
        if need + worst + 0.30 <= h:
            break

    def column(x, kicker, heading, lines, accent, fill, edge, width, body_color):
        card = rect(slide, x, top, w, h, fill, edge, width)
        card.text_frame.text = ""
        yy = top + 0.36
        tf = textbox(slide, x + 0.42, yy, inner_w, 0.26)
        write(tf, kicker, size=12, bold=True, color=accent, first=True)
        yy += 0.34
        tf = textbox(slide, x + 0.42, yy, inner_w, 0.52)
        write(tf, heading, size=27, bold=True, color=body_color, first=True)
        yy += 0.60
        for t in lines:
            hh = est_height(t, body_s, inner_w)
            tf = textbox(slide, x + 0.42, yy, inner_w, hh + 0.1)
            write(tf, t, size=body_s, color=body_color, first=True)
            yy += hh + 0.13

    column(MARGIN, "STEP ONE  ·  NOW", "Replicate", spec["step_one"],
           BLUE, BLUE_FILL, BLUE, 2.0, TEXT)
    column(MARGIN + w + 0.85, "STEP TWO  ·  LATER", "Extend", spec["step_two"],
           MUTED, WHITE, FAINT, 1.25, MUTED)

    # The restraint statement, given its own weight
    bar = rect(slide, MARGIN, top + h + 0.24, CONTENT_W, banner_h,
               AMBER_FILL, AMBER, 1.25)
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
    y = add_title(slide, spec["title"], spec.get("kicker"))

    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W, 0.45)
        write(tf, spec["lead"], size=17, color=MUTED, first=True)
        y += 0.52

    n = len(spec["findings"])
    gap = 0.26
    avail = (FOOTNOTE_Y - 0.16) - y
    # Height driven by the tallest card, so nothing clips.
    need = max(
        max(est_height(f, 15, CONTENT_W * 0.50),
            est_height(r, 15, CONTENT_W * 0.35))
        for f, r in spec["findings"]
    ) + 0.70
    h = min(need, (avail - gap * (n - 1)) / n)

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
    y = add_title(slide, spec["title"], spec.get("kicker"))

    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W, 0.42)
        write(tf, spec["lead"], size=17, color=MUTED, first=True)
        y += 0.46

    img = DIAGRAMS / spec["image"]
    avail_h = FOOTNOTE_Y - 0.18 - y
    avail_w = CONTENT_W

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
    y = add_title(slide, spec["title"], spec.get("kicker"))

    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W, 0.45)
        write(tf, spec["lead"], size=18, color=MUTED, first=True)
        y += 0.62

    cards = spec["cards"]
    n = len(cards)
    gap = 0.28
    w = (CONTENT_W - gap * (n - 1)) / n
    inner_w = w - 0.64
    numbered = spec.get("numbered")
    badge_h = 0.63 if numbered else 0.0

    # Card height follows the tallest card's content, capped by the slide.
    need = max(
        est_height(h_, 17, inner_w) + est_height(b_, 14, inner_w)
        for h_, b_ in cards
    ) + badge_h + 0.78
    h = min(need, (FOOTNOTE_Y - 0.16) - y)

    for i, (head, body) in enumerate(cards):
        x = MARGIN + i * (w + gap)
        muted = spec.get("muted", False)
        fill = WHITE if muted else BLUE_FILL
        edge = FAINT if muted else BLUE
        card = rect(slide, x, y, w, h, fill, edge, 1.5)
        card.text_frame.text = ""

        head_y = y + 0.36
        if numbered:
            badge = rect(slide, x + 0.32, head_y, 0.44, 0.44, BLUE, None,
                         shape=MSO_SHAPE.OVAL)
            tfb = badge.text_frame
            tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
            tfb.margin_left = tfb.margin_right = 0
            write(tfb, str(i + 1), size=14, bold=True, color=WHITE,
                  align=PP_ALIGN.CENTER, first=True)
            head_y += badge_h

        hh = est_height(head, 17, inner_w)
        tf = textbox(slide, x + 0.32, head_y, inner_w, hh + 0.1)
        write(tf, head, size=17, bold=True,
              color=MUTED if muted else TEXT, first=True)
        tf = textbox(slide, x + 0.32, head_y + hh + 0.16, inner_w,
                     h - (head_y - y) - hh - 0.3)
        write(tf, body, size=14, color=MUTED, first=True)

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number, spec.get("step"))
    add_notes(slide, spec.get("notes"))
    return slide


def slide_questions(prs, spec, number):
    slide = blank(prs)
    y = add_title(slide, spec["title"], spec.get("kicker"))

    tf = textbox(slide, MARGIN, y, CONTENT_W, 0.4)
    write(tf, spec["lead"], size=17, color=MUTED, first=True)
    y += 0.48

    body_w = CONTENT_W - 0.68
    limit = FOOTNOTE_Y - 0.16

    for q_s, why_s, gap in [(17, 13.5, 0.24), (16, 13, 0.20),
                            (15.5, 12.5, 0.16), (15, 12, 0.12)]:
        total = y
        for q, why, lean in spec["questions"]:
            total += (est_height(q, q_s, body_w) + 0.07
                      + est_height(why, why_s, body_w) + 0.05
                      + est_height(f"My current lean: {lean}", why_s, body_w)
                      + gap)
        if total <= limit:
            break

    for i, (q, why, lean) in enumerate(spec["questions"]):
        qh = est_height(q, q_s, body_w)
        badge = rect(slide, MARGIN, y + qh / 2 - 0.20, 0.40, 0.40, BLUE_FILL,
                     BLUE, 1.0, shape=MSO_SHAPE.OVAL)
        tfb = badge.text_frame
        tfb.vertical_anchor = MSO_ANCHOR.MIDDLE
        tfb.margin_left = tfb.margin_right = 0
        write(tfb, str(i + 1), size=13, bold=True, color=BLUE,
              align=PP_ALIGN.CENTER, first=True)

        tf = textbox(slide, MARGIN + 0.68, y, body_w, qh + 0.1)
        write(tf, q, size=q_s, bold=True, first=True)
        y += qh + 0.07

        wh = est_height(why, why_s, body_w)
        tf = textbox(slide, MARGIN + 0.68, y, body_w, wh + 0.1)
        write(tf, why, size=why_s, color=MUTED, first=True)
        y += wh + 0.05

        lean_text = f"My current lean: {lean}"
        lh = est_height(lean_text, why_s, body_w)
        tf = textbox(slide, MARGIN + 0.68, y, body_w, lh + 0.1)
        write(tf, lean_text, size=why_s, color=BLUE, italic=True, first=True)
        y += lh + gap

    add_footnote(slide, spec.get("sources", []))
    add_chrome(slide, number)
    add_notes(slide, spec.get("notes"))
    return slide


def slide_closing(prs, spec, number):
    slide = blank(prs)
    rect(slide, 0, 0, SLIDE_W, SLIDE_H, BLUE_FILL, None,
         shape=MSO_SHAPE.RECTANGLE).text_frame.text = ""

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
    rect(slide, 0, 0, SLIDE_W, SLIDE_H, WHITE, None,
         shape=MSO_SHAPE.RECTANGLE).text_frame.text = ""
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
    y = add_title(slide, spec["title"], spec.get("kicker"))

    if spec.get("lead"):
        tf = textbox(slide, MARGIN, y, CONTENT_W, 0.4)
        write(tf, spec["lead"], size=16, color=MUTED, first=True)
        y += 0.48

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


# ---------------------------------------------------------------- content
# Every slide declares its audience: "both", "michael", or "william".
# The two decks are generated from this one list so they cannot diverge.

NOTES_TITLE = (
    "Thanks for making the time. I want to walk you through where the project "
    "stands, share four things I found while reviewing the paper and the code, "
    "and then put four open questions to you. Planning is finished; nothing is "
    "built yet. That is deliberate, because I would rather get your input "
    "before writing code than after."
)

SLIDES = [
    # ---------------------------------------------------------- opening
    {
        "kind": "bullets", "audience": "both",
        "title": "Where things stand",
        "lead": "Planning is complete. Nothing is built yet. That is deliberate.",
        "bullets": [
            ("Five planning documents are finished",
             "What to build, how the pieces fit, what gets measured, and in what order."),
            ("The plan is two steps, not one",
             "First replicate what Caruca already does, using a language model. Only then extend."),
            ("I reviewed the original paper and the code in detail",
             "Four findings worth your attention, including one I need Michael to confirm."),
            ("I am here for your input, not a green light",
             "Four open questions at the end. I would rather resolve them now than rework later."),
        ],
        "sources": ["master_idea", "roadmap"],
        "notes": (
            "Set expectations early: this is a planning checkpoint, not a demo. "
            "The key message is that nothing has been built because I wanted the "
            "approach reviewed first. If they only remember one thing from this "
            "deck, it should be the two-step structure on the next slide."
        ),
    },

    # ---------------------------------------------------------- William primer
    {
        "kind": "bullets", "audience": "william",
        "kicker": "Background",
        "title": "What Caruca does",
        "lead": "Some shell tools need to know how a command behaves before they can safely optimise it.",
        "bullets": [
            ("The problem: tools need behavioural descriptions of commands",
             "Does this command read a file or write one? Can it be split across processors safely?"),
            ("Writing those descriptions by hand does not scale",
             "There are thousands of commands, each with dozens of options, and they differ between systems."),
            ("Caruca generates them automatically",
             "It reads the manual page, builds test invocations, runs them in a sandbox, and watches what "
             "each one actually touches."),
            ("It works: correct descriptions for 59 of 60 commands tested",
             "Published October 2025. Michael is a co-author."),
        ],
        "sources": ["caruca_white_paper"],
        "notes": (
            "William has no involvement with Caruca, so this slide exists to give "
            "him a standing start. Keep it to about ninety seconds. The important "
            "part is the third bullet: read the manual, build tests, run them, "
            "watch. That four-step shape recurs throughout the deck."
        ),
    },
    {
        "kind": "bullets", "audience": "william",
        "kicker": "Background",
        "title": "Why it is worth testing a language model here",
        "lead": "Caruca uses AI for one small step. Everything else is hand-written code.",
        "bullets": [
            ("Today the model does one job: read the manual page, describe the options",
             "Roughly 3,456 lines of hand-written code do everything after that."),
            ("The open question is how much of that hand-written work a model could do",
             "Nobody has measured it. Not in this paper, not elsewhere for this problem."),
            ("Answering it needs a fair comparison, not an impression",
             "Same inputs, same yardstick, cost and reliability measured on both sides."),
            ("There is a second payoff",
             "The findings feed a revised version of the paper, which was not accepted on first submission."),
        ],
        "sources": ["master_idea"],
        "notes": (
            "This is the 'why should I care' slide for William specifically. The "
            "third bullet is the methodological heart and is squarely in his "
            "wheelhouse, so pause there and invite him in."
        ),
    },

    # ---------------------------------------------------------- the anchor
    {
        "kind": "two_steps", "audience": "both",
        "title": "The goal, in two steps",
        "lead": "The order matters more than the ambition.",
        "step_one": [
            "Reproduce what Caruca does today, using a language model in "
            "place of its hand-written logic.",
            "Same inputs. Same yardstick. Measured head to head.",
            "Also measure what each approach costs, and whether repeated "
            "runs agree with each other.",
        ],
        "step_two": [
            "Only once step one is measured, extend to things Caruca was "
            "not built to cover.",
            "Destructive commands. Richer test conditions. Commands with "
            "poor documentation.",
            "Surveyed and sequenced, so we know what is there. Not started.",
        ],
        "banner": "We are not attempting step two yet. Step one has to work and be measured first.",
        "sources": ["roadmap", "master_idea"],
        "notes": (
            "This is the anchor slide of the whole deck. Say the banner line out "
            "loud rather than letting them read it. William's guidance was "
            "explicitly not to over-engineer the first version, and this slide is "
            "the direct answer to that. Everything ambitious later in the deck is "
            "parked in the right-hand column on purpose."
        ),
    },

    # ---------------------------------------------------------- comparison
    {
        "kind": "image", "audience": "both",
        "title": "How the pieces fit together",
        "lead": "Caruca's existing machinery is reused unchanged. The new work sits alongside it.",
        "image": "002_architecture_widescreen.png",
        "sources": ["system_architecture"],
        "notes": (
            "Three columns, left to right. The left is Caruca as it exists and it "
            "does not change. The middle is step one, which swaps only the first "
            "box for a single prompt and then reuses the same comparison yardstick. "
            "The right is step two, drawn dashed because it is later. Point out "
            "that we reuse Caruca's own sandbox, its annotator, and its verified "
            "answers rather than rebuilding any of them."
        ),
    },
    {
        "kind": "bullets", "audience": "both", "step": 1,
        "title": "Step one is deliberately simple",
        "lead": "The first version is not engineered to win. That is the point.",
        "bullets": [
            ("One prompt. No tools, no retries, no tuning",
             "Give the model a command's manual page, ask for a description of its options, stop there."),
            ("This follows William's guidance directly",
             "The goal is a fair control, not the best possible specification generator."),
            ("A weak first version makes the comparison more honest, not less",
             "If a plain prompt already does well, that is a real finding. If it does badly, that measures "
             "what Caruca's engineering actually buys."),
            ("Tuning it later is a separate experiment",
             "Mixing the two would make it impossible to say which part produced the result."),
        ],
        "sources": ["master_idea", "component_functionality"],
        "notes": (
            "If either of them pushes on 'why not make it better', the answer is "
            "the third bullet: a deliberately plain baseline is what makes the "
            "comparison interpretable. An optimised prompt would confound the "
            "result with prompt engineering effort."
        ),
    },

    # ---------------------------------------------------------- findings
    {
        "kind": "findings", "audience": "both",
        "kicker": "What the review turned up",
        "title": "Two things nobody has measured yet",
        "lead": "Both are straightforward to add, and both produce numbers that do not currently exist.",
        "findings": [
            ("The paper reports how long Caruca takes to run, but never what its "
             "AI step costs in tokens or money. No cost figure for the model exists.",
             "We measure tokens, cost and time on both sides, and report them. "
             "This is a number the original work never published."),
            ("Each command's description was generated once. Language models vary "
             "between runs, so run-to-run consistency was never tested.",
             "We generate repeatedly and report the spread, for the existing system "
             "as well as ours. Variation is itself a result worth reporting."),
        ],
        "sources": ["caruca_white_paper", "roadmap"],
        "notes": (
            "Frame these as gaps we can fill, not as oversights. Both are genuinely "
            "additive: neither changes any claim the paper makes, and both "
            "strengthen a resubmission. Michael may already know about the cost "
            "one; the repeatability one usually lands harder."
        ),
    },
    {
        "kind": "findings", "audience": "both",
        "kicker": "What the review turned up",
        "title": "Two things that affect the plan directly",
        "findings": [
            ("The published size of Caruca is 6,520 lines. Measuring the current "
             "code, roughly 3,130 of those lines are machine-generated command "
             "descriptions rather than hand-written logic.",
             "It changes what a claim about replacing hand-written code can honestly "
             "say: the real figure is about 3,456 lines. Michael, I would like you "
             "to confirm or correct this reading."),
            ("The step that calls the AI model cannot currently run. A library it "
             "depends on changed and removed the functions it used.",
             "Repairing it is the first task, and it is also a precondition for "
             "measuring cost at all. Small, well understood, already scoped."),
        ],
        "sources": ["roadmap", "caruca_white_paper"],
        "notes": (
            "The first one is the item I most want Michael to weigh in on. It is my "
            "interpretation from measuring the checkout, not something the paper "
            "states, and it materially affects what we can claim later. Ask him "
            "directly. The second is routine maintenance, mentioned only because it "
            "sits on the critical path."
        ),
    },

    # ---------------------------------------------------------- gaps
    {
        "kind": "bullets", "audience": "both", "step": 2,
        "kicker": "Step two material",
        "title": "Where testing could reach further",
        "lead": "Conditions the current test generator does not produce. All step two, none of it started.",
        "bullets": [
            ("Commands that compare two files never get related inputs",
             "Test files are generated independently, so tools like diff and comm are never given identical "
             "or overlapping content."),
            ("Directory tests never go deeper than one level",
             "Recursive options are exercised, but never against a tree deep enough to tell recursion from "
             "handling a single file."),
            ("File permissions are never varied",
             "Commands whose whole purpose is permissions have no test that changes them."),
            ("Empty files are never used",
             "A common real-world edge case, and a frequent source of bugs, is absent from the fixtures."),
        ],
        "sources": ["evaluation_gaps"],
        "notes": (
            "These four are drawn from nine issues the authors do not appear to "
            "discuss anywhere. I picked the ones with the clearest behavioural "
            "consequence. The full list, plus everything the authors already "
            "acknowledge themselves, is in the appendix. Stress that this is "
            "step-two material: it is surveyed so we know what is there, not "
            "queued up to start."
        ),
    },
    {
        "kind": "cards", "audience": "both", "step": 2, "muted": True,
        "kicker": "Step two material",
        "title": "What extending would actually mean",
        "lead": "Concretely, three groups of capability. Later, not now.",
        "cards": [
            ("Run destructive commands safely",
             "Commands that delete or overwrite cannot be tested without somewhere "
             "isolated to run them. This needs a technology choice and a hands-on "
             "test first."),
            ("Richer test conditions",
             "Symbolic links, file permissions, deeper directory trees, empty files, "
             "environment variables, related multi-file inputs, and pipes."),
            ("Commands with poor documentation",
             "Where no useful manual page exists, inspect the program itself instead: "
             "its help text, its format, its structure."),
        ],
        "sources": ["component_functionality", "evaluation_gaps"],
        "notes": (
            "Keep this brief. Its job is to show the extension path is concrete "
            "rather than hand-waved, while the muted styling and the step-two marker "
            "keep signalling that none of it is starting now."
        ),
    },

    # ---------------------------------------------------------- restraint
    {
        "kind": "cards", "audience": "both", "muted": True,
        "title": "What we are deliberately not doing",
        "lead": "Scope discipline, stated plainly.",
        "cards": [
            ("Not rebuilding Caruca with AI agents",
             "Replacing the whole pipeline with agent-driven reasoning is a separate, "
             "much larger experiment. Deferred until the simple comparison exists."),
            ("Not tuning the prompt to win",
             "The first version stays plain on purpose. Optimising it is a different "
             "experiment and would confound this one."),
            ("Not rewriting Caruca's own code",
             "Its sandbox, its annotator, its verified answers and its comparison "
             "script are reused as they are. One small repair is the only change."),
        ],
        "sources": ["roadmap", "master_idea"],
        "notes": (
            "This slide exists to answer the unspoken question of whether I am "
            "trying to do too much. Saying the boundary out loud is more convincing "
            "than hoping they infer it. If they push on any of the three, the answer "
            "is the same: it is deferred, not dismissed."
        ),
    },

    # ---------------------------------------------------------- plan
    {
        "kind": "cards", "audience": "both", "step": 1, "numbered": True,
        "title": "What gets built first",
        "lead": "Three tasks. None of them needs the sandbox or any undecided technology.",
        "cards": [
            ("Repair and measure the existing AI step",
             "Fix the library problem, then record tokens, cost, time and model for "
             "every run. Produces a cost figure that does not exist today."),
            ("Build the simple prompt version",
             "One prompt, manual page in, description out, in the same format Caruca "
             "already uses so the existing comparison tools work unchanged."),
            ("Compare them head to head",
             "Against the verified answers already in the repository, with repeat runs "
             "to measure consistency and a summary that can go straight into a paper."),
        ],
        "sources": ["roadmap"],
        "notes": (
            "Emphasise that all three run on my machine today. Nothing here waits on "
            "the sandbox technology decision, which is the biggest open unknown. That "
            "sequencing is deliberate: the highest-uncertainty piece blocks the least "
            "work."
        ),
    },
    {
        "kind": "bullets", "audience": "both",
        "title": "How we will know if it worked",
        "lead": "Six measures. The first four decide whether the approach is viable at all.",
        "bullets": [
            ("Correctness — does it produce the same descriptions?",
             "Compared against verified answers already in the repository, using Caruca's own method."),
            ("Cost and speed — what does each approach cost per command?",
             "Tokens, money and time, recorded for both."),
            ("Coverage — how many commands and behaviours are handled?",
             "Including how far step two eventually reaches beyond today's limits."),
            ("Consistency — do repeated runs agree?",
             "Reported as a spread, not a single number."),
            ("Overall change — one headline figure per measure above", None),
            ("Hand-written code replaced — with an important caveat",
             "Mostly not measurable in step one, since we replace one step and reuse the rest. See appendix."),
        ],
        "sources": ["master_idea", "data_telemetry_schema"],
        "notes": (
            "Do not dwell on all six. The last one carries a real caveat: in step one "
            "the model replaces only the description step, so any claim about "
            "replacing hand-written code would be narrow. I would rather say that "
            "now than have it challenged in review later. Question three at the end "
            "asks them directly what to do about it."
        ),
    },

    # ---------------------------------------------------------- questions
    {
        "kind": "questions", "audience": "both",
        "title": "Four questions for you",
        "lead": "These are genuinely open. Your answers change what I build.",
        "questions": [
            ("How should we safely run destructive commands?",
             "Three candidate technologies, with different trade-offs between isolation strength and "
             "keeping the system-call visibility Caruca depends on.",
             "spend a day testing the strongest option before committing."),
            ("Is measuring replaced hand-written code realistic yet?",
             "In step one the model replaces one step and reuses everything else, so the honest figure is "
             "narrow. The broad version needs the deferred agent rebuild.",
             "report the narrow figure, state the limit plainly, revisit later."),
            ("How many commands should the first comparison cover?",
             "There are 121 with verified answers available. All of them is thorough but slow to first "
             "result; a handful proves the approach faster.",
             "start with about ten, covering different command shapes, then widen."),
            ("Michael: is my reading of the code-size figure right?",
             "I measured roughly 3,130 of the 6,520 lines as machine-generated rather than hand-written. "
             "It affects what we can claim later.",
             "confirm before any of it appears in writing."),
        ],
        "sources": ["roadmap", "evaluation_gaps"],
        "notes": (
            "This is the part of the meeting I actually need. Give them room. "
            "Question one is the biggest unknown and blocks step two. Question four "
            "is specifically for Michael and takes him ten seconds to answer. Each "
            "one has my current lean attached so the conversation starts from a "
            "position rather than a blank page."
        ),
    },
    {
        "kind": "closing", "audience": "both",
        "headline": "Repair the AI step, then measure it",
        "body": [
            "It is small, well understood, and produces a cost figure that has never been published.",
            "Everything else in step one follows from it.",
            "I will come back with the first head-to-head numbers rather than another plan.",
        ],
        "ask": "Can we agree a checkpoint once the first comparison runs?",
        "notes": (
            "Close by proposing an actual next meeting rather than leaving it vague. "
            "The promise to return with numbers instead of more planning is the point: "
            "this should be the last planning conversation."
        ),
    },
]

APPENDIX = [
    {
        "kind": "table", "audience": "both",
        "title": "Appendix: what is in here",
        "rows": [
            ("Gaps the authors already note", "Issues the paper itself acknowledges, kept separate from new findings"),
            ("Remaining new gaps", "The rest of the issues not raised in the main deck"),
            ("The six measures in full", "Complete wording, as recorded in the planning documents"),
            ("Build order in detail", "All six phases, with what each one makes possible"),
            ("How correctness is compared", "Three different methods, and why they are not interchangeable"),
            ("Rough effort estimate", "Sizing for step one, deliberately kept out of the main deck"),
            ("Source documents", "Everything cited, and where to find it"),
        ],
        "row_h": 0.6,
    },
    {
        "kind": "bullets", "audience": "both",
        "kicker": "Appendix",
        "title": "Gaps the authors already acknowledge",
        "lead": "Raised by the paper itself. Included for completeness, and to keep them separate from new findings.",
        "bullets": [
            ("Symbolic links are not generated",
             "Noted in the paper as a possible extension."),
            ("Pipes are not tested",
             "Also noted as a possible extension. Relevant because the main consumer optimises pipelines."),
            ("Numbers used in tests are only -1, 0 and 1",
             "Stated openly in the paper. Commands sensitive to magnitude are only tested at the smallest values."),
            ("Environment variables are never varied",
             "One of three limitations the paper lists explicitly."),
            ("The headline coverage figure combines strong and weak matching",
             "The paper is transparent about this; the combined number is simply the one most likely to be quoted alone."),
        ],
        "sources": ["evaluation_gaps", "caruca_white_paper"],
    },
    {
        "kind": "bullets", "audience": "both",
        "kicker": "Appendix",
        "title": "Remaining new gaps, not shown earlier",
        "lead": "The rest of the issues that do not appear to be discussed in the paper.",
        "bullets": [
            ("Parallel safety is inferred from sequential runs",
             "Commands are never actually run at the same time, which is how the main consumer would run them."),
            ("The tooling is Linux-only, while the motivation cites other systems",
             "The paper motivates the problem partly with differences across systems, but tests only on Linux."),
            ("Real-world usage is sampled only from shell scripts on GitHub",
             "Command usage in build files, container definitions and scheduled jobs is not represented."),
            ("Test file contents cover five fixed types",
             "No spreadsheet, document or archive formats, and filenames rarely carry meaningful extensions."),
        ],
        "sources": ["evaluation_gaps"],
    },
    {
        "kind": "table", "audience": "both",
        "kicker": "Appendix",
        "title": "How correctness gets compared",
        "lead": "Three different methods. They measure different things and are not interchangeable.",
        "rows": [
            ("Description comparison",
             "Option-by-option diff against verified answers. What step one uses. Reuses Caruca's own script."),
            ("Specification comparison",
             "Compares the final specifications after running the commands. Heavier; needs the sandbox."),
            ("Running real test suites",
             "What the paper's own headline quality figures use: the consuming tools' actual tests are re-run. "
             "Heaviest, and deferred."),
            ("Why it matters",
             "Reporting a lighter method's number as if it were the heaviest method's would not survive review."),
        ],
        "row_h": 0.85,
        "sources": ["roadmap", "component_functionality"],
    },
    {
        "kind": "bullets", "audience": "both",
        "kicker": "Appendix",
        "title": "Rough effort estimate for step one",
        "lead": "Kept out of the main deck deliberately: these are estimates before any code exists.",
        "bullets": [
            ("Repair and measure the existing AI step — a few days",
             "Mostly a library migration with known replacements, plus recording what each run costs."),
            ("Build the simple prompt version — a few days",
             "Small by design. Most of the effort is matching the existing output format exactly."),
            ("Compare them head to head — one to two weeks",
             "Includes fixing a counting bug in the existing comparison script and running repeats."),
            ("Biggest uncertainty is not in step one at all",
             "It is the choice of technology for safely running destructive commands, which step one avoids."),
        ],
        "sources": ["roadmap"],
    },
    {
        "kind": "table", "audience": "both",
        "kicker": "Appendix",
        "title": "Source documents",
        "lead": "Supplied as PDFs alongside this deck.",
        "rows": [
            ("master_idea", "Goal, stakeholders, the six measures, and the components to build"),
            ("system_architecture", "How the existing and new pieces fit together, with the full diagram"),
            ("roadmap", "Six phases, what each unlocks, and what done means for each"),
            ("evaluation_gaps", "All fourteen opportunities to broaden testing, with sources"),
            ("component_functionality", "What each component takes in and produces, and its commands"),
            ("data_telemetry_schema", "What gets recorded for every run, and how results are stored"),
            ("caruca_white_paper", "The original paper, for reference"),
        ],
        "row_h": 0.56,
    },
]

MICHAEL_EXTRA = [
    {
        "kind": "bullets", "audience": "michael",
        "kicker": "Detail",
        "title": "What we reuse from Caruca, unchanged",
        "lead": "The new work attaches at existing seams rather than replacing anything.",
        "bullets": [
            ("The boundary between running and interpreting stays as it is",
             "Recorded behaviour is written to a file, so running can happen on a capable host while "
             "interpretation happens anywhere. We keep that seam and attach to it."),
            ("The annotator is reused as-is",
             "Step one does not touch it. Step two would need new interaction types for links and "
             "permissions, which is scoped but not started."),
            ("The verified answers and comparison script are reused",
             "121 curated command descriptions and the option-by-option diff. Roughly 80 hours of graduate "
             "student annotation reused rather than recreated."),
            ("Caruca is wrapped as a separate program, not imported",
             "It needs a newer Python than this machine has, and running commands needs a different host. "
             "A process boundary keeps both workable."),
        ],
        "sources": ["system_architecture", "component_functionality"],
        "notes": (
            "This slide is for Michael only. Its purpose is to make clear that "
            "nothing of his is being torn out. If he has concerns about the "
            "annotator changes in step two, this is the natural place for that "
            "conversation."
        ),
    },
    {
        "kind": "bullets", "audience": "michael",
        "kicker": "Detail",
        "title": "One thing to fix in the comparison script",
        "lead": "It affects one reported number, not the headline count.",
        "bullets": [
            ("The per-command match count is sound",
             "A command counts as matching only when every option matches. That logic is correct and we use "
             "it unchanged."),
            ("The percentage figure divides two different units",
             "Mismatches are counted per option, but the divisor counts data fields, so the resulting "
             "percentage is not option-level accuracy."),
            ("Consequence: it does not reproduce the paper's option-level figure",
             "The per-command count is unaffected, which is why step one leads with that one."),
            ("Fix is small and scoped to our copy",
             "Correct the divisor, and record which method produced every number we report."),
        ],
        "sources": ["roadmap"],
        "notes": (
            "Raise this carefully and factually. It does not affect the paper's "
            "headline claim, which is the per-command figure. Ask whether he wants "
            "the fix upstreamed or kept local to this project."
        ),
    },
]

WILLIAM_EXTRA = [
    {
        "kind": "bullets", "audience": "william",
        "kicker": "Detail",
        "title": "Why this comparison is worth running",
        "lead": "The result is useful whichever way it comes out.",
        "bullets": [
            ("If the plain prompt does well, that is a substantive finding",
             "It would suggest a large hand-built pipeline is not required for this class of problem."),
            ("If it does badly, that measures what the engineering buys",
             "Which is equally publishable, and strengthens rather than weakens the original work."),
            ("Either way we produce numbers that do not exist today",
             "Cost per command, and whether repeated runs agree. Neither has been reported for this problem."),
            ("The design keeps the comparison interpretable",
             "One variable changes at a time: same inputs, same yardstick, deliberately plain baseline."),
        ],
        "sources": ["master_idea", "roadmap"],
        "notes": (
            "This is aimed at William's methodological instincts. The last bullet "
            "is the one he is most likely to probe: be ready to talk about what is "
            "held constant and what is allowed to vary."
        ),
    },
]


# ---------------------------------------------------------------- assembly

def build(audience_key, audience_label, out_path):
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)

    slide_title(prs, audience_label)

    main = [s for s in SLIDES if s["audience"] in ("both", audience_key)]
    extra = MICHAEL_EXTRA if audience_key == "michael" else WILLIAM_EXTRA
    extra = [s for s in extra if s["audience"] in ("both", audience_key)]

    # Audience-specific detail slides sit just before the questions.
    q_index = next(i for i, s in enumerate(main) if s["kind"] == "questions")
    ordered = main[:q_index] + extra + main[q_index:]

    number = 2
    for spec in ordered:
        BUILDERS[spec["kind"]](prs, spec, number)
        number += 1

    slide_section(prs, "Appendix", "Supporting detail, for reading afterwards", number)
    number += 1
    for spec in APPENDIX:
        BUILDERS[spec["kind"]](prs, spec, number)
        number += 1

    prs.save(str(out_path))
    return len(prs.slides.__iter__.__self__._sldIdLst), out_path


if __name__ == "__main__":
    for key, label, fname in [
        ("michael", "Prof. Michael Greenberg", "caruca_v2_status_greenberg.pptx"),
        ("william", "Prof. William Eiers", "caruca_v2_status_eiers.pptx"),
    ]:
        count, path = build(key, label, HERE / fname)
        print(f"{path.name}: {count} slides")
