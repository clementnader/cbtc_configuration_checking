#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unidecode
from ...utils import *
from .load_xl import *


__all__ = ["load_params"]


LOADED_PARAMETERS = dict()

START_ROW = 3

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
    ws = wb.sheet_by_name(sh_name)
    if ws.nrows == 0:
        return {}

    param_name_column_on_sheet = PARAM_NAME_COL
    param_name_col_title = get_and_decode_xlrd_value(ws, 1, param_name_column_on_sheet)
    # Sometimes an extra column is added in the DC_PAR sheet for comments or computation.
    while (param_name_column_on_sheet <= ws.ncols + 1
           and (param_name_col_title is None or param_name_col_title.upper() != PARAM_NAME_TITLE)):
        param_name_column_on_sheet += 1
        param_name_col_title = get_and_decode_xlrd_value(ws, 1, param_name_column_on_sheet)

    if param_name_col_title is None or param_name_col_title.upper() != PARAM_NAME_TITLE:
        return {}

    param_dict = dict()
    for row in range(START_ROW, ws.nrows + 1):
        param_name = get_and_decode_xlrd_value(ws, row, param_name_column_on_sheet)
        if param_name is not None and param_name.upper() not in ["", "RESERVED"]:
            fr_name = get_and_decode_xlrd_value(ws, row, FR_NAME_COL)
            s_ns = get_and_decode_xlrd_value(ws, row, S_NS_COL)
            value = get_and_decode_xlrd_value(ws, row, VALUE_COL)
            unit = get_and_decode_xlrd_value(ws, row, UNIT_COL)
            param_dict[param_name.lower()] = {"fr_name": fr_name, "s_ns": s_ns, "value": value, "unit": unit}
    return param_dict


def get_and_decode_xlrd_value(ws: xlrd.sheet.Sheet, row: int, col: int) -> str:
    cell_value = get_xlrd_value(ws, row, col)
    if isinstance(cell_value, str):
        cell_value = unidecode.unidecode(cell_value).strip()
    return cell_value
