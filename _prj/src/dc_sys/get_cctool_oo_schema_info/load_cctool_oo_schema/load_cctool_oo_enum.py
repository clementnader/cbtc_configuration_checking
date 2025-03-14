#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ....utils import *
from .load_xl import *


__all__ = ["load_cctool_oo_enum_lists"]


SHEET_NAME = r"EnumList"
START_ROW = 2
ENUM_NAME_COL = 1
AVAILABLE_VALUES_START_COL = 3

LOADED_CCTOOL_OO_ENUM_LISTS = dict()


def load_cctool_oo_enum_lists(addr: str) -> dict:
    global LOADED_CCTOOL_OO_ENUM_LISTS
    if not LOADED_CCTOOL_OO_ENUM_LISTS:
        wb = load_cctool_oo_schema_wb(addr)
        cctool_oo_schema_sh = wb.sheet_by_name(SHEET_NAME)
        LOADED_CCTOOL_OO_ENUM_LISTS = get_cctool_oo_enums(cctool_oo_schema_sh)
    return LOADED_CCTOOL_OO_ENUM_LISTS


def get_cctool_oo_enums(ws: xlrd.sheet) -> dict:
    info_dict = dict()
    for row in range(START_ROW, ws.nrows + 1):
        sheet_name = get_xlrd_value(ws, row, ENUM_NAME_COL)
        if not sheet_name:
            continue
        list_available_values = list()
        for col in range(AVAILABLE_VALUES_START_COL, ws.ncols + 1):
            value = get_xlrd_value(ws, row, col)
            if not value:
                break
            list_available_values.append(f"{value}")
        info_dict[sheet_name] = list_available_values
    return info_dict
