#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..cctool_oo_schema import *
from .load_bop import *


__all__ = ["convert_switch_pos_to_ixl"]


def convert_switch_pos_to_ixl(sw_name: str, left_or_right: str) -> str:
    switch_bop_dict = load_dc_bop()
    reverse_equals_right = switch_bop_dict[sw_name]
    if left_or_right.upper().strip() == Switch_Position.GAUCHE:
        if reverse_equals_right:
            return "N"  # Normal
        else:
            return "R"  # Reverse
    if left_or_right.upper().strip() == Switch_Position.DROITE:
        if reverse_equals_right:
            return "R"  # Reverse
        else:
            return "N"  # Normal
