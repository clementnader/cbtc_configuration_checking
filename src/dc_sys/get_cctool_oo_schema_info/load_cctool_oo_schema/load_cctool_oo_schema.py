#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import unidecode
from ....utils import *
from .load_xl import load_cctool_oo_schema_wb

SHEET_NAME = r"CCTool-OO Schema"
START_LINE = 2

SHEET_COL = "B"
TITLE_COL = "C"
COLUMN_COL = "D"
# FDS_OBJ_COL = "F"
# FDS_ATTR_COL = "G"

LOADED_CCTOOL_OO_SCHEMA = dict()


def load_cctool_oo_schema(addr) -> dict:
    global LOADED_CCTOOL_OO_SCHEMA
    if not LOADED_CCTOOL_OO_SCHEMA:
        wb = load_cctool_oo_schema_wb(addr)
        cctool_oo_schema_sh = wb.sheet_by_name(SHEET_NAME)
        LOADED_CCTOOL_OO_SCHEMA = get_cctool_oo_schema(cctool_oo_schema_sh)
    return LOADED_CCTOOL_OO_SCHEMA


def get_cctool_oo_schema(sh: xlrd.sheet) -> dict:
    info_dict = dict()
    line = START_LINE
    # while line <= sh.nrows:
    for line in range(START_LINE, sh.nrows + 1):
        sheet_name = get_xlrd_value(sh, line, SHEET_COL)
        if not sheet_name:
            # line += 1
            continue
        if sheet_name not in info_dict:
            info_dict[sheet_name] = dict()
        title = get_clean_cell(sh, line, TITLE_COL)
        column = int(get_xlrd_value(sh, line, COLUMN_COL))
        if "::" not in title:
            if title in info_dict[sheet_name]:
                print_error(f"In CCTOOL-OO Schema, there is multiple times Title {Color.blue}{title}{Color.reset}"
                            f" for Spreadsheet {Color.blue}{sheet_name}{Color.reset}.")
            else:
                info_dict[sheet_name][title] = column
            # line += 1
        else:
            list_attr_name, sub_attr_name = get_list_attr_names(title)
            if list_attr_name not in info_dict[sheet_name]:
                info_dict[sheet_name][list_attr_name] = dict()
            if sub_attr_name not in info_dict[sheet_name][list_attr_name]:
                info_dict[sheet_name][list_attr_name][sub_attr_name] = list()
            info_dict[sheet_name][list_attr_name][sub_attr_name].append(column)
            # line += 1
            # list_max_nb = 1
            # list_delta = 0
            # new_sheet_name = sheet_name
            # new_list_attr_name = list_attr_name
            # new_sub_attr_name = first_sub_attr_name
            # while line <= sh.nrows and sheet_name == new_sheet_name and new_list_attr_name == list_attr_name:
            #     if new_sub_attr_name in info_dict[sheet_name][list_attr_name]:
            #         if new_sub_attr_name == first_sub_attr_name:
            #             list_max_nb += 1
            #     else:
            #         info_dict[sheet_name][list_attr_name][new_sub_attr_name] = column
            #         list_delta += 1
            #     line += 1
            #     new_sheet_name = get_xlrd_value(sh, line, SHEET_COL)
            #     if new_sheet_name is None:
            #         break
            #     title = get_clean_cell(sh, line, TITLE_COL)
            #     column = int(get_xlrd_value(sh, line, COLUMN_COL))
            #     if "::" not in title:
            #         break
            #     new_list_attr_name, new_sub_attr_name = get_list_attr_names(title)
            # info_dict[sheet_name][list_attr_name]["list_max_nb"] = list_max_nb
            # info_dict[sheet_name][list_attr_name]["list_delta"] = list_delta

    return info_dict


def get_list_attr_names(title: str):
    title = re.sub("[1-9][0-9]*", "", title)
    list_attr_name, sub_attr_name = title.split("::", 1)
    if sub_attr_name == "":
        sub_attr_name = "Cell"
    return list_attr_name, sub_attr_name


def get_clean_cell(sh: xlrd.sheet, line, col):
    cell_str = unidecode.unidecode(f"{get_xlrd_value(sh, line, col)}").strip()  # translate non-ASCII characters
    cell_str = cell_str.replace("'", ' ').replace('.', ' ').replace('#', '').replace('/', '')  # remove special chars
    cell_str = cell_str.replace("1st", "First").replace("2nd", "Second")
    cell_str = cell_str.title().replace(' ', '')  # camelcase
    return cell_str
