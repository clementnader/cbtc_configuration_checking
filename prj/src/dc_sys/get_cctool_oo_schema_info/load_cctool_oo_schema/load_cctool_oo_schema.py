#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unidecode
from ....utils import *
from .load_xl import *


__all__ = ["load_cctool_oo_schema"]


SHEET_NAME = r"CCTool-OO Schema"
START_LINE = 2
SHEET_COL = 2
TITLE_COL = 3
COLUMN_COL = 4

LOADED_CCTOOL_OO_SCHEMA = dict()


DC_SYS_SHEET_NAMES_TO_FIX = {
    "Coupling_area": "Coupling_Area",
    "Odometric_Zones": "Odometric_Zone",
}


def load_cctool_oo_schema(addr) -> dict:
    global LOADED_CCTOOL_OO_SCHEMA
    if not LOADED_CCTOOL_OO_SCHEMA:
        wb = load_cctool_oo_schema_wb(addr)
        cctool_oo_schema_sh = wb.sheet_by_name(SHEET_NAME)
        LOADED_CCTOOL_OO_SCHEMA = get_cctool_oo_schema(cctool_oo_schema_sh)
    return LOADED_CCTOOL_OO_SCHEMA


def get_cctool_oo_schema(ws: xlrd.sheet) -> dict:
    info_dict = dict()
    for line in range(START_LINE, ws.nrows + 1):
        sheet_name = get_xlrd_value(ws, line, SHEET_COL)
        if not sheet_name:
            continue
        if sheet_name in DC_SYS_SHEET_NAMES_TO_FIX:
            sheet_name = DC_SYS_SHEET_NAMES_TO_FIX[sheet_name]
        if sheet_name not in info_dict:
            info_dict[sheet_name] = dict()
        title = get_clean_cell(ws, line, TITLE_COL)
        column = int(get_xlrd_value(ws, line, COLUMN_COL))
        if "::" not in title:
            if title in info_dict[sheet_name]:
                print_error(f"In CCTOOL-OO Schema, there is multiple times Title {Color.blue}{title}{Color.reset}"
                            f" for Spreadsheet {Color.blue}{sheet_name}{Color.reset}.")
            else:
                info_dict[sheet_name][title] = column
        else:
            list_attr_name, sub_attr_name = get_list_attr_names(title)
            if list_attr_name not in info_dict[sheet_name]:
                info_dict[sheet_name][list_attr_name] = dict()
            if sub_attr_name not in info_dict[sheet_name][list_attr_name]:
                info_dict[sheet_name][list_attr_name][sub_attr_name] = list()
            info_dict[sheet_name][list_attr_name][sub_attr_name].append(column)
    return info_dict


def get_list_attr_names(title: str):
    title = re.sub("[1-9][0-9]*", "", title)
    list_attr_name, sub_attr_name = title.split("::", 1)
    if sub_attr_name == "":
        sub_attr_name = "Cell"
    return list_attr_name, sub_attr_name


def get_clean_cell(ws: xlrd.sheet, line: int, col: int):
    cell_str = unidecode.unidecode(f"{get_xlrd_value(ws, line, col)}").strip()  # translate non-ASCII characters
    cell_str = cell_str.replace("'", ' ').replace('.', ' ').replace('-', ' ').replace('/', ' ')  # remove special chars
    cell_str = cell_str.replace('#', "Number")  # remove special char
    cell_str = cell_str.replace("1st", "First").replace("2nd", "Second")  # remove leading numbers
    cell_str = cell_str.title().replace(' ', '')  # CamelCase
    return cell_str
