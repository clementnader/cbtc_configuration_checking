#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .load_bop import *


def convert_switch_pos_to_ixl(sw_name: str, left_or_right: str) -> str:
    switch_bop_dict = load_bop()
    reverse_equals_right = switch_bop_dict[sw_name]
    if left_or_right.upper().strip() == "GAUCHE":
        if reverse_equals_right:
            return "N"  # Normal
        else:
            return "R"  # Reverse
    if left_or_right.upper().strip() == "DROITE":
        if reverse_equals_right:
            return "R"  # Reverse
        else:
            return "N"  # Normal
