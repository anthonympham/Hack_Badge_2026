"""Auto-fit text rendering helper.

Given a block of text and a target box, word-wraps it in plain Python
(baking literal "\\n" line breaks into the string) and picks the largest
available font whose wrapped height still fits inside the box. Falls back
to the smallest font (and lets it overflow) if nothing fits.

Wrapping is done manually instead of via LVGL's long_mode/auto-wrap so we
don't depend on an LVGL label API whose exact Python binding name isn't
confirmed on this firmware build, and without relying on the `textwrap`
stdlib module, which may not be present in this MicroPython build.
"""

import lvgl

_BLACK = lvgl.color_hex(0x000000)

# (font, approx pixel height) confirmed present in this firmware build
# (see apps/schedule.py, the original apps/nametag.py), largest first.
_FONTS = [
    (lvgl.font_montserrat_48, 48),
    (lvgl.font_montserrat_24, 24),
    (lvgl.font_montserrat_16, 16),
    (lvgl.font_montserrat_14, 14),
]

# Conservative average character width as a fraction of font pixel size,
# for a proportional sans-serif font. Errs narrow (more line breaks than
# strictly necessary) rather than letting a line overflow max_width.
_AVG_CHAR_WIDTH_RATIO = 0.6


def _wrap(text: str, max_chars: int) -> str:
    """Greedy word-wrap. Preserves existing blank lines/paragraph breaks."""
    max_chars = max(1, max_chars)
    lines = []
    for paragraph in text.split("\n"):
        current = ""
        for word in paragraph.split(" "):
            candidate = word if not current else current + " " + word
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        lines.append(current)
    return "\n".join(lines)


def fit_label(parent, text: str, max_width: int, max_height: int):
    """Create a label under `parent` with `text`, auto-sized to fit the box."""
    label = lvgl.label(parent)
    label.set_width(max_width)
    label.set_style_text_color(_BLACK, 0)
    label.set_style_text_align(lvgl.TEXT_ALIGN.CENTER, 0)

    for font, px in _FONTS:
        max_chars = int(max_width / (px * _AVG_CHAR_WIDTH_RATIO))
        label.set_style_text_font(font, 0)
        label.set_text(_wrap(text, max_chars))
        label.update_layout()
        if label.get_height() <= max_height:
            break
    return label
