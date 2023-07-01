#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unidecode
from ...utils import *
from .load_xl import load_dc_par_wb


LOADED_PARAMETERS = dict()

START_LINE = 3

FR_NAME_COL = 1
S_NS_COL = 2
VALUE_COL = 3
UNIT_COL = 4
PARAM_NAME_COL = 6

PARAM_NAME_TITLE = "C_D413-12"


def load_params() -> dict:
    global LOADED_PARAMETERS
    if not LOADED_PARAMETERS:
        wb = load_dc_par_wb()
        sh_names = wb.sheet_names()
        for sh_name in sh_names:
            LOADED_PARAMETERS.update(get_sheet_param(wb, sh_name))
    return LOADED_PARAMETERS


def get_sheet_param(wb: xlrd.Book, sh_name: str) -> dict:
    sh = wb.sheet_by_name(sh_name)
    if sh.nrows == 0:
        return {}

    param_name_col_title = get_and_decode_xlrd_value(sh, 1, PARAM_NAME_COL)
    if param_name_col_title is None or param_name_col_title.upper() != PARAM_NAME_TITLE:
        return {}

    param_dict = dict()
    for line in range(START_LINE, sh.nrows+1):
        param_name = get_and_decode_xlrd_value(sh, line, PARAM_NAME_COL).lower()
        if param_name.upper() not in ("", "RESERVED"):
            fr_name = get_and_decode_xlrd_value(sh, line, FR_NAME_COL)
            s_ns = get_and_decode_xlrd_value(sh, line, S_NS_COL)
            value = get_and_decode_xlrd_value(sh, line, VALUE_COL)
            unit = get_and_decode_xlrd_value(sh, line, UNIT_COL)
            param_dict[param_name] = {"fr_name": fr_name, "s_ns": s_ns, "value": value, "unit": unit}
    return param_dict


def get_and_decode_xlrd_value(sh: xlrd.sheet, line: int, col: int) -> str:
    xlrd_line = get_xlrd_line(line)
    xlrd_col = get_xlrd_column(col)
    try:
        cell_value = sh.cell_value(xlrd_line, xlrd_col)
    except IndexError:
        cell_value = None
    if isinstance(cell_value, str):
        cell_value = unidecode.unidecode(cell_value).strip()
    return cell_value
