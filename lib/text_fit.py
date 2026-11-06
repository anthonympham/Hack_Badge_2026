"""Auto-fit text rendering helper.

Given a block of text and a target box, creates an LVGL label that wraps
to the box width and picks the largest available font whose wrapped
height still fits inside the box. Falls back to the smallest font (and
lets it overflow) if nothing fits.
"""

import lvgl

_BLACK = lvgl.color_hex(0x000000)

# Fonts confirmed present in this firmware build (see apps/schedule.py,
# the original apps/nametag.py), largest first.
_FONTS = [
    lvgl.font_montserrat_48,
    lvgl.font_montserrat_24,
    lvgl.font_montserrat_16,
    lvgl.font_montserrat_14,
]


def fit_label(parent, text: str, max_width: int, max_height: int):
    """Create a label under `parent` with `text`, auto-sized to fit the box."""
    label = lvgl.label(parent)
    label.set_width(max_width)
    # NOTE: untested on-device. lib/app_list.py has this exact call
    # commented out — if LABEL_LONG_MODE.WRAP errors, try LABEL_LONG.WRAP
    # instead, or check `dir(lvgl)` at the REPL for the real enum name.
    label.set_long_mode(lvgl.LABEL_LONG_MODE.WRAP)
    label.set_style_text_color(_BLACK, 0)
    label.set_style_text_align(lvgl.TEXT_ALIGN.CENTER, 0)
    label.set_text(text)

    for font in _FONTS:
        label.set_style_text_font(font, 0)
        label.update_layout()
        if label.get_height() <= max_height:
            break
    return label
