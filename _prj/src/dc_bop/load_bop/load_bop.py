#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ...cctool_oo_schema import *
from ...database_location import *


__all__ = ["load_dc_bop", "erase_dc_bop"]


LOADED_SWITCH_DIRECTIONS = dict()

SWITCH_SHEET = "SWITCH"

START_ROW = 3

SW_NAME_COL = 2
REVERSE_EQUALS_RIGHT_COL = 3
SW_NAME_2_COL = 4
REVERSE_EQUALS_RIGHT_2_COL = 5


def load_dc_bop() -> dict:
    global LOADED_SWITCH_DIRECTIONS
    if not LOADED_SWITCH_DIRECTIONS:
        if not DATABASE_LOCATION.dc_bop_addr:
            print_error(f"DC_BOP address is not filled.")
        print_log(f"Open DC_BOP file {Color.default}\"{DATABASE_LOCATION.dc_bop_addr}\"{Color.reset}.")
        wb = load_xlrd_wb(DATABASE_LOCATION.dc_bop_addr)
        sw_sheet = wb.sheet_by_name(SWITCH_SHEET)
        LOADED_SWITCH_DIRECTIONS = get_switch_bop(sw_sheet)
    return LOADED_SWITCH_DIRECTIONS


def get_switch_bop(switch_sheet: xlrd.sheet.Sheet) -> dict:
    if switch_sheet.nrows == 0:
        return {}

    bop_dict = dict()
    for row in range(START_ROW, switch_sheet.nrows + 1):
        sw_name = get_xlrd_value(switch_sheet, row, SW_NAME_COL)
        if sw_name:
            reverse_equals_right = convert_sw_pos(get_xlrd_value(switch_sheet, row, REVERSE_EQUALS_RIGHT_COL))
            bop_dict[sw_name] = reverse_equals_right

        sw_name2 = get_xlrd_value(switch_sheet, row, SW_NAME_2_COL)
        if sw_name2:
            reverse_equals_right2 = convert_sw_pos(get_xlrd_value(switch_sheet, row, REVERSE_EQUALS_RIGHT_2_COL))
            bop_dict[sw_name2] = reverse_equals_right2
    return bop_dict


def convert_sw_pos(reverse_equals_right: str):
    if reverse_equals_right.upper().strip() == YesOrNo.N:
        return False
    if reverse_equals_right.upper().strip() == YesOrNo.O:
        return True


def erase_dc_bop():
    global LOADED_SWITCH_DIRECTIONS
    LOADED_SWITCH_DIRECTIONS = dict()
