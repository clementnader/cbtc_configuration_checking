#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
from ..common_utils import *


__all__ = ["Color", "csi_bg_color", "remove_colors", "print_all_colors", "print_named_colors", "test_rainbow",
           "move_up", "move_down", "move_left", "move_right", "NBSP"]


if sys.platform == "win32":  # for Windows
    os.system("color")


ESCAPE_SEQ = "\x1B["  # "\x1B" is equivalent to "\033" or "\27" and gives ESC
NBSP = "\xA0"  # non-breaking space


# CSI: Control Sequence Introducer
def csi_seq(n: Union[int, str]) -> str:
    return f"{ESCAPE_SEQ}{n}m"


def csi_color_seq(color_int: int) -> str:
    return csi_seq(f"38;5;{color_int}")


def csi_bg_color(color_seq: str) -> str:
    return color_seq.replace("[38", "[48")


def duplicate_each_elem(i_list: list, nb_duplicates: int = 2) -> list:
    dup_list = list()
    for elem in i_list:
        for _ in range(nb_duplicates):
            dup_list.append(elem)
    return dup_list


class Color:
    """ANSI escape code
    Check https://en.wikipedia.org/wiki/ANSI_escape_code for more info"""
    # Reset
    reset = csi_seq(0)

    # Colors
    default = csi_color_seq(250)
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
    grey_blue = csi_color_seq(110)

    dark_green = csi_color_seq(22)
    dark_green2 = csi_color_seq(28)
    forest_green = csi_color_seq(29)
    green = csi_color_seq(76)
    green2 = csi_color_seq(40)
    mint_green = csi_color_seq(35)
    classic_dark_green = csi_color_seq(2)
    classic_light_green = csi_color_seq(10)
    vivid_green = csi_color_seq(82)
    vivid_green2 = csi_color_seq(118)
    vivid_green3 = csi_color_seq(119)
    light_green = csi_color_seq(154)
    pale_green = csi_color_seq(120)

    dark_red = csi_color_seq(88)
    red = csi_color_seq(160)
    light_red = csi_color_seq(9)
    standard_red = csi_color_seq(1)
    vivid_red = csi_color_seq(196)

    purple = csi_color_seq(91)
    dark_magenta = csi_color_seq(89)
    magenta = csi_color_seq(163)
    pink = csi_color_seq(213)
    pale_pink = csi_color_seq(225)

    orange_red = csi_color_seq(202)
    dark_orange = csi_color_seq(172)
    orange = csi_color_seq(208)
    light_orange = csi_color_seq(214)
    dark_brown = csi_color_seq(94)
    brown = csi_color_seq(130)
    light_brown = csi_color_seq(172)
    dark_yellow = csi_color_seq(3)
    yellow = csi_color_seq(220)
    yellow2 = csi_color_seq(11)
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
    reverse = csi_seq(7)

    # Rainbow
    rainbow = [csi_color_seq(_i) for _i in [
        52,  88,  124, 160, 196,  # red
        202, 208, 214, 220, 226,  # orange to yellow
        190, 154, 118, 82,  46,   # yellow to green
        47,  48,  49,  50,  51,   # green to blue
        45,  39,  33,  27,        # blue
        57,  56,  55,  54,  53,   # blue to purple
    ]]
    progress_pride = duplicate_each_elem([csi_color_seq(_i) for _i in [
        15, 213, 51, 95, 0,
        # white, pink, cyan, brown, black
    ]], 3) + duplicate_each_elem([csi_color_seq(_i) for _i in [
        196, 208, 220, 46, 27, 90,
        # red, orange, yellow, green, blue, purple
    ]], 3)


def move_up(nb_line: int):  # does not work in PyCharm interface
    return f"{ESCAPE_SEQ}{nb_line}A"


def move_down(nb_line: int):
    return f"{ESCAPE_SEQ}{nb_line}B"


def move_right(nb_char: int):
    return f"{ESCAPE_SEQ}{nb_char}C"


def move_left(nb_char: int):
    return f"{ESCAPE_SEQ}{nb_char}D"


def test_rainbow(progress_pride: bool = False):
    full_cell_char = "█"
    for color in (Color.progress_pride if progress_pride else Color.rainbow):
        print(color + full_cell_char + Color.reset, end="")
    print()


def print_all_colors():
    max_length = 164

    cur_len = 68
    start_len = (max_length-cur_len) // 2
    print(" " * start_len + "-"*68)
    print(" " * start_len + f"{'Standard colors':^32}    {'High-intensity colors':^32}")
    print(" " * start_len, end="")
    for i in range(16):
        print(f"{csi_color_seq(i)}{i:>3}{Color.reset}", end=" ")
        if i % 8 == -1 % 8:
            print(end="    ")

    print("\n\n" + "-"*164)
    print(f"{'216 colors':^164}")
    for i in range(16, 216+16):
        print(f"{csi_color_seq(i)}{i:>3}{Color.reset}", end=" ")
        if (i-16) % 36 == -1 % 36:
            print()
        elif (i-16) % 6 == -1 % 6:
            print(end="    ")

    cur_len = 96
    start_len = (max_length-cur_len) // 2
    print("\n\n" + " " * start_len + "-"*96)
    print(" " * start_len + f"{'Grayscale colors':^96}")
    print(" " * start_len, end="")
    for i in range(216+16, 256):
        print(f"{csi_color_seq(i)}{i:>3}{Color.reset}", end=" ")

    print("\n")


def print_named_colors():
    for name, val in get_class_attr_dict(Color).items():
        if isinstance(val, str):
            print(f" · {val}{name}{Color.reset}")


def remove_colors(string: str):
    res_string = string.replace(NBSP, "")
    res_string = re.sub("\\".join(c for c in ESCAPE_SEQ) + r".*?[mABCD]", r"", res_string)
    # the '?' is to remove the greedy behavior of the '*' quantifier
    # in order to match with the smallest text inside the brackets, if there is more than one pair of brackets
    return res_string
