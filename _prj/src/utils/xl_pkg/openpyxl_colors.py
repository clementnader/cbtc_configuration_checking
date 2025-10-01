#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common_utils import *


__all__ = ["XlFontColor", "XlBgColor", "get_xl_bg_dimmer_color"]


class XlFontColor:
    # status colors
    ko = "9C0006"
    ok = "006100"
    na = "9C5700"
    warning = "6E3700"
    # other colors
    dark_red = "9C0006"
    orange = "E97132"


class XlBgColor:
    # status colors
    ko = "FFC7CE"
    ok = "C6EFCE"
    na = "FFEB9C"
    warning = "FFCC99"
    # main colors
    yellow = "FFD050"
    light_yellow = "FFFFBB"
    green = "A0E0A0"
    light_green = "DDFFCC"
    blue = "9BC2E6"
    light_blue = "DDEBF7"
    # other colors
    orange = "FFAA77"
    light_orange = "FFCC99"
    light_pink = "FFCCCC"
    light_red = "FF9999"
    light_blue2 = "CCFFFF"
    light_blue3 = "99CCFF"
    light_pink2 = "FFCCDD"
    special_blue = "9999FF"
    special_yellow = "FFFF00"
    # grey
    grey = "BFBFBF"
    light_grey = "D9D9D9"
    # dc_sys colors
    dc_sys_yellow = "FFFF99"
    dc_sys_green = "CCFFCC"
    dc_sys_orange = "FFCC99"
    dc_sys_cyan = "CCFFFF"
    dc_sys_blue = "CCCCFF"
    dc_sys_pink = "FF99CC"


def get_xl_bg_dimmer_color(bg: str):
    xl_bg_colors_dict = get_class_attr_dict(XlBgColor)
    for key, val in xl_bg_colors_dict.items():
        if bg == val:
            if key.startswith("light_"):
                dimmer_key = key.removeprefix("light_")
                if dimmer_key in xl_bg_colors_dict:
                    return xl_bg_colors_dict[dimmer_key]
    return bg
