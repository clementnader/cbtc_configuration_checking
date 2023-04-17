#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ...utils import *
from ..dc_sys_sheets_info import SHEETS_INFO
from .extract_xl import get_dict
from .load_xl import load_wb
from .sheet_cols_name import get_cols_name_from_ref, get_lim_cols_name_from_ref

LOADED_SHEETS = {sh: None for sh in SHEETS_INFO}
LOADED_SHEETS_COLS = {sh: None for sh in SHEETS_INFO}

LOADED_SHEETS_OLD = {sh: None for sh in SHEETS_INFO}
LOADED_SHEETS_OLD_COLS = {sh: None for sh in SHEETS_INFO}


def load_sheet(obj_name: str, old: bool = False, generic_name: bool = False) -> dict:
    if old:
        global LOADED_SHEETS_OLD, LOADED_SHEETS_OLD_COLS
        if not LOADED_SHEETS_OLD[obj_name]:
            wb_old = load_wb(old)
            LOADED_SHEETS_OLD[obj_name], LOADED_SHEETS_OLD_COLS[obj_name] = get_sheet(wb_old, obj_name, generic_name)
        return LOADED_SHEETS_OLD[obj_name]
    else:
        global LOADED_SHEETS, LOADED_SHEETS_COLS
        if not LOADED_SHEETS[obj_name]:
            wb = load_wb(old)
            LOADED_SHEETS[obj_name], LOADED_SHEETS_COLS[obj_name] = get_sheet(wb, obj_name, generic_name)
        return LOADED_SHEETS[obj_name]


def get_sheet(wb: xlrd.Book, obj_name: str, generic_name: bool = False):
    sh = wb.sheet_by_name(SHEETS_INFO[obj_name]["sh_name"])

    # Get parameter or set default value
    fixed_cols_ref = SHEETS_INFO[obj_name].get("cols", [])
    generic_obj_name = generic_name or SHEETS_INFO[obj_name].get("generic_obj_name", False)
    lim_first_col = SHEETS_INFO[obj_name].get("lim_start_col", None)
    nb_max_limits = SHEETS_INFO[obj_name].get("nb_max_limits", 0)
    delta_between_limits = SHEETS_INFO[obj_name].get("delta_between_limits", 0)

    sh_dict = get_dict(sh, fixed_cols_ref=fixed_cols_ref, generic_obj_name=generic_obj_name,
                       lim_first_col=lim_first_col, nb_max_limits=nb_max_limits,
                       delta_between_limits=delta_between_limits)
    cols_name = get_cols_name_from_ref(sh, cols_ref=fixed_cols_ref)
    lim_cols_name = get_lim_cols_name_from_ref(sh, col_ref=lim_first_col, delta_between_limits=delta_between_limits)
    return sh_dict, {"fixed": cols_name, "limits": lim_cols_name}


def get_cols_name(obj_name, old: bool = False) -> dict[str, str]:
    if old:
        global LOADED_SHEETS_OLD, LOADED_SHEETS_OLD_COLS
        if not LOADED_SHEETS_OLD_COLS[obj_name]:
            wb_old = load_wb(old)
            LOADED_SHEETS_OLD[obj_name], LOADED_SHEETS_OLD_COLS[obj_name] = get_sheet(wb_old, obj_name)
        return LOADED_SHEETS_OLD_COLS[obj_name]["fixed"]
    else:
        global LOADED_SHEETS, LOADED_SHEETS_COLS
        if not LOADED_SHEETS_COLS[obj_name]:
            wb = load_wb(old)
            LOADED_SHEETS[obj_name], LOADED_SHEETS_COLS[obj_name] = get_sheet(wb, obj_name)
        return LOADED_SHEETS_COLS[obj_name]["fixed"]


def get_lim_cols_name(obj_name, old: bool = False) -> list[str]:
    if old:
        global LOADED_SHEETS_OLD, LOADED_SHEETS_OLD_COLS
        if not LOADED_SHEETS_OLD_COLS[obj_name]:
            wb_old = load_wb(old)
            LOADED_SHEETS_OLD[obj_name], LOADED_SHEETS_OLD_COLS[obj_name] = get_sheet(wb_old, obj_name)
        return LOADED_SHEETS_OLD_COLS[obj_name]["limits"]
    else:
        global LOADED_SHEETS, LOADED_SHEETS_COLS
        if not LOADED_SHEETS_COLS[obj_name]:
            wb = load_wb(old)
            LOADED_SHEETS[obj_name], LOADED_SHEETS_COLS[obj_name] = get_sheet(wb, obj_name)
        return LOADED_SHEETS_COLS[obj_name]["limits"]
