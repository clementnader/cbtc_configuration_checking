#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

if sys.platform == "win32" and ("SHELL" not in os.environ.keys() and "PYCHARM_HOSTED" not in os.environ.keys()):
    # For Windows when not using git-bash or pycharm
    os.system("color")


def csi_seq(color_int):
    # CSI Control Sequence Introducer
    escape_seq = f"\x1B["  # "\x1B" is equivalent to "\033" or "\27" and gives ESC
    if color_int == -1:  # end
        return f"{escape_seq}0m"
    else:
        return f"{escape_seq}38;5;{color_int}m"


class Color:
    end = csi_seq(-1)

    black = csi_seq(0)
    dark_red = csi_seq(1)
    dark_green = csi_seq(2)
    dark_yellow = csi_seq(3)
    dark_blue = csi_seq(4)
    dark_magenta = csi_seq(5)
    purple = csi_seq(5)
    dark_cyan = csi_seq(6)
    light_grey = csi_seq(7)

    dark_grey = csi_seq(8)
    red = csi_seq(9)
    light_green = csi_seq(10)
    green = csi_seq(10)
    yellow = csi_seq(11)
    blue = csi_seq(12)
    magenta = csi_seq(13)
    cyan = csi_seq(14)
    light_blue = csi_seq(14)
    white = csi_seq(15)


def bg_color(color_seq: str):
    return color_seq.replace("[38", "[48")
