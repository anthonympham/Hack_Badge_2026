"""Nametag app"""

import lvgl

from apps.base_app import BaseApp
from data.user_config import NAME_TEXT
from lib.epd import display, display_height
from lib.led_bar import leds
from lib.text_fit import fit_label

_WHITE = lvgl.color_hex(0xFFFFFF)
# White name band on hello_i_am_blank.png. Center the plate there.
_NAME_TOP = 221
_NAME_BOTTOM = 557
_NAME_WIDTH = 880  # margin inside the 960px-wide band
_NAME_HEIGHT = _NAME_BOTTOM - _NAME_TOP
_NAME_DY = (_NAME_TOP + _NAME_BOTTOM) // 2 - display_height // 2


class NametagApp(BaseApp):
    def __init__(self, name: str | None = None) -> None:
        self.name = "Nametag"
        self.sleep_ms = 100
        self.launched = False

    def run(self):
        if self.launched:
            leds.fill((0, 1, 1))
            display.draw_png("/data/graphics/hello_i_am_blank.png")

            scr = lvgl.obj()
            scr.remove_style_all()
            scr.set_size(lvgl.pct(100), lvgl.pct(100))
            scr.set_style_bg_opa(lvgl.OPA.TRANSP, 0)

            plate = lvgl.obj(scr)
            plate.remove_style_all()
            plate.set_size(_NAME_WIDTH, lvgl.SIZE_CONTENT)
            plate.align(lvgl.ALIGN.CENTER, 0, _NAME_DY)
            plate.set_style_bg_color(_WHITE, 0)
            plate.set_style_bg_opa(lvgl.OPA.COVER, 0)
            plate.set_style_pad_all(8, 0)

            fit_label(plate, NAME_TEXT, _NAME_WIDTH - 16, _NAME_HEIGHT - 16)

            lvgl.screen_load(scr)
            scr.update_layout()
            # screen_load dirties the whole panel. Keep the PNG everywhere else.
            display.lv_display.inv_p = 0
            plate.invalidate()
            lvgl.refr_now(display.lv_display)
            display.update()
            leds.fill((0, 1, 0))
