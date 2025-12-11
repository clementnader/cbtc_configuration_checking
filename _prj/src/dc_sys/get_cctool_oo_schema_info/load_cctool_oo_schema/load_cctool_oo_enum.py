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
        cctool_oo_schema_sheet = get_xl_sheet_by_name(wb, SHEET_NAME)
        LOADED_CCTOOL_OO_ENUM_LISTS = get_cctool_oo_enums(cctool_oo_schema_sheet)
    return LOADED_CCTOOL_OO_ENUM_LISTS


def get_cctool_oo_enums(ws: xlrd.sheet.Sheet) -> dict:
    info_dict = dict()
    for row in range(START_ROW, get_xl_number_of_rows(ws) + 1):
        sheet_name = get_xl_cell_value(ws, row=row, column=ENUM_NAME_COL)
        if not sheet_name:
            continue
        list_available_values = list()
        for column in range(AVAILABLE_VALUES_START_COL, get_xl_number_of_columns(ws) + 1):
            value = get_xl_cell_value(ws, row=row, column=column)
            if not value:
                break
            list_available_values.append(f"{value}")
        info_dict[sheet_name] = list_available_values
    return info_dict
