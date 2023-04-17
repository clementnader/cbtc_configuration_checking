#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from .load_xl import load_dc_bop_wb

LOADED_SWITCH_DIRS = dict()

START_LINE = 3

SW_NAME = 'A'
REVERSE_EQUALS_RIGHT = 'C'


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
        sw_name = get_xlrd_value(sw_sh, line, SW_NAME)
        reverse_equals_right = convert_sw_pos(get_xlrd_value(sw_sh, line, REVERSE_EQUALS_RIGHT))
        bop_dict[sw_name] = reverse_equals_right
    return bop_dict


def convert_sw_pos(reverse_equals_right: str):
    if reverse_equals_right.upper().strip() == "N":
        return False
    if reverse_equals_right.upper().strip() == "O":
        return True


def get_xlrd_value(sh: xlrd.sheet, line: int, col: str) -> str:
    xlrd_line = get_xlrd_line(line)
    xlrd_col = get_xlrd_column(col)
    try:
        cell_value = sh.cell_value(xlrd_line, xlrd_col)
    except IndexError:
        cell_value = None
    return cell_value
