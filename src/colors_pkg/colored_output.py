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


class Color:
    """ANSI escape code"""
    # Reset
    reset = csi_seq(0)

    # Standard Colors
    black = csi_color_seq(0)
    dark_red = csi_color_seq(1)
    dark_green = csi_color_seq(2)
    dark_yellow = csi_color_seq(3)
    dark_blue = csi_color_seq(4)
    dark_magenta = csi_color_seq(5)
    purple = csi_color_seq(5)
    dark_cyan = csi_color_seq(6)
    light_grey = csi_color_seq(7)

    # High Intensity Colors
    dark_grey = csi_color_seq(8)
    red = csi_color_seq(9)
    light_green = csi_color_seq(10)
    green = csi_color_seq(10)
    yellow = csi_color_seq(11)
    blue = csi_color_seq(12)
    magenta = csi_color_seq(13)
    cyan = csi_color_seq(14)
    light_blue = csi_color_seq(14)
    white = csi_color_seq(15)

    # SGR (Select Graphic Rendition)
    bold = csi_seq(1)
    faint = csi_seq(2)
    italic = csi_seq(3)
    underline = csi_seq(4)
    no_bold = csi_seq(22)
    no_faint = csi_seq(22)
    no_italic = csi_seq(23)
    no_underline = csi_seq(24)


def bg_color(color_seq: str):
    return color_seq.replace("[38", "[48")
