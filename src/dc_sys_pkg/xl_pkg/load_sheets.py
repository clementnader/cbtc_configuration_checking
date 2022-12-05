#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .load_xl import load_wb
from .extract_xl import get_dict
from .sheet_cols_name import get_cols_name_from_ref, get_lim_cols_name_from_ref
from ..dc_sys_sheets_info import SHEETS_INFO

LOADED_SHEETS = {sh: None for sh in SHEETS_INFO}
LOADED_SHEETS_COLS = {sh: None for sh in SHEETS_INFO}

LOADED_SHEETS_OLD = {sh: None for sh in SHEETS_INFO}
LOADED_SHEETS_OLD_COLS = {sh: None for sh in SHEETS_INFO}


def load_sheet(obj_name, old: bool = False):
    if old:
        global LOADED_SHEETS_OLD, LOADED_SHEETS_OLD_COLS
        if not LOADED_SHEETS_OLD[obj_name]:
            wb_old = load_wb(old)
            LOADED_SHEETS_OLD[obj_name], LOADED_SHEETS_OLD_COLS[obj_name] = get_sheet(wb_old, obj_name)
        return LOADED_SHEETS_OLD[obj_name]
    else:
        global LOADED_SHEETS, LOADED_SHEETS_COLS
        if not LOADED_SHEETS[obj_name]:
            wb = load_wb(old)
            LOADED_SHEETS[obj_name], LOADED_SHEETS_COLS[obj_name] = get_sheet(wb, obj_name)
        return LOADED_SHEETS[obj_name]


def get_sheet(wb, obj_name):
    sh = wb.sheet_by_name(SHEETS_INFO[obj_name]["sh_name"])
    # Get parameter or set default value
    fixed_cols_ref = SHEETS_INFO[obj_name]["cols"] if "cols" in SHEETS_INFO[obj_name] else []
    name_col = SHEETS_INFO[obj_name]["name_col"] if "name_col" in SHEETS_INFO[obj_name] else 'A'
    line_ref = SHEETS_INFO[obj_name]["line_ref"] if "line_ref" in SHEETS_INFO[obj_name] else 3
    lim_first_col = SHEETS_INFO[obj_name]["lim_start_col"] if "lim_start_col" in SHEETS_INFO[obj_name] else None
    nb_max_limits = SHEETS_INFO[obj_name]["nb_max_limits"] if "nb_max_limits" in SHEETS_INFO[obj_name] else 0
    delta_between_limits = SHEETS_INFO[obj_name]["delta_between_limits"] \
        if "delta_between_limits" in SHEETS_INFO[obj_name] else 0

    sh_dict = get_dict(sh, fixed_cols_ref=fixed_cols_ref, name_col=name_col, line_ref=line_ref,
                       lim_first_col=lim_first_col, nb_max_limits=nb_max_limits,
                       delta_between_limits=delta_between_limits)
    cols_name = get_cols_name_from_ref(sh, cols_ref=fixed_cols_ref)
    lim_cols_name = get_lim_cols_name_from_ref(sh, col_ref=lim_first_col, delta_between_limits=delta_between_limits)
    return sh_dict, {"fixed": cols_name, "limits": lim_cols_name}


def get_cols_name(obj_name, old: bool = False):
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


def get_lim_cols_name(obj_name, old: bool = False):
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
