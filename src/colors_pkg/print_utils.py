#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .colored_output import *


def print_log(*args):
    print(Color.light_grey, end="")
    print(*args, end="")
    print(Color.reset)


def print_warning(*args):
    print(f"{bg_color(Color.dark_yellow)}{Color.black}Warning{Color.reset}{Color.dark_yellow}: ", end="")
    print(*args, end="")
    print(f"{Color.reset}\n")
