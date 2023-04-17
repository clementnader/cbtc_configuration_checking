#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

if sys.platform == "win32" and ("SHELL" not in os.environ.keys() and "PYCHARM_HOSTED" not in os.environ.keys()):
    # For Windows when not using git-bash or pycharm
    os.system("color")


ESCAPE_SEQ = f"\x1B["  # "\x1B" is equivalent to "\033" or "\27" and gives ESC


def csi_seq(n):
    # CSI Control Sequence Introducer
    return f"{ESCAPE_SEQ}{n}m"


def csi_color_seq(color_int):
    # CSI Control Sequence Introducer
    return f"{ESCAPE_SEQ}38;5;{color_int}m"


def bg_color(color_seq: str):
    return color_seq.replace("[38", "[48")


def show_colors():
    for name, val in Color.__dict__.items():
        if not name.startswith("__") and not name.endswith("__") and isinstance(val, str):
            print(f" - {val}{name}{Color.reset}")


class Color:
    """ANSI escape code
Check https://en.wikipedia.org/wiki/ANSI_escape_code for more info"""
    # Reset
    reset = csi_seq(0)

    # Colors
    black = csi_color_seq(0)
    dark_grey = csi_color_seq(8)
    light_grey = csi_color_seq(7)
    white = csi_color_seq(15)

    dark_blue = csi_color_seq(21)
    blue = csi_color_seq(12)
    vivid_blue = csi_color_seq(45)
    light_blue = csi_color_seq(123)
    dark_turquoise = csi_color_seq(23)
    turquoise = csi_color_seq(30)
    cyan = csi_color_seq(51)

    dark_green = csi_color_seq(22)
    green = csi_color_seq(35)
    vivid_green = csi_color_seq(40)
    light_green = csi_color_seq(118)
    pale_green = csi_color_seq(120)

    dark_red = csi_color_seq(88)
    red = csi_color_seq(160)
    light_red = csi_color_seq(9)

    purple = csi_color_seq(91)
    dark_magenta = csi_color_seq(89)
    magenta = csi_color_seq(163)
    pink = csi_color_seq(213)
    pale_pink = csi_color_seq(225)

    dark_orange = csi_color_seq(202)
    orange = csi_color_seq(208)
    light_orange = csi_color_seq(214)
    brown = csi_color_seq(94)
    dark_yellow = csi_color_seq(3)
    yellow = csi_color_seq(220)
    light_yellow = csi_color_seq(228)
    beige = csi_color_seq(223)

    # SGR (Select Graphic Rendition)
    bold = csi_seq(1)
    no_bold = csi_seq(22)
    faint = csi_seq(2)
    no_faint = csi_seq(22)
    italic = csi_seq(3)
    no_italic = csi_seq(23)
    underline = csi_seq(4)
    no_underline = csi_seq(24)
