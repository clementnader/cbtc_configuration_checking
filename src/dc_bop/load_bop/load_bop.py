#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .load_xl import load_dc_bop_wb


LOADED_SWITCH_DIRS = dict()

START_LINE = 3

SW_NAME_COL = 2
REVERSE_EQUALS_RIGHT_COL = 3
SW_NAME_2_COL = 4
REVERSE_EQUALS_RIGHT_2_COL = 5


def load_bop() -> dict:
    global LOADED_SWITCH_DIRS
    if not LOADED_SWITCH_DIRS:
        wb = load_dc_bop_wb()
        sw_sh = wb.sheet_by_name("SWITCH")
        LOADED_SWITCH_DIRS = get_switch_bop(sw_sh)
    return LOADED_SWITCH_DIRS


def get_switch_bop(sw_sh: xlrd.sheet) -> dict:
    if sw_sh.nrows == 0:
        return {}

    bop_dict = dict()
    for line in range(START_LINE, sw_sh.nrows+1):
        sw_name = get_xlrd_value(sw_sh, line, SW_NAME_COL)
        if sw_name:
            reverse_equals_right = convert_sw_pos(get_xlrd_value(sw_sh, line, REVERSE_EQUALS_RIGHT_COL))
            bop_dict[sw_name] = reverse_equals_right

        sw_name2 = get_xlrd_value(sw_sh, line, SW_NAME_2_COL)
        if sw_name2:
            reverse_equals_right2 = convert_sw_pos(get_xlrd_value(sw_sh, line, REVERSE_EQUALS_RIGHT_2_COL))
            bop_dict[sw_name2] = reverse_equals_right2
    return bop_dict


def convert_sw_pos(reverse_equals_right: str):
    if reverse_equals_right.upper().strip() == "N":
        return False
    if reverse_equals_right.upper().strip() == "O":
        return True
